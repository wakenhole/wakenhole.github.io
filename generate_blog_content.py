import os
import sys
import datetime
import json
import time
import base64
import requests
import typing_extensions as typing
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
# 🟢 [추가됨] 명시적 도구 설정을 위한 protos 모듈 임포트
from google.generativeai import protos

# --- 설정 ---

API_KEY = os.environ.get("GEMINI_API_KEY")

# 모델 설정
# 주의: 3.0 Preview 모델이 API 키에서 활성화되지 않은 경우 404 오류가 날 수 있습니다.
# 오류 지속 시 "gemini-1.5-pro" 또는 "gemini-2.0-flash-exp"로 변경하세요.
TEXT_MODEL_NAME = "gemini-3.0-pro-preview" 
IMAGE_MODEL_NAME = "imagen-4.0-generate-001"

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
def generate_and_save_image(topic: str, summary: str) -> str:
    print(f"🎨 '{topic}' 주제로 이미지 생성 요청 중 ({IMAGE_MODEL_NAME})...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{IMAGE_MODEL_NAME}:predict?key={API_KEY}"
    
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

    for attempt in range(3):
        try:
            response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=120)
            response.raise_for_status()
            
            result = response.json()
            predictions = result.get('predictions', [])
            
            if predictions and predictions[0].get('bytesBase64Encoded'):
                base64_data = predictions[0]['bytesBase64Encoded']
                
                os.makedirs(ASSETS_DIR, exist_ok=True)
                with open(IMAGE_FILE_PATH, "wb") as f:
                    f.write(base64.b64decode(base64_data))
                
                # Windows 호환성을 위해 경로 구분자 교체
                raw_url = f"{RAW_URL_BASE}/{IMAGE_FILE_PATH.replace(os.sep, '/')}"
                print(f"✅ 이미지 저장 완료: {IMAGE_FILE_PATH}")
                return raw_url
                
        except Exception as e:
            print(f"⚠️ 이미지 생성 실패 (시도 {attempt+1}/3): {e}")
            time.sleep(2 ** attempt)

    print("❌ 이미지 생성 최종 실패")
    return ""

# --- 2. 텍스트 생성 (Gemini SDK 사용) ---

class BlogPostSchema(typing.TypedDict):
    topic: str
    summary: str
    content: str

def generate_topic_and_content() -> dict:
    print(f"[{DATE_STR}] {TEXT_MODEL_NAME} 모델로 블로그 글 생성 중...")

    # 🟢 [수정됨] protos를 사용하여 Google Search 도구를 명시적으로 정의
    # 이렇게 하면 SDK의 자동 파싱 오류(FunctionDeclaration 등)를 우회할 수 있습니다.
    search_tool = protos.Tool(
        google_search=protos.GoogleSearch()
    )

    model = genai.GenerativeModel(
        model_name=TEXT_MODEL_NAME,
        tools=[search_tool], # 수정됨: protos 객체 리스트 전달
        generation_config={
            "temperature": 0.7,
            "response_mime_type": "application/json",
            "response_schema": BlogPostSchema,
        },
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        }
    )

    prompt = (
        f"오늘 ({DATE_STR}), 한국 개발자들이 관심 가질만한 최신 기술 뉴스나 개발 팁을 선정해 주세요. "
        "Google Search 도구를 사용하여 반드시 최신 정보를 바탕으로 작성하세요. "
        "글은 전문적이지만 읽기 쉬운 톤으로 작성하고, 내용은 마크다운 포맷이어야 합니다. "
        "최소 1500자 이상 작성하세요."
    )

    try:
        response = model.generate_content(prompt)
        
        # JSON 모드를 사용하므로 텍스트를 바로 파싱 가능
        result_json = json.loads(response.text)
        
        print(f"✅ 글 생성 성공: {result_json.get('topic')}")
        
        image_url = generate_and_save_image(result_json['topic'], result_json['summary'])
        result_json['overlay_image'] = image_url
        result_json['teaser'] = image_url
        
        return result_json

    except Exception as e:
        print(f"🚨 텍스트 생성 중 오류 발생: {e}")
        import traceback
        traceback.print_exc() # 상세 에러 로그 출력
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
*Generated by {TEXT_MODEL_NAME} & {IMAGE_MODEL_NAME}*
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