---
title: "[CUDA Study #5] 행렬 곱셈(Matrix Multiplication) 최적화: Shared Memory와 Tiling 기법"
date: 2026-01-28 08:00:00 +0900
categories:
  - Tech
  - CUDA
tags:
  - CUDA
  - GPU Optimization
  - Shared Memory
  - Tiling
  - Matrix Multiplication
toc: true
toc_sticky: true
tagline: "Breaking the Memory Wall"
math: true
image:
  path: https://images.unsplash.com/photo-1550751827-4bd374c3f58b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80
---

딥러닝과 과학 연산의 핵심인 행렬 곱셈($C = A \times B$)은 연산 집약적인 작업인 동시에, 메모리 접근 효율에 따라 성능이 천차만별로 달라지는 작업입니다. 단순히 글로벌 메모리(Global Memory)만 사용해서 구현하면, GPU 연산 코어의 속도를 메모리 대역폭이 따라가지 못하는 **'Memory Wall'** 현상에 직면하게 됩니다.

오늘은 이를 극복하기 위해 GPU 내부의 고속 메모리인 **Shared Memory**를 활용한 **Tiling 기법**을 배우고, 실제 동작하는 전체 코드를 구현해 보겠습니다.

{% include ad-inpost.html %}

### 1. 왜 Shared Memory인가? (Global vs Shared)

GPU의 글로벌 메모리는 용량이 크지만 지연 시간(Latency)이 매우 깁니다. 반면, SM(Streaming Multiprocessor) 내부에 위치한 **Shared Memory**는 L1 캐시 수준의 속도를 자랑합니다.

행렬 곱셈에서 $C_{row, col}$ 하나의 원소를 계산하기 위해 $A$의 한 행과 $B$의 한 열을 읽어야 하는데, 이때 동일한 데이터가 여러 스레드에 의해 중복해서 읽힙니다. 이 중복된 데이터를 한 번만 글로벌 메모리에서 가져와 Shared Memory에 올려두고 공유하면, 비싼 메모리 접근 비용을 획기적으로 줄일 수 있습니다.

### 2. Tiling 기법의 핵심 원리

전체 행렬을 한꺼번에 처리하는 대신, **Tile(타일)**이라고 부르는 작은 블록 단위로 쪼개서 처리합니다.

1.  각 스레드 블록은 자신의 크기에 맞는 Tile 데이터를 글로벌 메모리에서 Shared Memory로 복사합니다.
2.  `__syncthreads()`를 호출하여 모든 스레드가 로딩을 마칠 때까지 기다립니다.
3.  Shared Memory에 로드된 작은 Tile들끼리 부분 곱셈 연산을 수행합니다.
4.  다음 Tile 영역으로 넘어가며 이 과정을 반복하여 최종 결과값을 누적합니다.

이를 통해 글로벌 메모리 접근 횟수를 Tile 크기 비율만큼 감소시킬 수 있습니다.

### 3. 전체 소스 코드 (Full Implementation)

이 코드는 $32 \times 32$ 크기의 Tile을 사용하여 행렬 곱셈을 수행합니다. 복사하여 바로 컴파일(`nvcc`) 후 실행이 가능합니다.

