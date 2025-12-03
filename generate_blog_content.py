import os
import sys
import datetime
import json
import time
import base64
import requests

# 🟢 [변경] 새로운 SDK 임포트
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# --- 설정 ---

API_KEY = os.environ.get("GEMINI_API_KEY")

# 🟢 [모델 변경] Gemini 3.0 Pro Preview
# (권한 문제 시 'gemini-2.0-flash'로 변경하면 동일한 코드로 작동합니다)
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

REPO_FULL_NAME = os.environ.get('GITHUB_REPOSITORY', 'wakenhole/wakenhole.github.io')
REPO_BRANCH = os.environ.get('GITHUB_REF_NAME', '0.0.5')
RAW_URL_BASE = f"https://raw.githubusercontent.com/{REPO_FULL_NAME}/{REPO_BRANCH}"

# --- SDK 초기화 ---
if not API_KEY:
    print("🚨 에러: GEMINI_API_KEY 환경 변수가 없습니다.")
    sys.exit(1)

# 🟢 [변경] 새로운 Client 방식 초기화
client = genai.Client(api_key=API_KEY)


# --- 1. 이미지 생성 (Imagen 4.0 - REST API) ---
# 이미지 생성은 기존 REST 방식이 여전히 가장 간편하고 호환성이 좋아 유지합니다.
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
                
                raw_url = f"{RAW_URL_BASE}/{IMAGE_FILE_PATH.replace(os.sep, '/')}"
                print(f"✅ 이미지 저장 완료: {IMAGE_FILE_PATH}")
                return raw_url
                
        except Exception as e:
            print(f"⚠️ 이미지 생성 실패 (시도 {attempt+1}/3): {e}")
            time.sleep(2 ** attempt)

    print("❌ 이미지 생성 최종 실패")
    return ""


# --- 2. 텍스트 생성 (New SDK & Pydantic) ---

# 🟢 [추가] Pydantic을 이용한 명확한 데이터 구조 정의
class BlogPost(BaseModel):
    topic: str = Field(description="블로그 글의 매력적인 제목 (15자 이내)")
    summary: str = Field(description="글의 핵심 요약 (30자 이내)")
    content: str = Field(description="마크다운 형식의 블로그 본문. 최소 1500자 이상.")

def generate_topic_and_content() -> dict:
    print(f"[{DATE_STR}] {TEXT_MODEL_NAME} 모델로 글 생성 중 (New SDK)...")

    prompt = (
        f"오늘 ({DATE_STR}), 한국 개발자들이 관심 가질만한 최신 기술 뉴스나 개발 팁을 선정해 주세요. "
        "반드시 Google Search 도구를 사용하여 최신 웹 정보를 검색하고 이를 바탕으로 글을 작성하세요. "
        "글은 전문적이지만 읽기 쉬운 톤으로 작성하고, 내용은 마크다운 포맷이어야 합니다. "
        "본문은 최소 1500자 이상 풍부하게 작성해주세요."
    )

    try:
        # 🟢 [변경] 새로운 generate_content 메서드 호출 방식
        response = client.models.generate_content(
            model=TEXT_MODEL_NAME,
            contents=prompt,
            config={
                # 사용자가 원했던 딕셔너리 형태의 tools 설정이 여기서 가능합니다.
                "tools": [{"google_search": {}}], 
                "response_mime_type": "application/json",
                # Pydantic 스키마를 직접 전달하여 자동 파싱 유도
                "response_schema": BlogPost, 
            },
        )

        # 🟢 [변경] Pydantic 모델로 자동 파싱된 결과 사용
        # response.parsed는 위에서 정의한 BlogPost 객체입니다.
        if not response.parsed:
             raise ValueError("응답 파싱 실패 (내용 없음)")

        result = response.parsed
        
        print(f"✅ 글 생성 성공: {result.topic}")
        
        # Pydantic 객체를 딕셔너리로 변환
        result_dict = result.model_dump()

        # 이미지 생성 연동
        image_url = generate_and_save_image(result.topic, result.summary)
        result_dict['overlay_image'] = image_url
        result_dict['teaser'] = image_url
        
        return result_dict

    except Exception as e:
        print(f"🚨 텍스트 생성 중 오류 발생: {e}")
        # 상세 디버깅 정보
        import traceback
        traceback.print_exc()
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
*Generated by {TEXT_MODEL_NAME} (Google Search Grounded) & {IMAGE_MODEL_NAME}*
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