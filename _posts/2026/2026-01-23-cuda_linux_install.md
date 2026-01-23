---
title: "[CUDA Study #1] CUDA 설치 (installation on Ubuntu)"
date: 2026-01-30 10:30:00 +0900
categories: [Tech, AI]
tags:
  - cuda
  - ubuntu
  - nvidia
  - nvcc
toc: true
toc_sticky: true
tagline: "AI"
image:
  path: https://upload.wikimedia.org/wikipedia/commons/b/b9/Nvidia_CUDA_Logo.jpg
---

CUDA 독학을 위한 환경 설정이다. 
삽질의 기록을 정리한다.

### OS 버전 확인

```sh
❯ cat /etc/os-release
```
```sh
PRETTY_NAME="Ubuntu 22.04.4 LTS"
NAME="Ubuntu"
VERSION_ID="22.04"
VERSION="22.04.4 LTS (Jammy Jellyfish)"
VERSION_CODENAME=jammy
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=jammy
```

### Nvidia 카드 확인 
```sh
❯ lspci | grep -i nvidia
```
```sh
04:00.0 3D controller: NVIDIA Corporation GP102GL [Tesla P40] (rev a1)
06:00.0 3D controller: NVIDIA Corporation GP102GL [Tesla P40] (rev a1)
```

{% include ad-inpost.html %}

### Driver 설치

```sh
> sudo apt install ubuntu-drivers-common

❯ sudo ubuntu-drivers devices
```
```sh
vendor   : NVIDIA Corporation
model    : GP102GL [Tesla P40]
manual_install: True
driver   : nvidia-driver-535 - distro non-free
driver   : nvidia-driver-545 - distro non-free
driver   : nvidia-driver-418-server - distro non-free
driver   : nvidia-driver-570 - distro non-free
driver   : nvidia-driver-570-server - distro non-free
driver   : nvidia-driver-535-server - distro non-free
driver   : nvidia-driver-580-server - distro non-free
driver   : nvidia-driver-390 - distro non-free
driver   : nvidia-driver-450-server - distro non-free
driver   : nvidia-driver-580 - distro non-free recommended
```

추천해주는 580 버전으로 설치한다. 

```sh
> sudo apt install nvidia-driver-580
> nvidia-smi
```
```sh
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 550.127.08             Driver Version: 550.127.08     CUDA Version: 12.4     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  Tesla P40                      Off |   00000000:04:00.0 Off |                  Off |
| N/A   21C    P8              9W /  250W |       0MiB /  24576MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
|   1  Tesla P40                      Off |   00000000:06:00.0 Off |                  Off |
| N/A   23C    P8              9W /  250W |       0MiB /  24576MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
|   2  Tesla P40                      Off |   00000000:07:00.0 Off |                  Off |
| N/A   24C    P0             50W /  250W |       0MiB /  24576MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
|   3  Tesla P40                      Off |   00000000:08:00.0 Off |                  Off |
| N/A   24C    P8             10W /  250W |       0MiB /  24576MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
|   4  Tesla P40                      Off |   00000000:0C:00.0 Off |                  Off |
| N/A   22C    P0             50W /  250W |       0MiB /  24576MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
|   5  Tesla P40                      Off |   00000000:0D:00.0 Off |                  Off |
| N/A   31C    P8              9W /  250W |       0MiB /  24576MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
|   6  Tesla P40                      Off |   00000000:0E:00.0 Off |                  Off |
| N/A   25C    P0             49W /  250W |       0MiB /  24576MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
|   7  Tesla P40                      Off |   00000000:0F:00.0 Off |                  Off |
| N/A   24C    P0             49W /  250W |       0MiB /  24576MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
```


### CUDA Toolkit 설치

```sh
wget https://developer.download.nvidia.com/compute/cuda/13.1.1/local_installers/cuda_13.1.1_590.48.01_linux.run
sudo sh cuda_13.1.1_590.48.01_linux.run
```
> 설치 패키지 목록 화면에서, Driver는 이미 설치 하였으므로 설치 하지 않는다 (드라이버 버전이 카드 모델과 안 맞을 수도 있음).
> cuda toolkit 버전과 driver 버전차이가 많이 나면, 안될 수도 있으니, 추후 실패하면 삭제하고 다시 낮은 버전으로 설치한다.

### PATH 추가

```sh
> vi ~/.bashrc
```
```sh
export PATH="/usr/local/cuda-13.1/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda-13.1/lib64:$LD_LIBRARY_PATH"
```

{% include ad-inpost.html %}

### nvcc 동작 확인

```sh
> nvcc --version
```
```sh
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2025 NVIDIA Corporation
Built on Tue_Dec_16_07:23:41_PM_PST_2025
Cuda compilation tools, release 13.1, V13.1.115
Build cuda_13.1.r13.1/compiler.37061995_0
```

### hello world 동작 수행


```cpp:test.cu
#include <stdio.h>
#include "cuda_runtime.h"
#include "device_launch_parameters.h"

__global__ void test01() {
    printf("the block ID is %d --- The thread ID is %\n", blockIdx.x, threadIdx.x);
}

int main () {
    printf("hellow world!\n");
    test01 <<<2, 32>>> ();
    cudaError_t err = cudaDeviceSynchronize();
    if (err != cudaSuccess) {
        printf("CUDA error: %s\n", cudaGetErrorString(err));
    }
    return 0;
}
```

{% include ad-inpost.html %}

#### build test 
```sh
> nvcc -o test test.cu
> ./test
```
```sh
hellow world!
the block ID is 0 --- The thread ID is 0
the block ID is 0 --- The thread ID is 1
the block ID is 0 --- The thread ID is 2
the block ID is 0 --- The thread ID is 3
the block ID is 0 --- The thread ID is 4
the block ID is 0 --- The thread ID is 5
the block ID is 0 --- The thread ID is 6
the block ID is 0 --- The thread ID is 7
the block ID is 0 --- The thread ID is 8
the block ID is 0 --- The thread ID is 9
the block ID is 0 --- The thread ID is 10
the block ID is 0 --- The thread ID is 11
the block ID is 0 --- The thread ID is 12
the block ID is 0 --- The thread ID is 13
the block ID is 0 --- The thread ID is 14
the block ID is 0 --- The thread ID is 15
the block ID is 0 --- The thread ID is 16
the block ID is 0 --- The thread ID is 17
the block ID is 0 --- The thread ID is 18
the block ID is 0 --- The thread ID is 19
....
```


---
**References:**
1. [CUDA Toolkit Installation]](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=22.04&target_type=runfile_local)
