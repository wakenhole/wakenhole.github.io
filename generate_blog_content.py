import os
import sys
import datetime
import requests
import json
import time
import base64
import re  # 🟢 [추가됨] 파일명 정규화용

# --- 설정 ---
API_KEY = os.environ.get("GEMINI_API_KEY")

# 모델 설정
TEXT_MODEL_NAME = "gemini-2.5-flash-preview-09-2025" 
TEXT_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{TEXT_MODEL_NAME}:generateContent?key={API_KEY}"

IMAGE_MODEL_NAME = "imagen-4.0-generate-001"
IMAGE_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{IMAGE_MODEL_NAME}:predict?key={API_KEY}"

KST = datetime.timezone(datetime.timedelta(hours=9))
now = datetime.datetime.now(KST)

DATE_STR = now.strftime("%Y-%m-%d")
TIME_STR = now.strftime("%Y-%m-%d %H:%M:%S +0900")
IMAGE_FILENAME = f"{DATE_STR}-cover.png"

POSTS_DIR = "_posts"
ASSETS_DIR = "assets/images"
IMAGE_FILE_PATH = os.path.join(ASSETS_DIR, IMAGE_FILENAME)

REPO_FULL_NAME = os.environ.get('GITHUB_REPOSITORY', 'wakenhole/wakenhole.github.io')
REPO_BRANCH = os.environ.get('GITHUB_REF_NAME', 'main')
RAW_URL_BASE = f"https://raw.githubusercontent.com/{REPO_FULL_NAME}/{REPO_BRANCH}"
# ---

