from multiprocessing import Process, Pool, Queue, current_process
from abc import ABC, abstractmethod
from builder.errors import BuilderError, BuilderValidationError
from builder.configurator import WallConfigurator

import logging.handlers
import logging
import time


class LogListener(Process):
    """Process that listens for log messages on a queue."""

    def __init__(self, queue, logfile='listener.log'):
        super().__init__()
        self.queue = queue
        self.logfile = logfile
        self.log = logging.getLogger()

    def configure_logging(self):
        """Configure the logging for the listener process."""
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)-8s %(processName)-15s - %(message)s'
        )
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(filename=self.logfile, mode='w')

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.log.addHandler(file_handler)
        self.log.addHandler(console_handler)

    def run(self):
        """Process that listens for log messages on the queue."""
        self.configure_logging()

        while True:
            try:
                record = self.queue.get()
                if record is None:
                    break
                logger = logging.getLogger(record.name)
                logger.handle(record)
            except Exception as e:
                print(f'Exception: {e}')

    def stop(self):
        """Stop the log listener process."""
        for handler in self.log.handlers:
            handler.flush()

        while not self.queue.empty():
            time.sleep(0.1)

        self.queue.put(None)
        self.join()


class WallBuilderAbc(ABC):
    """Abstract base class for the wall builder."""

    @abstractmethod
    def set_config(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def is_ready(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_ice(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get_cost(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def prepare(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def build(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def validate(self):
        raise NotImplementedError


class WallSection(WallBuilderAbc):
    """Represents a section of a wall."""

    config = WallConfigurator()

    def __init__(self, section_id=0, profile_id=None, start_height=0):
        self.section_id = section_id
        self.profile_id = profile_id
        self.start_height = start_height
        self.current_height = start_height
        self.day = 0

        self.log = logging.getLogger(self.__class__.__name__)
        self.log.addHandler(logging.NullHandler())

    def __eq__(self, other):
        return (
            self.section_id == other.section_id and
            self.profile_id == other.profile_id and
            self.start_height == other.start_height and
            self.current_height == other.current_height
        )

    def __repr__(self):
        return (f'WallSection(section_id={self.section_id}, '
                f'profile_id={self.profile_id}, '
                f'start_height={self.start_height}, '
                f'current_height={self.current_height}, '
                f'ready={self.is_ready()})')

    @classmethod
    def set_config(cls, config):
        cls.config = config
        return cls()

    def is_ready(self):
        return self.current_height >= self.config.target_height

    def get_ice(self):
        delta = self.current_height - self.start_height
        return delta * self.config.volume_ice_per_foot

    def get_cost(self):
        return self.get_ice() * self.config.cost_per_volume

    def validate(self):
        self._validate_start_height()
        self._validate_section_id()
        self._validate_profile_id()
        return self

    def _validate_start_height(self):
        if not isinstance(self.start_height, int):
            raise BuilderValidationError('The start height must be an integer')
        if not 0 <= self.start_height <= self.config.target_height:
            raise BuilderValidationError('The start height must be between 0 and the target height')

    def _validate_section_id(self):
        if not isinstance(self.section_id, int):
            raise BuilderValidationError('The section_id must be an integer')
        if self.section_id < 0:
            raise BuilderValidationError('The section_id must be a positive integer')

    def _validate_profile_id(self):
        if not isinstance(self.profile_id, (int, type(None))):
            raise BuilderValidationError('The profile_id must be an integer or None')
        if self.profile_id is not None and self.profile_id < 0:
            raise BuilderValidationError('The profile_id must be a positive integer')

    @staticmethod
    def prepare(queue):
        log = logging.getLogger()
        handler = logging.handlers.QueueHandler(queue)
        log.addHandler(handler)
        log.setLevel(logging.INFO)

    def build(self):
        original_name = current_process().name
        current_process().name = f'Worker-{original_name.split("-")[-1]}'

        if self.current_height < self.config.target_height:
            self.current_height += self.config.build_rate
            self.day += 1

            self.log.info(f'Added 1 foot to section {self.section_id} to reach'
                          f' {self.current_height} feet on day {self.day}')

        time.sleep(self.config.cpu_worktime)

        return self


class WallProfile(WallBuilderAbc):
    """Represents a profile of a wall."""

    config = WallConfigurator()

    def __init__(self, profile_id=0, sections=None):
        self.profile_id = profile_id
        self.sections = sections or []

        self.log = logging.getLogger(self.__class__.__name__)
        self.log.addHandler(logging.NullHandler())

    def __eq__(self, other):
        return (
            self.profile_id == other.profile_id and
            self.sections == other.sections
        )

    def __repr__(self):
        return (f"WallProfile(profile_id={self.profile_id}, "
                f"ice={self.get_ice()}, "
                f"cost={self.get_cost()}, "
                f"ready={self.is_ready()})")

    @classmethod
    def set_config(cls, config):
        cls.config = config
        return cls()

    def is_ready(self):
        return bool(self.sections) and all(section.is_ready() for section in self.sections)

    def get_ice(self):
        return sum(section.get_ice() for section in self.sections)

    def get_cost(self):
        return self.get_ice() * self.config.cost_per_volume

    def validate(self):
        self._validate_profile_id()
        self._validate_sections()
        return self

    def _validate_profile_id(self):
        if not isinstance(self.profile_id, int):
            raise BuilderValidationError('The profile_id must be an integer')
        if self.profile_id < 0:
            raise BuilderValidationError('The profile_id must be a positive integer')

    def _validate_sections(self):
        if not isinstance(self.sections, list):
            raise BuilderValidationError('The sections must be a list')
        if not all(isinstance(s, WallSection) for s in self.sections):
            raise BuilderValidationError('All sections must be WallSection objects')
        if not 1 <= len(self.sections) <= self.config.max_section_count:
            raise BuilderValidationError('The sections count must be between 1 and the max section count')

    @staticmethod
    def prepare(queue):
        log = logging.getLogger()
        handler = logging.handlers.QueueHandler(queue)
        log.addHandler(handler)
        log.setLevel(logging.INFO)

    def build(self):
        for section in self.sections:
            if not section.is_ready():
                section.build()

        return self


class WallManager(WallBuilderAbc):
    """Manages the construction of a wall."""

    config = WallConfigurator()

    def __init__(self, log_filepath='wall.log'):
        self.profiles = []
        self.sections = []

        self.log_filepath = log_filepath
        self.log = logging.getLogger()
        self.log.addHandler(logging.NullHandler())

        self.log_queue = Queue()
        self.prepare(self.log_queue)

    def report(self, start_time, end_time):
        self.log.info('-' * 80)
        self.log.info(f'TOTAL ICE : {self.get_ice()}')
        self.log.info(f'TOTAL COST: {self.get_cost()}')
        self.log.info('-' * 80)
        self.log.info(f"Calculation time: {end_time - start_time:.2f} seconds")
        self.log.info('-' * 80)

    def parse_profile_list(self):
        section_id = 0

        self.profiles.clear()
        self.sections.clear()

        for row in self.config.profiles:
            profile_id = self.config.profiles.index(row)
            profile = WallProfile(profile_id=profile_id)

            for column in row:
                section = WallSection(
                    section_id=section_id,
                    profile_id=profile_id,
                    start_height=column
                )
                profile.sections.append(section)
                section_id += 1

            self.profiles.append(profile)
            self.sections.extend(profile.sections)

        return self

    def set_profile_list(self, profiles_list):
        self.config.profiles = profiles_list
        return self

    def update_profiles(self):
        for profile in self.profiles:
            profile.sections = [
                section for section in self.sections if section.profile_id == profile.profile_id
            ]

        return self

    def get_profile(self, profile_id):
        try:
            return next(
                profile for profile in self.profiles if profile.profile_id == profile_id
            )
        except StopIteration:
            raise BuilderError(f"Profile with ID {profile_id} not found.")

    def get_section(self, section_id):
        try:
            return next(
                section for section in self.sections if section.section_id == section_id
            )
        except StopIteration:
            raise BuilderError(f"Section with ID {section_id} not found.")

    @classmethod
    def set_config(cls, config):
        cls.config = config
        return cls()

    def get_logs(self):
        with open(self.log_filepath, 'r') as file:
            logs = file.readlines()

        return {'logs': logs}

    def is_ready(self):
        return bool(self.sections) and all(section.is_ready() for section in self.sections)

    def get_ice(self):
        return sum(section.get_ice() for section in self.sections)

    def get_cost(self):
        return sum(section.get_cost() for section in self.sections)

    def validate(self):
        self._validate_profiles_list()
        return self

    def _validate_profiles_list(self):
        profiles_list = self.config.profiles
        if not isinstance(profiles_list, list):
            raise BuilderValidationError('The config_list must be a list')
        if not all(isinstance(element, list) for element in profiles_list):
            raise BuilderValidationError('All elements of config_list must be lists')
        for i, profiles in enumerate(profiles_list):
            for j, section_height in enumerate(profiles):
                if not isinstance(section_height, int):
                    raise BuilderValidationError(
                        f'Element at index [{i}][{j}] is not an integer.'
                    )

    @staticmethod
    def prepare(queue):
        current_process().name = 'Manager'
        log = logging.getLogger()
        log.setLevel(logging.INFO)

    def build(self, days=1, num_teams=1):
        log_listener = LogListener(queue=self.log_queue, logfile=self.log_filepath)
        log_listener.start()

        try:
            self.parse_profile_list()

            pool = Pool(
                processes=num_teams,
                initializer=WallSection.prepare,
                initargs=(self.log_queue,),
            )

            start_time = time.time()

            for _ in range(days):
                if self.is_ready():
                    break
                self.sections = pool.map(WallSection.build, self.sections)

            # No more sections to build, workers are relieved
            for _ in range(num_teams):
                self.log.info(f'{current_process().name} relieved - No jobs')

            pool.close()
            pool.join()

            end_time = time.time()
            self.report(start_time=start_time, end_time=end_time)
            self.update_profiles()

        except Exception as e:
            raise BuilderError(f"An error occurred: {e}")

        finally:
            log_listener.stop()

        return self


def main():
    config_list = [
        [21, 25, 28],
        [17],
        [17, 22, 17, 19, 17]
    ]

    config = WallConfigurator(profiles=config_list)

    builder = WallManager.set_config(config)
    builder.build(num_teams=20, days=1)


if __name__ == "__main__":
    main()
