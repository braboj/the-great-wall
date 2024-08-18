import logging
import logging.handlers
import multiprocessing
import time


def worker_process(queue, worker_id):
    logger = logging.getLogger(f"Worker-{worker_id}")
    queue_handler = logging.handlers.QueueHandler(queue)
    logger.addHandler(queue_handler)
    logger.setLevel(logging.INFO)

    for i in range(5):
        logger.info(f"Worker {worker_id} is working on task {i}")
        time.sleep(0.05)


def main():
    log_queue = multiprocessing.Queue()

    # Set up the root logger to listen to the queue
    listener = logging.handlers.QueueListener(log_queue, *logging.getLogger().handlers)
    listener.start()

    # Set up processes
    processes = []
    for worker_id in range(3):  # Create 3 worker processes
        p = multiprocessing.Process(target=worker_process, args=(log_queue, worker_id))
        processes.append(p)
        p.start()

    # Wait for processes to finish
    for p in processes:
        p.join()

    listener.stop()


if __name__ == "__main__":
    # Configure the root logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )

    for _ in range(3):
        main()
