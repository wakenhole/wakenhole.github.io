---
title: "Chapter 2. AVX Notations"
categories:
  - AVX
tags:p
  - SIMD
  - Programming
  - Notations
toc: true
header:
  image: https://colfaxresearch.com/wp-content/uploads/2017/09/Skylake-AVX512-banner-NOCTA.png
  teaser: https://colfaxresearch.com/wp-content/uploads/2017/09/Skylake-AVX512-banner-NOCTA.png
---

### Reference 
1. [Crunching Numbers with AVX and AVX2](https://www.codeproject.com/Articles/874396/Crunching-Numbers-with-AVX-and-AVX)
   
AVX는 기존 C++ programming과는 다른 용어들이 많이 존재하기 때문에 이에 대해서 알아보자. 

## Data type naming rule
기본적인 정의 방법은 다음과 같이 표시한다. 
```
__<bit_width><data_type>
```
\<ddd\>는 bit수를 의미하며 128, 256, 512가 지원된다. 

\<s\>는 data type을 나타내며 i, d, empty가 있다. 
i는 integer type (bit수 무관), d는 double-precision 64 bit floating point, 비어있는 경우는 가장 기본인 single-precision 32 bit floating point 이다.
따라서 아래와 같은 조합이 가능하다.


| Data Type	| Description |
|----------:|:-------------|
| __m128  | 128-bit vector containing 4 floats |
| __m128d | 128-bit vector containing 2 doubles |
| __m128i | 128-bit vector containing integers |
| __m256	| 256-bit vector containing 8 floats |
| __m256d | 256-bit vector containing 4 doubles​ |
| __m256i | 256-bit vector containing integers |
| __m512	| 512-bit vector containing 16 floats |
| __m512d | 512-bit vector containing 8 doubles​ |
| __m512i | 512-bit vector containing integers |


## Instrinc naming rule
기본적인 정의 방법은 다음과 같이 표시한다. 

```
_mm<bit_width>_<operation>_<data_type>
```
이 포맷은 아래와 같이 구성된다. 
1. <bit_width>: return 되는 (때로는 사용되는) bit 수를 의미한다. 128인 경우는 해당 영역이 비어있다.
3. <operation>: 일종의 함수 이름으로 instrinsc operation을 나타낸다.
4. <data_type>: instrinsic의 primary argument의 데이터 타입이며, 대략적인 종류는 아래와 같다.

| Data Type	| Description |
|----------:|:-------------|
| ps | vectors contain single-precision packed data |
| pd | vectors contain double-precision packed data |
| epi8/epi16/epi32/epi64 | vectors contain 8/16/32/64 bits signed integers packed data |
| epu8/epu16/epu32/epu64 | vectors contain 8/16/32/64 bits unsigned integers packed data |
| si128/si256/si512 | unspecified 128/256/512 bits vector |

앞선 예제에서 살펴봤던 아래 구현은 16bit integer 32개를 add operation 한 후 512 bit vector를 return 하는 함수이다.
```cpp
__m512i A, B;
A = _mm512_add_epi16(A,B); // 1 instrinsic is used
```