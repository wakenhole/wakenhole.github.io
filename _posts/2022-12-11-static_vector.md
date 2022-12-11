---
title: "static_vector"
categories:
  - Programming
tags:
  - Optimization
  - C++
  - vector
toc: true
toc_sticky: true
tagline: "C++"
header:
  overlay_image: https://images.unsplash.com/photo-1625459201773-9b2386f53ca2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1630&q=80
  overlay_filter: 0.5
  caption: "[**Unsplash**](https://unsplash.com)"
  actions:
    - label: "More Info"
      url: "https://unsplash.com"
  teaser: https://images.unsplash.com/photo-1550439062-609e1531270e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80
---

## Reference
1. [Boost](https://www.boost.org/doc/libs/1_80_0/doc/html/boost/container/static_vector.html)
2. [Open standard](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0843r2.html)

## Overview 

To implement the time critical real time application, we have to avoid to allocate the memory dynamically. 
Especially, huge page expose applications to high latency variation. 
However, lots of modern standard library container, such as std::vector, std::map, std::list and so on, use dynamic memory allocation when resize its capacity. 

Therefore, dynamic-resizable sequence container with compile-time fixed capacity is required.
One of most popular one is boost:static_vector. 

## Member functions

* push_back(value) - Inserts an element at the end of the container.
* emplace_back(value) - Inserts an element at the end of the container(Faster than push_back).
* at(index) - Returns the element stored at the mentioned index.
* empty() - Returns  a Boolean value true if the vector is empty.
* begin() - Returns an iterator to the first element of the vector.
* end() - Returns an iterator to the end of the vector. It should be noted that it is the end of the container and not the last element.
* rbegin() - Returns an iterator to the first element of the  reversed vector. It reverses the vector and gives the last element as the first element.
* rend() - Returns an iterator to the end of the reversed vector.
* size() - Returns the no of elements in the vector.
* max_size() - Returns the largest possible size of the vector.
* shrink_to_fit () -  Tries to deallocate the excess memory allocated. The size of the vector remains unchanged but the memory allocated would have been reduced.
* insert(iterator, value) - Inserts the specified value at the position pointed by the iterator.
* emplace(iterator, value) - Inserts the specified value at the position pointed by the iterator.
* front() - Returns the first value of the container.
* back() - Returns the last value of the container.
* nth(position) - Returns an iterator to the mentioned position.
* index_of(iterator) - Returns the index of the position the iterator is pointing to.
* pop_back() - Removes the last element of the list

## Example
> https://godbolt.org/z/1G3vYohdz 

```cpp
#include <iostream>
#include<boost/container/static_vector.hpp>
using namespace std;

int main() {
  //Different ways of initializing the vector container
  boost::container::static_vector<int,8> v1;
  boost::container::static_vector<int,8> v2(5,1);
  boost::container::static_vector<int,8> v3{0,1,2,3,4};  
  std::cout<<"v1: max_size="<< v1.max_size() << ", capacity=" << v1.capacity() <<std::endl;
  std::cout<<"Is vector v1 empty "<< std::boolalpha << v1.empty() <<std::endl;
  std::cout<<"v1: current_size="<< v1.size() << ", capacity=" << v1.capacity() <<std::endl;
  //Inserting values into v1
  std::cout<<"Inserting elements into v1" << std::endl;
  v1.push_back(0);
  v1.push_back(1);
  v1.emplace_back(4);
  std::cout<<"v1: current_size="<< v1.size() << ", capacity=" << v1.capacity() <<std::endl;
  std::cout<<"v1 = [ ";
  for(int i:v1)
    std::cout<<i<<" ";
  std::cout<< "]" <<std::endl;

  std::cout<<"Inserting 2 and 3 at v1[2]" << std::endl;
  //Initializing an iterator to point to the position mentioned
  auto it=v1.nth(2);    
  v1.insert(it,3);
  v1.emplace(it,2);
  std::cout<<"v1 = [ ";
  for(int i:v1)
    std::cout<<i<<" ";
  std::cout<< "]" <<std::endl;

  std::cout<<"v2 = [ ";
  for(int i:v2)
    std::cout<<i<<" ";
  std::cout<< "]" <<std::endl;
  
  
  std::cout<<"v3 = [ ";
  for(int i:v3)
    std::cout<<i<<" ";
  std::cout<< "]" <<std::endl;  
  std::cout<<"Resize v3 with 5" << std::endl;
  v3.resize(8,5);
  std::cout<<"v3 = [ ";
  for(int i:v3)
    std::cout<<i<<" ";
  std::cout<< "]" <<std::endl;
  
  //Iterating through the vectors
  //Resizing vectors this size should be within the mentioned size
  v1.resize(8);
  std::cout<<"after resizing v1 = [ ";
  for(auto i = v1.begin();i!=v1.end();i++)
    std::cout<<*i<<"  ";
  std::cout<< "]" <<std::endl;

  std::cout<<"reverse order v3 =[ ";
  for(auto i = v3.rbegin();i!=v3.rend();i++)
    std::cout<<*i<<"  ";
  std::cout<< "]" <<std::endl;
  
  std::cout<<"The first element of vector v1 is "<<v1.front()<<std::endl;
  std::cout<<"The element at index 3 of vector v1 is "<<v1.at(3)<<std::endl;
  std::cout<<"The last element of vector v1 is "<<v1.back()<<std::endl;  
}
```


### Output
```
v1: max_size=8, capacity=8
Is vector v1 empty true
v1: current_size=0, capacity=8
Inserting elements into v1
v1: current_size=3, capacity=8
v1 = [ 0 1 4 ]
Inserting 2 and 3 at v1[2]
v1 = [ 0 1 2 3 4 ]
v2 = [ 1 1 1 1 1 ]
v3 = [ 0 1 2 3 4 ]
Resize v3 with 5
v3 = [ 0 1 2 3 4 5 5 5 ]
after resizing v1 = [ 0  1  2  3  4  0  0  0  ]
reverse order v3 =[ 5  5  5  4  3  2  1  0  ]
The first element of vector v1 is 0
The element at index 3 of vector v1 is 3
The last element of vector v1 is 0
``` 



