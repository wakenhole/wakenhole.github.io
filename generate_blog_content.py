import os
import sys
import datetime
import json
import time
import base64
import requests # 이미지는 REST API 사용 (SDK 지원 범위 고려)
import typing_extensions as typing # 스키마 정의용
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# --- 설정 ---

API_KEY = os.environ.get("GEMINI_API_KEY")

# 모델 설정
TEXT_MODEL_NAME = "gemini-2.5-flash"
IMAGE_MODEL_NAME = "imagen-4.0-generate-001" # 이미지는 REST 엔드포인트 유지

# KST (한국 표준시) 설정
KST = datetime.timezone(datetime.timedelta(hours=9))
now = datetime.datetime.now(KST)

# 파일 관련 설정
DATE_STR = now.strftime("%Y-%m-%d")
TIME_STR = now.strftime("%Y-%m-%d %H:%M:%S +0900")
IMAGE_FILENAME = f"{DATE_STR}-cover.png"

POSTS_DIR = "_posts"
ASSETS_DIR = "assets/images"
FILENAME = f"{DATE_STR}-draft-topic.md"
FILE_PATH = os.path.join(POSTS_DIR, FILENAME)
IMAGE_FILE_PATH = os.path.join(ASSETS_DIR, IMAGE_FILENAME)

# GitHub URL 설정
REPO_FULL_NAME = os.environ.get('GITHUB_REPOSITORY', 'wakenhole/wakenhole.github.io')
REPO_BRANCH = os.environ.get('GITHUB_REF_NAME', '0.0.5')
RAW_URL_BASE = f"https://raw.githubusercontent.com/{REPO_FULL_NAME}/{REPO_BRANCH}"

# --- SDK 초기화 ---
if not API_KEY:
    print("🚨 에러: GEMINI_API_KEY 환경 변수가 없습니다.")
    sys.exit(1)

genai.configure(api_key=API_KEY)

# --- 1. 이미지 생성 (Imagen 4.0 REST API) ---
# 참고: Imagen 3/4 모델은 현재 Python SDK보다 REST 방식 호출이 더 명확한 경우가 많아 유지하되 구조를 개선함
def generate_and_save_image(topic: str, summary: str) -> str:
    print(f"🎨 '{topic}' 주제로 이미지 생성 요청 중 (Imagen 4.0)...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{IMAGE_MODEL_NAME}:predict?key={API_KEY}"
    
    # 프롬프트 고도화
    image_prompt = (
        f"A cinematic, high-resolution digital art blog cover for a tech article about '{topic}'. "
        f"Concept: {summary}. "
        "Style: Cyberpunk, futuristic, neon blue and purple lighting, dark background, minimal, 8k resolution. "
        "No text, no words."
    )

    payload = {
        "instances": [{ "prompt": image_prompt }],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": "16:9",
            "outputMimeType": "image/png"
        }
    }

    # 재시도 로직
    for attempt in range(3):
        try:
            response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            predictions = result.get('predictions', [])
            
            if predictions and predictions[0].get('bytesBase64Encoded'):
                base64_data = predictions[0]['bytesBase64Encoded']
                
                # 저장
                os.makedirs(ASSETS_DIR, exist_ok=True)
                with open(IMAGE_FILE_PATH, "wb") as f:
                    f.write(base64.b64decode(base64_data))
                
                raw_url = f"{RAW_URL_BASE}/{IMAGE_FILE_PATH.replace(os.sep, '/')}"
                print(f"✅ 이미지 저장 완료: {IMAGE_FILE_PATH}")
                return raw_url
                
        except Exception as e:
            print(f"⚠️ 이미지 생성 실패 (시도 {attempt+1}/3): {e}")
            time.sleep(2 ** attempt)

    print("❌ 이미지 생성 최종 실패")
    return ""

# --- 2. 텍스트 생성 (Gemini SDK 사용) ---

# 출력 데이터 구조 정의 (TypedDict)
class BlogPostSchema(typing.TypedDict):
    topic: str
    summary: str
    content: str

def generate_topic_and_content() -> dict:
    print(f"[{DATE_STR}] Gemini SDK로 최신 기술 블로그 글 생성 중...")

    # 모델 설정 (JSON 모드 활성화)
    model = genai.GenerativeModel(
        model_name=TEXT_MODEL_NAME,
        generation_config={
            "temperature": 0.7,
            "response_mime_type": "application/json", # 핵심: JSON 강제 출력
            "response_schema": BlogPostSchema,        # 핵심: 스키마 지정
        },
        # 안전 설정 (블로그 글이므로 차단 확률 낮춤)
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )

    # 프롬프트 구성
    prompt = (
        f"오늘 ({DATE_STR}), 한국 개발자들이 관심 가질만한 최신 기술 뉴스나 개발 팁을 선정해 주세요. "
        "Google Search 도구를 사용하여 최신 정보를 바탕으로 작성하세요. "
        "글은 전문적이지만 읽기 쉬운 톤으로 작성하고, 내용은 마크다운 포맷이어야 합니다. "
        "최소 1000자 이상 작성하세요."
    )

    try:
        # 도구 사용 (Google Search)
        response = model.generate_content(
            prompt,
            tools='google_search_retrieval' # Grounding 도구 활성화
        )
        
        # SDK가 자동으로 JSON 파싱을 처리함 (text 속성 접근 시)
        # 만약 Grounding이 실패하거나 검색 결과가 없어도 모델 지식으로 생성 시도
        result_json = json.loads(response.text)
        
        print(f"✅ 글 생성 성공: {result_json.get('topic')}")
        
        # 이미지 생성 연동
        image_url = generate_and_save_image(result_json['topic'], result_json['summary'])
        result_json['overlay_image'] = image_url
        result_json['teaser'] = image_url
        
        return result_json

    except Exception as e:
        print(f"🚨 텍스트 생성 중 치명적 오류: {e}")
        # 상세 디버깅을 위해 response feedback 확인 가능
        sys.exit(1)

# --- 3. 파일 저장 ---

def create_markdown_file(data: dict):
    try:
        os.makedirs(POSTS_DIR, exist_ok=True)
        
        md_content = f"""---
layout: post
title: "{data.get('topic', 'Untitled')}"
subtitle: "{data.get('summary', '')}"
date: {TIME_STR}
author: AI_Writer
categories: [Tech, Trends]
tags: [Gemini, Automation, {DATE_STR}]
published: false
toc: true
toc_sticky: true
header:
  overlay_image: {data.get('overlay_image', '')}
  overlay_filter: 0.5
  teaser: {data.get('teaser', '')}
---

{data.get('content')}

---
*Generated by Gemini 2.5 Flash & Imagen 4.0*
"""
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            f.write(md_content)
        
        print(f"⭐ 마크다운 파일 생성 완료: {FILE_PATH}")

    except IOError as e:
        print(f"❌ 파일 쓰기 오류: {e}")
        sys.exit(1)

# --- 메인 실행 ---
if __name__ == "__main__":
    blog_data = generate_topic_and_content()
    if blog_data:
        create_markdown_file(blog_data)