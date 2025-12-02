import os
import sys
import datetime
import requests
import json

# --- 설정 ---
API_KEY = os.environ.get("GEMINI_API_KEY")
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
    Google Search grounding을 사용하여 최신 정보를 활용합니다.
    """
    if not API_KEY:
        print("에러: GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
        sys.exit(1)

    print(f"[{DATE_STR}] Gemini API를 호출하여 블로그 주제를 생성합니다...")

    # LLM이 따라야 할 시스템 지침
    system_prompt = (
        "당신은 IT/기술 블로그의 전문 에디터입니다. 한국 독자를 대상으로 오늘 날짜의 최신 "
        "기술 트렌드, 흥미로운 개발 소식, 또는 깊이 있는 프로그래밍 주제 중 하나를 선정합니다. "
        "결과는 반드시 JSON 스키마를 따라야 합니다. 생성된 주제는 15자 이내, 요약은 30자 이내로 작성합니다."
    )

    # 사용자 질의 (Google Search grounding을 통해 최신 정보를 가져오도록 유도)
    user_query = (
        f"오늘 ({DATE_STR}), 한국 개발자들이 가장 관심 가질 만한 최신 기술 뉴스 또는 "
        "유용한 개발 팁 주제 하나와 이에 대한 짧은 부제를 생성해 주세요."
    )

    # JSON 응답 스키마
    response_schema = {
        "type": "OBJECT",
        "properties": {
            "topic": { "type": "STRING", "description": "15자 이내의 한국어 블로그 글 제목." },
            "summary": { "type": "STRING", "description": "블로그 글의 부제로 사용할 30자 이내의 짧은 요약." }
        },
        "required": ["topic", "summary"]
    }

    payload = {
        "contents": [{ "parts": [{ "text": user_query }] }],
        "tools": [{ "google_search": {} }], # Google Search grounding 활성화
        "systemInstruction": {
            "parts": [{ "text": system_prompt }]
        },
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": response_schema
        }
    }

    try:
        response = requests.post(
            API_URL,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload),
            timeout=30 # 타임아웃 설정
        )
        response.raise_for_status() # HTTP 오류 발생 시 예외 발생

        result = response.json()
        
        # 응답 파싱 및 JSON 데이터 추출
        json_string = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')
        
        if not json_string:
             # 파싱 실패 시 기본 주제 제공
            print("경고: 주제 생성 API 응답이 비어있거나 파싱에 실패했습니다. 기본 주제를 사용합니다.")
            return {"topic": "오늘의 블로그 제목 (수동 입력 필요)", "summary": "최신 트렌드 반영 실패"}


        # JSON 문자열을 Python 딕셔너리로 변환
        topic_data = json.loads(json_string)
        print(f"성공적으로 주제를 생성했습니다: {topic_data['topic']}")
        return topic_data

    except requests.exceptions.RequestException as e:
        print(f"요청 중 오류가 발생했습니다: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류가 발생했습니다: {e}")
        print(f"받은 원본 응답 텍스트: {json_string}")
        sys.exit(1)
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")
        sys.exit(1)


# 2. 마크다운 파일 생성
def create_markdown_file(topic_data):
    """
    생성된 주제를 바탕으로 Jekyll Front Matter를 포함한 마크다운 파일을 생성합니다.
    """
    try:
        # _posts 디렉토리가 없으면 생성
        os.makedirs(POSTS_DIR, exist_ok=True)

        # Front Matter 및 기본 내용 작성
        markdown_content = f"""---
layout: post
title: "{topic_data.get('topic', '오늘의 블로그 제목 (수동 입력 필요)')}"
subtitle: "{topic_data.get('summary', '주제에 대한 짧은 요약')}"
date: {TIME_STR}
author: WakenHole
categories: [Tech, Development] # 기본 카테고리
tags: [Gemini, Automation, Daily] # 기본 태그
published: false # 이 값이 true여야 블로그에 게시됩니다.
---

## ✍️ 글 작성 시작

위에서 자동으로 생성된 주제와 요약을 바탕으로 내용을 작성해 보세요.

---
### 💡 참고 정보 (Gemini 검색 결과 활용)

* 이 주제는 LLM이 최신 트렌드를 반영하여 제안한 것입니다.
* 글을 작성하기 전에 관련 정보를 추가로 검색해보면 좋습니다.

### 🖼️ 이미지 첨부 위치

![이미지 대체 텍스트](assets/images/placeholder.webp)

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

