+++
title = "Fast Algorithms for $\\pi$ and Elliptic Integrals"
date = "2023-03-05T14:04:04-08:00"
toc = true
tags = [
	"math",
	"number theory"
]
math = true
+++

On this installment of Chill Math Friends, we learned a bit about a fast algorithm for $\pi$ and elliptic integrals.

## Gauss-Legendre Algorithm

Let's start by diving into the [Gauss-Legendre algorithm](https://en.wikipedia.org/wiki/Gauss%E2%80%93Legendre_algorithm). The algorithm is:

1. Start with $a_0=1, b_0=\frac 1 {\sqrt 2}$
2. Repeat the following until desired accuracy \begin{align*}
   a_{n+1} & = \frac{a_n + b_n} 2 \\\
    b_{n+1} & = \sqrt{a_n b_n} \\\
    t_{n+1} & = 1 - 2 \cdot \sum_{j=1}^n 2^j (a_j^2 - b_j^2)^2
   \end{align*}
3. We then have an approximation $p_n$ of $\pi$ with $$p_n = \frac{(a_n + b_n)^2}{t_n}$$

This approximation is quadratic, in the sense that $|\pi - p_{n+1}| < 0.075 \cdot |\pi - p_n|^2$, so in just 25 iterations, it gives 45 million correct digits of $\pi$.

But why does it work? Secretly: elliptic integrals.

Let's get a little more intuition for the sequences above. First, note that the geometric mean $\sqrt{x \cdot y}$ and the arithmetic mean $\frac{x + y} 2$ for two positive reals $x \not = y$ satisfy
$$\sqrt{x\cdot y} < \frac{x + y}2$$
This can be seen via algebra:
$$0 < (x-y)^2 = x^2 - 2xy + y^2 = x^2 + 2xy + y^2 - 4xy = (x+y)^2 - 4xy$$
which gives $4xy < (x+y)^2$.

Next, let us generalize the sequence above so that $a_0 = a$ and $b_n = b$. We show that $a_n$ and $b_n$ converge monotonically to a common limit we label $\text{AGM}(a,b)$ ([arithmetic-geometric mean](https://en.wikipedia.org/wiki/Arithmetic%E2%80%93geometric_mean)), with $a_n$ decreasing monotonically to it and $b_n$ increasing monotonically to it.

First, note that by the AM-GM inequality above, $b_n < a_n$ for all $n$. This implies $b_{n+1} = \sqrt{a_n \cdot b_n} > \sqrt{b_n \cdot b_n} = b_n$ and $a_{n+1} = \frac{a_n + b_n} 2 < \frac{a_n + a_n} 2 = a_n$. Both sequences are bounded $b = b_0 \leq b_n < a_n \leq a_0 = a$, so they are convergent. Finally, the difference between the sequences limits to zero
\begin{align*}
a\_{n+1}^2 - b\_{n+1}^2 & = \left( \frac {a_n + b_n} 2 \right)^2 - a_n b_n = \frac{a_n^2 + 2_anb_n +b_n^2 -4a_nb_n}4 \\\
& = \frac{(a_n - b_n)^2} 4 = \frac{a_n - b_n}{4(a_n + b_n)} (a_n^2 - b_n^2) < \frac 1 4 (a_n^2 - b_n^2)
\end{align*}
which gives that $a_n^2 - b_n^2 = 4^{-n} (a^2 - b^2)$.

Next comes an integral out of nowhere
$$I(a, b) \coloneqq \int_0^{\pi /2 } \frac{d\theta} {\sqrt{a^2 \cos^2 \theta + b^2 \sin^2 \theta}}$$
but it turns out that it is invariant on the whole AGM sequence, that is $I(a_n, b_n) = I(a_0, b_0)$ for all $n$. It turns out further that, setting $m \coloneqq \text{AGM}(a,b)$,

$$I(a,b) = I(a_n, b_n) = \lim_{n \to \infty} I(a_n, b_n) = I(\lim_{n \to \infty} a_n, \lim_{n \to \infty} b_n) = I(m, m) = \frac{\pi}{2 \cdot m}$$

You can see the details in [this paper by Lorenz Milla](https://arxiv.org/abs/1907.04110), which can be followed with just calculus and algebra knowledge.
In the end, they derive an expression involving only $\pi$.

## Elliptic Integrals

Note that $I(a, b)$ can be written in the form below $K(n)$, which is the standard definition of an elliptic integral of the first kind
$$K(n) \coloneqq \int_0^{\pi/2} \frac 1{\sqrt{1 - n^2 \sin^2 \theta}} d\theta$$

Now you might wonder, what does this integral have to do with ellipses? And that connection isn't as direct as the elliptic integral of the second kind $E(n)$, which arises when calculating the arc length of an ellipse
$$E(n) = \int_0^{\pi/2} \sqrt{1 - n^2 \sin^2 \theta} d\theta$$

To see this, recall that the equation of an ellipse is $\frac {x^2}{a^2} + \frac{y^2}{b^2} = 1$. Using $x = a \cos \theta, y = b\sin \theta$, the formula for the arc length of a quarter of the ellipse is
\begin{align*}
L & = \int ds = \int \sqrt{dx^2 + dy^2} \\\
& = \int_0^{\pi / 2} \sqrt{a^2 \sin^2 \theta + b^2 \cos^2 \theta} d\theta \\\
& = b \int_0^{\pi / 2} \sqrt{1 - (1 - \frac{a^2}{b^2}) \sin^2 \theta} d\theta
\end{align*}
which has the same form as $E(n)$.

There is a long history to the theory of elliptic integrals, studied actively in the 18th and 19th centuries by Euler, Gauss, Legendre, Abel, and others. A lot of attention was dedicated to classifying the curves that give rise to these integrals (for example, see [this historical overview from 1896](https://www.cambridge.org/core/journals/proceedings-of-the-edinburgh-mathematical-society/article/on-the-geometrical-representation-of-elliptic-integrals-of-the-first-kind/50D34F10FCBDF68AED3DE8FB8113CF66)). It turns out that there are many curves in this class, such as the [lemniscate](https://en.wikipedia.org/wiki/Lemniscate), which satisfies
$$(x^2 + y^2)^2 - a^2(x^2 - y^2) = 0$$
This can also be parametrized with
\begin{align*}
x & = a \cos \theta \sqrt{1 - \frac 1 2 \sin^2 \theta} \\\
y & = \frac a {\sqrt 2} \sin \theta \cos \theta
\end{align*}
so
\begin{align*}
ds^2 & = dx^2 + dy^2 \\\
& = \frac{a^2 d\theta^2}{2(1 - \frac 1 2 \sin^2 \theta)} \\\
\implies s & = \frac a{\sqrt 2} \int_0^{\pi/2} \frac{d\theta}{\sqrt{1 - \frac 1 2 \sin^2 \theta}} = \frac a {\sqrt 2} K\left(\frac 1 {\sqrt 2}\right)
\end{align*}
