---
title: "OpenClaw에 GLM-4.7 붙여봤다: 중국 LLM이 생각보다 쓸만하다"
date: 2026-02-03 14:40:00 +0900
categories:
  - Tech
  - AI
tags:
  - OpenClaw
  - GLM-4.7
  - Kimi
  - AI 에이전트
  - LLM 비교
tagline: "미국 LLM 절반 가격에 80% 성능, 에이전트 브레인으로 충분했다"
image:
  path: https://www.cnet.com/a/img/resize/23206224e5c665a8630c1778319bd0d272a242a8/hub/2026/01/30/a0605f4b-533d-410e-9bbf-49113e923a1b/image.png?auto=webp&fit=crop&height=675&width=1200
---

## 에이전트 브레인 비용이 생각보다 빠르게 쌓인다

OpenClaw를 쓰다 보면 생각보다 API 비용이 빠르게 쌓인다. 에이전트가 목표 하나를 처리하면서 내부적으로 수십 번 reasoning을 돌리기 때문이다. Claude나 GPT-4o를 브레인으로 쓰면 성능은 좋은데, 상시 가동 기준으로 매달 비용이 부담스러운 수준이 된다.

그래서 대안을 찾다가 중국 LLM 쪽을 테스트해봤다. Zhipu AI의 **GLM-4.7**과 Moonshot의 **Kimi**다.

{% include ad-inpost.html %}

## 중국 LLM, 실제로 써보니

솔직히 처음엔 반신반의했다. 중국산 모델이라고 하면 한국어나 복잡한 논리 처리에서 약할 것 같다는 선입견이 있었다.

그런데 막상 써보니 달랐다. 에이전트 작업 기준으로 **미국 top-tier 모델 대비 80% 이상의 성능**은 충분히 나온다고 느꼈다. 특히 시스템 명령 생성이나 스크립트 작성 쪽은 생각보다 정확했다. 한국어 명령도 잘 이해하고 처리했다.

가격 차이는 확실하다. 대략 미국 LLM의 **절반 이하** 수준이다.

| 모델 | 입력 ($/1M 토큰) | 출력 ($/1M 토큰) | 비고 |
| :--- | :---: | :---: | :--- |
| Claude 3.5 Sonnet | $3.00 | $15.00 | 미국, 고성능 |
| GPT-4o | $2.50 | $10.00 | 미국, 범용 |
| Gemini 2.5 Flash | $0.10 | $0.40 | 미국, 경량 |
| **Zhipu GLM-4.7** | **$0.07** | **$0.35** | 중국, 에이전트 특화 |
| **Kimi** | **$0.07~0.15** | **$0.30~0.60** | 중국, 긴 컨텍스트 강점 |

상시 가동하는 에이전트라면 이 차이가 누적으로 크게 느껴진다.

## GLM-4.7을 OpenClaw에 연결하는 방법

GLM-4.7은 OpenAI 호환 API를 제공해서, 기존 OpenClaw 설정을 거의 바꾸지 않아도 된다. `.env` 파일에서 아래만 수정하면 된다.

```bash
LLM_PROVIDER="openai"
OPENAI_API_KEY="your_zhipu_api_key_here"
OPENAI_BASE_URL="https://open.bigmodel.ai/api/paas/v4/"
BRAIN_MODEL="glm-4.7"
```

API 키는 [BigModel.ai](https://bigmodel.ai)에서 발급받을 수 있다.

## 어떤 경우에 쓸 만한가

모든 작업에 중국 LLM이 적합한 건 아니다. 내 기준으로 정리하면 이렇다.

**GLM / Kimi가 잘 맞는 작업:**
- 반복적인 에이전트 루프 (비용이 쌓이는 구조)
- 스크립트 생성, 파일 조작, 시스템 명령 처리
- 긴 문서 요약 (Kimi는 컨텍스트 윈도우가 특히 길다)

**미국 모델이 더 나은 경우:**
- 섬세한 창의적 글쓰기
- 복잡한 멀티스텝 추론
- 영어 중심의 전문 도메인 지식

## 결론

비용 대비 성능만 놓고 보면 GLM-4.7이나 Kimi는 충분히 실용적이다. 에이전트 브레인처럼 반복 호출이 많은 구조라면 특히 더 그렇다.

미국 LLM 절반 이하 가격에 80% 성능이면, 항상 최고 성능이 필요한 게 아니라면 써볼 이유는 충분하다. 나는 당분간 OpenClaw 브레인을 GLM-4.7로 유지할 생각이다.

{% include ad-inpost.html %}

**References:**
- [Zhipu AI (BigModel) 공식](https://bigmodel.ai)
- [OpenClaw GitHub](https://github.com/openclaw)
- [Kimi API 문서](https://platform.moonshot.cn)
