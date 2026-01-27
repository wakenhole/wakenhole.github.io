---
title: "[CUDA Study #4] 실전 예제로 이해하는 Block, Thread, Warp의 계층 구조"
date: 2026-01-30 11:00:00 +0900
categories:
  - Tech
  - AI
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


```cpp
#include <stdio.h>
#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#define SIZE 1024

__global__ void vectorAdd(int* A, int* B, int* C, int n) {
    // warp is consist of 32 threads
    // if 128 threads / block, 4 warp / block (128/32)
    int i = threadIdx.x;
    C[i] = A[i] + B[i];
}

int main () {

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

    // Step 4
    for (int i=0; i< SIZE; i++){
        A[i] = i;
        B[i] = SIZE-i;
    }
    cudaMemcpy(d_A, A, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, B, size, cudaMemcpyHostToDevice);

    vectorAdd <<<1, 1024>>> (d_A, d_B, d_C, SIZE);
    cudaMemcpy(C, d_C, size, cudaMemcpyDeviceToHost);

    printf("End\n");
    for (int i = 0; i< SIZE; i++){
        printf("%d + %d = %d\n", A[i], B[i], C[i]);
    }

    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    free(A);
    free(B);
    free(C);
    return 0;
}
```


```cpp
#include <stdio.h>
#include "cuda_runtime.h"
#include "device_launch_parameters.h"

#define SIZE 2048

__global__ void vectorAdd(int* A, int* B, int* C, int n) {
    int i = threadIdx.x + blockIdx.x * blockDim.x;
    C[i] = A[i] + B[i];
}

int main () {

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

    // Step 4
    for (int i=0; i < SIZE; i++){
        A[i] = i;
        B[i] = SIZE-i;
    }
    cudaMemcpy(d_A, A, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, B, size, cudaMemcpyHostToDevice);

    vectorAdd <<<2, 1024>>> (d_A, d_B, d_C, SIZE);
    cudaMemcpy(C, d_C, size, cudaMemcpyDeviceToHost);

    printf("End\n");
    for (int i = 0; i < SIZE; i++){
        printf("%d + %d = %d\n", A[i], B[i], C[i]);
    }

    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    free(A);
    free(B);
    free(C);
    return 0;
}
```

