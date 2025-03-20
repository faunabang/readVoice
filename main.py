import subprocess
import signal
import os
import sys

# 현재 실행 중인 Python 인터프리터의 경로를 가져옴 (가상 환경 포함)
python_executable = sys.executable

# 프로세스를 저장할 리스트
processes = []

try:
    # Flask 서버 실행
    flask_process = subprocess.Popen([python_executable, "app.py"])
    processes.append(flask_process)

    # 추가 Python 스크립트 실행
    other_process = subprocess.Popen([python_executable, "audio.py"])
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
