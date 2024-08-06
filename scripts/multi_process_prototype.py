from multiprocessing import Pool, Manager
import logging

# Constants
VOLUME_ICE_PER_FOOT = 195  # cubic yards
COST_PER_VOLUME = 1900  # Gold Dragon coins
MAX_HEIGHT = 30  # Feet

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(message)s')


class WallSection(object):
    """Represents a section of a wall."""

    def __init__(self, start_height):
        self.start_height = start_height
        self.current_height = start_height

    def __repr__(self):
        return (f"WallSection(start_height={self.start_height}, "
                f"current_height={self.current_height}, "
                f"ice={self.get_ice()}, "
                f"cost={self.get_cost()}, "
                f"ready={self.is_ready()}"
                f")"
                )

    def is_ready(self):
        """Returns True if the wall section is ready to be constructed."""
        return self.current_height >= MAX_HEIGHT

    def get_ice(self):
        delta = self.current_height - self.start_height
        return delta * VOLUME_ICE_PER_FOOT

    def get_cost(self):
        return self.get_ice() * COST_PER_VOLUME

    def build(self):
        """Build the section by one foot per day."""

        if self.current_height < MAX_HEIGHT:
            self.current_height += 1

        return self


class WallProfile(object):
    """Represents a profile of a wall."""

    def __init__(self, full_name, sections):
        self.full_name = full_name
        self.sections = sections

    def __repr__(self):
        return (f"WallProfile(full_name={self.full_name}, "
                f"ice={self.get_ice()}, "
                f"cost={self.get_cost()}, "
                f"ready={self.is_ready()}"
                f")"
                )

    def is_ready(self):
        """Returns True if the wall profile is ready to be constructed."""
        return all(section.is_ready() for section in self.sections)

    def get_ice(self):
        """Returns the total ice consumed by the wall profile."""
        return sum(section.get_ice() for section in self.sections)

    def get_cost(self):
        """Returns the total cost of the wall profile."""
        return self.get_ice() * COST_PER_VOLUME

    def build(self):
        """Builds the wall profile section by section."""

        # Build each section
        for section in self.sections:
            if not section.is_ready():
                section.build()

        return self


class WallBuilder(object):
    """Manages the construction of a wall."""

    def __init__(self):
        self.config_list = []
        self.wall_profiles = []
        self.sections = []

    @staticmethod
    def create_profile(heights, index):
        sections = [WallSection(start_height) for start_height in heights]
        return WallProfile(f"P{index + 1:02d}", sections)

    def set_config(self, config_list):
        self.config_list = config_list

    def get_sections(self):

        sections = []

        for profile in self.wall_profiles:
            sections.extend(profile.sections)

        return sections

    def get_ice(self):
        return sum(section.get_ice() for section in self.sections)

    def get_cost(self):
        return sum(section.get_cost() for section in self.sections)

    def build(self, max_teams=None, days=None):

        # Create the wall profiles
        self.wall_profiles = [
            self.create_profile(heights, index) for
            index, heights in enumerate(self.config_list)
        ]

        # Get the number of sections
        self.sections = self.get_sections()

        # Check if construction teams are specified
        if max_teams is None:
            max_teams = len(self.sections)

        # Check if construction days are specified
        if days is None:
            days = MAX_HEIGHT

        # Create a pool of workers
        with Pool(processes=max_teams) as pool:

            # Distribute the workers to each section
            for day in range(days):

                # Check if all sections are ready
                if all(section.is_ready() for section in self.sections):
                    break

                logging.info(f"Day {day + 1}")

                # Map a section from a profile to a worker
                self.sections = pool.map(WallSection.build, self.sections)

                # Log the progress
                for section in self.sections:
                    logging.info(section)

            logging.info('-' * 80)
            logging.info(f'TOTAL ICE : {self.get_ice()}')
            logging.info(f'TOTAL COST: {self.get_cost()}')
def main():

    config_list = [
        [0, 0],
        [0, 0],
        [0, 0],
    ]

    builder = WallBuilder()
    builder.set_config(config_list)
    builder.build(max_teams=3)


if __name__ == "__main__":
    main()
