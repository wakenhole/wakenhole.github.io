---
title: "Undefined Behavior"
categories:
  - Compiler
tags:
  - Optimization
  - LLVM
toc: true
header:
  image: https://2.bp.blogspot.com/-uilL1GOdl0E/WrVbVxsAxHI/AAAAAAAAAoU/oDi-ww1rx8I-xlHhmFHtUiLK_FgCUVajQCLcBGAs/s1600/DragonPony.png
  teaser: https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTs942VryGg2sW4OTDaVuHRbOqzK1bOBeeyEw&usqp=CAU
---


# Undefined behavior (UB)

Complier는 최적화를 위해서 다양한 기법을 적용하는데, 이 결과로 기대한 결과와 다른 결과가 나올 수가 있다. 이러한 프로그램은 잘못 짠 프로그램으로 간주하고 compiler는 특별한 행동을 할 필요는 없다.
## overflow
Singed overflow 문제로, compiler는 x+1 > x를 비교해서 return 하는 것이 아니라 그냥 true를 return 한다.
```cpp
int foo(int x) {
    return x+1 > x; // either true or UB due to signed overflow
}
```
```asm
foo(int):                                # @foo(int)
        movl    $1, %eax
        retq
```

Pointer arithmetic overflow 문제로, compiler는 p+a & p+b를 비교하는 것이 아니라 a와 b만 비교한다. 
gcc와 llvm의 차이가 있지만, 결과는 같다.
```cpp
int overflow(int*p, int a, int b) {
   return (p + a >  p + b ? a : b);
}
overflow((int*)0xffffffff, 1, 0);
```

```assembly
.clang
overflow(int*, int, int):                            # @overflow(int*, int, int)
        movl    %edx, %eax
        cmpl    %edx, %esi
        cmovgel %esi, %eax
        retq
.gcc
test(int*, int, int):
        movslq  %esi, %rsi
        movslq  %edx, %rcx
        movq    %rsi, %rax
        salq    $2, %rcx
        salq    $2, %rsi
        cmpq    %rcx, %rsi
        cmovle  %edx, %eax
        ret
```

## Poison value: Deferred UB
p가 0xFFFFFFFF 일지라도 n=0이라면 문제가 없는 코드이다.
하지만 아래 코드와 같이 최적화를 할경우 undefined behavior가 발생한다. 
따라서 이런 당장 발생하지 않는 변수에 대해서 poision value라고 하고 eventually undefined behavior를 발생시킬 수 있다.

```cpp
int n = 0;
for (auto i = 0; i < n; ++i){
  a[i] = p + 0x1;
}
```
```cpp
// optimized
int n = 0;
auto temp = p + 0x1;
for (auto i = 0; i < n; ++i){
  a[i] = temp;
}
```