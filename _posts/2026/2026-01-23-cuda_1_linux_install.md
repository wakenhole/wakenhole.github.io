---
title: "[CUDA Study #1] 우분투(Ubuntu) CUDA 개발 환경 구축: 드라이버부터 Hello World까지"
date: 2026-01-23 10:30:00 +0900
categories: [Tech, CUDA]
tags:
  - CUDA
  - Ubuntu
  - NVIDIA
  - Environment Setup
  - Troubleshooting
toc: true
toc_sticky: true
tagline: "CUDA Learning"
math: true
image:
  path: https://upload.wikimedia.org/wikipedia/commons/b/b9/Nvidia_CUDA_Logo.jpg
---

딥러닝 모델 학습이나 고성능 병렬 처리를 위해 NVIDIA GPU를 사용한다면, **CUDA(Compute Unified Device Architecture)** 환경 설정은 피할 수 없는 통과의례입니다. 하지만 OS 버전, 드라이버 버전, 그리고 Toolkit 버전 간의 호환성 문제로 인해 설치 과정은 종종 '삽질'의 연속이 되곤 합니다.

오늘은 **Ubuntu 22.04 LTS** 환경에서 **Tesla P40** GPU를 기준으로, 드라이버 설치부터 CUDA Toolkit 12.8 세팅, 그리고 간단한 Hello World 예제 구동까지의 과정을 기록으로 남깁니다.

{% include ad-inpost.html %}

### 1. 시스템 환경 확인 (Pre-requisites)

설치에 앞서 현재 시스템의 OS 버전과 장착된 GPU 장치를 정확히 파악해야 합니다. 호환성 문제가 발생했을 때 가장 먼저 확인해야 할 지표이기 때문입니다.

#### OS 버전 확인
```sh
cat /etc/os-release
```
**[Result]** Ubuntu 22.04.4 LTS (Jammy Jellyfish)임을 확인했습니다.

#### GPU 장치 확인
시스템에 장착된 NVIDIA 장치를 리스트업 합니다.
```sh
lspci | grep -i nvidia
```
**[Result]** Tesla P40 (GP102GL) 카드가 정상적으로 인식되고 있습니다. 본 포스팅에서는 P40 8장이 꽂힌 서버를 기준으로 진행합니다.

### 2. NVIDIA 드라이버 설치

우분투에서는 `ubuntu-drivers-common` 패키지를 통해 시스템에 적합한 드라이버를 추천받을 수 있습니다.

**설치 가능한 드라이버 목록 조회:**
```sh
sudo apt install ubuntu-drivers-common
sudo ubuntu-drivers devices
```

출력된 리스트 중 `recommended` 태그가 붙은 버전을 설치하는 것이 일반적입니다. 하지만 최신 CUDA 버전(13.x)을 사용하기 위해 **nvidia-driver-580** 버전을 선택하여 설치를 진행했습니다.

```sh
# 드라이버 설치
sudo apt install nvidia-driver-580

# 설치 후 상태 확인 (재부팅 권장)
nvidia-smi
```

`nvidia-smi` 명령어가 정상적으로 실행되고, GPU 목록과 드라이버 버전(550.xx 이상)이 표기된다면 하드웨어 레벨의 준비는 끝난 것입니다.

> **Tip:** `nvidia-smi` 화면 우측 상단의 `CUDA Version: 13.0` 표기는 드라이버가 지원하는 최대 CUDA 버전을 의미하며, 실제 설치된 Toolkit 버전과는 다를 수 있습니다.

### 3. CUDA Toolkit 설치

이제 개발에 필요한 컴파일러와 라이브러리가 포함된 CUDA Toolkit을 설치합니다. 작성일 기준 최신 버전인 **CUDA 12.8.0**을 설치합니다.

**설치 파일 다운로드 및 실행:**
```sh
wget https://developer.download.nvidia.com/compute/cuda/12.8.0/local_installers/cuda_12.8.0_570.86.10_linux.run
sudo sh cuda_12.8.0_570.86.10_linux.run
```

#### ⚠️ 설치 시 주의사항
설치 스크립트 실행 후 나타나는 선택 화면에서 **Driver 항목의 체크를 해제([ ])** 해야 합니다.
* **이유:** 우리는 앞 단계(`apt`)에서 이미 시스템에 최적화된 드라이버를 설치했기 때문입니다. Toolkit에 포함된 드라이버를 덮어씌울 경우 충돌이 발생할 수 있습니다.

![Code Screen](https://images.unsplash.com/photo-1542831371-29b0f74f9713?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80)

### 4. 환경 변수 설정 (Environment Variables)

설치가 완료되었더라도 시스템이 `nvcc` 등의 명령어를 인식할 수 있도록 경로(PATH)를 지정해야 합니다.

`.bashrc` 파일을 열어 다음 내용을 하단에 추가합니다.

```sh
vi ~/.bashrc
```

```bash
# ~/.bashrc 하단에 추가
export PATH="/usr/local/cuda/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/cuda/lib64:$LD_LIBRARY_PATH"
```

저장 후 `source ~/.bashrc`를 실행하거나 터미널을 재시작하여 적용합니다.

**설치 확인:**
```sh
nvcc --version
```
위 명령 입력 시 `Cuda compilation tools, release 13.1` 메시지가 출력되면 성공입니다.

### 5. Hello World 실전 테스트

환경 설정이 제대로 되었는지 검증하기 위해, GPU 커널을 사용하는 간단한 C++ 코드를 작성하고 실행해 봅니다.

#### 소스 코드 작성 (`test.cu`)

```cpp:test.cu
#include <stdio.h>
#include "cuda_runtime.h"
#include "device_launch_parameters.h"

// GPU에서 실행될 커널 함수
__global__ void test01() {
    printf("Block ID: %d --- Thread ID: %d\n", blockIdx.x, threadIdx.x);
}

int main () {
    printf("Hello World! Starting CUDA Test...\n");
    
    // 2개의 블록, 각 블록당 32개의 스레드 실행 요청
    test01 <<<2, 32>>> ();
    
    // 디바이스 동기화 (GPU 작업이 끝날 때까지 대기)
    cudaError_t err = cudaDeviceSynchronize();
    
    if (err != cudaSuccess) {
        printf("CUDA error: %s\n", cudaGetErrorString(err));
    }
    
    return 0;
}
```

#### 컴파일 및 실행

`nvcc` 컴파일러를 사용하여 실행 파일을 생성합니다.

```sh
# 컴파일
nvcc -o test test.cu

# 실행
./test
```

**실행 결과:**
터미널에 `Hello World!` 메시지와 함께 0번부터 31번까지의 Thread ID가 Block 0과 Block 1에서 각각 출력된다면 모든 설정이 완벽하게 끝난 것입니다.

---

### 마치며

이제 기본적이고도 가장 중요한 환경 설정이 완료되었습니다. 이 과정은 새로운 서버를 세팅할 때마다 반복되므로, 본인의 환경에 맞는 버전을 잘 기록해두는 것이 좋습니다. 다음 포스팅에서는 본격적인 CUDA 프로그래밍 예제를 다뤄보겠습니다.

**References:**
1. [NVIDIA CUDA Toolkit Archive](https://developer.nvidia.com/cuda-downloads)

{% include ad-inpost.html %}