---
title: "Introduction To AVX"
categories:
  - AVX
tags:
  - SIMD
  - Programming
toc: true
toc_sticky: true
tagline: "Basic Chapter 1"
header:
  overlay_image: https://cdn.appuals.com/wp-content/uploads/2022/02/Intel-3rd-Gen-Xeon-Scalable-5-Custom-2060x1373-1.jpg
  overlay_filter: 0.5
  caption: "Photo credit: [**Unsplash**](https://unsplash.com)"
  actions:
    - label: "More Info"
      url: "https://unsplash.com"
  teaser: https://images.unsplash.com/photo-1498050108023-c5249f4df085?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1172&q=80
---

## Reference 
1. [SIMD basic](https://www.cs.cmu.edu/afs/cs/academic/class/15213-s19/www/lectures613/04-simd.pdf)
2. [Intel Instrinsics Guide](https://www.intel.com/content/www/us/en/docs/intrinsics-guide/index.html)

## Single Instruction Multiple Data(SIMD)

데이터 처리 속도를 높이기 위해 병렬처리 (Parallel processing) 기법을 많이 사용한다. 흔히 많이 알고 있는 방법은 CPU core level에서 
여러 multiple process or thread를 생성해서 multiple core를 동시에 (simultaneously) 활용하여 처리하는 방식이다. 
하지만 SIMD는 CPU core level 동작이 아닌 data level에서 병렬 처리를 위해 등장한 vectorize 기술로 여러 데이터에데서 반복적인 동일한 연산을 처리하는데 주로 사용된다.


![image](https://user-images.githubusercontent.com/2586880/202849587-f7b398be-7a9f-48c4-86bf-36220830f322.png)
{:.image-caption}
*Scalar*

![image](https://user-images.githubusercontent.com/2586880/202849607-9e44e4d8-3107-4dfa-808f-22b8100b53ba.png)
{:.image-caption}
*SIMD*

## Simple Example

실제로 구현 예제는 아래와 같다. 
32 bits integer 16개를 덧셈 연산하는 것이다. 
__m512i라는 변수는 512 bits (32*16)을 저장하고 있다고 보면된다. 
16개의 덧셈 동작을 한번에 처리 할 수 있으므로 연산속도가 약 16배 빨라진다고 생각할 수 있다.


 ```cpp
int A[16], B[16];
for (auto i : 16){
    A[i] = A[i] + B[i]; // 16 instrinsics are used
}
```
```cpp
__m512i A, B;
A = _mm512_add_epi16(A,B); // 1 instrinsic is used
```

