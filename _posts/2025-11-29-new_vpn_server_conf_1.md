---
title: "[NEW] 간단한 개인용 VPN 서버 구축의 모든것 1: Marzban VPN"
categories:
  - VPN 
tags:
  - Marzban
  - xray
  - v2ray
  - 중국
  - docker
  - Virtual Private Network
toc: true
toc_sticky: true
tagline: "VPN"
header:
  overlay_image: https://images.unsplash.com/photo-1691435828932-911a7801adfb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3132&q=80
  overlay_filter: 0.5
  caption: "[**Unsplash**](https://unsplash.com)"
  teaser: https://images.unsplash.com/photo-1691435828932-911a7801adfb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3132&q=80
---


## Marzban을 선택한 이유
X-UI보다 더 적극적으로 유지관리되고 있고, gRPC/Reality 등 최신 Xray 기능을 패널에서 쉽게 쓸 수 있다. Docker 기반이라 업데이트와 백업도 단순하다. 이 글은 **Ubuntu 20.04/22.04 단일 서버에 Marzban을 설치**하는 가장 간단한 흐름만 정리했다.


## 준비물
1. Ubuntu 20.04/22.04 이상의 VM (vCPU 1~2, RAM 1~2 GB 정도면 단일 사용자용으로 충분)
2. 루트 권한 또는 sudo 권한 계정
3. 도메인 1개(선택)와 80/443 포트 개방 – HTTPS 패널, Reality를 쓰면 더 안전
4. 방화벽에서 22(SSH), 80/443(패널/인증서), 서비스용 인바운드 포트를 허용


## 1. 서버 기본 세팅
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y ca-certificates curl git ufw
sudo timedatectl set-timezone Asia/Seoul
sudo ufw allow 22/tcp
sudo ufw allow 80,443/tcp
sudo ufw enable
```


## 2. Docker + Docker Compose 설치
```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker "$USER"
sudo systemctl enable --now docker
sudo apt install -y docker-compose-plugin
```

> 만약 바로 `docker` 명령이 안된다면 `newgrp docker` 로 그룹 재적용 또는 새 세션을 연다.


## 3. (선택) 무료 TLS 인증서 발급
패널/인바운드를 HTTPS로 노출하려면 먼저 인증서를 준비한다.
```bash
sudo apt install -y snapd
sudo snap install core && sudo snap refresh core
sudo snap install --classic certbot
sudo certbot certonly --standalone -d vpn.example.com
```
인증서 경로는 `/etc/letsencrypt/live/vpn.example.com/fullchain.pem` 과 `privkey.pem` 이 된다.


## 4. Marzban 내려받기와 환경파일
```bash
sudo mkdir -p /opt && cd /opt
sudo git clone https://github.com/Gozargah/Marzban
cd Marzban
sudo cp .env.example .env
sudo cp ./config.json.example ./config.json   # 인바운드 설정 기본값
```

`.env`에서 꼭 손대는 항목 예시:
```bash
PANEL_HOST=0.0.0.0      # 패널 바인딩
PANEL_PORT=8000         # 패널 포트
SSL=true                # HTTPS 사용 여부
SSL_CERT_FILE=/etc/letsencrypt/live/vpn.example.com/fullchain.pem
SSL_KEY_FILE=/etc/letsencrypt/live/vpn.example.com/privkey.pem
TZ=Asia/Seoul
LOG_LEVEL=info
XRAY_API_HOST=xray
XRAY_API_PORT=10085
```

`config.json`은 Xray 인바운드 정의 파일이다. 기본으로 VLESS/gRPC 가 들어있으며, Reality·WS·Trojan 등 필요에 맞게 수정 후 저장한다.


## 5. 컨테이너 기동
```bash
sudo docker compose pull
sudo docker compose up -d
sudo docker compose ps
```
`healthy` 상태면 정상. 로그는 `sudo docker compose logs -f marzban` 으로 확인한다.


## 6. 관리자 계정 만들기
```bash
sudo docker compose exec marzban python3 -m marzban.cli admin create \
  --username admin --password '강한_패스워드'

