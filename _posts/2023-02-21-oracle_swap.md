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

## Oracle 클라우드 메모리 부족 문제

Oracle cloud의 경우 매우 매력적인 무로 VM서비스를 제공한다. 
대역폭 및 성능도 좋지만, 무엇보다도 평생 무제한 서비스가 매력적으로 느껴진다. 
하지만 x86 서버의 경우 메모리는 1GB만 무료로 제공한다. (ARM은 4G까지 무료)
Kubernetes 및 Visual Studio Code server 등을 돌리기에는 부족하고, 사용하다보면 SSH가 멈추거나 끊기는 문제가 발생한다. 
이를 해결하기 위해서 무료로 제공되는 50G volume storage에 일부 영역을 swap으로 지정해서 사용하면 이러한 문제를 해결할 수 있다. 


> 2GB swap 영역 생성하기
```sh
sudo fallocate -l 2G /swapfile
```
{: #code-example-1}
