---
title: "Euler-Maclaurin Formula"
date: 2022-08-31T09:58:27-07:00
draft: false
toc: true
---

In the [math test post](/blog/binomial-poisson), we briefly discussed how to arrive at Stirling's approximation.
Here, we go deeper.

## Asymptotic Behavior of the Harmonic Series

Let's begin by understanding the asymptotic behavior of the harmonic series.
The harmonic series $H_n = \sum_{i=1}^n \frac 1 i$ can be estimated with an integral
$$
    \sum_{i=1}^n \frac 1 i \approx \int_1^n \frac 1 x dx = \ln n,
$$
with
$$
    \lim_{n \to \infty} (H_n - \ln n) = \gamma,
$$
where $\gamma$ ~ 0.57... is the [Euler-Mascherroni constant](https://en.wikipedia.org/wiki/Euler%27s_constant).

## Euler-Maclaurin Formula

We can get even more terms in this approximation with the [Euler-Maclaurin formula](https://en.wikipedia.org/wiki/Euler%E2%80%93Maclaurin_formula).
Let's look at the details of this formula.
Suppose we have a function $f: \R \to \R$ that is continuously differentiable $p$ many times on $[n, m]$.
Defining the quantities
\begin{align*}
    S & = \sum_{i=n}^m f(i) \\\
    I & = \int_n^m f(x) dx,
\end{align*}
we have
$$
    S - I = \sum_{k=1}^p \frac{B_k}{k!} \left( f^{(k-1)}(m) - f^{(k-1)}(n) \right) + R_p,
$$
where $B_k$ is the $k$th Bernoulli number (with $B_1 = \frac 1 2$) and $R_p$ is an error term depending on $n, m, f$, and $p$.

### Bernoulli Numbers

[Bernoulli numbers](https://en.wikipedia.org/wiki/Bernoulli_number) arise in many places.
An explicit definition is
$$
    B_n = \sum_{k=0}^n \sum_{v=0}^k (-1)^v {k \choose v} \frac{(v+1)^n}{k+1}.
$$
A recursive definition is
$$
    B_n = 1 - \sum_{k=}^{n-1} {n \choose k} \frac{B_k} {m - k +1}.
$$
A few terms of this sequence are
$$
    1, \frac 1 2, \frac 1 6, 0, -\frac 1{30}, 0, \frac 1 {42}, 0, \dots .
$$
Indeed, all the odd terms larger than 1 are zero.

The error term $R_p$ can be expressed as an integral of the periodized Bernoulli polynomials $P_k(x) \coloneqq B_k(x - \lfloor x \rfloor)$,
$$
    R_p = (-1)^{p+1} \int_n^m f^{(p)}(x) \frac{P_p(x)}{p!} dx.
$$

### Bernoulli Polynomials

The [Bernoulli polynomials](https://en.wikipedia.org/wiki/Bernoulli_polynomials) $B_k(x)$, in turn, are defined recursively via
\begin{align*}
    B\'\_k(x) & = k B_{k-1}(x), \\\
    \int_0^1 B_k(x) dx & = 0.
\end{align*}
An explicit formula is
$$
    B_n(x) = \sum_{i=0}^n \frac 1 {i+1} \sum_{k=0}^i (-1)^k {i \choose k} (x+k)^n.
$$

### Low-Order Terms of the Euler-Maclaurin Formula

Returning to the Euler-Maclaurin formula, we can write out a few low order terms
\begin{align*}
    \sum_{i=n}^m f(i) & = \int_n^m f(x) dx + \frac{f(n) + f(m)}2 + \int_n^m f\'(x) P_1(x) dx \\\
                      & = \int_n^m f(x) dx + \frac{f(n) + f(m)}2 + \frac 1 6 \frac{f\'(m) - f\'(n)}{2!} - \int_n^m f\'\'(x) \frac{P_2(x)}{2!} dx \\\
                      & = \int_n^m f(x) dx + \frac{f(n) + f(m)}2 + \frac 1 6 \frac{f\'(m) - f\'(n)}{2!} + \int_n^m f\'\'\'(x) \frac{P_3(x)}{3!} dx.
\end{align*}

### Darboux Formula

The [Darboux formula](https://mathworld.wolfram.com/DarbouxsFormula.html) seems like a neat generalization that unites Euler-Maclaurin and Taylor series and can be proved via integration by parts, but it's quickly getting too abstract for me.

## References

- And see a fuller derivation [here](https://math.stackexchange.com/questions/352733/reference-for-proof-of-harmonic-number-asymptotic-expansion?rq=1).
- [*An Elementary View of Euler's Summation Formula*, Apostol, T.](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.384.3289&rep=rep1&type=pdf) (PDF link)
- [*Concrete Mathematics*, Graham, Knuth, Patashnik](https://www.google.com/books/edition/Concrete_Mathematics/cjgPAQAAMAAJ?hl=en) ([PDF link](https://www.csie.ntu.edu.tw/~r97002/temp/Concrete%20Mathematics%202e.pdf))
