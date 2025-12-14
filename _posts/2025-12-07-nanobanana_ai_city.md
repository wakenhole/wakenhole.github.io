---
title: "나노바나나로 완성하는 나만의 작은 세상: 도시 미니어처 만들기 완전 정복 (프롬프트 예제 포함)"
lastmod: 2025-12-07 08:23:04 +0900
categories: [Tech]
tags: [AI, 나노바나나, 스테이블디퓨전, 미니어처, 아이소메트릭, 프롬프트, GitHub Actions]
toc: true
toc_sticky: true
header:
  overlay_image: https://image.fmkorea.com/files/attach/new5/20251204/9238675627_486616_2b304f1520d0fa462d5ec6881b9f42b0.jpg
  overlay_filter: 0.5
  teaser: https://image.fmkorea.com/files/attach/new5/20251204/9238675627_486616_0a7895c0f99bdffa28d66eb719c1f8a7.jpg
---

최근 커뮤니티에서 세상을 축소해놓은 듯한 아기자기하면서도 정교한 '도시 미니어처' 이미지가 큰 인기를 끌고 있습니다. 마치 거인이 되어 세상을 내려다보는 듯한 이 독특한 시각적 경험은 '나노바나나'(Google 이미지 생성 AI 모델)를 통해 누구나 쉽게 구현할 수 있습니다.


오늘은 클리앙 등지에서 화제가 된 이 멋진 미니어처 스타일을 내 손으로 직접 만드는 방법을 상세히 알아보겠습니다. 핵심은 카메라 앵글과 질감을 표현하는 정확한 '프롬프트'에 있습니다.

{% include ad-inpost.html %}
### 1. 기본편: 정교한 도시 미니어처 만들기



미니어처 스타일의 핵심은 두 가지입니다. 바로 **'아이소메트릭(Isometric)'** 뷰와 **'틸트 시프트(Tilt-shift)'** 효과입니다.

* **아이소메트릭(Isometric View):** 3차원 물체를 2차원 평면에 표현할 때, 원근감을 배제하고 X, Y, Z축이 각각 120도를 이루도록 그리는 방식입니다. 게임 '심시티'나 '롤러코스터 타이쿤'의 시점을 생각하시면 쉽습니다. 이 시점이 장난감 같은 느낌을 극대화합니다.
* **틸트 시프트(Tilt-shift):** 실제 사진 기법 중 하나로, 특정 영역에만 초점을 맞추고 나머지는 흐릿하게 날려버리는(아웃포커싱) 기법입니다. 이 효과를 적용하면 실제 풍경도 마치 작은 모형을 찍은 것처럼 보이게 됩니다.

이 두 가지 요소를 조합하여, 나만의 작은 도시를 건설하는 기본 프롬프트를 소개합니다.

**🎯 기본 도시 미니어처 프롬프트 (예제: 강남구)**

```markdown
Present a clear, 45° top-down isometric miniature 3D cartoon scene of 강남구, featuring its most iconic landmarks and architectural elements. Use soft, refined textures with realistic PBR materials and gentle, lifelike lighting and shadows. Integrate the good weather conditions directly into the city environment to create an immersive atmospheric mood.
Use a clean, minimalistic composition with a soft, solid-colored background.
At the top-center, place the title “강남구” in large bold text"
All text must be centered with consistent spacing, and may subtly overlap the tops of the buildings.
Square 1080x1080 dimension.
````
-----

{% include ad-inpost.html %}

**🎯 날씨 포함 프롬프트**

기본적인 도시 건설에 익숙해졌다면, 이제 그 작은 세상에 생명력을 불어넣을 차례입니다. 비가 오거나 눈이 내리는 날씨 효과는 미니어처의 디테일을 한층 더 돋보이게 만들고 감성적인 분위기를 연출합니다.

```markdown
Present a clear, 45° top-down isometric miniature 3D cartoon scene of 강남구, featuring its most iconic landmarks and architectural elements. Use soft, refined textures with realistic PBR materials and gentle, lifelike lighting and shadows. Integrate the current weather conditions directly into the city environment to create an immersive atmospheric mood.
Use a clean, minimalistic composition with a soft, solid-colored background.
At the top-center, place the title “강남구” in large bold text, a prominent weather icon beneath it, then the date (small text) and temperature (medium text).
All text must be centered with consistent spacing, and may subtly overlap the tops of the buildings.
Square 1080x1080 dimension.
```

![북경시 날씨](https://github.com/user-attachments/assets/7eaf11df-5102-46cd-92f6-a5e7723ea978)

### 2\. 응용편: 날씨와 분위기를 더한 미니어처

날씨 효과를 추가할 때는 단순히 '비'나 '눈'이라는 단어만 추가하는 것이 아니라, 그 날씨로 인해 파생되는 환경 효과(젖은 바닥, 반사, 안개 등)를 함께 명시해 주는 것이 중요합니다.

```
(isometric view:1.3), miniature city diorama at night, heavy rain falling, wet asphalt streets, reflections of neon lights on puddles, tiny people with umbrellas, misty atmosphere, detailed skyscrapers, tilt-shift lens effect, cinematic lighting, dramatic shadows, cozy atmosphere

