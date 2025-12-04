import os
import sys
import datetime
import requests
import json
import time
import re
import argparse # 👈 인자(Argument) 처리를 위해 추가

# --- 설정 ---
API_KEY = os.environ.get("GEMINI_API_KEY")

# 텍스트 모델 설정
TEXT_MODEL_NAME = "gemini-2.5-flash-preview-09-2025" 
TEXT_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{TEXT_MODEL_NAME}:generateContent?key={API_KEY}"

KST = datetime.timezone(datetime.timedelta(hours=9))
now = datetime.datetime.now(KST)

DATE_STR = now.strftime("%Y-%m-%d")
TIME_STR = now.strftime("%Y-%m-%d %H:%M:%S +0900")

POSTS_DIR = "_posts"

# --- 1. 인자 파싱 설정 (Workflow에서 값을 받아옴) ---
def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate Blog Post with Gemini")
    parser.add_argument("--category", type=str, required=True, help="블로그 글의 대주제 (예: Tech, Investment)")
    parser.add_argument("--audience", type=str, required=True, help="타겟 독자 (예: 개발자, 초보 투자자)")
    parser.add_argument("--topic_keyword", type=str, default="최신 트렌드", help="글감 키워드 (예: AI 뉴스, 미국 주식)")
    parser.add_argument("--tags", type=str, default="Blog", help="콤마로 구분된 태그 (예: IT, AI)")
    return parser.parse_args()

# ---

def validate_image_url(url):
    # (기존 코드와 동일)
    if not url: return ""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 ...'} # 짧게 줄임
        response = requests.get(url, headers=headers, timeout=5, stream=True)
        if response.status_code == 200 and 'image' in response.headers.get('Content-Type', '').lower():
            response.close()
            return url
        response.close()
        return ""
    except Exception:
        return ""

def generate_topic_and_content(args): # 👈 args를 받도록 수정
    if not API_KEY:
        print("🚨 에러: GEMINI_API_KEY가 설정되지 않았습니다.")
        sys.exit(1)

    print(f"[{DATE_STR}] Gemini API 호출 중... 카테고리: {args.category}")

    # 🟢 [수정됨] 변수화된 시스템 프롬프트
    system_prompt = (
        f"당신은 전문적인 '{args.category}' 블로그 에디터입니다. \n"
        f"주제는 최근 뉴스나 트렌드 기반으로 선정하며, '{args.audience}'가 흥미를 가질만한 내용이어야 합니다.\n"
        "응답은 오직 JSON 형식이어야 합니다. Markdown 포맷을 사용하지 말고 순수 JSON 텍스트만 반환하세요."
    )

    # 🟢 [수정됨] 변수화된 사용자 질의
    user_query = (
        f"오늘({DATE_STR}) '{args.audience}'를 위한 '{args.topic_keyword}' 관련 블로그 글을 작성해 주세요. \n"
        "글 작성시 사실에 기반해서 작성해야하고, 참조한 출처가 있다면 반드시 명시해야 합니다. \n"
        "1. **주제(topic)**: 임팩트 있는 **10자 내외**의 제목.\n"
        "2. **내용(content)**: 깊이 있는 내용으로 마크다운 형식 **최소 1000자 이상** 작성. 본문 중간중간에 `##` 를 사용하여 소제목을 명확히 구분해 주세요.\n"
        "3. **이미지(image_url)**: 주제와 관련된 **저작권 문제없는 공개 이미지(Unsplash 등)의 직접 링크(URL)** 하나를 검색해서 찾아주세요.\n\n"
        "응답은 다음 JSON 구조를 엄격히 따라 주세요: "
        '{"topic": "제목(10자 내외)", "summary": "요약", "content": "본문(1000자 이상)", "image_url": "https://..."}'
    )

    payload = {
        "contents": [{ "parts": [{ "text": user_query }] }],
        "tools": [{ "google_search": {} }], 
        "systemInstruction": { "parts": [{ "text": system_prompt }] },
    }
    
    # (이하 API 호출 및 파싱 로직은 기존 코드와 동일하지만, topic_data 반환 부분만 유지)
    topic_data = {}
    # ... (API 호출 중략 - 기존과 동일) ...
    
    # 편의를 위해 API 호출 부분은 기존 코드 그대로 사용하되, 
    # 실제 구현 시에는 위에서 만든 payload를 사용하여 request를 보냅니다.
    # (여기서는 생략된 API 호출 로직이 있다고 가정합니다)
    
    # 실제 실행을 위해 간략화된 호출 예시 (기존 루프 복원 필요)
    try:
        response = requests.post(TEXT_API_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload), timeout=90)
        result = response.json()
        # ... (파싱 로직 기존 동일) ...
        # 테스트를 위해 파싱 로직 복사 필요 시 알려주세요.
        # 여기선 결과가 나왔다고 가정하고 진행합니다.
        
        # 실제 코드 병합 시 기존의 재시도(Retry) 로직을 그대로 유지하세요.
        # 임시로 파싱 로직을 간소화하여 적지 않았습니다.
    except Exception as e:
        print(f"Error: {e}")

    # --- (중요) 기존 코드의 Loop 및 Parsing 로직을 그대로 유지하세요 --- 
    # 단, payload 변수만 위에서 만든 것으로 대체하면 됩니다.
    
    # (테스트용 더미 데이터 반환 방지 - 실제 코드에선 삭제)
    # 실제로는 API 응답을 파싱해서 topic_data를 채워야 합니다.
    
    return topic_data

def create_markdown_file(topic_data, args): # 👈 args 추가
    try:
        os.makedirs(POSTS_DIR, exist_ok=True)
        content = topic_data.get('content', '')
        
        # 광고 삽입 로직 (기존 동일)
        ad_code = "\n{% include ad-inpost.html %}\n"
        content = re.sub(r'^(##\s+.*)', f'{ad_code}\\1', content, count=3, flags=re.MULTILINE)

        topic_title = topic_data.get('topic', 'draft-topic')
        safe_title = re.sub(r'[^\w\s-]', '', topic_title).strip().replace(' ', '-')
        if len(safe_title) > 50: safe_title = safe_title[:50]
        
        # 파일명에 카테고리 포함 (선택사항)
        filename = f"{DATE_STR}-{safe_title}.md"
        file_path = os.path.join(POSTS_DIR, filename)
        
        # 🟢 [수정됨] Front Matter에 인자 반영
        # args.tags는 "IT, AI" 문자열로 들어오므로 리스트 포맷으로 변환
        tags_list = f"[{args.tags}]" 
        
        markdown_content = f"""---
title: "{topic_title}"
subtitle: "{topic_data.get('summary', '')}"
date: {TIME_STR}
author: WakenHole
categories: [{args.category}] 
tags: {tags_list}
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
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"⭐ 파일 생성 완료: {file_path}")

    except IOError as e:
        print(f"파일 쓰기 실패: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 1. 인자 받기
    args = parse_arguments()
    
    # 2. 로직 실행 시 args 전달
    # 주의: generate_topic_and_content 내부의 API 호출 부분은 
    # 기존 코드의 retry loop 로직을 그대로 사용하되 payload만 교체해야 합니다.
    data = generate_topic_and_content(args)
    
    if data and data.get('topic'):
        create_markdown_file(data, args)
    else:
        # (기존 로직 유지) API 호출 실패 시 처리
        # 코드를 합칠 때 기존의 retry loop가 잘 포함되었는지 확인해주세요.
        pass
