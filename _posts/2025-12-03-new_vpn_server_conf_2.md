---
title: "[NEW] 간단한 개인용 VPN 서버 구축의 모든것 1: Marzban VPN"
categories:
  - VPN 
tags:
  - v2ray
  - Marzban
  - 중국
  - vless
  - vmess
  - Virtual Private Network
toc: true
toc_sticky: true
published: false
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



```json
{
  "log": {
    "loglevel": "warning"
  },
  "routing": {
    "rules": [
      {
        "ip": [
          "geoip:private"
        ],
        "outboundTag": "BLOCK",
        "type": "field"
      }
    ]
  },
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
  "outbounds": [
    {
      "protocol": "freedom",
      "tag": "DIRECT"
    },
    {
      "protocol": "blackhole",
      "tag": "BLOCK"
    }
  ]
}
```