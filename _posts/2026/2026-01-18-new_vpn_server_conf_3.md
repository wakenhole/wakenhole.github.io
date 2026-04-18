---
title: "[NEW] 간단한 개인용 VPN 서버 구축의 모든것 3: 3x-ui로 구축하는 Xray 패널 완벽 가이드"
categories: [Tech, Networking & VPN]
date: 2026-01-18 16:00:00 +0900
tags:
  - 3x-ui
  - VPN구축
  - Xray
  - VLESS
  - Reality
  - VPS
toc: true
toc_sticky: true
published: true
tagline: "VPN"
image:
  path: https://3x-ui.com/wp-content/uploads/2025/09/65422981-1024x1024.jpg
---

무료로 사용할 수 있는 강력한 VPN 서버 관리 패널, **3x-ui**를 활용하여 초보자도 10분 만에 고성능 VPN 서버를 구축하는 방법을 소개합니다.

### 전체 글 목록
1. [VPN용 VM 서버 구축](https://wakenhole.github.io/2023/vpn_server_conf_1/)
2. [VPN 서버 보안 설정](https://wakenhole.github.io/2023/vpn_server_conf_2/)
3. [X-UI 설치 및 설정](https://wakenhole.github.io/2023/vpn_server_conf_3/)
4. [Marzban VPN 설치](https://wakenhole.github.io/2025/new_vpn_server_conf_1/)
5. [Marzban VPN 설정](https://wakenhole.github.io/2025/new_vpn_server_conf_2/)

{% include ad-inpost.html %}

### Reference
1. [3X-UI github](https://github.com/MHSanaei/3x-ui?tab=readme-ov-file)
2. [3X-UI wiki](https://github.com/MHSanaei/3x-ui/wiki)

오늘은 일전에 소개한 X-UI는 더이상 update가 되고 있지 않다, X-UI를 기반으로 Xray 최신 core가 들어가 있는 새로운 VPN 서버 opensource 설치 방법을 설명한다. 

**[MHSanaei/3x-ui](https://github.com/MHSanaei/3x-ui)**를 활용하여, 초보자도 10분 만에 고성능 VPN 서버를 구축하는 방법을 소개합니다. "[X-UI 설치 및 설정](https://wakenhole.github.io/2023/vpn_server_conf_3/)" 여기서 소개한 방법과 크게 차이가 없으니 더 자세한 내용은 위 링크를 참고하여도 좋다.

> **⚠️ 주의사항:** 본 가이드는 네트워크 학습 및 개인 정보 보호(Privacy)를 위한 교육 목적으로 작성되었습니다. 불법적인 용도로의 사용을 금합니다.

### 1. 준비물: 해외 VPS 서버

가장 먼저 서버가 필요합니다. AWS, Oracle Cloud(무료 티어 추천), Vultr, DigitalOcean 등 해외 리전을 제공하는 호스팅 업체를 이용하세요.

* **OS 권장:** Ubuntu 22.04 LTS 또는 Debian 11/12
* **사양:** CPU 1 Core, RAM 1GB 이상이면 충분합니다.
* **필수:** 서버의 공인 IP 주소를 알고 있어야 하며, 방화벽(Firewall)에서 80, 443 포트와 패널 접속용 포트를 열어두어야 합니다.

한국용 VPN을 만들경우는 "[VPN용 VM 서버 구축](https://wakenhole.github.io/2023/vpn_server_conf_1/)" 글을 참고하면 좋습니다.

### 2. SSL 설정
"[VPN 서버 보안 설정](https://wakenhole.github.io/2023/vpn_server_conf_2/)"을 참고해서 SSL 설정을 하기를 바랍니다. 

### 3. 3x-ui 패널 설치하기

터미널(SSH)을 통해 서버에 접속했다면, 설치는 명령어 한 줄이면 끝납니다. MHSanaei가 제공하는 **원클릭 설치 스크립트**를 사용합니다.

```bash
bash <(curl -Ls https://raw.githubusercontent.com/mhsanaei/3x-ui/master/install.sh)
```

이 명령어를 입력하면 설치 마법사가 시작됩니다.
1.  **설치 확인:** `y`를 입력하여 진행합니다.
2.  **계정 설정:** 관리자 페이지 접속을 위한 `Username`, `Password`, `Port`를 설정합니다. 
    * *팁: 보안을 위해 포트는 10000번대 이상의 임의의 숫자(예: 20530)를 추천합니다.*

설치가 완료되면 다음과 같은 메시지가 뜹니다.
> `http://your_server_ip:port`

{% include ad-inpost.html %}

### 4. 패널 접속 및 기본 설정

웹 브라우저를 열고 `http://서버IP:포트`로 접속한 뒤, 방금 설정한 아이디와 비밀번호로 로그인합니다.

로그인으로 하고 Panel Setting > General > General > URI path를 "/"를 수정한다. 보안 경고가 뜨지만, 편의성을 위해서 가볍게 무시한다. 

 Panel Setting > General > Certificates 에서 public key와 private key를 위에서 생성한 SSL key 경로로 입력해준다. 

  * /root/cert.crt
  * /root/private.key

### 5. 핵심: VLESS-Reality 인바운드 생성

이제 실제로 VPN 연결을 받아줄 '문(Inbound)'을 만들어야 합니다. 
우리는 현재 가장 빠르고 차단이 어려운 **VLESS + Reality + Vision** 조합을 사용할 것입니다. 도메인 구매나 SSL 인증서 발급 과정 없이, IP만으로 강력한 보안 연결이 가능합니다.

좌측 메뉴의 **[Inbounds]** -> **[Add Inbound]**를 클릭하고 아래와 같이 설정하세요.

* **Remark:** 원하는 이름 (예: MyVPN-Reality)
* **Protocol:** `vless`
* **Listening IP:** (비워둠)
* **Port:** `443` 
    * *주의: Reality 방식은 443 포트 사용을 강력 권장합니다.*
* **Transmission:** `TCP`
* **Security:** `Reality` (이것을 선택하는 것이 핵심입니다!)

#### Reality 세부 설정 (중요)
Security를 Reality로 선택하면 아래 추가 옵션이 나옵니다.
* **uTLS:** `Chrome` 또는 `Firefox`
* **Dest:** `www.microsoft.com:443` 또는 `www.google.com:443`
    * *설명: 내 트래픽을 마치 마이크로소프트나 구글 등 신뢰할 수 있는 사이트에 접속하는 것처럼 위장(Camouflage)하는 기술입니다.*
* **SNI:** 위 Dest와 동일한 도메인 입력 (예: `www.microsoft.com`)
* **ShortId:** 입력칸 옆의 ⚡(생성) 버튼 클릭
* **Private Key:** 입력칸 옆의 ⚡(생성) 버튼 클릭 
    * *중요: 이때 생성된 **Public Key**는 클라이언트 설정 시 필요하므로 자동으로 저장되지만, 만약을 위해 확인해 둡니다.*

모두 입력했다면 하단의 **[Create]** 버튼을 누릅니다.

![Cyber Security](https://images.unsplash.com/photo-1563206767-5b1d97289374?ixlib=rb-4.0.3&auto=format&fit=crop&w=1472&q=80)

<br>

### 6. 클라이언트(PC/모바일) 연결하기

생성된 Inbound 리스트에서 **[Info]** 아이콘(눈 모양 또는 정보 아이콘)을 누르면 QR코드와 `vless://`로 시작하는 URL이 나옵니다.

#### 추천 클라이언트 앱
* **Windows:** [v2rayN](https://github.com/2dust/v2rayN) 또는 [Nekoray](https://github.com/MatsuriDayo/nekoray)
* **Android:** [v2rayNG](https://github.com/2dust/v2rayNG)
* **iOS:** **V2Box** (무료) 또는 **Shadowrocket** (유료, 3,300원 - 강력 추천)
* **Mac:** V2Box 또는 Foxray

**연결 방법 (예시: 스마트폰):**
1.  3x-ui 패널 화면에 QR코드를 띄웁니다.
2.  스마트폰 앱(v2rayNG 등)을 켜고 `+` 버튼 -> `QR코드 스캔`을 선택하여 화면을 찍습니다.
3.  서버가 목록에 추가되면 선택 후 `Connect`(연결) 버튼을 누릅니다.
4.  유튜브나 구글이 잘 열리는지, `fast.com`에서 속도가 잘 나오는지 테스트합니다.

<br>

### 7. 3x-ui만의 강력한 기능들

MHSanaei 버전의 3x-ui는 단순한 연결 외에도 강력한 관리 기능을 제공합니다.

1.  **트래픽 제한:** 친구와 공유할 때, 특정 사용자에게 "월 50GB"만 쓰도록 제한을 걸 수 있습니다. (Traffic Limit 설정)
2.  **기간 제한:** "30일 뒤 만료"되도록 설정하여 임시 계정을 발급할 수 있습니다. (Expire Date 설정)
3.  **텔레그램 봇 연동:** 서버 상태나 트래픽 사용량을 텔레그램으로 알림 받을 수 있습니다.

---

### 마치며

이제 여러분은 언제 어디서나 안전하고 자유롭게 인터넷을 즐길 수 있는 전용망을 갖게 되었습니다. 공공 와이파이(카페, 공항 등)를 쓸 때도 이 VPN을 켜면 해킹 위협으로부터 안전해집니다.

3x-ui는 오픈소스 커뮤니티의 노력으로 계속 진화하고 있으니, GitHub 저장소를 종종 확인하며 업데이트를 챙겨주시길 바랍니다.

**Reference:**
* [GitHub - MHSanaei/3x-ui Official Repository](https://github.com/MHSanaei/3x-ui)