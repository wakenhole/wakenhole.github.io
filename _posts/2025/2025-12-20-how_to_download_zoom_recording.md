---
title: "[팁] Zoom(줌) 녹화 영상 다운로드 완벽 가이드: 다운로드 권한/버튼이 없을 때 해결 방벙"
date: 2025-12-18 09:00:00 +0900
categories: [Tech, Software Guides]
tags:
  - Zoom
  - 줌
  - Zoom 강의
  - 다운로드
  - Download
  - 권한
  - youtube-dl
toc: true
toc_sticky: true
tagline: "Productivity"
image:
  path: https://www.webwise.ie/wp-content/uploads/2020/04/IMG009.jpg
---


Zoom 녹화 영상은 종종 제한된 기간 동안만 제공되며, 나중에 다시 참조하기 위해 다운로드할 수 있는 쉬운 방법을 제공하지 않는 경우가 많습니다.

하지만 해결책이 있습니다. `youtube-dl`을 사용하면 이전에 녹화된 Zoom 통화나 회의를 다운로드할 수 있습니다.

{% include ad-inpost.html %}

### 나중을 위한 요약 명령어 (Shorthand command)

우리가 Zoom 녹화를 다운로드하기 위해 실행할 명령어는 대략 다음과 같은 형태가 될 것입니다. (상세 내용은 아래 단계별 가이드를 참고하세요.)

```bash
./youtube-dl --referer "[https://zoom.us/](https://zoom.us/)" \
  --add-header "Cookie: <cookie string>" \
  '<video_url>'
```

{% include ad-inpost.html %}

### 단계별 가이드: Zoom 다시보기 및 녹화 영상 다운로드 방법

#### 1단계 - youtube-dl 다운로드 (Step 1)

먼저 `youtube-dl`을 다운로드해야 합니다. [youtube-dl Github](https://github.com/ytdl-org/youtube-dl)의 다운로드 및 사용 지침을 따르세요.

#### 2단계 - Zoom 녹화 페이지 방문 (Step 2)

**2a 단계 (Step 2a)**

다운로드하려는 Zoom 녹화 페이지를 방문했을 때 다음 작업을 수행합니다.

1. 다운로드하려는 녹화 영상의 URL로 이동한 뒤, `Ctrl` + `Shift` + `I` (Windows) 또는 `Cmd` + `Opt` + `I` (Mac) 키를 눌러 브라우저의 **개발자 도구(Developer Tools)**를 엽니다.
2. 개발자 도구 상단의 **Network(네트워크)** 탭을 클릭합니다.
3. `Ctrl` + `R` 또는 `F5`를 눌러 페이지를 **새로고침**합니다.
4. 개발자 도구의 검색 상자(Filter)에 `.mp4`를 입력하여 검색합니다.
5. 검색된 항목의 **Request Headers** 섹션에서 쿠키(Cookie) 정보를 찾아 복사합니다.

> **주의:** `Cookie:` 라는 텍스트도 내용과 함께 포함하여 복사해야 합니다.

![Cookie](https://michaelabrahamsen.com/images/dev-journal/2020-06-20-182359_1919x753.png)

이제 우리가 사용할 명령어는 다음과 같은 모습이 됩니다:

```bash
./youtube-dl --referer "[https://zoom.us/](https://zoom.us/)" \
  --add-header "cookie: <cookie content>" \
  "<add video url here>"

```

**2b 단계 (Step 2b)**

2a 단계에서 보고 있던 것과 동일한 비디오 요청(Request)에서 **Request URL**을 복사합니다. 이번에는 **General** 섹션에 있는 Request URL 필드의 값을 가져오면 됩니다.

![alt text](https://michaelabrahamsen.com/images/dev-journal/2020-06-20-182715_958x754.png)

이를 통해 아래와 같이 최종 명령어를 완성할 수 있습니다.

**완성된 명령어 예시:**

```bash
./youtube-dl -o output-filename.mp4 --referer "[https://zoom.us/](https://zoom.us/)" \
  --add-header "Cookie: _zm_lang=en-US; _zm_mtk_guid=5865f0b8352b4fdbb0224c586a09eaf0; ... (생략) ..." \
  '[https://ssrweb.zoom.us/cmr/replay/2020/05/07/87850353261/....mp4?response-content-type=video](https://ssrweb.zoom.us/cmr/replay/2020/05/07/87850353261/....mp4?response-content-type=video)...'

```

위 명령어를 터미널에 입력하면 다운로드가 시작됩니다.

{% include ad-inpost.html %}

---

*본 글은 Michael Abrahamsen의 [How to download zoom recording](https://michaelabrahamsen.com/posts/how-to-download-zoom-recordings/) 게시물을 원문 그대로 번역하여 작성되었습니다.*
