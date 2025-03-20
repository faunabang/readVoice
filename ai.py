import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

def get_AI(query):
    os.environ['OPENAI_API_KEY'] = openai_key
    client = OpenAI()

    prompt=[]
    prompt.append({"role": "developer", "content": f"""
주어진 교내 방송 음성을 요약하세요.  

### 요구사항  
- 방송에서 실제로 말한 내용만 요약하세요.  
- 불필요한 단어를 줄이고, 핵심 키워드만 남기세요.  
- 문장보다는 간략한 정보 전달 방식으로 정리하세요.
- 입력이 짧다면 요약도 짧게 유지하세요. 내용을 추가하지 마세요.  

출력 예시:  
방송: "오늘 급식은 김치찌개와 불고기입니다. 맛있게 드세요!"  
요약: "급식: 김치찌개, 불고기"  

방송: "오전 10시에 체육관에서 학생회 모임이 있습니다."  
요약: "학생회 모임 - 10시, 체육관"
                   """})
    prompt.append({"role": "user", "content": query})

    completion = client.chat.completions.create(
            model="gpt-4o",
            messages=prompt
        )
    answer = completion.choices[0].message.content
    
    return answer

if __name__=='__main__':
    answer = get_AI(input("User: "))
    print("ChatGPT:", answer)
