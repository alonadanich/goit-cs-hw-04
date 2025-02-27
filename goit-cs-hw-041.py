import threading
import time
from collections import defaultdict

def search_keywords_in_file(filename, keywords, result_dict, lock, times):
    start_time = time.time()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            content = file.read().lower()
            for keyword in keywords:
                if keyword.lower() in content:
                    with lock:
                        result_dict[keyword].append(filename)
    except Exception as e:
        print(f"Помилка обробки файлу {filename}: {e}")

    end_time = time.time()
    times[filename] = end_time - start_time

def threaded_search(file_list, keywords):
    result_dict = defaultdict(list)
    threads = []
    lock = threading.Lock()
    times = {}

    for file in file_list:
        thread = threading.Thread(target=search_keywords_in_file, args=(file, keywords, result_dict, lock, times))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return dict(result_dict), times

if __name__ == "__main__":
    keywords = ["механізм", "програму", "реалізовано"]
    files = ["file1.txt", "file2.txt", "file3.txt"]

    start_time = time.time()
    result, times = threaded_search(files, keywords)
    end_time = time.time()

    print("Threading results:", result)
    for file, duration in times.items():
        print(f"Час виконання потоку для {file}: {duration:.4f}секунд")

    print(f"Загальний час виконання (Threading): {end_time - start_time:.4f} секунд")