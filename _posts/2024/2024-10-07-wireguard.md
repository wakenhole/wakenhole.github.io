---
title: "Wireguard & OpenVPN 손쉽게 구축하기"
categories: [Tech, Networking & VPN]
tags:
  - wireguard
  - OpenVPN
  - Virtual Private Network
toc: true
toc_sticky: true
tagline: "VPN"
header:
  overlay_image: https://images.unsplash.com/photo-1484557052118-f32bd25b45b5?q=80&w=3869&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D
  overlay_filter: 0.5
  caption: "[**Unsplash**](https://unsplash.com)"
  teaser: https://images.unsplash.com/photo-1484557052118-f32bd25b45b5?q=80&w=3869&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D
---


{% include ad-inpost.html %}

## 전체 글 목록

## Reference
1. [VPN용 VM 서버 구축](https://wakenhole.github.io/vpn/vpn_server_conf_1/)
2. [VPN 서버 보안 설정](https://wakenhole.github.io/vpn/vpn_server_conf_2/)
3. [X-UI 설치 및 설정](https://wakenhole.github.io/vpn/vpn_server_conf_3/)

## V2Ray 이외 기타 VPN 

V2Ray는 설치가 조금 복잡하긴 하지만, 몇 가지 큰 장점이 있다. 
1. 복수의 사용자에게 배포하기 용이함.
2. 다양한 Protocol 제공 가능
3. 다양한 스마트폰용 VPN Application에서 사용 가능
4. 다양한 기능 사용가능 (예를들면 Android v2ray의 앱별 VPN 적용)
5. OpenWRT에서 제공하는 Passwall 등에서 유용하게 사용

하지만 오늘 소개할 Wireguard나 OpenVPN의 경우도 다양한 장점이 있다.  
1. 설치가 매우 간단함
2. 모든 종류의 기기에 Client App이 있음 (X-UI의 경우 MAC 이나 윈도우에서 사용에 한계가 있음)
3. GL.iNet MT2500과 같이 전문 Server용 기기도 저렴하게 구매 가능 (서버 운용비 절약 가능)


{% include ad-inpost.html %}

### Wireguard 서버 설정


```
mkdir wireguard
cd wireguard
curl -O https://raw.githubusercontent.com/angristan/wireguard-install/master/wireguard-install.sh
chmod +x wireguard-install.sh
./wireguard-install.sh
```

위와 같이 Script를 실행하고나면, Server IP 및 Port를 설정하게 된다. 
KT Cloud(혹은 본인 서버)의 IP 주소를 입력하고, Port도 반드시 Server에서 접근 허용이 되어 있어야 한다. [포트 설정](https://wakenhole.github.io/vpn/vpn_server_conf_1/)
Wireguard의 경우 UDP를 사용하기 때문에 UDP를 open 시켜줘야 한다. 

V2Ray와 다른 점은 사용자 별로 매번 추가해 줘야 한다. 
신규 사용자를 추가할 경우 Script를 재실행하여, **Add a new user **를 해주면 된다. 

```
$ ./wireguard-install.sh
Welcome to WireGuard-install!
The git repository is available at: https://github.com/angristan/wireguard-install

It looks like WireGuard is already installed.

What do you want to do?
   1) Add a new user
   2) List all users
   3) Revoke existing user
   4) Uninstall WireGuard
   5) Exit
Select an option [1-5]:
```

{% include ad-inpost.html %}

### OpenWRT 서버 설정

```
mkdir openvpn
cd openvpn
curl -O https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh
chmod +x openvpn-install.sh
./openvpn-install.sh
```

OpenWRT는 Wireguard와 비슷하다. 다만 Mobile 환경에서 자주 끊어지는 것 같아서 본인은 사용을 지양하는 편이다. 
OpenWRT는 TCP 및 UDP를 선택적으로 사용이 가능하다. 