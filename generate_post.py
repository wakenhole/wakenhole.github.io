import os
import sys
import datetime
import requests
import json
import time
import re
import argparse
import traceback

# --- 설정 ---
API_KEY = os.environ.get("GEMINI_API_KEY")

# 사용자가 지정한 모델명 유지
TEXT_MODEL_NAME = "gemini-2.5-flash" 
TEXT_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{TEXT_MODEL_NAME}:generateContent?key={API_KEY}"

KST = datetime.timezone(datetime.timedelta(hours=9))
now = datetime.datetime.now(KST)

DATE_STR = now.strftime("%Y-%m-%d")
TIME_STR = now.strftime("%Y-%m-%d %H:%M:%S +0900")

POSTS_DIR = "_posts"

# --- 1. 인자 파싱 설정 (Workflow 연동용) ---
def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate Blog Post with Gemini")
    parser.add_argument("--category", type=str, required=True, help="블로그 글의 대주제 (예: Tech)")
    parser.add_argument("--audience", type=str, required=True, help="타겟 독자 (예: 개발자)")
    parser.add_argument("--topic_keyword", type=str, default="최신 트렌드", help="글감 키워드")
    parser.add_argument("--tags", type=str, default="Blog", help="콤마로 구분된 태그")
    return parser.parse_args()

# ---

def validate_image_url(url):
    """
    주어진 URL이 유효한 이미지 링크인지 확인합니다.
    디버깅 로그를 포함하여 실패 원인을 추적합니다.
    """
    if not url:
        print("[DEBUG] 이미지 URL이 비어 있습니다.")
        return ""
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print(f"[DEBUG] 🔗 이미지 링크 검사: {url[:60]}...")
        response = requests.get(url, headers=headers, timeout=10, stream=True) # 타임아웃 10초로 연장
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '').lower()
            if 'image' in content_type:
                print(f"[DEBUG] ✅ 유효한 이미지입니다 ({content_type}).")
                response.close()
                return url
            else:
                print(f"[DEBUG] ⚠️ 이미지가 아닙니다 ({content_type}).")
        else:
            print(f"[DEBUG] ❌ 링크 접속 실패 (Status {response.status_code}).")
        
        response.close()
        return ""
    except Exception as e:
        print(f"[DEBUG] ❌ 링크 검사 중 에러: {e}")
        return ""

