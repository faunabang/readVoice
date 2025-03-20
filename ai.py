import os
from openai import OpenAI

def get_AI(query):
    
    client = OpenAI()

    prompt=[]
    prompt.append({"role": "developer", "content": f"""
                   다음 제공되는 교내 방송 내용을 핵심 내용을 중심으로 요약하여라. 제공된 정보만을 통해 요약을 작성하며, 그 외에 다른 말은 일절 작성하지 말고, 한국어로 작성하여라.
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
