---
title: "[NEW] 간단한 개인용 VPN 서버 구축의 모든것 1: Marzban VPN 설치"
categories: [Tech, Networking & VPN]
tags:
  - v2ray
  - Marzban
  - 중국
  - vless
  - vmess
  - Virtual Private Network
toc: true
toc_sticky: true
tagline: "VPN"
image:
  path: https://images.unsplash.com/photo-1691435828932-911a7801adfb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3132&q=80
---


## 전체 글 목록
1. [VPN용 VM 서버 구축](https://wakenhole.github.io/vpn/vpn_server_conf_1/)
2. [VPN 서버 보안 설정](https://wakenhole.github.io/vpn/vpn_server_conf_2/)
3. [X-UI 설치 및 설정](https://wakenhole.github.io/vpn/vpn_server_conf_3/)
4. [Marzban VPN 설치](https://wakenhole.github.io/vpn/new_vpn_server_conf_1/)
5. [Marzban VPN 설정](https://wakenhole.github.io/vpn/new_vpn_server_conf_2/)

{% include ad-inpost.html %}

## Reference
1. [Marzban](https://github.com/Gozargah/Marzban)
2. [Marzban Installation](https://gozargah.github.io/marzban/en/docs/installation)

## Marzban에 대해서 

X-UI를 잘 사용하고 있었지만, Xray 업데이트에 따른 추가 업데이트가 없는 상황에서, GUI platform을 변경하는 것이 좋다고 생각했다. 
Xray 예전 버전은 Google에서 국가를 제대로 인지하지 못해서, 기능 몇가지가 차단되는 문제가 있으며, Google Gemini도 사용하지 못한다. 

### 사전 서버 준비

사전 서버 준비는 기존과 동일하며, 아래 두글을 통해서 진행하면 된다. 

1. [VPN용 VM 서버 구축](https://wakenhole.github.io/vpn/vpn_server_conf_1/)
2. [VPN 서버 보안 설정](https://wakenhole.github.io/vpn/vpn_server_conf_2/)


{% include ad-inpost.html %}


### Marzban 설치

아래 명령어를 통해서 설치를 시작하자. Database 종류에 따라서 다른 설치 script도 있지만, 기본적인 SQLite를 이용한 방법을 사용한다. 

```sh
sudo bash -c "$(curl -sL https://github.com/Gozargah/Marzban-scripts/raw/master/marzban.sh)" @ install
```

> Marzban 데이터는 /var/lib/marzban 디렉토리에 저장됩니다.
> 
> Marzban 애플리케이션 파일(docker-compose.yml 및 .env)은 /opt/marzban 디렉토리에 저장됩니다.


### Marzhan 기본 설정

설치가 완료 되고 나면, Log가 나올텐데, Ctrl+C를 하여 강제 종료를 한다. 

아래 명령어를 통해서 관리자 계정을 생성한다. 
추후 Dashboard에 접근 및 설정하기 위해서 이다. 

```
marzban cli admin create --sudo
```

기타 명령어는 아래를 통해서 확인할 수 있다. (크게 건드릴 것은 없음)

```
marzban --help
```

{% include ad-inpost.html %}

### SSL 설정

현재 상태에서는 dashboard가 http (http://YOUR_SERVER_IP:8000/dashboard/)로 접속 되고 https 사용이 되지 않는다. 

따라서 아래와 같이 설정해주자. 
CA file를 marzban의 container가 사용하는 local path로 복사한다. 
```
mkdir /var/lib/marzban/certs
cp /root/cert.crt /var/lib/marzban/certs
cp /root/private.key /var/lib/marzban/certs
```

/opt/marzban/.env 을 vi나 nano로 열어서 아래 변수를 수정한다. 
```
UVICORN_PORT = 443
UVICORN_SSL_CERTFILE = "/var/lib/marzban/certs/cert.crt"
UVICORN_SSL_KEYFILE = "/var/lib/marzban/certs/private.key"
XRAY_SUBSCRIPTION_URL_PREFIX = https://YOUR_DOMAIN
```

아래 명령어를 통해서 marzban을 재시작 해준다. 

```
marzban restart
```

이제 아래 링크가 잘 접속되는지 확인해보도록 하자 

> https://YOUR_SERVER_IP:8000/dashboard/
