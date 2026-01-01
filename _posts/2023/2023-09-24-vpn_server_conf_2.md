---
title: "간단한 개인용 VPN 서버 구축의 모든것 2: VPN 서버 보안 설정 (V2Ray using X-UI)"
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

## 서버 업데이트
[1편](https://wakenhole.github.io/vpn/vpn_server_conf_1/)을 통해서 서버가 준비되면, 서버를 업데이트 하자. 

```sh
apt update && apt upgrade -y
```

```sh
apt install curl socat -y
```

## 서버 보안 설정
보안을 설정하는 이유는 여러가지가 있지만, 개인용으로 사용하는 VPN이다보니 개인정보에 대한 우려가 많이 있을 수 있다. 

또한 V2Ray client를 사용하다보면, 내 VPN서버 주소가 유출될 가능성이 높은데, 
외부 사용자가 침입해서 사용하는 것을 막는 것이 중요하다. 


## 서버 Password 설정
사실 [1편](https://wakenhole.github.io/vpn/vpn_server_conf_1/)에서 준비한 서버를 private키로만 접속을 하는것이 가장 안전하다. 

KT의 경우 default가 password로 접속이 가능하기 때문에, 아래 명령어를 통해서 복잡한 비밀번호로 변경할 수 있다.

```sh
sudo passwd
```


## 방화벽 해제
KT의 경우 VM Port 접속 설정할 경우 방화벽이 자동으로 등록되니 이 과정은 스킵해도 됩니다. 
{: .notice--info}

아래 명령어를 통해서 V2Ray를 위해 사용할 Port의 방화벽을 해제하도록 하자.

```
iptables -I INPUT 1 -p tcp --dport 3000 -j ACCEPT
iptables -I INPUT 1 -p tcp --dport 5000 -j ACCEPT
iptables -I INPUT 1 -p tcp --dport 80 -j ACCEPT
iptables -I INPUT 1 -p tcp --dport 443 -j ACCEPT
```


## SSL 환경 구축
우선 SSL환경을 구축하기 위한 Script를 다운로드 및 설치 한다. 

```sh
curl https://get.acme.sh | sh
```

```
~/.acme.sh/acme.sh --set-default-ca --server letsencrypt
```

무료 SSL 인증을 위해서 e-mail을 등록한다. xxxx@xxxx.com를 실제 e-mail로 변경후 명령어 입력 하면 된다. 

```
~/.acme.sh/acme.sh --register-account -m xxxx@xxxx.com
```


다음은 host name (ktvpn.duckdns.org) 을 등록한다.
```
~/.acme.sh/acme.sh --issue -d ktvpn.duckdns.org --standalone
```

아래와 같은 출력을 확인할 수 있다. 

```
Success
Verify finished, start to sign.
Lets finalize the order.
Le_OrderFinalize='https://acme-v02.api.letsencrypt.org/acme/finalize/1325....4816116'
Downloading cert.
Le_LinkCert='https://acme-v02.api.letsencrypt.org/acme/cert/0327ebc42....158'
Cert success.

....

Your cert is in: /root/.acme.sh/ktvpn.duckdns.org_ecc/ktvpn.duckdns.org.cer
Your cert key is in: /root/.acme.sh/ktvpn.duckdns.org_ecc/ktvpn.duckdns.org.key
The intermediate CA cert is in: /root/.acme.sh/ktvpn.duckdns.org_ecc/ca.cer
And the full chain certs is there: /root/.acme.sh/ktvpn.duckdns.org_ecc/fullchain.cer
```

마지막으로 생성된 key를 /root 폴더에 설치해주도록 한다.

```
~/.acme.sh/acme.sh --installcert -d ktvpn.duckdns.org --key-file /root/private.key --fullchain-file /root/cert.crt
```

![image](https://github.com/wakenhole/wakenhole.github.io/assets/2586880/e18cfa81-c065-4f93-88a9-d25c40f124f0)

