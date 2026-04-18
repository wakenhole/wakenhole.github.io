---
title: "[CUDA Study #4] 벡터 덧셈(Vector Addition): CUDA 메모리 워크플로우와 글로벌 인덱싱"
date: 2026-01-28 06:00:00 +0900
categories:
  - Tech
  - CUDA
tags:
  - Parallel Computing
  - Vector Addition
  - GPU Programming
  - Memory Management
toc: true
toc_sticky: true
tagline: "Scalable Indexing in CUDA"
math: true
image:
  path: https://images.unsplash.com/photo-1518770660439-4636190af475?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80
---

이번 포스팅에서는 CUDA 프로그래밍의 기본 워크플로우를 벡터 덧셈(Vector Addition) 예제를 통해 살펴봅니다. 특히, 단일 블록과 멀티 블록 환경에서의 인덱싱 방식을 비교하며, 대규모 데이터 처리를 위한 글로벌 인덱스 계산법을 익히겠습니다.

CUDA 프로그래밍의 본질은 "수많은 스레드에게 어떻게 효율적으로 일감을 나눠주느냐"에 있습니다. 단순히 하나의 블록만 사용하는 수준을 넘어, 데이터의 크기에 맞춰 블록을 확장하고 각 스레드가 처리해야 할 정확한 데이터 위치를 계산하는 법을 익혀야 합니다.

이번 포스팅에서는 1,024개의 데이터를 처리하는 단일 블록 방식과, 2,048개의 데이터를 처리하는 멀티 블록 방식의 예제를 비교하며 CUDA 프로그래밍의 핵심 워크플로우를 정리합니다.

{% include ad-inpost.html %}

### 1. CUDA 프로그래밍의 4단계 워크플로우

GPU 연산을 수행하기 위해서는 Host(CPU)와 Device(GPU) 사이의 유기적인 협력이 필요합니다. 모든 CUDA 프로그램은 대개 다음의 4단계를 거칩니다.

1.  **메모리 할당 (Allocation):** CPU(`malloc`)와 GPU(`cudaMalloc`) 각각에 데이터를 저장할 공간을 확보합니다.
2.  **데이터 전송 (H2D Copy):** 연산을 위해 CPU의 데이터를 GPU 메모리로 복사합니다 (`cudaMemcpyHostToDevice`).
3.  **커널 실행 (Kernel Launch):** GPU 스레드들이 병렬로 연산을 수행합니다.
4.  **결과 회수 (D2H Copy):** 연산이 끝난 결과를 다시 CPU 메모리로 가져옵니다 (`cudaMemcpyDeviceToHost`).

### 2. Case 1: 단일 블록 기반의 벡터 덧셈 (SIZE = 1024)

첫 번째 예제는 1,024개의 정수를 더하는 코드입니다. 하나의 블록이 가질 수 있는 최대 스레드 수(보통 1,024개)를 꽉 채워 연산합니다.

```cpp
#define SIZE 1024

__global__ void vectorAdd(int* A, int* B, int* C, int n) {
    // 단일 블록이므로 threadIdx.x가 곧 데이터의 인덱스 i가 됩니다.
    int i = threadIdx.x;
    C[i] = A[i] + B[i];
}

int main() {
    // Step 1 Assign memory pointer
    int *A, *B, *C;
    int *d_A, *d_B, *d_C;
    int size = SIZE * sizeof(int);

    // Step 3 Allocate and initialize CPU memory
    A = (int*)malloc(size);
    B = (int*)malloc(size);
    C = (int*)malloc(size);

    // Step 2 Allocate and initialize GPU
    cudaMalloc((void**)&d_A, size);
    cudaMalloc((void**)&d_B, size);
    cudaMalloc((void**)&d_C, size);

    // Step 4 Assign values
    for (int i=0; i< SIZE; i++){
        A[i] = i;
        B[i] = SIZE-i;
    }

    // Step 5 Copy data from Host to Device
    cudaMemcpy(d_A, A, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, B, size, cudaMemcpyHostToDevice);
    
    // Step 6 Launch kernel with 1 block of 1024 threads
    vectorAdd <<<1, 1024>>> (d_A, d_B, d_C, SIZE);

    // Step 7 Copy result from Device to Host
    cudaMemcpy(C, d_C, size, cudaMemcpyDeviceToHost);

    // Step 8 Print results
    printf("End\n");
    for (int i = 0; i< SIZE; i++){
        printf("%d + %d = %d\n", A[i], B[i], C[i]);
    }

    // Step 9 Free memory
    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    free(A);
    free(B);
    free(C);
}
```

