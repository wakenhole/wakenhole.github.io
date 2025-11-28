---
title: "Oracle Cloud Free Tier Memory 부족 문제 해결하기"
categories:
  - Cloud
tags:
  - Oracle 
  - Cloud
  - 오라클
  - 메모리
  - swap
toc: true
toc_sticky: true
tagline: "Oracle"
header:
  overlay_image: https://1330878074.rsc.cdn77.org/wp-content/uploads/2022/05/Oracle-Enhances-its-Comprehensive-Cloud-Security-Capabilities-with-Integrated-Threat-Management.jpg
  overlay_filter: 0.5
  caption: "[**Unsplash**](https://unsplash.com)"
  teaser: https://1330878074.rsc.cdn77.org/wp-content/uploads/2022/05/Oracle-Enhances-its-Comprehensive-Cloud-Security-Capabilities-with-Integrated-Threat-Management.jpg
---

{% include ad-inpost.html %}


## Oracle 클라우드 메모리 부족 문제

Oracle cloud의 경우 매우 매력적인 무로 VM서비스를 제공합니다. 
대역폭 및 성능도 좋지만, 무엇보다도 평생 무제한 서비스가 매력적입니다. 

하지만 x86 서버의 경우 메모리는 1GB만 무료로 제공하여 (ARM은 4G까지 무료),
Kubernetes 및 Visual Studio Code server 등을 돌리기에는 부족하고, 사용하다보면 SSH가 멈추거나 끊기는 문제가 발생합니다. 

이를 해결하기 위해서 무료로 제공되는 50G volume storage에 일부 영역을 swap으로 지정해서 사용하면 이러한 문제를 해결할 수 있습니다. 


### 2GB swap 영역 생성하기

```sh
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
```

아래와 같이 결과가 출력됩니다. 
```sh
Setting up swapspace version 1, size = 2 GiB (2147479552 bytes)
no label, UUID=7e7bbce4-e489-488c-a4db-6e7950aa727e
```


### swap 활성화
```sh
sudo swapon /swapfile
```

아래와 같이 swap space가 2GB 할당된 것을 확인할 수 있습니다. 
```sh
$ sudo swapon --show
NAME      TYPE SIZE USED PRIO
/swapfile file   2G   0B   -2
```
```sh
$ free -h
               total        used        free      shared  buff/cache   available
Mem:           965Mi       218Mi       249Mi       0.0Ki       497Mi       593Mi
Swap:          2.0Gi          0B       2.0Gi
```

### 재부팅 후 자동 설정
/etc/fstab 파일을 수정해 주시면 됩니다.

```sh
sudo vi /etc/fstab
```

해당파일을 열면 아래와 같은 내용이 있는데, 

```sh
LABEL=cloudimg-rootfs   /        ext4   discard,errors=remount-ro       0 1
LABEL=UEFI      /boot/efi       vfat    umask=0077      0 1
```


아래 처럼 한줄 추가해 주시면 됩니다. 

```sh
LABEL=cloudimg-rootfs   /        ext4   discard,errors=remount-ro       0 1
LABEL=UEFI      /boot/efi       vfat    umask=0077      0 1
/swapfile swap swap defaults 0 0
```

