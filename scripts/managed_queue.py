import multiprocessing
import random
import time


class Worker(object):

    def build(self, queue):
        """Function to be executed in a worker process."""

        while True:

            # Simulate a computation delay
            time.sleep(0.01)

            # Put the result in the queue
            queue.put(random.random())

            break


class BuilderManager(object):

    @staticmethod
    def process_results(queue):
        """Function to process results from the queue."""
        while not queue.empty():
            result = queue.get()
            print(f"Result: {result}")

    def build(self):

        workers = [Worker() for _ in range(4)]

        # Create a manager and a shared queue
        with multiprocessing.Manager() as manager:

            queue = manager.Queue()

            # Create a pool of worker processes
            with multiprocessing.Pool(processes=4) as pool:

                # Use pool.starmap to map numbers to the worker function with the shared queue
                pool.starmap(
                    func=Worker.build,
                    iterable=[(worker, queue) for worker in workers]
                )

            # After all processes have completed, process the results
            self.process_results(queue)


def main():

    managers = [BuilderManager()] * 4
    for manager in managers:
        manager.build()


if __name__ == '__main__':
    main()
