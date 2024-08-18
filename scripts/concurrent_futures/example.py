from concurrent.futures import ProcessPoolExecutor
import time


def worker(param1, param2):
    print(f'Worker {param1}-{param2} started')
    time.sleep(0.1)
    print(f'Worker {param1}-{param2} finished')


def main():
    with ProcessPoolExecutor(max_workers=5) as executor:
        for i in range(5):
            executor.submit(worker, i, i + 1)


if __name__ == "__main__":
    main()
