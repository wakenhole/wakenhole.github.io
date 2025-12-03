import os
import sys
import datetime
import requests
import json
import time
import base64

# --- 설정 ---
API_KEY = os.environ.get("GEMINI_API_KEY")

# 🟢 [복구됨] 안정적인 프리뷰 모델 버전으로 롤백
TEXT_MODEL_NAME = "gemini-2.5-flash-preview-09-2025" 
TEXT_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{TEXT_MODEL_NAME}:generateContent?key={API_KEY}"

# 이미지 생성 모델
IMAGE_MODEL_NAME = "imagen-4.0-generate-001"
IMAGE_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{IMAGE_MODEL_NAME}:predict?key={API_KEY}"

# KST (한국 표준시) 기준으로 오늘 날짜와 시간을 설정
KST = datetime.timezone(datetime.timedelta(hours=9))
now = datetime.datetime.now(KST)

# 파일 이름 포맷
DATE_STR = now.strftime("%Y-%m-%d")
TIME_STR = now.strftime("%Y-%m-%d %H:%M:%S +0900")
IMAGE_FILENAME = f"{DATE_STR}-cover.png"

# 파일 경로
POSTS_DIR = "_posts"
ASSETS_DIR = "assets/images"
FILENAME = f"{DATE_STR}-draft-topic.md"
FILE_PATH = os.path.join(POSTS_DIR, FILENAME)
IMAGE_FILE_PATH = os.path.join(ASSETS_DIR, IMAGE_FILENAME)

# GitHub 환경 변수
REPO_FULL_NAME = os.environ.get('GITHUB_REPOSITORY', 'wakenhole/wakenhole.github.io')
REPO_BRANCH = os.environ.get('GITHUB_REF_NAME', 'main')
RAW_URL_BASE = f"https://raw.githubusercontent.com/{REPO_FULL_NAME}/{REPO_BRANCH}"
# ---

