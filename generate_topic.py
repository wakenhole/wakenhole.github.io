import os
import sys
import datetime
import requests
import json
import time

# --- 설정 ---
API_KEY = os.environ.get("GEMINI_API_KEY")
# 모델 이름을 변수로 분리하여 관리 용이성 및 디버깅을 높임
MODEL_NAME = "gemini-2.5-flash-preview-09-2025" 
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent?key={API_KEY}"

# KST (한국 표준시) 기준으로 오늘 날짜와 시간을 설정
KST = datetime.timezone(datetime.timedelta(hours=9))
now = datetime.datetime.now(KST)

# 파일 이름과 Front Matter에 사용할 날짜/시간 포맷
DATE_STR = now.strftime("%Y-%m-%d")
TIME_STR = now.strftime("%Y-%m-%d %H:%M:%S +0900")

# 파일 경로
POSTS_DIR = "_posts"
FILENAME = f"{DATE_STR}-draft-topic.md"
FILE_PATH = os.path.join(POSTS_DIR, FILENAME)
# ---

# 1. 주제 생성을 위한 LLM 호출
def generate_topic():
    """
    Gemini API를 호출하여 최신 트렌드를 반영한 블로그 주제와 요약을 JSON 형태로 요청합니다.
    """
    if not API_KEY:
        print("🚨 에러: GEMINI_API_KEY 환경 변수가 설정되지 않았습니다. GitHub Secrets를 확인하세요.")
        sys.exit(1)

    print(f"[{DATE_STR}] Gemini API를 호출하여 블로그 주제를 생성합니다...")

    # 🟢 [수정됨] 시스템 지침 변경: JSON 형식 '만' 반환하도록 강력하게 지시
    system_prompt = (
        "당신은 IT/기술 블로그의 전문 에디터입니다. 한국 독자를 대상으로 오늘 날짜의 최신 "
        "기술 트렌드, 흥미로운 개발 소식, 또는 깊이 있는 프로그래밍 주제 중 하나를 선정합니다. "
        "응답은 다른 텍스트 설명 없이, 오직 JSON 객체만 반환해야 합니다. "
        "JSON 객체는 반드시 'topic'(15자 이내 제목)과 'summary'(30자 이내 요약) 필드를 포함해야 합니다."
    )

    # 사용자 질의 (Google Search grounding을 통해 최신 정보를 가져오도록 유도)
    user_query = (
        f"오늘 ({DATE_STR}), 한국 개발자들이 가장 관심 가질 만한 최신 기술 뉴스 또는 "
        "유용한 개발 팁 주제 하나와 이에 대한 짧은 부제를 다음 JSON 형식으로 생성해 주세요: "
        '{"topic": "제목", "summary": "요약"}'
    )

    # 🔴 [제거됨] generationConfig 제거 (Tool use와 충돌하는 부분)
    payload = {
        "contents": [{ "parts": [{ "text": user_query }] }],
        "tools": [{ "google_search": {} }], # Google Search grounding 활성화
        "systemInstruction": {
            "parts": [{ "text": system_prompt }]
        },
    }
    
    # 🔎 디버깅 로그 출력
    print("\n--- 전송할 API 요청 페이로드 (Debug) ---")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print("------------------------------------------\n")


    # API 호출 (최대 3회 재시도 로직 추가)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(
                API_URL,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(payload),
                timeout=45 # 타임아웃 45초로 연장
            )
            
            # HTTP 오류 발생 시
            if response.status_code != 200:
                print(f"⚠️ HTTP 오류 발생: {response.status_code}")
                print(f"⚠️ 오류 메시지: {response.text}")
                
                # 4xx 클라이언트 오류 시 재시도 없이 종료
                if response.status_code < 500:
                    print("클라이언트 오류(4xx)입니다. 설정을 확인해 주세요.")
                    sys.exit(1)
                
                # 서버 오류(5xx) 시 재시도
                raise requests.exceptions.RequestException(f"API 서버 오류: {response.status_code}")

            # 성공적인 응답 (200 OK)
            result = response.json()
            
            # 🟢 [수정 없음] 응답 텍스트 파싱. 모델이 JSON 형식만 반환하도록 프롬프트에서 지시했기 때문에 이 텍스트를 바로 JSON.loads로 파싱합니다.
            json_string = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')
            
            if not json_string:
                 print("🚨 심각한 오류: Gemini가 텍스트 응답을 반환하지 않았습니다. 원본 응답:", result)
                 return {"topic": "API 응답 오류로 주제 생성 실패", "summary": "내용을 수동으로 입력해 주세요."}

            # JSON 문자열을 Python 딕셔너리로 변환
            # (만약 모델이 불필요한 마크다운 백틱(```json)을 추가했다면 이 부분에서 에러가 날 수 있음)
            topic_data = json.loads(json_string.strip().replace('```json', '').replace('```', ''))
            print(f"\n✅ 성공적으로 주제를 생성했습니다: {topic_data['topic']}")
            return topic_data

        except requests.exceptions.RequestException as e:
            print(f"❌ 요청 중 오류가 발생했습니다 (시도 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                # 지수 백오프 (2초, 4초 대기)
                wait_time = 2 ** (attempt + 1)
                print(f"재시도합니다. {wait_time}초 대기...")
                time.sleep(wait_time)
            else:
                print("최대 재시도 횟수에 도달했습니다. 스크립트를 종료합니다.")
                sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"🚨 JSON 파싱 오류가 발생했습니다: {e}")
            print(f"받은 원본 응답 텍스트: {json_string[:500]}...")
            sys.exit(1)
        except Exception as e:
            print(f"🚨 예상치 못한 오류 발생: {e}")
            sys.exit(1)


# 2. 마크다운 파일 생성
def create_markdown_file(topic_data):
    """
    생성된 주제를 바탕으로 Jekyll Front Matter를 포함한 마크다운 파일을 생성합니다.
    """
    try:
        os.makedirs(POSTS_DIR, exist_ok=True)

        markdown_content = f"""---
layout: post
title: "{topic_data.get('topic', '오늘의 블로그 제목 (수동 입력 필요)')}"
subtitle: "{topic_data.get('summary', '주제에 대한 짧은 요약')}"
date: {TIME_STR}
author: WakenHole
categories: [Tech, Development] 
tags: [Gemini, Automation, Daily] 
published: false # 이 값이 true여야 블로그에 게시됩니다.
---

## ✍️ 글 작성 시작

위에서 자동으로 생성된 주제와 요약을 바탕으로 내용을 작성해 보세요.

---
### 💡 참고 정보

* 이 주제는 LLM이 최신 트렌드를 반영하여 제안한 것입니다.

### 🖼️ 이미지 첨부 위치

![이미지 대체 텍스트](assets/images/{DATE_STR}-image.webp)

"""
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print(f"⭐ 마크다운 파일이 성공적으로 생성되었습니다: {FILE_PATH}")

    except IOError as e:
        print(f"파일 쓰기 중 오류가 발생했습니다: {e}")
        sys.exit(1)

if __name__ == "__main__":
    generated_topic = generate_topic()
    if generated_topic:
        create_markdown_file(generated_topic)