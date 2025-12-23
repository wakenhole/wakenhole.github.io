---
title: "Basic Chapter 6. Understanding Performance Metric"
categories: [Tech, Parallel Computing]
tags:
  - SIMD
  - AVX
  - Programming
  - Performance
toc: true
classes: wide
header:
  image: https://cdn.comparitech.com/wp-content/uploads/2018/11/Latency-vs-Throughput-.jpg
  teaser: https://cdn.comparitech.com/wp-content/uploads/2018/11/Latency-vs-Throughput-.jpg
---

## Reference
1. [Software Optimization Reference Manual](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html#optimization)
2. [Agner Fog's Guide](https://www.agner.org/optimize/)
3. [μops](https://uops.info/background.html)
4. [Pipeline Latency and Throughput](https://mediaspace.illinois.edu/media/t/1_j92uv9l2)

## Overview 

일반적으로 Software의 성능은 cache miss, IO bandwidth, bus bandwidth 등에 영향을 받지만 여기서는 그 이외의 부분에 대해서 논의 한다. 
이를 통해서 instruction sequence의 chain latency를 최소화 할수 있는 방법을 이해할 수 있다.

## Definition

가장 중요한 두 정의는 아래와 같다. 

### Latency

> The number of clock cycles that are required for the execution core to complete the execution of all of the μops that form an instruction.


하나의 instruction을 구성하는 μops들을 수행 완료를 하는데 걸리는 시간이다. 즉 피연산자가 준비된 시점 부터 결과 데이터 도출되는데 까지 걸리는 clock cycle 수를 말한다. 

일반적으로는 다른 instruction과의 경쟁이 없는 상태에서 측정된 것이다. 


### Throughput

> The number of clock cycles required to wait before the issue ports are free to accept the same instruction again. For many instructions, the throughput of an instruction can be significantly less than its latency.

Intel의 정의에 따르면, 하나의 instruction이 다시 수행을 하기 위해 필요한 clock cycle을 의미한다. 이는 흔히 Reciprocal throughput 정의를 따르는데 이는 CPU의 pipeline과 instruction level prallelism를 고려하기 위함이다. 
즉 


![image](https://user-images.githubusercontent.com/2586880/203658732-b7c12a92-fcb2-402b-8d56-4145b6bd7783.png)


* Instruction fetch (IF)
    * Get the next instruction.
* Instruction decode & register fetch (ID)
    * Decode the instruction and get the registers from the register file.
* Execution/effective address calculation (EX)
    * Perform the operation.
        * For load and stores, calculate the memory address (base + immed).
        * For branches, compare and calculate the branch destination.
* Memory access/branch completion (MEM)
    * For load and stores, perform the memory access.
    * For taken branches, update the program counter.
* Writeback (WB)
    * Write the result to the register file.
    * For stores and branches, do nothing.





### Port Usage

> We use the following notation for the port usage: 3*p015+1*p23, for example, denotes an instruction with four μops; three of these μops can each be executed on ports 0, 1, and 5, and one μop can be executed on ports 2 and 3. 


| Port Number | Main Purpose | Width |
|:--------|:-------:|--------:|
| 0 | FMA, general vector | 256-bit |
| 1 |  FMA, general vector |  256-bit | 
| 2 |  Load unit + addressing | 512-bit | 
| 3 |  Load unit + addressing | 512-bit | 
| 4 |  Store unit | 512-bit | 
| 5 |  Permute FMA, general vector | 512-bit | 
| 6 | + Addressing, scalar, branch | 64-bit | 