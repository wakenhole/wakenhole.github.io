import os
import sys
import datetime
import requests
import json
import time

# --- 설정 ---
API_KEY = os.environ.get("GEMINI_API_KEY")
# 모델 이름 설정
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

# 1. 주제 및 글 작성을 위한 LLM 호출
def generate_topic_and_content():
    """
    Gemini API를 호출하여 최신 트렌드를 반영한 블로그 주제, 요약, 전체 글 내용, 
    그리고 주제에 적합한 이미지 링크(overlay_image, teaser)를 생성합니다.
    """
    if not API_KEY:
        print("🚨 에러: GEMINI_API_KEY 환경 변수가 설정되지 않았습니다. GitHub Secrets를 확인하세요.")
        sys.exit(1)

    print(f"[{DATE_STR}] Gemini API를 호출하여 블로그 주제와 초안 글을 생성합니다...")

    # 🟢 [수정됨] 시스템 지침: 이미지 링크 생성 지시 추가
    system_prompt = (
        "당신은 IT/기술 블로그의 전문 작가이자 에디터입니다. 한국 독자를 대상으로 오늘 날짜의 최신 "
        "기술 트렌드 또는 유용한 개발 팁에 대한 글을 작성합니다. "
        "글은 전문적이고 흥미로운 톤앤매너로 작성하며, 완성된 마크다운 형식이어야 합니다. "
        "응답은 다른 텍스트 설명 없이, 오직 JSON 객체만 반환해야 합니다. "
        "JSON 객체는 반드시 'topic'(15자 이내 제목), 'summary'(30자 이내 요약), 'content'(마크다운 형식의 본문), "
        "'overlay_image'(주제에 적합한 고해상도 배경 이미지 URL), 'teaser'(주제에 적합한 썸네일 이미지 URL) 필드를 포함해야 합니다. "
        "이미지 URL은 Unsplash 또는 Pexels와 같은 고품질 무료 스톡 이미지 사이트의 링크여야 합니다."
    )

    # 🟢 [수정됨] 사용자 질의: 이미지 필드를 포함하도록 JSON 형식 업데이트
    user_query = (
        f"오늘 ({DATE_STR}), 한국 개발자들이 가장 관심 가질 만한 최신 기술 뉴스 또는 "
        "유용한 개발 팁에 대한 블로그 글(최소 500자 분량)을 작성해 주세요. "
        "응답은 다음 JSON 형식으로 제공해야 합니다: "
        '{"topic": "제목", "summary": "요약", "content": "## 부제목\\n\\n글 내용...", "overlay_image": "URL1", "teaser": "URL2"}'
    )

    # Tool use (Google Search grounding) 활성화
    payload = {
        "contents": [{ "parts": [{ "text": user_query }] }],
        "tools": [{ "google_search": {} }], 
        "systemInstruction": {
            "parts": [{ "text": system_prompt }]
        },
    }
    
    # 디버깅 로그
    print("\n--- 전송할 API 요청 페이로드 (Debug) ---")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print("------------------------------------------\n")


    # API 호출 (최대 3회 재시도)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 글 작성에 시간이 더 걸릴 수 있으므로 90초로 타임아웃 유지
            response = requests.post(
                API_URL,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(payload),
                timeout=90 
            )
            
            if response.status_code != 200:
                print(f"⚠️ HTTP 오류 발생: {response.status_code}")
                print(f"⚠️ 오류 메시지: {response.text}")
                
                if response.status_code < 500:
                    print("클라이언트 오류(4xx)입니다. 설정을 확인해 주세요.")
                    sys.exit(1)
                
                raise requests.exceptions.RequestException(f"API 서버 오류: {response.status_code}")

            result = response.json()
            json_string = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')
            
            if not json_string:
                 print("🚨 심각한 오류: Gemini가 텍스트 응답을 반환하지 않았습니다. 원본 응답:", result)
                 return {"topic": "API 응답 오류로 주제 생성 실패", "summary": "내용을 수동으로 입력해 주세요.", "content": "글 내용 생성에 실패했습니다.", "overlay_image": "", "teaser": ""}

            # JSON 문자열 파싱 (백틱 제거 로직 포함)
            # JSONDecodeError 방지를 위해 스트립/교체 로직을 안전하게 처리
            json_string_clean = json_string.strip().replace('```json', '').replace('```', '')
            topic_data = json.loads(json_string_clean)
            print(f"\n✅ 성공적으로 글 초안을 생성했습니다. 제목: {topic_data['topic']}")
            return topic_data

        except requests.exceptions.RequestException as e:
            print(f"❌ 요청 중 오류가 발생했습니다 (시도 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
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
    생성된 주제와 내용을 바탕으로 Jekyll Front Matter를 포함한 마크다운 파일을 생성합니다.
    """
    try:
        os.makedirs(POSTS_DIR, exist_ok=True)
        
        content = topic_data.get('content', '글 내용 생성에 실패했습니다.')
        
        # 🟢 [추가됨] 이미지 URL 기본값 설정 (JSON에 필드가 없거나 비어 있을 경우 대비)
        overlay_image = topic_data.get('overlay_image', '')
        teaser = topic_data.get('teaser', '')

        markdown_content = f"""---
layout: post
title: "{topic_data.get('topic', '오늘의 블로그 제목 (수동 입력 필요)')}"
subtitle: "{topic_data.get('summary', '주제에 대한 짧은 요약')}"
date: {TIME_STR}
author: WakenHole
categories: [Tech, Development] 
tags: [Gemini, Automation, Daily] 
published: false # 이 값이 true여야 블로그에 게시됩니다.
header:
  overlay_image: {overlay_image}
  overlay_filter: 0.5
  teaser: {teaser}
---

{content}

---

### 🖼️ 이미지 및 최종 검토

* **⚠️ 중요:** 위 `header`에 삽입된 이미지 링크를 검토하세요. 저작권 문제 없는지, 링크가 깨지지 않았는지 확인 후 발행해 주세요.
* **광고:** 원하는 위치에 직접 광고 코드를 삽입하세요.

"""
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print(f"⭐ 글 초안 파일이 성공적으로 생성되었습니다: {FILE_PATH}")

    except IOError as e:
        print(f"파일 쓰기 중 오류가 발생했습니다: {e}")
        sys.exit(1)

if __name__ == "__main__":
    generated_data = generate_topic_and_content()
    if generated_data:
        create_markdown_file(generated_data)