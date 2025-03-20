import pyaudio
import numpy as np
import wave
import time
from datetime import datetime
import json
import os
from stt import ClovaSpeechClient
from ai import get_AI

FILE_EXTENSION = ".mp3"
THRESHOLD = 2000
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SILENCE_DURATION = 3

audio = pyaudio.PyAudio()

def is_silent(data):
    return max(np.frombuffer(data, dtype=np.int16)) < THRESHOLD

def save_recording(frames):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date = datetime.now().strftime("%Y-%m-%d")
    audio_dir = f"./audio/{date}"
    stt_file = f"./stt/{date}.json"

    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

    audio_filename = f"{audio_dir}/{timestamp.replace(':', '_').replace(' ', '_')}.mp3"

    wf = wave.open(audio_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"{audio_filename}에 저장되었습니다.")

    # STT 수행
    stt_client = ClovaSpeechClient()
    response = stt_client.req_upload(file=audio_filename, completion='sync')
    if response.status_code == 200:
        stt_result = response.json().get('text', '').strip()
        
        # STT 결과가 비어있으면 건너뛰기
        if not stt_result:
            print("STT 결과가 비어 있어 AI 요약을 수행하지 않습니다.")
            return
        # STT 결과가 짧으면 건너뛰기
        elif len(stt_result) <= 6:
            print("STT 결과가 너무 짧아 AI 요약을 수행하지 않습니다.")
            return

        # AI 요약 수행
        ai_summary = get_AI(stt_result)

        if not os.path.exists("./stt"):
            os.makedirs("./stt")

        if os.path.exists(stt_file):
            with open(stt_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []

        data.append({
            "timestamp": timestamp,
            "audio_filename": audio_filename,
            "stt_text": stt_result,
            "ai_summary": ai_summary
        })

        with open(stt_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"STT 및 AI 요약 결과가 {stt_file}에 저장되었습니다.")
    else:
        print(f"STT 요청 실패: {response.status_code}, {response.text}")


def record_audio():
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    try:
        while True:
            frames = []
            recording = False
            silent_start = None
            print("소리를 감지하고 있습니다...")

            while True:
                data = stream.read(CHUNK, exception_on_overflow=False)

                if not is_silent(data):
                    if not recording:
                        print("\n녹음 시작")
                        recording = True
                    frames.append(data)
                    silent_start = None
                elif recording:
                    if silent_start is None:
                        silent_start = time.time()
                    elif time.time() - silent_start >= SILENCE_DURATION:
                        print("\n녹음 종료 및 파일 저장")
                        save_recording(frames)
                        break
                    else:
                        frames.append(data)
    except KeyboardInterrupt:
        print("\nCtrl+C 발생 - 녹음을 중지합니다.")
        if frames:
            save_recording(frames)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == '__main__':
    record_audio()
