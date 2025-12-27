---
title: "구글 드라이브 대용량 동영상 다운로드, Python으로 완벽 자동화하기 (Feat. gdrive-download-video)"
date: 2025-12-27 10:00:00 +0900
categories: [Tech, Software Guides]
tags:
  - Google Drive
  - Python
  - Crawling
  - Automation
  - Open Source
toc: true
toc_sticky: true
tagline: "Python Automation"
math: true
mermaid: true
image:
  path: https://static.macupdate.com/screenshots/349863/m/google-drive-screenshot.png?v=1670917133
---

![Online Learning](https://images.unsplash.com/photo-1501504905252-473c47e087f8?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80){: width="400px"}

온라인 강의나 스터디 자료를 구글 드라이브로 공유받는 경우가 많습니다. 그런데 **오른쪽 위에 있어야 할 '다운로드' 버튼이 아예 없거나 비활성화**되어 있어 당황한 적 없으신가요?

공유자가 '뷰어(보기 전용)' 권한만 설정하면 브라우저에서만 볼 수 있고 파일 저장이 불가능합니다. 인터넷이 느린 카페나 비행기 안에서 공부하고 싶은데, 영상을 다운로드할 수 없어 답답하셨을 겁니다.

오늘은 **다운로드가 막혀있는 영상**은 물론, **수십 개의 강의가 들어있는 폴더를 통째로** 내 컴퓨터에 저장하는 방법을 소개합니다.

{% include ad-inpost.html %}

### 1. 준비물: 파이썬(Python)

우리는 개발자가 만들어둔 도구를 가져다 쓸 것입니다. 이 도구가 작동하기 위해선 **[파이썬(Python)]** 프로그램이 컴퓨터에 설치되어 있어야 합니다. (검색창에 '파이썬 설치'를 입력하면 1분이면 설치 가능합니다.)

### 2. 설치하기

윈도우의 '명령 프롬프트(cmd)'나 맥의 '터미널'을 열고 아래 명령어를 순서대로 복사-붙여넣기 하세요.

```bash
# 1. 도구 다운로드 (깃허브 복제)
git clone https://github.com/wakenhole/gdrive-download-video.git

# 2. 폴더로 이동
cd gdrive-download-video

# 3. 필요한 부품 설치
pip install -r requirements.txt
```

{% include ad-inpost.html %}

### 3. 사용 방법 (상황별 가이드)

다운로드하려는 대상이 "영상 하나"인지, "강의 폴더 전체"인지에 따라 명령어가 다릅니다.

#### 상황 A: 영상 1개만 다운로드하고 싶을 때

보고 싶은 영상의 주소(URL)에서 **Video ID**를 찾으세요.
> 주소 예시: `https://drive.google.com/file/d/1HFkHQYetpcNnyQo.../view`
> **Video ID:** `d/` 뒤에 있는 `1HFkHQYetpcNnyQo...` 부분

이제 아래 명령어를 입력합니다. `gdrive_videoloader.py`를 사용합니다.

```bash
# 기본 사용법: python gdrive_videoloader.py [영상ID]
python gdrive_videoloader.py 1HFkHQYetpcNnyQoxxxxxX1I1TAcF6Q0us

# 꿀팁: 파일 이름을 내가 정하고 싶다면? (-o 옵션 사용)
# 예: python gdrive_videoloader.py [영상ID] -o "1강_오리엔테이션.mp4"
python gdrive_videoloader.py 1HFkHQYetpcNnyQoxxxxxX1I1TAcF6Q0us -o my_lecture.mp4
```

#### 상황 B: 시즌 전체(폴더)를 통째로 받고 싶을 때 (강추 👍)

강의가 20강까지 있는데 하나씩 다운로드하기 귀찮으시죠? 폴더 주소의 **Folder ID**만 알면, 그 안의 모든 영상을 자동으로 찾아 다운로드해 줍니다. 심지어 하위 폴더 구조까지 그대로 유지됩니다.

> 주소 예시: `https://drive.google.com/drive/folders/1FolderIDExample...`
> **Folder ID:** `folders/` 뒤에 있는 부분

이번엔 `gdrive_video_download.py`를 사용합니다.

```bash
# 사용법: python gdrive_video_download.py [폴더ID] -v
python gdrive_video_download.py 1HFkHQYetpcNnyQoxxxxxX1I1TAcF6Q0us -v
```

* `-v` 옵션을 붙이면 현재 어떤 파일이 다운로드되고 있는지 자세히 보여줍니다.

{% include ad-inpost.html %}

### 4. 이 도구가 좋은 이유

1.  **다운로드 버튼이 없어도 OK:** 보기 전용(View-only) 권한인 파일도 문제없이 저장됩니다.
2.  **대용량 경고 패스:** 구글 드라이브 특유의 "바이러스 검사 불가" 경고창 때문에 다운로드가 끊기는 현상이 없습니다.
3.  **폴더 구조 유지:** 강의 자료가 `1주차`, `2주차` 폴더로 나뉘어 있어도 그 구조 그대로 내 컴퓨터에 저장됩니다.

### 5. 주의사항

* 내려받은 강의 영상은 **반드시 본인의 학습 목적으로만 개인 소장**해야 합니다.
* 타인에게 공유하거나 인터넷에 올릴 경우 저작권법 위반으로 처벌받을 수 있습니다.

이제 인터넷 연결 걱정 없이, 쾌적한 환경에서 열공하세요!

---
**References:**
1. [gdrive-download-video Tool (GitHub)](https://github.com/wakenhole/gdrive-download-video/blob/main/README.md)

{% include ad-inpost.html %}