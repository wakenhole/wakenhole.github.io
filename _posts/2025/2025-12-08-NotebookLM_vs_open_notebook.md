---
title: "Google NotebookLM 써봤는데, 딱 하나가 아쉽다"
tagline: "편하긴 한데 PDF라서 수정이 안 된다는 게 문제"
date: 2025-12-08 10:00:00 +0900
categories: [Tech, AI]
tags:
  - NotebookLM
  - OpenNotebook
  - Self-Hosted
  - RAG
  - AI
toc: true
toc_sticky: true
image:
  path: https://images.unsplash.com/photo-1611571741792-edb58d0ceb67
---

## 쓰다 보니 불편한 게 생겼다

솔직히 처음 NotebookLM을 써봤을 때 꽤 놀랐다. 문서 여러 개 올려두고 "이거 요약해줘", "이 내용 중에 ~한 부분 찾아줘" 하면 척척 답해준다. 특히 여러 PDF를 한꺼번에 올려서 cross-reference 하는 기능이 생각보다 훨씬 편했다.

그런데 쓰다 보니 한 가지가 계속 걸렸다.

**결과물이 PDF로만 나온다.**

요약본이나 정리된 내용을 받아서 조금 더 다듬거나 내 스타일로 편집하고 싶은데, PDF라서 수정이 안 된다. 복사-붙여넣기를 하면 포맷이 다 깨지고, 결국 처음부터 다시 타이핑해야 하는 상황이 생긴다. 이게 한두 번이면 괜찮은데, 반복하다 보면 꽤 번거롭다.

{% include ad-inpost.html %}

## Open Notebook이라는 대안

그래서 찾아보다 알게 된 게 **Open Notebook**이다. NotebookLM의 핵심 기능을 오픈소스로 구현해서 로컬에서 돌릴 수 있는 프로젝트인데, 가장 큰 차이점들을 정리해보면 이렇다.

| Feature | **Google NotebookLM** | **Open Notebook** |
| :--- | :--- | :--- |
| **배포 방식** | Google 클라우드 (SaaS) | Self-Hosted (Docker/Local) |
| **데이터 보안** | Google 서버로 전송됨 | 로컬 저장, 외부 전송 없음 |
| **LLM 백엔드** | Gemini 고정 | OpenAI, Claude, Ollama 등 선택 가능 |
| **결과물 편집** | PDF (수정 불가) | 커스터마이징 가능 |
| **오디오 화자** | 2명 고정 | 1~4명, 프롬프트로 조정 가능 |
| **초기 설정** | 바로 사용 | Docker 환경 구성 필요 |

PDF 수정 문제만 보면 Open Notebook이 확실히 더 유연하다. 출력 포맷도 자유롭게 조정할 수 있고, 어떤 LLM을 쓸지도 직접 고를 수 있다.

## 그런데 직접 써보지는 않았다

솔직하게 말하면 Open Notebook은 아직 직접 설치해서 써보지 않았다. Docker 환경 구성이 필요하고, API 키 관리도 해야 하는 등 초기 세팅 비용이 있다. NotebookLM처럼 그냥 웹에서 바로 쓰는 것과는 다르다.

다만 아래 상황이라면 충분히 시도해볼 만하다고 본다.

- 회사 내부 문서나 민감한 자료를 다루는데 클라우드로 올리기 껄끄러운 경우
- Gemini가 아닌 특정 모델(예: Claude, 로컬 LLM)을 써야 하는 경우
- 결과물을 직접 편집하거나 자동화 파이프라인에 연결하고 싶은 경우

## 결론

개인용으로 가볍게 쓰기엔 NotebookLM이 압도적으로 편하다. 설치할 것도 없고, 그냥 문서 올리면 된다.

다만 PDF로만 결과가 나오는 점은 분명한 한계다. 결과물을 가공하거나 편집해야 하는 워크플로우라면 Open Notebook을 진지하게 고려해볼 만하다. 나도 시간 되면 직접 설치해서 비교해볼 예정이다.

{% include ad-inpost.html %}

**References:**
- [Open Notebook GitHub](https://github.com/gabrielchua/open-notebooklm)
- [Google NotebookLM 공식](https://notebooklm.google.com)
