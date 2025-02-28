
import time
import multiprocessing
from collections import defaultdict

BUFFER_SIZE = 4096
MAX_PROCESSES = 4

def search_keywords_in_file(filename, keywords, queue):
    start_time = time.time()
    found_words = defaultdict(list)
    try:
        with open(filename, "r", encoding="utf-8") as file:
            while True:
                buffer = file.read(BUFFER_SIZE).lower()
                if not buffer:
                    break
                for keyword in keywords:
                    if keyword.lower() in buffer:
                        found_words[keyword].append(filename)
                        break
    except Exception as e:
        print(f"Помилка обробки файлу {filename}: {e}")

    end_time = time.time()
    queue.put((dict(found_words), filename, end_time - start_time))

def multiprocess_search(file_list, keywords):
    result_dict = defaultdict(list)
    queue = multiprocessing.Queue()
    processes = []
    times ={}

    num_processes = min(MAX_PROCESSES, len(file_list))
    chunks = [file_list[i::num_processes] for i in range(num_processes)]

    for chunk in chunks:
        for file in chunk:
            process = multiprocessing.Process(target=search_keywords_in_file, args=(file, keywords, queue))
            processes.append(process)
            process.start()

    for process in processes:
        process.join()

    while not queue.empty():
        partial_result, filename, duration = queue.get()
        for key, value in partial_result.items():
            result_dict[key].extend(value)
        times[filename] = duration

    return dict(result_dict), times

if __name__ == "__main__":
    keywords = ["держструктур", "Катріона", "Пуанкаре"]
    files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt"]

    start_time = time.time()
    result, times =multiprocess_search(files, keywords)
    end_time = time.time()

    print("Multiprocessing results:", result)
    for file, duration in times.items():
        print(f"Час виконання процесу для {file}: {duration:.4f} секунд")
    print(f"Загальний час виконання (Multiprocessing): {end_time - start_time:.4f} секунд")