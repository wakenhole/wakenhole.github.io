---
title: "Load and Store"
categories:
  - AVX
tags:
  - SIMD
  - Programming
  - Optimization
toc: true
toc_sticky: true
tagline: "Advanced Chapter 1"
header:
  overlay_image: https://images.unsplash.com/photo-1504376830547-506dedfe1fe9?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80
  overlay_filter: 0.5
  caption: "[**Unsplash**](https://unsplash.com)"
  actions:
    - label: "More Info"
      url: "https://unsplash.com"
  teaser: https://images.unsplash.com/photo-1605379399642-870262d3d051?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1206&q=80
---

## Register & Memory
AVX vectorize 구현시 가장 중요한 것은 Memory와 Register 관리 이다.
AVX 연산 자체는 빠르다고 하더라도, 이를 사용하기 위해서는 register에 load 해야 하고, 연산 후에 다시 memory에 저장해야 하기 때문이다. 


## Bad example

예를 들면 A[16]+B[16] 덧셈을 element-wise 하기 위한 아래 예제를 살펴보자. 

```cpp
int input_A[16];
int input_B[16];
int output[16];
__m512i A = _mm512_load_si512(input_A); // 8 cycle
__m512i B = _mm512_load_si512(input_B); // 8 cycle
__m512i C = _mm512_add_epi32(A,B);      // 1 cycle
_mm512_store_epi32(output_A, C);        // 5 cycle
```

언듯 보기에는 잘 구현된 코드이지만, 실제 각 instrinsic에서 소모되는 cycle은 아래와 같다. 

| | _mm512_load_si512 | _mm512_add_epi32 | _mm512_store_epi32 |
|:--:|:-----:|:--------:||:--------:|
|latency| 8 | 1 | 5 |
|throughput| 0.5 | 0.5 | 1 |


실제로 16개의 add 연산을 1 cycle에 처리한다고 하더라도 사용되는 cycle은 22 cycle이다. scalar level 연산을 1cycle이 가정하면 소모되는 16 cycle 보다 느리다는 의미이다. (scalar가 register load되는 시간 제외)
이 경우는 vectorize를 하지 않는 것이 오히려 바람직 할 수도 있다. 

## Good example

하지만 만약 A+B, A-B, B-A를 모두 구해야 하는 상황 이라면 아래와 같을 수 있다. 


```cpp
int input_A[16];
int input_B[16];
int ApB[16];
int AmB[16];
int BmA[16];
__m512i A = _mm512_load_si512(input_A); // 8 cycle
__m512i B = _mm512_load_si512(input_B); // 8 cycle
__m512i o1 = _mm512_add_epi32(A,B);      // 1 cycle
__m512i o2 = _mm512_sub_epi32(A,B);      // 1 cycle
__m512i o3 = _mm512_sub_epi32(B,A);      // 1 cycle
_mm512_store_epi32(ApB, o1);        // 5 cycle
_mm512_store_epi32(AmB, o2);        // 5 cycle
_mm512_store_epi32(BmA, o3);        // 5 cycle
```

사용되는 total 34 cycle로 scalar에서 소모될 것으로 예상되는 48 cycle 보다 빠르다는 것을 알 수 있다. 
즉 한번 load한 후 다중 연산을 할 수 있도록 구성하는 것이 중요하다. 