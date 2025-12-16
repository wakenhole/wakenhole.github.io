---
title: "[IB Math] Applications of Integration: Finding the Volume of Revolution (Washer Method Problem Walkthrough)"
date: 2025-12-15 09:00:00 +0900
categories: [IB]
tags: [Math, Calculus, Volume of Revolution, Washer Method, Integration]
use_math: true
toc: true
toc_sticky: true
tagline: "Study"
header:
  overlay_image: https://isa.edu.gr/uploads/images/5953b0b961e2a/ODRAT50.jpg
  overlay_filter: 0.5
  caption: "[**Unsplash**](https://unsplash.com)"
  teaser: https://ibstudies.com/wp-content/uploads/2015/12/IB-maths-Tutor-in-gurgaon.png
---

## Introduction

In the IB Math (Calculus) curriculum, one type of problem that students often find tricky is finding the **Volume of Revolution**. Particularly when two or more graphs appear, and the region being rotated is separated from the axis of rotation, you must use the **Washer Method** (where the center is hollowed out like a donut) rather than the simple Disk Method.

Today, through a problem involving rotating a region where a trigonometric function meets a straight line around the $x$-axis, we will review everything together, from **setting up the integration interval** to applying **integration by parts**.

---

## 1. Problem

As shown in the figure below, there is a closed region $S$ enclosed between the curve $y = x + 2\cos x$ ($0 \le x \le 2\pi$) and the line $y = x$.

![Problem Image](https://github.com/user-attachments/assets/c2c6feea-42bc-4aa8-8a0a-3c39e6edfcfd){: width="500px"}

**Problem:**
Find the volume $V$ of the solid generated when the region $S$ is rotated by $2\pi$ about the $x$-axis.

> **(a)** Find the coordinates of the points where the two graphs meet.
> 
> **(b)** (i) Write down an integral that represents the volume $V$. (ii) Find the value of the volume $V$.

---

## 2. Key Concepts

Here are the mathematical tools needed to solve this problem.

### 1) Washer Method
This is the formula used when the cross-section of the solid of revolution is in the shape of a washer (a disk with a hole in it). You subtract the area of the inner circle from the area of the outer circle.

$$V = \pi \int_{a}^{b} \left( [R(x)]^2 - [r(x)]^2 \right) dx$$

* **$R(x)$ (Outer Radius):** The function that is **farther** from the axis of rotation (the $x$-axis).
* **$r(x)$ (Inner Radius):** The function that is **closer** to the axis of rotation (the $x$-axis).

### 2) Integration Techniques
* **Integration by Parts:** Used to solve forms like $\int x \cos x \, dx$. ($\int u dv = uv - \int v du$)
* **Half-angle Identity:** Used when integrating $\cos^2 x$. ($\cos^2 x = \frac{1+\cos 2x}{2}$)

---

## 3. Solution

### Step 1: Find Integration Interval (Intersection Points) (Part a)

To find the points where the two graphs meet, set the equations equal to each other.

$$x + 2\cos x = x$$
$$2\cos x = 0 \quad \Rightarrow \quad \cos x = 0$$

Within the given range $0 \le x \le 2\pi$, the values where cosine becomes 0 are:

> **$x$-coordinates of intersection (Integration Interval):** $x = \frac{\pi}{2}, \quad x = \frac{3\pi}{2}$

<br>

### Step 2: Set up the Integral (Part b-i)

In the interval $\frac{\pi}{2} < x < \frac{3\pi}{2}$, the value of $\cos x$ is **negative (-)**.
Therefore, $x + 2\cos x$ is smaller than $x$, so the positional relationship of the graphs is as follows:

* **Upper (Outer, $R$):** $y = x$
* **Lower (Inner, $r$):** $y = x + 2\cos x$

Substitute these into the volume formula:

$$V = \pi \int_{\frac{\pi}{2}}^{\frac{3\pi}{2}} \left( (x)^2 - (x + 2\cos x)^2 \right) dx$$

<br>

### Step 3: Calculate the Volume (Part b-ii)

#### 1. Simplify the Integrand
Expand the expression inside the brackets to simplify it.

$$x^2 - (x + 2\cos x)^2$$
$$= x^2 - (x^2 + 4x\cos x + 4\cos^2 x)$$
$$= -4x\cos x - 4\cos^2 x$$

If we factor out the constant $-4$, the expression to integrate is:
$$V = -4\pi \int_{\frac{\pi}{2}}^{\frac{3\pi}{2}} (x\cos x + \cos^2 x) \, dx$$

#### 2. Calculate the Integral
It is best to split this integral into two parts (**A** and **B**) for calculation.

**(A) $\int x\cos x \, dx$ (Integration by Parts)**
Set $u = x$ and $dv = \cos x \, dx$. Then $du = dx$ and $v = \sin x$.
$$\int x\cos x \, dx = x\sin x - \int \sin x \, dx = x\sin x + \cos x$$
Applying the bounds $[\frac{\pi}{2}, \frac{3\pi}{2}]$:
$$\left[ x\sin x + \cos x \right]_{\frac{\pi}{2}}^{\frac{3\pi}{2}} = \left(-\frac{3\pi}{2} + 0\right) - \left(\frac{\pi}{2} + 0\right) = -2\pi$$

**(B) $\int \cos^2 x \, dx$ (Half-angle Identity)**
$$\int \frac{1 + \cos 2x}{2} \, dx = \frac{1}{2}x + \frac{1}{4}\sin 2x$$
Applying the bounds $[\frac{\pi}{2}, \frac{3\pi}{2}]$:
$$\left[ \frac{1}{2}x + \frac{1}{4}\sin 2x \right]_{\frac{\pi}{2}}^{\frac{3\pi}{2}} = \left(\frac{3\pi}{4} + 0\right) - \left(\frac{\pi}{4} + 0\right) = \frac{\pi}{2}$$

#### 3. Combine Final Results
Substitute the values obtained back into the original expression for volume.

$$V = -4\pi \times ((A) + (B))$$
$$V = -4\pi \times \left( -2\pi + \frac{\pi}{2} \right)$$
$$V = -4\pi \times \left( -\frac{3\pi}{2} \right)$$
$$\therefore V = 6\pi^2$$

---

## 4. Conclusion

The final answer to this problem is **$6\pi^2$**.

The most important point when solving this problem is to **grasp the upper/lower relationship of the graphs within the interval** so that you do not swap $R$ and $r$. Also, the key to the calculation is remembering to use the **half-angle identity** without panicking when a squared trigonometric term ($\cos^2 x$) appears.

If this was helpful, please leave a comment or a like! :)