---
title: "Windows 11 우회 설치 완전 가이드 | 자동 스크립트 사용"
date: 2025-10-28
categories:
  - Tech
tags: [Windows11, MediaCreationTool, TPM우회, Rufus, ISO]
toc: true
toc_sticky: true
toc_icon: "cog"
tagline: ""
ads: true
header:
  overlay_image: https://images.unsplash.com/photo-1624571404553-49e7dbfbc90e?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=2970
  overlay_filter: 0.5
  caption: "[**Unsplash**](https://unsplash.com)"
  teaser: https://images.unsplash.com/photo-1679269241012-f7640862d242?ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&q=80&w=3132
---

# 🪄 Windows 11 우회 설치 완전 가이드  
_AveYo **MediaCreationTool.bat** 사용법_

> ⚠️ **요약:** TPM, Secure Boot, CPU 제한으로 Windows 11 설치가 막힐 때  
> AveYo의 **MediaCreationTool.bat** 스크립트를 이용하면 안전하게 ISO 생성 및 업그레이드가 가능합니다.  
> 단, Microsoft는 비호환 PC의 설치를 **공식적으로 지원하지 않으며**, 반드시 **백업 후 진행**하세요.


{% include ad-inpost.html %}
---

## 📘 목차
1. [MediaCreationTool.bat 소개](#media-creation-toolbat-소개)  
2. [누구에게 적합한가](#누구에게-적합한가)  
3. [준비물 및 체크리스트](#준비물-및-체크리스트)  
4. [설치 절차](#설치-절차)  
5. [설치 중 주요 옵션](#설치-중-주요-옵션)  
6. [설치 후 점검 사항](#설치-후-점검-사항)  
7. [고급 팁](#고급-팁)  
8. [FAQ](#faq)  
9. [참고 링크](#참고-링크)

---

## 💡 Media Creation Tool.bat 소개

**MediaCreationTool.bat**은 오픈소스 개발자 **AveYo**가 제작한 Windows 11 설치 도우미입니다.  
이 스크립트는 Microsoft 공식 서버에서 **정품 ISO 파일을 직접 다운로드**하며,  
TPM 2.0·Secure Boot·CPU 검사 등 **설치 제한을 자동으로 우회**합니다.

- ✅ ISO / USB 설치 미디어 자동 생성  
- ✅ TPM / Secure Boot / CPU 검사 자동 우회  
- ✅ Windows 10에서 바로 업그레이드 가능  
- ✅ 완전 무료 & 깃허브 공개


{% include ad-inpost.html %}

🔗 **공식 GitHub:** [https://github.com/AveYo/MediaCreationTool.bat](https://github.com/AveYo/MediaCreationTool.bat)

{% include ad-inpost.html %}
---

## 👥 누구에게 적합한가

| 구분 | 권장 여부 |
|------|-----------|
| 개인용 구형 PC | ✅ 실험/테스트용으로 적합 |
| 회사/공공기관 PC | ❌ 비권장 (보안/정책 위반 가능) |
| 개발·테스트 환경 | ✅ 좋음 (가상머신, 샌드박스 등) |
| 장기 사용 메인 PC | ⚠️ 가능은 하지만 업데이트 제한 주의 |

> ⚠️ **중요:** Microsoft는 비호환 장치에서 Windows 11 설치 시  
> **보안 업데이트 제공을 보장하지 않습니다.**

---

## 🧰 준비물 및 체크리스트

- 💾 **전체 시스템 백업 (시스템 이미지 추천)**  
- 🔑 **정품 Windows 10 설치 및 관리자 권한**  
- 🌐 **안정적인 인터넷 연결 (ISO 다운로드용)**  
- 💽 **8GB 이상 USB 또는 충분한 디스크 공간**  
- 🧩 **복구 드라이브 준비 (문제 시 복원용)**

> ✅ 설치 전 `제어판 → 복구 → 복원 드라이브 만들기`로 복구 USB를 꼭 만들어 두세요.


{% include ad-inpost.html %}
---

## ⚙️ 설치 절차

### ① GitHub에서 파일 다운로드

{% include ad-inpost.html %}

1. [MediaCreationTool.bat 저장소](https://github.com/AveYo/MediaCreationTool.bat) 접속  
2. 우측 **Code → Download ZIP** 클릭  
3. 압축 해제 (예: `C:\MediaCreationTool` 폴더)

---


{% include ad-inpost.html %}

### ② 관리자 권한으로 실행
- `MediaCreationTool.bat`을 **우클릭 → 관리자 권한으로 실행**
- PowerShell 창이 열리면 아래와 같은 메뉴가 표시됩니다:



- 여기서 **“11”** (Windows 11)을 선택합니다.

---

### ③ 동작 모드 선택

| 모드 | 설명 |
|------|------|
| **Auto Upgrade** | 현재 PC를 그대로 Windows 11로 업그레이드 |
| **Create ISO** | ISO 파일만 생성 |
| **Create USB** | 부팅 가능한 설치 USB 생성 |
| **Select in MCT** | 세부 옵션 수동 선택 가능 |

> 💡 **처음이라면 → `Create ISO` 권장**  
> ISO로 안전하게 파일을 만든 후 USB 설치나 업그레이드를 진행하세요.


{% include ad-inpost.html %}
---

### ④ 자동 우회 패치 적용
AveYo의 스크립트에는 내부적으로 `Skip_TPM_Check_on_Dynamic_Update.cmd`가 포함되어 있어  
설치 중 다음과 같은 제한이 자동으로 해제됩니다:

| 제한 항목 | 기본 상태 | 우회 후 |
|------------|------------|----------|
| TPM 2.0 | 필수 | 무시됨 |
| Secure Boot | 필수 | 무시됨 |
| 4GB RAM 미만 | 차단 | 허용 |
| 지원되지 않는 CPU | 차단 | 허용 |

✅ “이 PC는 Windows 11을 실행할 수 없습니다” 메시지가 **표시되지 않습니다.**

---

### ⑤ 설치 진행
- **Auto Upgrade** → 바로 업그레이드 (파일/앱 유지 가능)  
- **Create USB** → USB로 부팅 후 설치 (클린 설치 권장)

> ⚠️ **설치 후 “지원되지 않는 하드웨어” 워터마크가 표시될 수 있습니다.**  
> 기능에는 영향이 없지만, Microsoft는 향후 업데이트를 제한할 수 있습니다.

---

## 🔍 설치 중 주요 옵션

| 옵션 | 의미 |
|------|------|
| Keep Files & Apps | 기존 데이터 유지 (업그레이드용) |
| Nothing | 완전 새로 설치 (클린 설치) |
| Partition Select | 직접 파티션 지정 가능 (고급 사용자용) |

> 💡 설치 중 오류나 부팅 문제 시, 복구 USB로 “시스템 복원” 기능을 사용하세요.


{% include ad-inpost.html %}
---

## 🧾 설치 후 점검 사항

1. ⚙️ **설정 → 시스템 → 정품 인증** 상태 확인  
2. 💡 **장치 관리자**에서 드라이버 정상 작동 여부 확인  
3. 🔔 업데이트 메뉴에서 “이 PC는 지원되지 않습니다” 메시지 확인 가능  
4. 🔁 문제 시 복구 드라이브로 복원 / Windows 10 재설치 가능

---

## 🧠 고급 팁

- **워터마크 제거**  
일부 스크립트로 가능하지만, 시스템 무결성에 영향을 줄 수 있어 권장하지 않습니다.  
- **TPM 체크만 우회하고 싶을 때**  
`Skip_TPM_Check_on_Dynamic_Update.cmd` 단독 실행 가능  
- **안정성 유지 팁**  
BIOS 업데이트 + 최신 칩셋/그래픽 드라이버 설치  
가능하다면 TPM 모듈 장착으로 정식 호환 유지


{% include ad-inpost.html %}
---

## ❓ FAQ

**Q1. 업데이트 계속 받을 수 있나요?**  
A1. 일부 보안 업데이트는 제공되지만, Microsoft가 이를 보장하지 않습니다.

**Q2. 설치 실패 시?**  
A2. 복구 USB로 부팅 → 시스템 복원 또는 Windows 10 이미지로 복구하세요.

**Q3. 회사 PC에 적용 가능할까요?**  
A3. 보안/정책 위반 우려가 있으므로 절대 권장하지 않습니다.

---

## 🔗 참고 링크

{% include ad-inpost.html %}

- 🔹 [MediaCreationTool.bat (AveYo)](https://github.com/AveYo/MediaCreationTool.bat)  
- 🔹 [Rufus 공식 사이트](https://rufus.ie/)  
- 🔹 [Microsoft 공식 Windows 11 최소 사양 문서](https://learn.microsoft.com/windows/)

---

## 🎨 썸네일 디자인 제안
**제목:** `Windows 11 우회 설치 완전 가이드`  
**부제:** `AveYo MediaCreationTool.bat 사용법 · 백업 필수`  
**이미지 구성:**  
- 배경: 어두운 블루 그라디언트  
- 중앙: Windows 로고 + USB 아이콘  
- 하단 배너: `⚠️ 백업 필수 / 기업 비권장`  
- 크기: 1280×720  



{% include ad-inpost.html %}
---

## 🏁 마무리

이 가이드는 **구형 PC에서 Windows 11을 시험적으로 설치하려는 사용자**를 위한 안내입니다.  
설치 전에는 반드시 **전체 백업**을 수행하고,  
업무용 환경에서는 **정식 호환 하드웨어로 업그레이드**하는 것이 가장 안전합니다.  

> 💬 도움이 되셨다면 댓글로 경험을 공유해주세요!  
> ⚙️ 다음 글에서는 “Rufus로 Windows 11 우회 설치 USB 만드는 방법”을 다룹니다.

---