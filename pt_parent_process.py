import subprocess
import threading

def subprocess_one():
    subprocess.run(["python", "political_twitter_sample.py", "Configs/config_file_1.json"])

def subprocess_two():
    subprocess.run(["python", "political_twitter_sample.py", "Configs/config_file_2.json"])

def subprocess_three():
    subprocess.run(["python", "political_twitter_sample.py", "Configs/config_file_3.json"])

def main():
    while True:
        print("restarting and calling subprocesses")
        thread_one = threading.Thread(target=subprocess_one)
        thread_two = threading.Thread(target=subprocess_two)
        thread_three = threading.Thread(target=subprocess_three)
        thread_one.start()
        thread_two.start()
        thread_three.start()
        thread_one.join()
        thread_two.join()
        thread_three.join()


if __name__ == "__main__":
    main()