sudo docker compose exec marzban python3 -m marzban.cli admin token --username admin
```
토큰을 복사해서 웹 패널 로그인이나 API 호출에 사용한다. 기본 접속 주소는 `https://vpn.example.com:8000` 혹은 지정한 도메인/포트 조합이다.


## 7. 인바운드/사용자 발급 빠른 예시
1. `config.json`에서 Reality나 gRPC, WS 인바운드를 필요에 맞게 수정한다.
2. 적용: `sudo docker compose restart xray`.
3. 사용자 추가:
```bash
sudo docker compose exec marzban python3 -m marzban.cli user create \
  --username alice --data-limit 20GB --expire 30d
```
4. QR/링크 출력:
```bash
sudo docker compose exec marzban python3 -m marzban.cli user url --username alice
```


## 8. 업데이트 & 백업
- 업데이트: `cd /opt/Marzban && sudo git pull && sudo docker compose pull && sudo docker compose up -d`
- 데이터: `/opt/Marzban/data` (sqlite/redis 등)와 `config.json`, `.env`를 주기적으로 백업
- 서비스 재시작: `sudo docker compose restart`


## 9. 장애 대처 체크리스트
- 패널 접속 불가: 방화벽(ufw/security-group)에서 80/443/패널 포트 허용 여부 확인
- 인증서 오류: 도메인 A레코드가 서버 IP를 가리키는지, certbot 만료 여부 확인
- 클라이언트 연결 불가: `config.json` 인바운드 포트/프로토콜과 방화벽, ISP 차단 여부 점검
- 로그 확인: `sudo docker compose logs -f xray` / `marzban`


## Reference
1. [Marzban GitHub](https://github.com/Gozargah/Marzban)
2. [Xray Project](https://github.com/XTLS/Xray-core)
3. [Let’s Encrypt / Certbot](https://certbot.eff.org/)

### X-UI GUI Web https접속


이제는 관리자 페이지를 **https**로 접속할 수 있다. 

> https://ktvpn.duckdns.org:5000/

## X-UI를 활용한 V2Ray 설정

아래 VPN 목록 화면으로 들어가서 **+** 버튼을 누르자.
![image](https://github.com/wakenhole/wakenhole.github.io/assets/2586880/b4b9d958-0896-4a44-b4dd-88cb73fe2295)

다양한 프로토콜 조합으로 VPN을 만들 수 있지만, 일단 본 강좌에서는 두 가지만 설명하도록 한다. 
1. VMESS
2. VLESS with TLS
   
### VMESS without TLS

당연히 VMESS도 암호화가 가능하지만, 연습삼아 해보도록 하자. 가끔 TLS 문제인지 아닌지 확인시 필요할 경우가 있다. 

아래와 같이 설정한다. 
* remark: 이름 (임의)
* protocol: vmess
* 端口(port): 3000 ([1편](https://wakenhole.github.io/vpn/vpn_server_conf_1/)에서 설정한 포트 번호)


![image](https://github.com/wakenhole/wakenhole.github.io/assets/2586880/335bea59-f5c4-4e69-804c-47b4e3412ec7)

오른쪽 아래의 추가 (X加) 버튼을 눌러서 추가하자.

### VLESS with TLS

가장 많이 사용되는 방식이고, 황금방패가 차단하는 경우가 잘없다. 혹시 차단되더라도 포트만 변경해주면된다. 

아래와 같이 설정한다. 
* remark: 이름 (임의)
* protocol: vless
* 端口 (Port): 3001 ([1편](https://wakenhole.github.io/vpn/vpn_server_conf_1/)에서 설정한 포트 번호)
* 域名 (Domain name): ktvpn.duckdns.org
* 公钥文件路径 (Public key): /root/cert.crt
* 密钥文件路径 (Private key): /root/private.key

![image](https://github.com/wakenhole/wakenhole.github.io/assets/2586880/9f264f54-aba8-40f2-839b-3bd137165815)

오른쪽 아래의 추가 (X加) 버튼을 눌러서 추가하자.

### V2Ray 설정 완료

아래와 같이 목록이 생성되었으면, V2Ray 서버 설정이 완료 된것이다.

![image](https://github.com/wakenhole/wakenhole.github.io/assets/2586880/23eaec31-1b48-4b6b-a148-f2c204cdfd81)
