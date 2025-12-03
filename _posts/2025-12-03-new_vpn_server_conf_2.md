---
title: "[NEW] 간단한 개인용 VPN 서버 구축의 모든것 2: Marzban VPN 설정"
categories:
  - VPN 
tags:
  - Xray
  - Marzban
  - 중국
  - vless
  - vmess
  - Virtual Private Network
toc: true
toc_sticky: true
published: true
tagline: "VPN"
header:
  overlay_image: https://images.unsplash.com/photo-1691435828932-911a7801adfb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3132&q=80
  overlay_filter: 0.5
  caption: "[**Unsplash**](https://unsplash.com)"
  teaser: https://images.unsplash.com/photo-1691435828932-911a7801adfb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3132&q=80
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

### Marzban 설정

SSL 설정까지 완료 되면 아래 링크르 들어가고, Marzban 설치시 만든 admin 계정으로 로그인 합니다.

> https://YOUR_SERVER_IP:8000/dashboard/

![Marzban Login](https://user-images.githubusercontent.com/20836193/236632486-F3E3D0C3-1C7C-4D1C-8E2E-1CFF1C8D1E2D.png)

### Marzban 설정 추가

본 글에서는 3가지 설정 방법을 다룬다

1. VLESS TCP REALITY
2. VLESS TCP NOTLS
3. Shadowsocks TCP

로그인을 하고 나면 아래와 같은 화면이 나오며, 우측 상단의 설정 버튼을 클릭합니다. 

![Image](https://github.com/user-attachments/assets/d4852929-a785-4bdb-be8c-5d8a74759cb1)

설정 버튼을 클릭하고 나면 아래와 같은 창이 나오며, 아래 json을 참고해서 inbound 설정을 추가 하면 됩니다.

![Image](https://github.com/user-attachments/assets/597d17bd-c1d1-488b-8559-45bfe3271bb2)



```json
{
    ...
  "inbounds": [
    {
      "tag": "VLESS TCP REALITY",
      "listen": "0.0.0.0",
      "port": 443,
      "protocol": "vless",
      "settings": {
        "clients": [],
        "decryption": "none"
      },
      "streamSettings": {
        "network": "tcp",
        "tcpSettings": {},
        "security": "reality",
        "realitySettings": {
          "show": false,
          "dest": "www.microsoft.com:443",
          "xver": 0,
          "serverNames": [
            "SERVER_NAME",
            ""
          ],
          "privateKey": "PRIVATE_KEY",
          "SpiderX": "/example",
          "shortIds": [
            "SHORT_ID"
          ]
        }
      },
      "sniffing": {
        "enabled": true,
        "destOverride": [
          "http",
          "tls",
          "quic"
        ]
      }
    },
    {
      "tag": "VLESS TCP NOTLS",
      "listen": "0.0.0.0",
      "port": 443,
      "protocol": "vless",
      "settings": {
        "clients": [],
        "decryption": "none"
      },
      "streamSettings": {
        "network": "tcp",
        "tcpSettings": {},
        "security": "none"
      },
      "sniffing": {
        "enabled": true,
        "destOverride": [
          "http",
          "tls",
          "quic"
        ]
      }
    },
    {
      "tag": "Shadowsocks TCP",
      "listen": "0.0.0.0",
      "port": 1080,
      "protocol": "shadowsocks",
      "settings": {
        "clients": [],
        "network": "tcp,udp"
      }
    }
  ],
   ...
}
```
### PRIVATE_KEY 및 SHORT_ID 생성 방법

PRIVATE_KEY는 아래 명령어를 통해서 생성할 수 있습니다.


```sh
docker exec marzban-marzban-1 xray x25519
```

SHORT_ID는 16진수 8자리 문자열로 생성하면 됩니다. 예를 들어, `a1b2c3d4` 와 같은 형식입니다.

```sh
openssl rand -hex 8
```

SERVER_NAME은 설치한 서버 주소를 입력하면 된다.

### 사용자 추가 

Creat User 버튼을 누루고 나면, 아래 이미지와 같이 User 생성이 가능하다.
원하는 protocol을 선택하고, ID 및 기타 설정을 완료 한 후에 생성 버튼을 누르면 된다. 
VLESS의 경우 ID는 UUID 형식이다. 자동 생성 되니 입력할 필요 없다.

![Image](https://github.com/user-attachments/assets/c14180c5-56cc-4679-85b3-25336225a250)

User를 생성하고나면, User 목록에 추가된 것을 확인할 수 있다.
QR Code 또는 shared link를 통해서 단말 app에 쉽게 서버 설정을 추가할 수 있다.
