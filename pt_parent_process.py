import subprocess
import threading

def subprocess_one():
    subprocess.call(["python", "political_twitter_sample_1.py"])

def subprocess_two():
    subprocess.call(["python", "political_twitter_sample_2.py"])

def subprocess_three():
    subprocess.call(["python", "political_twitter_sample_3.py"])

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