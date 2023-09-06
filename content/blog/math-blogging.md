+++
title = "Math Blogging"
date = "2019-11-07"
tags = [
    "math",
    "blogging",
    "hugo"
]
+++

A few cute derivations to test math blogging with [Hugo](https://gohugo.io).

## Binomial Limit to Poisson

A basic fact about Binomial distributions is that they can be approximated by the Poisson distribution in a certain limit.
As is often the case in probability, you can show this with generating functions.
Here, however, we will show the pointwise limit of distributions.

First, let us recall a few definitions.
The Binomial variable $\text{Bi}(n, \frac \lambda n)$ has the probability mass function (pmf)

$$
    p_B\left \(k; n, \frac \lambda n \right \) = {n \choose k} \left(\frac \lambda n \right)^k \left(1 - \frac \lambda n \right)^{n-k},
$$

while the Poisson variable $\text{Po}(\lambda)$ has the pmf

$$
    p_P (k; \lambda ) = e^{-\lambda} \frac{\lambda^k}{k!}.
$$

**Theorem 1:** The sequence of random variables $\\{ X_n \\}_{i=1}^\infty$ with $X_n \sim \text{Bi}(n, \frac \lambda n)$ limits in distribution to $\text{Po}(\lambda)$ as $n \to \infty$.

_Proof:_ We want to show that for a fixed $k$

$$
    \lim_{n \to \infty} \underbrace{{n \choose k} \left(\frac \lambda n \right)^k \left(1 - \frac \lambda n \right)^{n-k}}\_{\text{Binomial pmf}} = \underbrace{e^{-\lambda} \frac{\lambda^k}{k!}}\_{\text{Poisson pmf}}
$$

The limit

$$
    \lambda^k \left(1 - \frac \lambda n \right)^{n-k} \to e^{-\lambda} \lambda^k
$$

follows straight from one of the definitions of $e$[^1]

$$
    \lim_{n \to \infty} \left(1 + \frac \lambda n \right)^n = e^{\lambda}.
$$

The limit

$$
    {n \choose k} \frac 1 {n^k} \to \frac 1 {k!}
$$

can be shown by a laborious Stirling's approximation, but it is really enough to note the following[^2]

$$
    1 = \frac{n^k}{n^k} \geq \frac{ n^{\underline k} } { n^k } \geq \frac{(n-k+1)^k}{n^k} \overset{n \to \infty}{\to} 1.
$$

Putting the two limits together gives us our result. $\Box$

## Deriving Stirling's Formula

So I've used [Stirling's formula](https://en.wikipedia.org/wiki/Stirling%27s_approximation) maybe twenty times, but now I realize I've never seen a proof.
How do we derive it though?

**Theorem 2:** We have that $n! \sim \sqrt{2\pi n} \left( \frac n e \right)^n$ asymptotically (the ratio tends to 1 as $n \to \infty$).

_Proof sketch:_

\begin{align}
n! & = \int_0^\infty x^n e^{-x} dx & \tag{Definition} \\\
 & = \int_0^\infty e^{n \ln x - x} dx & \tag{Algebra} \\\
 & = e^{n \ln n} n \int_0^\infty e^{n (\ln y - x)} dy & \tag{Change of Variables} \\\
 & \sim \sqrt{\frac{2\pi} n} e^{-n} n e^{n \ln n} & \tag{Laplace's Method}
\end{align}

This gives us the relation we want $\Box$.

Laplace's method refers to the following statement.

**Theorem 3:** Suppose that:

- $f: [a, b] \to \R$ is twice differentiable on $[a,b]$
- $f(x)$ attains a unique maximum on $[a, b]$ at $x_0$
- $f''(x_0)<0$.

Then

$$
    \int_a^b e^{nf(x)} dx \sim e^{nf(x_0)} \sqrt{\frac{2\pi}{-nf''(x_0)}}
$$

as $n \to \infty$.

We will not prove this one, but refer you [here](https://en.wikipedia.org/wiki/Laplace%27s_method#Formal_statement_and_proof).[^4]

A few more Stirling approximation facts:

- you can get even more terms in the asymptotic expansion[^3] by using the [Euler-Maclaurin formula](https://en.wikipedia.org/wiki/Euler%E2%80%93Maclaurin_formula),
- a simple bound of $\sqrt{2\pi n} \left( \frac n e \right)^n e^{\frac 1 {12n + 1}} < n! < \sqrt{2\pi n} \left( \frac n e \right)^n e^{\frac 1 {12n}}$ is available due to [Robbins](https://www.jstor.org/stable/2308012).

{{< figure src="/images/pumps2019.jpg" height="400px" width="600px" caption="A bonus test picture." >}}

## Footnotes

[^1]:
    One way to show this definition is to take logs, Taylor expand, and rely on the continuity of $e^x$:
    $$n \log \left(1 + \frac \lambda n \right) = n \left( \frac \lambda n + O\left(\frac \lambda n\right)^2 \right) \to \lambda.$$

[^2]:
    Here we use the _[falling factorial](https://en.wikipedia.org/wiki/Falling_and_rising_factorials)_ notation:
    $$n^{\underline k} \coloneqq n (n-1) \cdots (n-(k-1)) = \frac{n!}{(n-k)!}.$$

[^3]: [NIST DLMF](https://dlmf.nist.gov/) is a useful reference for [asymptotic expansion](https://en.wikipedia.org/wiki/Asymptotic_expansion) (see e.g. the Gamma function chapter).
[^4]:
    By the way, [footnotes can be multi-line](https://michelf.ca/projects/php-markdown/extra/#footnotes).
    For more information on the Markdown parser used by hugo, see the [Goldmark repo](https://github.com/yuin/goldmark).
    [Here](https://gohugo.io/getting-started/configuration-markup) are the default settings used by Hugo.
