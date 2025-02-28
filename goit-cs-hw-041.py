
import threading
import time
from queue import Queue
from collections import defaultdict

BUFFER_SIZE = 4096
MAX_THREADS = 4

def search_keywords_in_file(filename, keywords, result_dict, lock, times):
    start_time = time.time()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            while True:
                buffer = file.read(BUFFER_SIZE).lower()
                if not buffer:
                    break
                for keyword in keywords:
                    if keyword.lower() in buffer:
                        with lock:
                            result_dict[keyword].append(filename)
                        break
    except Exception as e:
        print(f"Помилка обробки файлу {filename}: {e}")

    end_time = time.time()
    times[filename] = end_time - start_time

def threaded_search(file_list, keywords):
    result_dict = defaultdict(list)
    threads = []
    lock = threading.Lock()
    times = {}
    queue = Queue()

    for file in file_list:
        queue.put(file)

    def worker():
        while not queue.empty():
            file = queue.get()
            search_keywords_in_file(file, keywords, result_dict, lock, times)
            queue.task_done()

    for _ in range(min(MAX_THREADS, len(file_list))):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return dict(result_dict), times

if __name__ == "__main__":
    keywords = ["держструктур", "Катріона", "Пуанкаре"]
    files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt"]

    start_time = time.time()
    result, times = threaded_search(files, keywords)
    end_time = time.time()

    print("Threading results:", result)
    for file, duration in times.items():
        print(f"Час виконання потоку для {file}: {duration:.4f}секунд")

    print(f"Загальний час виконання (Threading): {end_time - start_time:.4f} секунд")