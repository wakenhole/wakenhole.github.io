---
title: "GitHub 블로그(Jekyll) 검색 엔진 최적화(SEO) 완벽 가이드: 필수 설정 4가지"
date: 2024-05-22
categories: [Tech]
description: "깃허브 블로그가 구글과 네이버에 검색되지 않을 때 해결하는 방법. robots.txt 파일명 오류 수정부터 _config.yml 설정, 사이트맵 제출까지 필수 SEO 체크리스트를 정리했습니다."
tags:
  - Google Search Console 
  - GitHub Pages
  - Jekyll
  - Bing Webmaster Tools
  - SEO
toc: true
toc_sticky: true
tagline: "github.io"
header:
  overlay_image: https://1330878074.rsc.cdn77.org/wp-content/uploads/2022/05/Oracle-Enhances-its-Comprehensive-Cloud-Security-Capabilities-with-Integrated-Threat-Management.jpg
  overlay_filter: 0.5
  caption: "[**Unsplash**](https://unsplash.com)"
  teaser: https://1330878074.rsc.cdn77.org/wp-content/uploads/2022/05/Oracle-Enhances-its-Comprehensive-Cloud-Security-Capabilities-with-Integrated-Threat-Management.jpg


---



블로그를 열심히 만들고 글을 썼는데, 구글이나 네이버 검색 결과에 내 글이 나오지 않는다면 정말 맥이 빠지는 일입니다. "내 글은 왜 검색이 안 되지?"라고 고민하고 계신가요?

특히 GitHub Pages와 Jekyll로 만든 블로그는 우리가 직접 검색 엔진에게 "내 블로그는 여기 있고, 이런 글들이 있어"라고 알려주는 작업이 필요합니다. 오늘은 제 블로그(GitHub Pages)를 점검하면서 발견한 **실제 문제점**들을 바탕으로, 검색 노출을 위해 반드시 확인해야 할 4가지 설정을 정리해 드립니다.

## 1. 치명적인 실수: `robot.txt`가 아니라 `robots.txt`입니다



가장 먼저 제 저장소를 점검하다가 아주 사소하지만 치명적인 실수를 발견했습니다. 바로 크롤러(검색 로봇)를 위한 규칙 파일의 이름이 잘못되어 있었습니다.

* **잘못된 파일명:** `robot.txt` (현재 상태)
* **올바른 파일명:** `robots.txt` (**'s'가 반드시 붙어야 함**)

검색 엔진 봇은 사이트에 방문하면 가장 먼저 **`robots.txt`** 파일을 찾습니다. 파일명이 다르면 봇은 규칙을 찾지 못하고, 사이트맵의 위치도 파악하기 어려워집니다.

**해결 방법:**
루트 디렉토리에 있는 파일명을 변경하고, 아래 내용을 담아주세요.

```text
User-agent: *
Allow: /

Sitemap: [https://wakenhole.github.io/sitemap.xml](https://wakenhole.github.io/sitemap.xml)
```

## 2. _config.yml의 URL 설정 점검
Jekyll 블로그의 심장부인 _config.yml 파일 설정은 SEO에 지대한 영향을 미칩니다. 특히 url 값이 정확하지 않으면, 블로그의 '표준 주소(Canonical URL)'가 제대로 생성되지 않아 검색 엔진이 페이지를 중복으로 인식하거나 무시할 수 있습니다.

현재 minimal-mistakes 테마를 사용 중이시라면, 이 테마는 _config.yml의 정보를 바탕으로 메타 태그를 자동 생성합니다.

#### 체크 포인트:
_config.yml 파일을 열어 url 항목이 자신의 실제 블로그 주소와 정확히 일치하는지 확인하세요.

```
# _config.yml
url: "[https://wakenhole.github.io](https://wakenhole.github.io)" # 마지막에 슬래시(/)를 넣지 않는 것이 일반적입니다.
baseurl: "" # 서브 경로가 없다면 비워둡니다.
title: "블로그 제목"
description: "검색 결과에 보여질 블로그 설명"
```

## 3. 사이트맵(Sitemap) 자동 생성 확인
사이트맵(sitemap.xml)은 우리 블로그의 지도입니다. 현재 저장소에 sitemap.xml 파일이 존재하지만, 이 파일이 글을 쓸 때마다 자동으로 갱신되는지 확인이 필요합니다. Jekyll에서는 플러그인을 통해 이를 자동화하는 것이 가장 좋습니다.

#### 설정 방법:

 * Gemfile에 플러그인이 있는지 확인합니다.

```
   gem 'jekyll-sitemap'
```

 * _config.yml의 plugins 항목에 추가되어 있는지 확인합니다.

```
   plugins:
  - jekyll-sitemap
```

이렇게 설정하고 배포하면, https://wakenhole.github.io/sitemap.xml 주소로 접속했을 때 최신 글 목록이 XML 형태로 자동으로 생성됩니다.

## 4. 구글 서치 콘솔(Google Search Console)에 등록하기

모든 준비가 끝났다면 이제 구글에게 정식으로 인사를 건네야 합니다. '구글 서치 콘솔'은 내 사이트가 구글에서 어떻게 보이는지 모니터링하고 관리하는 필수 도구입니다.

#### 등록 단계:

 * 속성 추가: 구글 서치 콘솔에 접속하여 https://wakenhole.github.io를 URL 접두어 방식으로 추가합니다.
 * 소유권 확인: minimal-mistakes 테마 사용자는 _config.yml에 인증 코드를 넣는 것만으로 소유권 확인이 가능합니다. 서치 콘솔에서 제공하는 HTML 태그 값(content="..." 내부의 값)을 복사하세요.

```
   # _config.yml
analytics:
  google:
    verification: "구글에서_받은_긴_인증_코드"
```

 * 사이트맵 제출: 소유권 확인 후, 메뉴의 [Sitemaps] 로 이동하여 위에서 만든 sitemap.xml의 URL을 입력하고 제출 버튼을 누릅니다. '성공' 상태가 뜨면 며칠 내로 구글 봇이 글을 수집하기 시작합니다.

## 마치며

블로그 검색 노출은 하루아침에 이루어지지 않습니다. 하지만 오늘 정리한 robots.txt 파일명 수정과 같은 기본적인 설정들이 되어 있지 않다면 아무리 기다려도 노출되지 않습니다. 지금 바로 설정을 점검하고, 여러분의 소중한 글들이 더 많은 사람들에게 닿을 수 있도록 준비해 보세요!

