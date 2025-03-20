import subprocess
import signal
import os

# 프로세스를 저장할 리스트
processes = []

try:
    # Flask 서버 실행
    flask_process = subprocess.Popen(["python", "app.py"])
    processes.append(flask_process)

    # 추가 Python 스크립트 실행
    other_process = subprocess.Popen(["python", "audio.py"])
    processes.append(other_process)

    # 부모 프로세스가 종료될 때까지 대기
    for process in processes:
        process.wait()

except KeyboardInterrupt:
    # CTRL + C가 눌리면 모든 자식 프로세스 종료
    print("\nCTRL + C detected! Terminating all subprocesses...")
    for process in processes:
        process.terminate()  # 자식 프로세스 종료
        process.wait()       # 프로세스가 종료될 때까지 대기

print("All processes terminated.")