이 방식은 직관적이지만 명확한 한계가 있습니다. 하드웨어 사양에 따라 하나의 블록에 할당할 수 있는 스레드 수는 제한되어 있기 때문에, 처리해야 할 데이터가 1,024개를 넘어서면 이 코드는 정상적으로 동작하지 않습니다.

### 3. Case 2: 멀티 블록과 글로벌 인덱싱 (SIZE = 2048)

데이터가 늘어날 때는 **Grid(블록의 집합)**를 확장해야 합니다. 두 번째 예제는 2,048개의 데이터를 처리하기 위해 2개의 블록을 사용합니다. 이때 가장 중요한 개념이 바로 **글로벌 인덱스(Global Index)** 계산입니다.

#### 글로벌 인덱스 계산 공식
여러 블록에 흩어져 있는 스레드가 전체 데이터 중 자신의 위치를 찾으려면 다음과 같은 수식이 필요합니다.

$$i = threadIdx.x + (blockIdx.x \times blockDim.x)$$

* `threadIdx.x`: 현재 블록 내에서의 스레드 번호
* `blockIdx.x`: 현재 블록의 번호
* `blockDim.x`: 한 블록당 스레드 개수

```cpp
#define SIZE 2048

__global__ void vectorAdd(int* A, int* B, int* C, int n) {
    // 멀티 블록 환경에서의 글로벌 인덱스 계산
    int i = threadIdx.x + blockIdx.x * blockDim.x;
    
    // 데이터 범위를 벗어나지 않도록 방어 코드 추가 가능 (if i < n)
    C[i] = A[i] + B[i];
}

int main() {
    // ... GPU 메모리 할당 (cudaMalloc) ...

    // 2개의 블록, 각 블록당 1024개 스레드 (총 2048개)
    vectorAdd <<<2, 1024>>> (d_A, d_B, d_C, SIZE);

    // ... 결과 회수 및 메모리 해제 (cudaFree) ...
}
```

### 4. 코드 분석: 왜 멀티 블록인가?

단일 블록(`<<<1, 1024>>>`)과 멀티 블록(`<<<2, 1024>>>`)의 차이는 단순히 데이터 처리량에만 있지 않습니다.

| 구분 | 단일 블록 (1, 1024) | 멀티 블록 (2, 1024) |
| :--- | :--- | :--- |
| **최대 데이터** | 1,024개 (하드웨어 한계) | 이론상 무제한 (Grid 확장 가능) |
| **인덱싱** | `i = threadIdx.x` | `i = threadIdx.x + blockIdx.x * blockDim.x` |
| **병렬성** | 하나의 SM만 사용 가능성 높음 | 여러 SM에 블록을 분산하여 효율 극대화 |

스케일링이 가능한 코드를 짜기 위해서는 항상 **멀티 블록** 환경을 염두에 두어야 합니다. 데이터 사이즈(`N`)가 커질 때 `GridSize = (N + BlockSize - 1) / BlockSize`와 같은 공식을 사용하여 동적으로 블록 수를 결정하는 것이 실무적인 정석입니다.

### 5. 마치며: 메모리 해제의 중요성

예제 코드의 마지막 부분에는 `cudaFree()`와 `free()`가 꼼꼼하게 작성되어 있습니다. GPU 메모리는 한정된 자원이므로, 연산이 끝난 후 명시적으로 해제하지 않으면 **Memory Leak(메모리 누수)**이 발생하여 다음 프로그램을 실행할 때 메모리 부족 오류를 겪게 됩니다.

이제 여러분은 벡터 덧셈을 통해 CUDA의 기본적인 메모리 흐름과 인덱싱 체계를 마스터했습니다. 다음 포스팅에서는 대량의 데이터 연산 시 성능의 병목이 되는 **Memory Latency**를 줄이는 방법, `Shared Memory`에 대해 알아보겠습니다.

---
**References:**
1. NVIDIA CUDA C++ Programming Guide - Vector Addition Example.
2. CUDA Best Practices Guide - Scalable Indexing.

{% include ad-inpost.html %}

