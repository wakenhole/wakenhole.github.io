---
title: "간단한 개인용 VPN 서버 구축의 모든것 1: VPN용 VM 서버 구축 (V2Ray using X-UI)"
categories:
  - VPN 
tags:
  - V2Ray
  - x-ui
  - 중국
  - vless
  - vmess
  - Astrill
  - 판다
  - KT Cloud
  - iwinv Cloud
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

## 전체 글 목록
1. [VPN용 VM 서버 구축](https://wakenhole.github.io/vpn/vpn_server_conf_1/)
2. [VPN 서버 보안 설정](https://wakenhole.github.io/vpn/vpn_server_conf_2/)
3. [X-UI 설치 및 설정](https://wakenhole.github.io/vpn/vpn_server_conf_3/)

## Reference
1. [V2Ray](https://www.v2ray.com/)
2. [X-UI, a multi-user Xray graphical management panel](https://seakfind.github.io/2021/10/10/X-UI/)
3. [중국 외노자를 위한 VPS에 VPN 구축기 (V2ray with X-UI 제어콘솔)](https://www.clien.net/service/board/lecture/17799473)

## VPN 사용의 필요성

중국에 거주하다보면, 외국인은 VPN을 사용할 수 밖에 없다. 
기본적으로 Google, 카카오톡, 네이버 등 많은 한국 싸이트들이 중국에서 막혀 있고, 
일부 한국 싸이트 들은 중국에서 접속을 비정상 접속이라고 간주하고 차단하기 때문이다. 
결국 중국에서 baidu등으로 모든 것을 옮길 수 있을정도가 아니라면, VPN 사용은 필수이다.

## 개인용 VPN 서버의 필요성

중국에서 가장 많이 사용하는 VPN은 판다, Astrill 등 다양하게 있지만, 가격은 보통 1년에 10-20만원 수준이다. 
비싼 가격은 아니지만 사실 속도 및 안정성에 문제가 있다. 
한국만 사용하다보면 어느 순간 끊기는 문제가 발생하기 때문에, 국가를 변경해가면서 사용할 수 밖에 없다. 
(실제 약관에는 무제한이라고 하지만, 사용량이 많으면 QoS를 관리하는 것 같다.)

특히 게임등을 원활하게 하려면 ping이 안적적으로 150 ms 이내가 나와야 하지만, 
기본적으로 jitter가 크기 때문에 사용하기에 어려움이 있다. 
게임을 할정도로 안정적인 서비스를 하려면 더 비싼 subscription을 가입해야 한다. 

## Cloud 선택 및 구축

하지만 한국에서 제공하는 다양한 Cloud 업체의 VM (Virtual Machine)를 활용해서 개인용 VPN을 구축하게 되면, 
훨씬 안정적인 서비스와 속도를 높은 가성비로 (거의 무료?) 사용할 수 있다.
추천 하는 Cloud 는 아래 두가지 이다. 
* [KT Cloud](https://cloud.kt.com/)
* [iwinv Cloud](https://www.iwinv.kr/)

AWS, Azure, GCP의 경우 가격이 비싸기 때문에 가성비가 나오지 않는다. 
KT는 가격은 비싸지만 무료 3개월 사용가능 하다. (가족 계정 돌려쓰기로 수년 사용 가능)
iwinv의 경우 가격이 저렴해서 무난하게 사용하기에 좋다. 
Oracle은 무료로 서버를 제공하지만, 절대 추천하지 않는다. 
우선 2주 정도 사용되고 나면, 어떤 이유에서인지 서버가 비정상상태가 된다. (아니면 중국에서 IP 차단 가능성 있음)

## KT Cloud 구축 하기 

KT Cloud 가입 후 결재 정보를 등록하고 나면 무료 할인 쿠폰을 받을 수 있다. 
3개월에 100만원까지 사용하는 것이기 때문에, 
비싼 서버에 수천 GB 를 사용하지만 않는다면 10만원으로도 충분하다.

### VPN용 VM 서버 생성
아래 그림을 참조해서 적당한 서버를 골라주면 된다. 
기타 설정은 굳이 안해도 무관하다. 
위치는 Seoul/Central등 아무 곳이나 선택해주면 된다. 

> Server > Server

![image](https://user-images.githubusercontent.com/2586880/270099105-810e87cd-ec40-42a8-b52b-1450a04f6f24.png)
* 위치: Seoul (본인 선택)
* 서버 이름: 본인 선택
* OS: Ubuntu 20.04 (버전은 중요하지 않음)
* 사양: 1 vcore, 1 GB (사양도 최소것으로 해도 문제 없음)
* 고급설정: 필요 없음  

### VM Port 설정
> Server > Server > 접속 설정 버튼 클릭

서버가 생성되고나면 등록된 e-mail로 SSH 접속을 위한 key가 날라온다.
이것을 이용해서 우리는 SSH 접속을 해야 한다. 하지만 사전에 SSH를 접속하기 위한 Port (22)를 열어 줘야 한다. 

![image](https://user-images.githubusercontent.com/2586880/270139894-d23ddb39-0730-424c-ac9d-1960928346ed.png)

위 사진과 같이 포트를 추가한다. 
* 22: SSH
* 80/443: SSL을 위한 http/https 포트
* 3000: V2Ray 포트 (여러개를 나눠서 쓰려면 여러개 만들면 됨)
* 5000: V2Ray 관리자 Web

추가적으로 **공인 IP**에 적혀 있는 IP 주소 (e.g., 14.14.14.14)는 기록해두록하자. 


### 서버 접속하기 

서버 설정이 끝났으므로 메일로 날아온 Private Key를 이용해서 서버를 접속해 보자. 
메일로 날아온 아래와 같은 키를 긁어서 kt-vpn.pem이라는 파일을 생성해주자. 

```
-----BEGIN RSA PRIVATE KEY-----
MIICXgIBAAKBgQCb/o59G1k0r1u3t1wm1LPd+rl+FX6ywwTFMIPS+KbsTrPekbWX
AoGAQ7G7896iX5KZ

...

+cJxEeVaEiW
HnTDV2UNdmCpnkjjh48z9n8mDp8r1oRBxczZgkG2yeVCqw==
-----END RSA PRIVATE KEY-----
```

본인의 취향에 맞게 putty, mobaXterm 등을 사용해서 ssh로 접속해 주면된다. 

> Session > SSH 

![image](https://user-images.githubusercontent.com/2586880/270100322-23a8b715-494a-48c5-a0a1-1625e68a7f67.png)
* Remote host: 생성된 VM의 공인 IP
* Use private key 활성화 해서 아까 저장한 kt-vpn.pem을 선택해 주면 됨
* username은 root로 하면 됨

맥 사용시에는 Terminal을 열어서 아래 명령어로 간단히 접속할 수 있다. 
```sh
ssh -i {private key file} root@{공인 IP}
```
//예제 (공인 IP = 14.14.14.14)
```sh
ssh -i kt-vpn.pem root@14.14.14.14
```

## DNS 등록

마지막으로 DNS (Domain Name Service) 설정까지 하도록 하자

### DNS 사용의 필요성

DNS는 꼭 필요한 것은 아니니 다음 chapter로 넘어가도 무방하다. 
다만 공인 IP 주소는 외우기가 힘들기 때문에, 하나쯤 만들어 두면, 편리하게 사용할 수 있다. 

### Duck DNS를 이용한 무료 DNS 서버 

[Duck DNS](https://www.duckdns.org/)에 가입한 후 아래 그림 같은 곳에 sub domain 이름을 적당히 정한 후 생성한다. 
(본 글에서 ktvpn.duckdns.org로 사용)
![image](https://user-images.githubusercontent.com/2586880/270111450-0116b5c0-dc58-4f22-909e-c684271fab84.png)

생성된 리스트에서, Current IP를 KT Cloud의 공인 IP로 변경 후 update ip 버튼을 눌러 적용한다. 

![image](https://github.com/wakenhole/wakenhole.github.io/assets/2586880/5dc8d091-69c0-4e51-9e19-93005bd339d6)

적용하고 나면 KT Cloud의 공인 IP 대신, 지정한 subdomain 주소로 접속이 가능하다.

```sh
ssh -i kt-vpn.pem root@ktvpn.duckdns.org
```

여기 까지 완료하면 VPN 서버를 구축하기 위한 VM 생성은 완료된 것이다. 
