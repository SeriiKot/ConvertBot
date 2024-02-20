import psutil
import time
import subprocess

def is_process_running(process_name):
    for process in psutil.process_iter():
        if process.name() == process_name:
            return True
    return False

def start_main_script():
    print("Starting main.py...")
    subprocess.Popen(["python3", "main.py"])

if __name__ == "__main__":
    process_name = "python"  # Имя процесса, который вы хотите проверить (например, "python")
    while True:
        if not is_process_running(process_name):
            start_main_script()
        time.sleep(300)  # Пауза на 5 минут (300 секунд)