# 1-1. 이미지 생성 및 저장
def generate_and_save_image(topic, summary):
    """
    주제에 맞는 이미지를 생성하고 로컬에 저장한 후, GitHub Raw URL을 반환합니다.
    """
    print("🎨 블로그 주제 기반 이미지 생성 요청 중...")

    image_prompt = (
        f"A cinematic, high-resolution digital art cover image for a tech blog post about '{topic}'. "
        f"The image should be modern, visually engaging, and abstractly represent '{summary}'. "
        "Use a dark background with neon blue and purple accents. "
        "Aspect ratio: 16:9 for blog header/teaser."
    )
    
    image_payload = {
        "instances": { "prompt": image_prompt }, 
        "parameters": { 
            "sampleCount": 1,
            "aspectRatio": "16:9",
            "outputMimeType": "image/png"
        } 
    }
    
    max_retries = 3
    base64_data = None
    for attempt in range(max_retries):
        try:
            image_response = requests.post(
                IMAGE_API_URL,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(image_payload),
                timeout=120
            )
            image_response.raise_for_status()

            image_result = image_response.json()
            predictions = image_result.get('predictions', [])

            if predictions and predictions[0].get('bytesBase64Encoded'):
                base64_data = predictions[0]['bytesBase64Encoded']
                break
            else:
                print("⚠️ 이미지 API가 Base64 데이터를 반환하지 않았습니다. 재시도합니다.")
                time.sleep(2 ** attempt)

        except requests.exceptions.RequestException as e:
            print(f"❌ 이미지 요청 중 오류 발생 (시도 {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                return ""

    if not base64_data:
        return ""

    try:
        os.makedirs(ASSETS_DIR, exist_ok=True)
        image_data = base64.b64decode(base64_data)
        
        with open(IMAGE_FILE_PATH, "wb") as f:
            f.write(image_data)
            
        print(f"✅ 이미지 파일이 성공적으로 저장되었습니다: {IMAGE_FILE_PATH}")
        
        raw_image_url = f"{RAW_URL_BASE}/{IMAGE_FILE_PATH.replace(os.sep, '/')}"
        print(f"🔗 생성된 Raw URL: {raw_image_url}")
        return raw_image_url

    except Exception as e:
        print(f"❌ 이미지 파일 저장 중 오류 발생: {e}")
        return ""

# 1-2. 주제 및 글 작성을 위한 LLM 호출
def generate_topic_and_content():
    """
    Gemini API를 호출하여 최신 트렌드를 반영한 블로그 주제, 요약, 전체 글 내용을 생성합니다.
    """
    if not API_KEY:
        print("🚨 에러: GEMINI_API_KEY 환경 변수가 설정되지 않았습니다. GitHub Secrets를 확인하세요.")
        sys.exit(1)

    print(f"[{DATE_STR}] Gemini API를 호출하여 블로그 주제와 초안 글을 생성합니다...")

    system_prompt = (
        "당신은 IT/기술 블로그의 전문 작가이자 에디터입니다. 한국 독자를 대상으로 오늘 날짜의 최신 "
        "기술 트렌드 또는 유용한 개발 팁에 대한 글을 작성합니다. "
        "글은 전문적이고 흥미로운 톤앤매너로 작성하며, 완성된 마크다운 형식이어야 합니다. "
        "응답은 다른 텍스트 설명 없이, 오직 JSON 객체만 반환해야 합니다. "
        "JSON 객체는 반드시 'topic'(15자 이내 제목), 'summary'(30자 이내 요약), 'content'(마크다운 형식의 본문) 필드를 포함해야 합니다."
    )

    user_query = (
        f"오늘 ({DATE_STR}), 한국 개발자들이 가장 관심 가질 만한 최신 기술 뉴스 또는 "
        "유용한 개발 팁에 대한 블로그 글(최소 500자 분량)을 작성해 주세요. "
        "응답은 다음 JSON 형식으로 제공해야 합니다: "
        '{"topic": "제목", "summary": "요약", "content": "## 부제목\\n\\n글 내용..."}'
    )

    payload = {
        "contents": [{ "parts": [{ "text": user_query }] }],
        "tools": [{ "google_search": {} }], 
        "systemInstruction": {
            "parts": [{ "text": system_prompt }]
        },
    }
    
    topic_data = {}
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(
                TEXT_API_URL, 
                headers={'Content-Type': 'application/json'},
                data=json.dumps(payload),
                timeout=90 
            )
            
            if response.status_code != 200:
                print(f"⚠️ HTTP 오류 발생: {response.status_code}")
                # 🟢 [수정됨] 오류 내용을 반드시 출력하도록 수정
                print(f"⚠️ 상세 오류 메시지: {response.text}")
                
                if response.status_code < 500:
                    print("🚨 클라이언트 오류(4xx)가 발생하여 스크립트를 중단합니다.")
                    sys.exit(1)
                raise requests.exceptions.RequestException(f"API 서버 오류: {response.status_code}")

            result = response.json()
            json_string = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')
            
            if not json_string:
                 topic_data = {"topic": "API 응답 오류", "summary": "내용 없음", "content": "글 내용 생성 실패"}
                 break

            json_string_clean = json_string.strip().replace('```json', '').replace('```', '')
            topic_data = json.loads(json_string_clean)
            print(f"\n✅ 성공적으로 글 초안 데이터를 생성했습니다. 제목: {topic_data['topic']}")
            break 

        except requests.exceptions.RequestException as e:
            print(f"❌ API 요청 중 예외 발생: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                print("최대 재시도 횟수 도달. 텍스트 생성을 건너뜁니다.")
                sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"🚨 JSON 파싱 오류가 발생했습니다: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"🚨 예상치 못한 오류 발생: {e}")
            sys.exit(1)
            
    # 텍스트 생성 성공 후 이미지 생성 실행
    if topic_data:
        image_url = generate_and_save_image(topic_data.get('topic', '기술 트렌드'), topic_data.get('summary', '블로그 표지 이미지'))
        topic_data['overlay_image'] = image_url
        topic_data['teaser'] = image_url
        
    return topic_data


# 2. 마크다운 파일 생성
def create_markdown_file(topic_data):
    """
    생성된 주제와 내용을 바탕으로 Jekyll Front Matter를 포함한 마크다운 파일을 생성합니다.
    """
    try:
        os.makedirs(POSTS_DIR, exist_ok=True)
        
        content = topic_data.get('content', '글 내용 생성에 실패했습니다.')
        
        markdown_content = f"""---
layout: post
title: "{topic_data.get('topic', '오늘의 블로그 제목 (수동 입력 필요)')}"
subtitle: "{topic_data.get('summary', '주제에 대한 짧은 요약')}"
date: {TIME_STR}
author: WakenHole
categories: [Tech, Development] 
tags: [Gemini, Automation, Daily] 
published: false # 이 값이 true여야 블로그에 게시됩니다.
toc: true
toc_sticky: true
header:
  overlay_image: {topic_data.get('overlay_image', '')}
  overlay_filter: 0.5
  teaser: {topic_data.get('teaser', '')}
---

{content}

---

### 🖼️ 이미지 및 최종 검토

* **⚠️ 중요:** 위 `header`에 삽입된 이미지 링크는 GitHub 저장소에 커밋되어 생성된 것입니다.
* **이미지 경로:** `assets/images/{IMAGE_FILENAME}`
* **최종 검토:** AI가 생성한 글과 이미지가 주제에 맞는지 확인 후 발행해 주세요.
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
    
    if generated_data and generated_data.get('topic'):
        create_markdown_file(generated_data)
    else:
        print("🚨 데이터 생성에 실패했습니다.")
        sys.exit(1)