Negative Prompt:
daylight, dry streets, clear sky, low resolution, ugly, blurry
```

  * **핵심 포인트:** `heavy rain falling`과 함께 `wet asphalt streets`, `reflections of neon lights on puddles`를 추가하여 비 오는 날 특유의 질척이고 반짝이는 질감을 표현했습니다. `misty atmosphere`는 도시의 원경을 부드럽게 처리하여 깊이감을 더해줍니다. 눈 오는 날을 원한다면 `heavy snow`, `snow covered roofs` 등으로 응용할 수 있습니다.

![북경시 날씨 및 분위기](https://github.com/user-attachments/assets/fac5d15a-647b-4e7d-a445-c01f21695435)



-----

{% include ad-inpost.html %}
### 3\. 심화편: GitHub Actions로 생성 자동화하기

매번 프롬프트를 입력하는 것이 번거롭다면, 개발자들의 놀이터인 GitHub를 이용해 이 과정을 자동화할 수도 있습니다. GitHub Actions는 특정 이벤트(예: 매일 아침 9시)가 발생했을 때 미리 정의된 스크립트를 실행해 주는 도구입니다.

이 방법을 사용하려면 AI 모델을 실행시킬 수 있는 API(예: Stable Diffusion WebUI의 API 모드 또는 외부 유료 API)가 필요합니다. 여기서는 개념적인 워크플로우 흐름을 소개합니다.

**⚙️ GitHub Actions 워크플로우 예시 (.github/workflows/daily\_miniature.yml)**

이 워크플로우는 매일 정해진 시간에 파이썬 스크립트를 실행하여 이미지를 생성하고, 생성된 이미지를 저장소에 자동으로 커밋하는 예시입니다.

```yaml
name: Daily Miniature Generator

on:
  schedule:
    # 매일 한국 시간 오전 10시 (UTC 01:00) 에 실행
    - cron: '0 1 * * *'
  workflow_dispatch: # 수동 실행 옵션

jobs:
  generate-and-post:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          pip install requests Pillow # API 호출 및 이미지 처리를 위한 라이브러리

      - name: Generate Image via API script
        env:
          API_URL: ${{ secrets.SD_API_URL }} # 리포지토리 시크릿에 저장된 API 주소
          API_KEY: ${{ secrets.SD_API_KEY }} # 인증 키
        run: |
          # 여기에 실제로 API를 호출하고 이미지를 저장하는 파이썬 스크립트를 실행합니다.
          # 예: python generate_image.py --prompt "isometric view, miniature..."
          echo "Image generation started..."
          # python scripts/generate_miniature.py (실제 구현 필요)

      - name: Commit and Push generated image
        run: |
          git config --global user.name 'GitHub Action'
          git config --global user.email 'action@github.com'
          git add assets/images/daily_miniature/*.png
          git commit -m "Auto-generated daily miniature image"
          git push
```

**자동화 구축을 위한 팁:**

1.  **API 확보:** Stable Diffusion을 로컬이나 클라우드 서버(Colab 등)에서 API 모드로 실행하거나, Stability AI 같은 유료 API 서비스를 이용해야 합니다.
2.  **스크립트 작성:** 위 워크플로우에서 호출할 `generate_miniature.py` 같은 스크립트를 작성해야 합니다. 이 스크립트는 API에 위에서 배운 프롬프트를 전송하고, 결과 이미지를 받아 로컬 경로에 저장하는 역할을 합니다.
3.  **보안:** API 키와 같은 민감한 정보는 반드시 GitHub Repository의 'Settings -\> Secrets'에 저장하여 노출을 막아야 합니다.

이제 여러분도 나노바나나와 함께 책상 위의 작은 조물주가 되어보세요. 프롬프트는 정답이 없습니다. 다양한 시도를 통해 여러분만의 독창적인 미니어처 세상을 만들어 보시길 바랍니다.
