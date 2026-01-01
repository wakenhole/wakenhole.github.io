---
title: "간단한 개인용 VPN 서버 구축의 모든것 3: X-UI 설치 및 설정 (V2Ray using X-UI)"
categories: [Tech, Networking & VPN]
tags:
  - v2ray
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
image:
  overlay_image: https://images.unsplash.com/photo-1691435828932-911a7801adfb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3132&q=80
  overlay_filter: 0.5
  caption: "[**Unsplash**](https://unsplash.com)"
  path: https://images.unsplash.com/photo-1691435828932-911a7801adfb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=3132&q=80
---


## 전체 글 목록
1. [VPN용 VM 서버 구축](https://wakenhole.github.io/2023/vpn_server_conf_1/)
2. [VPN 서버 보안 설정](https://wakenhole.github.io/2023/vpn_server_conf_2/)
3. [X-UI 설치 및 설정](https://wakenhole.github.io/2023/vpn_server_conf_3/)
4. [Marzban VPN 설치](https://wakenhole.github.io/2025/new_vpn_server_conf_1/)
5. [Marzban VPN 설정](https://wakenhole.github.io/2025/new_vpn_server_conf_2/)


## Reference
1. [V2Ray](https://www.v2ray.com/)
2. [X-UI, a multi-user Xray graphical management panel](https://seakfind.github.io/2021/10/10/X-UI/)
3. [중국 외노자를 위한 VPS에 VPN 구축기 (V2ray with X-UI 제어콘솔)](https://www.clien.net/service/board/lecture/17799473)

## X-UI에 대해서 

X-IU는 사용하기 어려운 V2Ray Core를 Web GUI로 설정가능하게 해주는 도구이다. 
설치는 매우 쉬우니 따라해보도록 하자. 

## X-UI를 활용한 V2Ray 설치

### X-UI 다운로드 및 설치

```
bash <(curl -Ls https://raw.githubusercontent.com/vaxilu/x-ui/master/install.sh)
```

설치 하고 나면 중국어로 나오는데, **[y/n]** 선택에서 당황하지 말고 y를 누르면된다.




아래와 같이 V2Ray GUI 관리자 페이지의 설정을 하자.
1. 계정명 (임의)
2. 비밀번호 (임의)
3. 포트 번호 ([1편](https://wakenhole.github.io/vpn/vpn_server_conf_1/)에서 설정한 포트 번호)

![image](https://github.com/wakenhole/wakenhole.github.io/assets/2586880/2c6d5e3c-1d82-4470-a2aa-c4b6cbd1d49a)


### X-UI 설정

X-UI 설정을 해보자.
```
x-ui
```
15를 입력해서 bbr을 설정한다. (필수 아님)

사실 기본으로 사용해도 무관해서 굳이 설정 할 필요는 없다. 

기타 자세한 사용방법은 [X-UI](https://seakfind.github.io/2021/10/10/X-UI/) 설명되어 있으니 참고하자. 


### X-UI 구동

X-UI를 구동한다. 

```
x-ui start
```

중국어로 녹색 글자가 표시된다면 성공이다.

## X-UI GUI 관리자 모드

### X-UI GUI Web 접속
그럼 관리자 페이지를 브라우저로 접속해보자

반드시 처음에는 **http** 를 사용해서 설치시 설장한 포트 및 계정/비밀번호로 접속 가능하다.

> http://ktvpn.duckdns.org:5000/


![image](https://github.com/wakenhole/wakenhole.github.io/assets/2586880/c5d7875b-3314-4d3d-aa24-2a16d7853529)



### X-UI 관리자 모드 
접속하면 아래와 같은 페이지를 확인할 수 있다. 
중국어지만 간단하다. 
왼쪽 메뉴 5개 중 위에 부터 3개만 사용한다. 
1. 상태
2. 목록 (VPN 목록)
3. 설정
![image](https://github.com/wakenhole/wakenhole.github.io/assets/2586880/c3aba13a-e9fe-4319-973e-92f17afab6cc)


### X-UI GUI SSL 설정
본 관리자 화면 및 VPN을 암호화 설정하자. (중국 황금방패로 부터 지켜내기 위해)

아래 화면과 같이 [2편](https://wakenhole.github.io/vpn/vpn_server_conf_2/)에서 생성한 SSL Certification File을 설정한다.

마지막에 保存XX를 눌러서 저장한다. 

![image](https://github.com/wakenhole/wakenhole.github.io/assets/2586880/7f78a061-c248-429b-8c1a-e3782f98d8e0)

### X-UI 재시작
설정을 적용하기 위해 x-ui를 재시작 하자.
```
x-ui restart
```

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
