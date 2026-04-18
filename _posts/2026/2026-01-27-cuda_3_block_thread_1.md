---
title: "[CUDA Study #3] CUDA 동작 구조 기본: Block, Thread, Warp의 계층 구조"
date: 2026-01-27 11:00:00 +0900
categories:
  - Tech
  - CUDA
tags:
  - CUDA
  - GPU Architecture
  - Thread Hierarchy
  - Warp
  - Programming
toc: true
toc_sticky: true
tagline: "Hands-on CUDA Architecture"
math: true
image:
  path: https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80
---

지난 포스팅에서 우리는 CUDA의 논리적 구조와 하드웨어 구조를 이론적으로 살펴보았습니다. 하지만 "하나의 블록이 하나의 SM에 할당된다"거나 "스레드들이 32개씩 묶여 Warp를 이룬다"는 개념은 코드로 직접 확인하기 전까지는 다소 추상적으로 느껴질 수 있습니다.

오늘은 실제 CUDA 커널 코드를 통해 **Block ID**, **Thread ID**, 그리고 계산된 **Warp ID**가 어떻게 상호작용하는지 증명해 보겠습니다.

{% include ad-inpost.html %}

### 1. 실전 예제 코드: 계층 구조 확인하기

아래 코드는 각 스레드가 자신이 속한 블록과 스레드의 번호를 출력하고, 이를 바탕으로 자신이 어떤 **Warp**에 속해 있는지 계산하여 보여주는 예제입니다.

```cpp
#include <stdio.h>
#include "cuda_runtime.h"
#include "device_launch_parameters.h"

// GPU에서 실행될 커널 함수
__global__ void test01() {
    // 1 Warp는 32개의 스레드로 구성되므로, threadIdx.x를 32로 나누면 Warp ID를 얻을 수 있습니다.
    int warp_ID = threadIdx.x / 32;
    
    printf("Block ID: %d --- Thread ID: %d --- Warp_ID: %d\n", 
           blockIdx.x, threadIdx.x, warp_ID);
}

int main () {
    printf("Hello World! Starting CUDA Test...\n");

    // [설정] 2개의 블록(Grid), 각 블록당 512개의 스레드(Block) 실행 요청
    // 이 설정에 따라 총 1024개의 스레드가 생성됩니다.
    test01 <<<2, 512>>> ();

    // 디바이스 동기화 (GPU 작업이 끝날 때까지 CPU는 대기)
    cudaError_t err = cudaDeviceSynchronize();

    if (err != cudaSuccess) {
        printf("CUDA error: %s\n", cudaGetErrorString(err));
    }

    return 0;
}
```

### 2. 코드 심층 분석: 논리에서 물리로의 전환

위 코드에서 주목해야 할 핵심 포인트는 세 가지입니다.

#### 1) 커널 실행 구성 (`<<<2, 512>>>`)
우리는 `Grid`를 2개의 `Block`으로, 각 `Block`을 512개의 `Thread`로 구성했습니다.
* **Total Threads:** $2 \times 512 = 1024$ 스레드
* **Hardware Mapping:** 이 설정에 따라 GPU 내부의 **스케줄러**는 2개의 블록을 가용한 **SM(Streaming Multiprocessor)**에 할당합니다. 만약 SM이 2개 이상이라면 각 블록은 서로 다른 SM에서 병렬로 실행될 수 있습니다.

#### 2) Warp ID의 계산 (`threadIdx.x / 32`)
NVIDIA GPU 아키텍처에서 하드웨어가 명령어를 내리는 최소 단위는 **Warp(32개 스레드의 묶음)**입니다. 
* 예제에서 블록 크기를 32로 설정했기 때문에, **하나의 블록은 정확히 16개의 Warp**가 됩니다.
* 만약 블록 크기를 64로 설정했다면, 한 블록 내에서 `Warp_ID` 0번(스레드 0~31)과 1번(스레드 32~63)이 존재하게 됩니다.

#### 3) `blockIdx`와 `threadIdx`
이 변수들은 CUDA 런타임이 제공하는 내장 변수로, 수많은 병렬 스레드 중에서 **"현재 이 코드를 실행 중인 나"**가 누구인지 식별하게 해줍니다.

![GPU Microarchitecture](https://images.unsplash.com/photo-1591405351990-4726e331f141?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80)

### 3. 실행 결과 시뮬레이션 및 관계도

위 코드를 실행하면 다음과 같은 형태의 출력을 얻게 됩니다. (순서는 GPU 스케줄링에 따라 달라질 수 있습니다.)

| 실행 단위 | Block ID | Thread ID | Warp ID (Calculated) | 설명 |
|:---:|:---:|:---:|:---:|:---|
| Block 0 | 0 | 0 ~ 31 | 0 | 블록 0번 내의 첫 번째 워프 |
| Block 1 | 1 | 0 ~ 31 | 0 | 블록 1번 내의 첫 번째 워프 |
| Block 0 | 0 | 32 ~ 63 | 1 | 블록 0번 내의 두 번째 워프 |
| Block 1 | 1 | 32 ~ 63 | 1 | 블록 1번 내의 두 번째 워프 |

#### 핵심 개념 정리
1.  **Thread:** 개별 데이터를 처리하는 최하위 실행 단위입니다.
2.  **Warp:** 하드웨어(SM)가 명령어를 한 번에 던지는 32개 스레드의 집합입니다. 
3.  **Block:** 공유 메모리를 공유할 수 있는 스레드들의 논리적 그룹입니다. 하나의 블록은 반드시 하나의 SM에 통째로 들어갑니다.

### 4. 성능 최적화를 위한 통찰

이 예제를 통해 우리는 왜 **Block Size를 32의 배수**로 잡아야 하는지 명확히 이해할 수 있습니다. 
만약 블록 사이즈를 48로 잡는다면 어떻게 될까요?
* 첫 번째 Warp: 32개 스레드가 가득 참 (Full Efficiency)
* 두 번째 Warp: 16개 스레드만 사용하고 나머지 16개는 유휴 상태 (50% Efficiency)
결국 하드웨어 자원을 낭비하게 됩니다. 따라서 숙련된 CUDA 개발자는 항상 **Warp의 크기(32)**를 염두에 두고 자원을 할당합니다.

### 5. 마치며

제공된 예제 코드는 단순해 보이지만, CUDA 아키텍처의 근간을 관통하는 중요한 원리를 담고 있습니다. `threadIdx.x / 32`라는 연산 하나가 소프트웨어적 인덱스를 하드웨어적 실행 단위로 연결해 주는 가교 역할을 하기 때문입니다.

---
**References:**
1. NVIDIA CUDA C++ Programming Guide - Thread Hierarchy.
2. Professional CUDA C Programming (John Cheng et al.).

{% include ad-inpost.html %}
