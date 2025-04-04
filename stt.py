import requests
import json

class ClovaSpeechClient:
    # Clova Speech invoke URL
    invoke_url = 'https://clovaspeech-gw.ncloud.com/external/v1/9858/bed51b24f18c618c578044a09df0ee6c95d7383d0a48670e8e9be0fec36dca2f'
    # Clova Speech secret key
    secret = '7fd7f567bf974224a37795d8b181a9bd'

    def req_upload(self, file, completion, callback=None, userdata=None, forbiddens=None, boostings=None,
                   wordAlignment=True, fullText=True, diarization=None, sed=None):
        request_body = {
            'language': 'ko-KR',
            'completion': completion,
            'callback': callback,
            'userdata': userdata,
            'wordAlignment': wordAlignment,
            'fullText': fullText,
            'forbiddens': forbiddens,
            'boostings': boostings,
            'diarization': diarization,
            'sed': sed,
            "keywordBoosting": {
                "boostings": [
                {
                    # 장소
                    "words": "제주과학고등학교, 제주과학고, 제주과고, 과학고, 과고, 제곽, 1층 교무실, 2층 교무실, 간식실, 강당, 기숙사, 노래방, 도서관, 도서관 스터디룸, 물리실험실, 무한상상실, 면학실, 멀미실, 멀티미디어실, 배지실, 생물실험실, 수학실, 연구동, VR 체험실, 전문 기자재실, 지구과학실, 체력단련실, 체육관, 학생부실, 학생활동실, 화학실험실, 행정실, 회의실",
                    "weight": 3 # 0~5, 0은 미적용
                },
                {
                    # 선생님
                    "words": "강신혜, 강지연, 고경석, 김민철, 김진욱, 김태경, 문지섭, 박강희, 박주희, 양동애, 양은심, 양원, 원선아, 유지호, 이경숙, 이윤우, 정지용, 조현태, 차민서, 최바울, 최원태, 최정호, 한승진, 현지수",
                    "weight": 2
                },
                {
                    # 26기
                    "words": "강수완, 고대욱, 고미르, 김도현, 김미래, 김범석, 김영한, 김예은, 김유진, 김재준, 김지현, 김태원, 김형건, 문지환, 박민준, 부지성, 양예솔, 이주하, 정예찬, 조민석, 현민서, 고은우, 김가현, 김동연, 김동휘, 김라엘, 김소진, 김승준, 문대원, 문지원, 박서율, 박소은, 부권준, 성준석, 손문진, 양선홍, 정유근, 현유진, 현채은, 홍은찬",
                    "weight": 4
                },
                {
                    # 25기
                    "words": "강서현, 고민석, 고창환, 김나연, 김도율, 김도훈, 김아영, 김예림, 김채현, 박건우, 박태현, 양승우, 오치영, 이예찬, 이은상, 장지호, 정우진, 최향아, 현승원, 강지윤, 김빛나, 김승환, 김태이, 김현상, 김효빈, 박성빈, 변용훈, 송민준, 양다현, 유서준, 이권, 이세호, 이준이, 정하정, 최승운, 현도훈, 현정운",
                    "weight": 4
                },
                {
                    # 행사명
                    "words": "R&E, 과제연구 영어 발표대회, 미니체육대회, 산울림 축제, 수학 과학 정보 경시대회, 수학 여행, 신입생 적응 캠프, 아이스 브레이킹, 자연 탐사, 전문 기자재 체험의 날, 정서지원 미술치료, 진로 특성화 개인 연구 활동, 할로윈, 학술논문읽기대회, 스팀 산출물 대회, 무한상상 스팀",
                    "weight": 2
                }
                ],
            },
            "forbidden": {
                "forbiddens": "병호실"
            }
        }
        headers = {
            'Accept': 'application/json;UTF-8',
            'X-CLOVASPEECH-API-KEY': self.secret
        }
        # print(json.dumps(request_body, ensure_ascii=False).encode('UTF-8'))
        files = {
            'media': open(file, 'rb'),
            'params': (None, json.dumps(request_body, ensure_ascii=False).encode('UTF-8'), 'application/json')
        }
        response = requests.post(headers=headers, url=self.invoke_url + '/recognizer/upload', files=files)
        return response

if __name__ == '__main__':
    res = ClovaSpeechClient().req_upload(file='won.m4a', completion='sync')
    # print(res.text)
    if res.status_code == 200:
        response_json = res.json()
        print(response_json.get('text', '텍스트를 찾을 수 없습니다.'))
    else:
        print(f"Error: {res.status_code}, {res.text}")