```cpp
#include <stdio.h>
#include <cuda_runtime.h>

#define N 1024       // 행렬의 크기 (N x N)
#define TILE_SIZE 32 // 타일 크기 (Warp 크기인 32와 맞춤)

// [Kernel] Shared Memory를 활용한 타일링 행렬 곱셈
__global__ void matrixMulTiled(float* A, float* B, float* C, int n) {
    // 공유 메모리 선언 (타일 크기만큼)
    __shared__ float s_A[TILE_SIZE][TILE_SIZE];
    __shared__ float s_B[TILE_SIZE][TILE_SIZE];

    int bx = blockIdx.x;  int by = blockIdx.y;
    int tx = threadIdx.x; int ty = threadIdx.y;

    // 결과 행렬 C의 행/열 인덱스 계산
    int row = by * TILE_SIZE + ty;
    int col = bx * TILE_SIZE + tx;

    float sum = 0.0f;

    // 타일 단위로 루프 수행
    for (int t = 0; t < (n / TILE_SIZE); ++t) {
        // 1. 글로벌 메모리에서 타일 데이터를 공유 메모리로 로드
        s_A[ty][tx] = A[row * n + (t * TILE_SIZE + tx)];
        s_B[ty][tx] = B[(t * TILE_SIZE + ty) * n + col];

        // 2. 모든 스레드가 로드를 마칠 때까지 대기 (Barrier Sync)
        __syncthreads();

        // 3. 공유 메모리에 로드된 타일 데이터를 이용해 부분 합 계산
        for (int k = 0; k < TILE_SIZE; ++k) {
            sum += s_A[ty][k] * s_B[k][tx];
        }

        // 4. 다음 타일 계산 전 동기화
        __syncthreads();
    }

    // 최종 결과 저장
    if (row < n && col < n) {
        C[row * n + col] = sum;
    }
}

int main() {
    int size = N * N * sizeof(float);
    float *h_A, *h_B, *h_C, *h_Verify;
    float *d_A, *d_B, *d_C;

    // Host 메모리 할당
    h_A = (float*)malloc(size);
    h_B = (float*)malloc(size);
    h_C = (float*)malloc(size);
    h_Verify = (float*)malloc(size);

    // 데이터 초기화
    for (int i = 0; i < N * N; i++) {
        h_A[i] = 1.0f;
        h_B[i] = 2.0f;
    }

    // Device 메모리 할당
    cudaMalloc(&d_A, size);
    cudaMalloc(&d_B, size);
    cudaMalloc(&d_C, size);

    // Host -> Device 데이터 복사
    cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, size, cudaMemcpyHostToDevice);

    // 커널 실행 구성 (2D Grid, 2D Block)
    dim3 threadsPerBlock(TILE_SIZE, TILE_SIZE);
    dim3 blocksPerGrid(N / TILE_SIZE, N / TILE_SIZE);

    printf("Executing Matrix Multiplication (N=%d, Tile=%d)...\n", N, TILE_SIZE);
    
    // 시간 측정을 위한 이벤트 등록
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);

    matrixMulTiled<<<blocksPerGrid, threadsPerBlock>>>(d_A, d_B, d_C, N);

    cudaEventRecord(stop);
    cudaEventSynchronize(stop);
    
    float milliseconds = 0;
    cudaEventElapsedTime(&milliseconds, start, stop);

    // 결과 복사 Device -> Host
    cudaMemcpy(h_C, d_C, size, cudaMemcpyDeviceToHost);

    // 검증 (CPU 연산과 비교 - 첫 번째 원소만 예시로 확인)
    printf("Sample Result: C[0] = %f (Expected: %f)\n", h_C[0], (float)N * 1.0f * 2.0f);
    printf("GPU Execution Time: %f ms\n", milliseconds);

    // 자원 해제
    cudaFree(d_A); cudaFree(d_B); cudaFree(d_C);
    free(h_A); free(h_B); free(h_C); free(h_Verify);

    return 0;
}
```

### 4. 기술 포인트 분석

이 코드의 성능 비결은 크게 세 가지로 요약할 수 있습니다.

| 기술 요소 | 설명 | 기대 효과 |
| :--- | :--- | :--- |
| **`__shared__` 메모리** | 각 블록의 L1 캐시 영역에 데이터를 수동으로 캐싱 | 글로벌 메모리 대역폭 소모 감소 |
| **`__syncthreads()`** | 블록 내 모든 스레드의 실행 지점을 일치시킴 | 데이터 로드 완료 보장 및 데이터 무결성 유지 |
| **Coalesced Access** | 인접한 스레드가 인접한 메모리 주소에 접근 | 하드웨어 레벨의 메모리 읽기 최적화 유도 |

특히 `__syncthreads()`는 Shared Memory를 사용할 때 필수적인 요소입니다. 만약 동기화 없이 연산을 시작하면, 특정 스레드는 아직 데이터 로딩이 끝나지 않은 메모리 값을 읽어 잘못된 결과값을 산출할 수 있기 때문입니다.

### 5. 마치며: 성능을 더 높이려면?

오늘 구현한 Tiling 기법은 Naive한 구현보다 수배에서 수십 배 빠른 성능을 보여줍니다. 하지만 여기서 더 나아가려면 **Bank Conflict**를 피하기 위한 메모리 정렬, **Loop Unrolling**, 또는 **Tensor Core**를 활용한 혼합 정밀도(Mixed Precision) 연산 등을 적용할 수 있습니다.

CUDA의 세계는 깊고 방대하지만, Shared Memory를 자유자재로 다룰 수 있게 된 지금 여러분은 이미 중급 개발자로 올라서는 문턱을 넘으셨습니다. 다음 시간에는 GPU 내부의 읽기 전용 고속 메모리인 **Constant Memory**와 **Texture Memory**의 활용법에 대해 알아보겠습니다.

---
**References:**
1. NVIDIA Programming Guide - Shared Memory.
2. CUDA C Programming - Performance Analysis for Matrix Multiplication.

{% include ad-inpost.html %}
