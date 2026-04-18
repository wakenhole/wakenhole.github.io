import os
import sys
import datetime
import requests
import json
import time
import re  # 파일명 정규화 및 광고 삽입용

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
FILENAME = f"{DATE_STR}-draft-topic.md"

# ---

def validate_image_url(url):
    """
    주어진 URL이 유효한 이미지 링크인지 확인합니다.
    안정성을 위해 HEAD 대신 GET(stream=True)을 사용합니다.
    """
    if not url:
        return ""
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"🔗 이미지 링크 유효성 검사 중: {url[:60]}...")
        response = requests.get(url, headers=headers, timeout=5, stream=True)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '').lower()
            if 'image' in content_type:
                print(f"✅ 유효한 이미지 링크입니다 ({content_type}).")
                response.close()
                return url
            else:
                print(f"⚠️ 링크가 이미지가 아닙니다 ({content_type}). 빈 값 사용.")
                response.close()
                return ""
        else:
            print(f"❌ 유효하지 않은 링크 (Status {response.status_code}). 빈 값 사용.")
            return ""
    except Exception as e:
        print(f"❌ 링크 검사 중 오류 발생: {e}. 빈 값 사용.")
        return ""

def generate_topic_and_content():
    if not API_KEY:
        print("🚨 에러: GEMINI_API_KEY가 설정되지 않았습니다.")
        sys.exit(1)

    print(f"[{DATE_STR}] Gemini API({TEXT_MODEL_NAME}) 호출 중...")

    # 강화된 시스템 프롬프트
    system_prompt = (
        "당신은 금융 부동산 투자자 블로그 에디터입니다. 오늘 날짜의 최신 금용 및 부동산 투자 관련 주제로 선정하세요. "
        "주제는 최근 일주일 뉴스 기반으로 선정하며, 독자들이 관심 가질 만한 내용이어야 합니다."
        "응답은 오직 JSON 형식이어야 합니다. Markdown 포맷을 사용하지 말고 순수 JSON 텍스트만 반환하세요."
    )

    # 강화된 사용자 질의
    user_query = (
        f"오늘({DATE_STR}) 주식과 부동산에 한국인 투자자들이 관심 있을 주제로 블로그 글을 작성해 주세요. \n"
        "글 작성시 사실에 기반해서 작성해야하고, 참조한 출처가 있다면 반드시 명시해야 합니다. \n"
        "1. **주제(topic)**: 임팩트 있는 **10자 내외**의 제목.\n"
        "2. **내용(content)**: 깊이 있는 내용으로 마크다운 형식 **최소 800자 이상** 작성. 본문 중간중간에 `##` 를 사용하여 소제목을 명확히 구분해 주세요.\n"
        "3. **이미지(image_url)**: 주제와 관련된 **저작권 문제없는 공개 이미지(Unsplash 등)의 직접 링크(URL)** 하나를 검색해서 찾아주세요.\n\n"
        "응답은 다음 JSON 구조를 엄격히 따라 주세요: "
        '{"topic": "제목(10자 내외)", "summary": "요약", "content": "본문(800자 이상)", "image_url": "https://..."}'
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
                print(f"⚠️ API 오류: {response.text}")
                if response.status_code < 500: sys.exit(1)
                raise requests.exceptions.RequestException(f"Status {response.status_code}")

            try:
                result = response.json()
                candidates = result.get('candidates', [{}])
                if not candidates:
                    print(f"⚠️ 생성된 후보가 없습니다.")
                    continue
                parts = candidates[0].get('content', {}).get('parts', [{}])
                json_string = parts[0].get('text', '')
            except Exception as e:
                print(f"⚠️ 응답 파싱 실패: {e}")
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

    # 이미지 URL 유효성 검사 및 할당
    if topic_data:
        raw_url = topic_data.get('image_url', '')
        valid_url = validate_image_url(raw_url)
        
        topic_data['overlay_image'] = valid_url
        topic_data['teaser'] = valid_url
        
    return topic_data

def create_markdown_file(topic_data):
    try:
        os.makedirs(POSTS_DIR, exist_ok=True)
        content = topic_data.get('content', '')
        
        # 🟢 [추가됨] 광고 코드 삽입 로직
        # Markdown 헤더(## 소제목)를 찾아서 그 앞에 광고 코드를 삽입합니다.
        # count=3으로 설정하여 최대 3개까지만 삽입합니다.
        ad_code = "\n{% include ad-inpost.html %}\n"
        
        # 정규표현식: 라인의 시작(^)에 ## 공백이 있는 패턴을 찾음 (Multiline 모드)
        content = re.sub(r'^(##\s+.*)', f'{ad_code}\\1', content, count=1, flags=re.MULTILINE)

        topic_title = topic_data.get('topic', 'draft-topic')

        # 파일명 생성: 공백을 하이픈으로, 특수문자 제거
        safe_title = re.sub(r'[^\w\s-]', '', topic_title).strip().replace(' ', '-')
        if len(safe_title) > 50: safe_title = safe_title[:50]
            
        filename = f"{DATE_STR}-{safe_title}.md"
        file_path = os.path.join(POSTS_DIR, filename)
        
        markdown_content = f"""---
title: "{topic_title}"
tagline: "{topic_data.get('summary', '')}"
date: {TIME_STR}
categories: [Tech, Development] 
tags: [Gemini, Automation] 
published: false
toc: true
toc_sticky: true
image:
  path: {topic_data.get('teaser', '')}
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
    data = generate_topic_and_content()
    if data and data.get('topic'):
        create_markdown_file(data)
    else:
        print("🚨 최종적으로 데이터 생성에 실패했습니다.")
        sys.exit(1)