def generate_and_save_image(topic, summary):
    print("🎨 블로그 주제 기반 이미지 생성 요청 중...")
    
    image_prompt = (
        f"A cinematic, high-resolution digital art cover image for a tech blog post about '{topic}'. "
        f"The image should be modern, visually engaging, and abstractly represent '{summary}'. "
        "Use a dark background with neon blue and purple accents. "
        "Aspect ratio: 16:9 for blog header/teaser."
    )
    
    image_payload = {
        "instances": [
            { "prompt": image_prompt }
        ],
        "parameters": { 
            "sampleCount": 1, 
            "aspectRatio": "16:9"
        } 
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            image_response = requests.post(
                IMAGE_API_URL,
                headers={'Content-Type': 'application/json'},
                data=json.dumps(image_payload),
                timeout=120
            )
            
            if image_response.status_code != 200:
                print(f"⚠️ 이미지 생성 API 오류 ({image_response.status_code}): {image_response.text}")
                image_response.raise_for_status()

            image_result = image_response.json()
            predictions = image_result.get('predictions', [])

            if predictions and predictions[0].get('bytesBase64Encoded'):
                base64_data = predictions[0]['bytesBase64Encoded']
                
                os.makedirs(ASSETS_DIR, exist_ok=True)
                image_data = base64.b64decode(base64_data)
                with open(IMAGE_FILE_PATH, "wb") as f:
                    f.write(image_data)
                
                raw_image_url = f"{RAW_URL_BASE}/{IMAGE_FILE_PATH.replace(os.sep, '/')}"
                print(f"✅ 이미지 생성 및 저장 완료: {raw_image_url}")
                return raw_image_url
            else:
                print("⚠️ 이미지 데이터가 응답에 없습니다. 재시도합니다.")
                time.sleep(2 ** attempt)

        except Exception as e:
            print(f"❌ 이미지 생성 실패 (시도 {attempt + 1}): {e}")
            if attempt < max_retries - 1: time.sleep(2 ** attempt)
            else: return ""
    return ""

def generate_topic_and_content():
    if not API_KEY:
        print("🚨 에러: GEMINI_API_KEY가 설정되지 않았습니다.")
        sys.exit(1)

    print(f"[{DATE_STR}] Gemini API({TEXT_MODEL_NAME}) 호출 중...")

    system_prompt = (
        "당신은 IT/기술 블로그 에디터입니다. 오늘 날짜의 최신 기술 트렌드나 개발 팁을 주제로 선정하세요. "
        "응답은 오직 JSON 형식이어야 합니다. Markdown 포맷을 사용하지 말고 순수 JSON 텍스트만 반환하세요."
    )

    user_query = (
        f"오늘({DATE_STR}) 한국 개발자를 위한 블로그 글 주제와 내용을 작성해 주세요. "
        "다음 JSON 구조를 엄격히 따라 주세요: "
        '{"topic": "제목", "summary": "요약", "content": "마크다운 본문"}'
    )

    payload = {
        "contents": [{ "parts": [{ "text": user_query }] }],
        "tools": [{ "google_search": {} }], 
        "systemInstruction": { "parts": [{ "text": system_prompt }] },
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
                print(f"⚠️ 텍스트 API 오류: {response.text}")
                if response.status_code < 500: sys.exit(1)
                raise requests.exceptions.RequestException(f"Status {response.status_code}")

            try:
                result = response.json()
            except json.JSONDecodeError:
                print(f"🚨 API 응답이 JSON이 아닙니다.")
                continue

            try:
                candidates = result.get('candidates', [{}])
                if not candidates:
                    print(f"⚠️ 생성된 후보가 없습니다. 응답: {result}")
                    continue
                parts = candidates[0].get('content', {}).get('parts', [{}])
                json_string = parts[0].get('text', '')
            except Exception as e:
                print(f"⚠️ 응답 구조 파싱 실패: {e}")
                continue
            
            if not json_string:
                continue

            json_string_clean = json_string.strip().replace('```json', '').replace('```', '')
            
            try:
                topic_data = json.loads(json_string_clean)
                print(f"✅ 주제 생성 성공: {topic_data.get('topic')}")
                break
            except json.JSONDecodeError as e:
                print(f"🚨 JSON 파싱 실패. 재시도합니다.")
                time.sleep(2)
                continue

        except Exception as e:
            print(f"❌ 요청 오류: {e}")
            time.sleep(2 ** attempt)

    if topic_data:
        image_url = generate_and_save_image(topic_data.get('topic', ''), topic_data.get('summary', ''))
        topic_data['overlay_image'] = image_url
        topic_data['teaser'] = image_url
        
    return topic_data

def create_markdown_file(topic_data):
    try:
        os.makedirs(POSTS_DIR, exist_ok=True)
        content = topic_data.get('content', '')
        topic_title = topic_data.get('topic', 'draft-topic')

        # 🟢 [수정됨] 파일명 생성 로직: 주제를 이용하여 안전한 파일명 생성
        # 공백을 하이픈으로, 특수문자는 제거 (한글/영문/숫자/하이픈만 허용)
        safe_title = re.sub(r'[^\w\s-]', '', topic_title).strip().replace(' ', '-')
        
        # 파일명 길이 제한 (너무 길 경우 잘라냄)
        if len(safe_title) > 50:
            safe_title = safe_title[:50]
            
        filename = f"{DATE_STR}-{safe_title}.md"
        file_path = os.path.join(POSTS_DIR, filename)
        
        markdown_content = f"""---
layout: post
title: "{topic_title}"
subtitle: "{topic_data.get('summary', '')}"
date: {TIME_STR}
author: WakenHole
categories: [Tech, Development] 
tags: [Gemini, Automation] 
published: false
toc: true
toc_sticky: true
header:
  overlay_image: {topic_data.get('overlay_image', '')}
  overlay_filter: 0.5
  teaser: {topic_data.get('teaser', '')}
---

{content}

---
*AI Generated Content*
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"⭐ 파일 생성 완료: {file_path}")

    except IOError as e:
        print(f"파일 쓰기 실패: {e}")
        sys.exit(1)

if __name__ == "__main__":
    data = generate_topic_and_content()
    if data and data.get('topic'):
        create_markdown_file(data)
    else:
        print("🚨 최종적으로 데이터 생성에 실패했습니다.")
        sys.exit(1)