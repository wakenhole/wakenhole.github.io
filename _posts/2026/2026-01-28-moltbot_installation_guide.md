---
title: "Moltbot(구 Clawdbot) 설치 가이드: Windows/Mac 환경별 정리"
date: 2026-01-28 17:55:00 +0900
categories:
  - Tech
  - AI
tags:
  - Moltbot
  - Clawdbot
  - AI Agent
  - Installation Guide
  - Automation
  - Security
toc: true
toc_sticky: true
tagline: "Your Personal AI Operating System"
math: true
mermaid: true
image:
  path: https://www.youngurbanproject.com/wp-content/uploads/2026/01/Moltbot-Setup-Guide-ClawdBot-Installation.jpg
---

Clawdbot이 Moltbot으로 이름이 바뀌었다. 2026년 1월에 Anthropic에서 상표권 요청을 해서 리브랜딩한 것이다. 기능 자체는 그대로다.

에이전틱 AI 도구 중에서 가장 많이 언급되는 도구인데, 설치 과정이 OS마다 좀 다르고 보안 설정을 제대로 안 하면 리스크가 있어서 정리해둔다.

{% include ad-inpost.html %}

---

## 구조 이해: 로컬에서 게이트웨이가 실행된다

Moltbot은 클라우드 기반이 아니라 사용자 하드웨어에서 게이트웨이(Gateway)를 직접 실행하는 구조다. 외부에서 메시징 앱(텔레그램, 왓츠앱 등)을 통해 내 컴퓨터에 명령을 내릴 수 있고, 대화 기록은 로컬 마크다운 형식으로 저장된다.

* **게이트웨이(Gateway):** 채널 연결과 제어 평면 담당
* **Pi 에이전트:** Claude, GPT 등 LLM을 통해 판단
* **권한 범위:** 파일 시스템 접근, 브라우저 자동화, 터미널 명령 실행 가능

이 구조 때문에 데이터가 외부로 나가지 않는다는 장점이 있지만, 동시에 보안 설정이 중요해진다.

---

## 시스템 요구사항

| 리소스 | 최소 | 권장 |
| :--- | :--- | :--- |
| **CPU** | 2코어 | 4코어 이상 (Apple Silicon 권장) |
| **RAM** | 2GB (챗 전용) | 4GB~8GB (브라우저 자동화용) |
| **저장공간** | 20GB | 50GB+ (NVMe SSD 권장) |
| **런타임** | Node.js v22+ | pnpm (소스 빌드 시) |

24시간 가동을 원한다면 Mac Mini(M4 이상)가 실용적인 선택이다. 보안상 격리가 필요하다면 월 5달러 수준의 VPS를 쓰는 방법도 있다.

---

## macOS 설치

macOS에서 가장 깔끔하게 돌아간다.

1. 터미널에서 `xcode-select --install` 실행 (개발자 도구 설치)
2. 원클릭 설치:
    ```bash
    curl -fsSL https://molt.bot/install.sh | bash
    ```
3. 설치 후 `exec zsh` 실행해서 설정 반영
4. macOS 전용 메뉴바 앱으로 게이트웨이 상태 모니터링 및 Talk Mode 활성화 가능

---

## Windows 설치 (WSL2 방식)

Windows는 WSL2 경유가 공식 권장 방식이다.

1. PowerShell(관리자)에서 `wsl --install` 실행 후 재부팅
2. Ubuntu 터미널에서 Node.js v22 설치
3. CLI 전역 설치:
    ```bash
    npm install -g moltbot@latest
    ```
4. 데몬 등록 (시스템 시작 시 자동 실행):
    ```bash
    moltbot --install-daemon
    ```

---

## 온보딩 및 LLM 연결

설치 완료 후:
```bash
moltbot onboard --install-daemon
```

지원하는 LLM 백엔드:
* **Anthropic (Claude 4.5):** 에이전트 지시 이행과 보안성이 가장 안정적
* **OpenAI (GPT-5):** 빠른 도구 호출 속도, 범용성
* **Ollama (Local):** 완전 오프라인, 데이터 유출 차단

온보딩에서 '모델 페일오버(Model Failover)'를 활성화하면 주 모델 오류 시 보조 모델로 자동 전환된다.

---

## 보안 설정: 반드시 해야 할 것들

내 컴퓨터 전권을 AI에게 주는 구조라서 보안은 기본이다.

1. **페어링 코드:** 8자리 코드를 통한 명시적 승인 — 낯선 접근 차단
2. **Docker 샌드박싱:** 위험하거나 외부 스크립트 실행은 Docker 컨테이너 안에서만. 호스트 시스템과 격리
3. **Tailscale 연동:** 공인 IP를 노출하지 않고 전용 VPN망으로만 게이트웨이에 접근

이 세 가지 없이 그냥 실행하는 건 추천하지 않는다.

---

## 유지보수 명령어

```bash
moltbot doctor    # 시스템 진단
moltbot status    # 상태 확인
moltbot update    # 최신 업데이트
moltbot restart   # 에이전트 재시작
```

{% include ad-inpost.html %}
