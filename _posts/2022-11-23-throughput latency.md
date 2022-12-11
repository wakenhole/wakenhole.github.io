---
title: "Understanding Performance Metric"
categories:
  - AVX
tags:
  - SIMD
  - Programming
  - Performance
toc: true
toc_sticky: true
tagline: "Basic Chapter 3"
header:
  overlay_image: https://images.unsplash.com/photo-1498084393753-b411b2d26b34?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1632&q=80
  overlay_filter: 0.5
  caption: "[**Unsplash**](https://unsplash.com)"
  teaser: https://images.unsplash.com/photo-1498050108023-c5249f4df085?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1172&q=80
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

Intel의 정의에 따르면, 하나의 instruction이 다시 수행을 하기 위해 필요한 clock cycle을 의미한다. 이는 흔히 reciprocal throughput 정의를 따르는데 이는 CPU의 pipeline과 instruction level prallelism를 고려하기 위함이다. 
즉, CPU pipeline에서 같은 instruction을 다시 수행하기 위한 시간이 1 cycle이라고 할지라도, 동시에 2개가 수행될 수 있으면 throughput은 0.5 cycle이다.
예를 들면, _mm512_add_epi16 가 0.5 cycle throughput을 가진다. 


## Example

아래 그림은 latency와 cycle의 개념적인 의미를 보여준다. 

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

