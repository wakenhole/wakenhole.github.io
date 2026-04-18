---
title: "Gemini API 무료로 써봤는데, 유료로 바꿔야 할까?"
date: 2025-12-31 09:00:00 +0900
categories:
  - Tech
  - AI
tags:
  - Gemini
  - Google Cloud
  - Python
  - API
toc: true
toc_sticky: true
tagline: "무료 tier 품질이 아쉬워서 유료 전환을 고민해봤다"
image:
  path: /assets/img/posts/2026/260101-ai-teasure.png
---

## 무료로 쓰다 보니 한계가 느껴졌다

토픽 리서치 자동화 작업에 Gemini API를 꽤 오래 써왔다. 무료 tier라서 비용 부담 없이 쓸 수 있다는 게 장점이었는데, 쓰다 보니 결과물 품질이 기대보다 많이 떨어졌다.

특히 복잡한 내용을 정리하거나 문맥을 이어서 써야 하는 작업에서 답변이 두루뭉술하거나 핵심을 빗나가는 경우가 종종 있었다. 같은 프롬프트를 Claude나 GPT에 넣어보면 확실히 차이가 느껴졌다.

그래서 "유료로 바꾸면 달라질까?" 하는 생각이 들어서 Gemini API 요금 구조를 제대로 한번 파봤다.

{% include ad-inpost.html %}

## 현재 무료 모델 현황 (2025년 12월 기준)

무료 tier에서 쓸 수 있는 모델들을 정리하면 이렇다.

| 모델 | 상태 | 분당 요청 | 일일 요청 | 특징 |
| :--- | :--- | :--- | :--- | :--- |
| **gemini-2.5-flash** | 제한적 | ~2 RPM | ~20~50 RPD | 가장 높은 버전이지만 한도가 너무 낮음 |
| **gemini-2.5-flash-lite** | 활성 | 15~30 RPM | ~1,500 RPD | 실질적인 무료 주력 모델 |
| **gemini-2.5-pro** | 무료 제거됨 | 0 | 0 | 유료 전환 필수 |
| **gemini-2.0-flash** | 레거시 | 10 RPM | 1,500 RPD | 구형, 성능 열세 |

내가 쓰던 모델은 `gemini-2.5-flash-lite` 계열이었는데, 일일 1,500회 요청은 충분했다. 문제는 **모델 자체의 품질**이었다.

## 유료로 가면 얼마나 드나

유료 전환 시 과금 구조는 **100만 토큰 당** 달러로 계산된다.

| 모델 | 입력 (≤128k) | 출력 (≤128k) |
| :--- | :--- | :--- |
| **Gemini 2.5 Pro** | $1.25 | $10.00 |
| **Gemini 2.5 Flash** | $0.10 | $0.40 |
| **Gemini 2.5 Flash-Lite** | $0.075 | $0.30 |

Flash 모델 기준으로 보면 소규모 개인 사용은 생각보다 크게 비싸지 않다. 짧은 요청을 수백 번 해도 몇 달러 수준이다. 반면 Pro 모델은 출력 비용이 $10/1M 토큰으로 꽤 뛴다.

한 가지 중요한 차이는 **데이터 처리 정책**이다.

- **무료 tier**: 내가 보낸 프롬프트가 Google 모델 개선에 사용될 수 있음
- **유료 tier**: 데이터가 학습에 사용되지 않음

민감한 내용을 다루거나 비즈니스 용도라면 이 차이가 중요하다.

## 새로운 SDK로 바꿔야 한다

2025년 11월부터 기존 `google-generativeai` 라이브러리가 deprecated됐다. 새 SDK는 `google-genai`다. 온라인 튜토리얼 대부분이 아직 구버전을 쓰고 있어서 주의가 필요하다.

```bash
pip install google-genai
# google-generativeai 는 이제 쓰지 말 것
```

새 SDK 기본 사용법은 이렇다.

```python
import os
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="여기에 프롬프트",
    config=types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=500,
    )
)

print(response.text)
```

과거 `genai.GenerativeModel` 방식에서 `genai.Client` 중심으로 바뀐 게 핵심이다.

## 결론: 유료 전환할 만한가

개인적으로 아직 유료로 전환하지는 않았다. 품질 문제가 모델 tier 때문인지, 프롬프트 설계 문제인지 아직 확신이 없어서다.

다만 판단 기준을 세워보면 이렇다.

- **무료로 충분한 경우**: 요청 횟수가 적고 품질보다 비용이 중요한 경우
- **유료 전환 고려**: 결과물 품질이 실제 업무에 영향을 주고, 데이터 보안이 중요한 경우

Flash 모델 유료 기준으로는 비용 자체가 크지 않으니, 품질 차이가 실제로 있다면 전환하는 게 맞을 것 같다. 조만간 테스트해볼 예정이다.

{% include ad-inpost.html %}

**References:**
- [Gemini Developer API Pricing](https://ai.google.dev/gemini-api/docs/pricing)
- [Google Gen AI SDK 문서](https://googleapis.github.io/python-genai/)