def generate_topic_and_content(args):
    if not API_KEY:
        print("🚨 [CRITICAL] GEMINI_API_KEY가 없습니다.")
        sys.exit(1)

    print(f"[{DATE_STR}] Gemini API 호출 시작... 카테고리: {args.category}")

    # 🟢 동적 프롬프트 생성 (인자 반영)
    system_prompt = (
        f"당신은 전문적인 '{args.category}' 블로그 에디터입니다. \n"
        f"주제는 최근 뉴스나 트렌드 기반으로 선정하며, 의견이나 견해를 적기보다는 '{args.audience}'가 흥미를 가질만한 정보나 꿀팁 위주의 내용이어야 합니다.\n"
        "응답은 오직 JSON 형식이어야 합니다. Markdown 포맷을 사용하지 말고 순수 JSON 텍스트만 반환하세요."
    )

    user_query = (
        f"오늘({DATE_STR}) '{args.audience}'를 위한 '{args.topic_keyword}' 관련 블로그 글을 작성해 주세요. \n"
        "글 작성시 사실에 기반해서 작성해야하고, 참조한 출처가 있다면 반드시 명시해야 합니다. \n"
        "1. **주제(topic)**: 흥미를 끄는 **10자 내외**의 제목.\n"
        "2. **내용(content)**: 깊이 있는 내용으로 마크다운 형식 **최소 1000자 이상** 작성. 본문 중간에 `##` 를 사용해 소제목을 명확히 구분해 주세요.\n"
        "3. **이미지(image_url)**: 주제와 관련된 **저작권 문제없는 공개 이미지(Unsplash, Pexels 등)의 '직접 다운로드 가능한' URL** 하나를 찾아주세요. 웹페이지 링크가 아닌, `.jpg`, `.png` 등으로 끝나는 실제 이미지 파일 주소여야 합니다.\n\n"
        "응답은 다음 JSON 구조를 엄격히 따라 주세요: "
        '{"topic": "제목(10자 내외)", "summary": "요약", "content": "본문(1000자 이상)", "image_url": "https://..."}'
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
            print(f"[DEBUG] API 요청 시도 {attempt + 1}...")
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
                    print(f"⚠️ [DEBUG] 후보군(candidates) 없음. 안전 차단됨?")
                    continue
                parts = candidates[0].get('content', {}).get('parts', [{}])
                json_string = parts[0].get('text', '')
                
                # print(f"[DEBUG] 원본 응답:\n{json_string[:200]}...") # 필요시 주석 해제

            except Exception as e:
                print(f"⚠️ 응답 구조 파싱 실패: {e}")
                continue
            
            if not json_string:
                continue

            # 🟢 [핵심 수정] 정규식으로 JSON 블록만 추출 (안정성 강화)
            json_string_clean = ""
            match = re.search(r'```json\s*(.*?)\s*```', json_string, re.DOTALL)
            if match:
                json_string_clean = match.group(1).strip()
            else:
                # 마크다운 없이 JSON만 왔을 경우 대비
                match_raw = re.search(r'(\{.*\})', json_string, re.DOTALL)
                if match_raw:
                    json_string_clean = match_raw.group(1).strip()
                else:
                    json_string_clean = json_string.strip()
            
            try:
                topic_data = json.loads(json_string_clean)
                print(f"✅ 주제 생성 성공: {topic_data.get('topic')}")
                break
            except json.JSONDecodeError as e:
                print(f"🚨 JSON 파싱 실패. (텍스트 일부: {json_string_clean[:50]}...)")
                time.sleep(2)
                continue

        except Exception as e:
            print(f"❌ 요청 중 예외 발생: {e}")
            traceback.print_exc()
            time.sleep(2 ** attempt)

    # 이미지 URL 처리 및 검증 (최대 2회 추가 시도)
    if topic_data:
        for img_attempt in range(3): # 총 3번 시도 (기본 1 + 추가 2)
            print(f"[DEBUG] 이미지 검증 시도 {img_attempt + 1}...")
            raw_url = topic_data.get('image_url', '')
            valid_url = validate_image_url(raw_url)
            if valid_url:
                topic_data['overlay_image'] = valid_url
                topic_data['teaser'] = valid_url
                break # 성공 시 루프 탈출
            
            print("⚠️ 유효한 이미지를 찾지 못해, 다른 이미지 URL을 다시 요청합니다.")
            topic_data['image_url'] = "" # 기존 URL 초기화
            if img_attempt < 2: # 마지막 시도에서는 재요청 안함
                # 간단한 이미지 재요청 프롬프트
                retry_payload = {"contents": [{ "parts": [{ "text": f"'{topic_data.get('topic')}' 주제에 맞는 다른 이미지 URL을 찾아주세요. 직접 링크여야 합니다." }] }]}
                # (실제 구현에서는 generate_topic_and_content의 일부를 재사용하여 API 호출)
                # 이 부분은 간소화된 예시이며, 실제로는 API를 다시 호출하는 로직이 필요합니다.
                # 지금은 실패 시 빈 값으로 두는 것으로 유지합니다.
                topic_data['overlay_image'] = ""
                topic_data['teaser'] = ""
        
    return topic_data

def create_markdown_file(topic_data, args):
    try:
        if not topic_data:
            print("🚨 데이터가 없어 파일을 생성하지 않습니다.")
            return

        os.makedirs(POSTS_DIR, exist_ok=True)
        content = topic_data.get('content', '')

        # 광고 삽입: 두 번째 소제목(##)부터 최대 3개의 광고를 삽입합니다.
        ad_code = "\n{% include ad-inpost.html %}\n"
        parts = re.split(r'(^##\s+.*$)', content, flags=re.MULTILINE)
        
        new_content_parts = [parts[0]]
        ad_count = 0
        
        for i in range(1, len(parts), 2):
            heading = parts[i]
            body = parts[i+1] if (i + 1) < len(parts) else ""
            if i > 1 and ad_count < 1: # 첫번째 소제목(i=1)은 건너뜁니다.
                new_content_parts.append(ad_code + heading)
                ad_count += 1
            else:
                new_content_parts.append(heading)
            new_content_parts.append(body)
        
        content = "".join(new_content_parts)

        topic_title = topic_data.get('topic', 'draft-topic')
        safe_title = re.sub(r'[^\w\s-]', '', topic_title).strip().replace(' ', '-')
        if len(safe_title) > 50: safe_title = safe_title[:50]
        
        filename = f"{DATE_STR}-{safe_title}.md"
        file_path = os.path.join(POSTS_DIR, filename)
        
        # 🟢 태그와 카테고리를 YAML 리스트 포맷으로 변환
        tag_list = [t.strip() for t in args.tags.split(',')]
        tags_yaml = "\n".join([f"  - {tag}" for tag in tag_list])
        
        markdown_content = f"""---
title: "{topic_title}"
tagline: "{topic_data.get('summary', '')}"
lastmod: {TIME_STR}
categories: 
  - {args.category}
tags:
{tags_yaml}
published: false
toc: true
toc_sticky: true
image:
  path: {topic_data.get('teaser', '')}
sitemap: 
    changefreq : monthly
    priority : 0.5
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
    # 1. 워크플로에서 전달된 인자 파싱
    args = parse_arguments()
    print(f"[DEBUG] 시작 설정: {args}")
    
    # 2. 콘텐츠 생성
    data = generate_topic_and_content(args)
    
    # 3. 파일 저장
    if data and data.get('topic'):
        create_markdown_file(data, args)
    else:
        print("🚨 최종적으로 데이터 생성에 실패했습니다.")
        sys.exit(1)