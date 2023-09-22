+++
title = "A Diversion Into Number Theory"
date = "2023-02-18T12:12:48-08:00"
toc = true
tags = [
    "math",
    "number theory"
]
+++

My good friend [Jordan](https://jasnyder.github.io/) and I are doing some recreational math together.
Here are some notes.

## Why is the multinomial coefficient always an integer?

From the combinatorial perspective, the answer is short and obvious.
But, dear reader, we here at Slow Math Friends, are into the long and arduous.
We're going to give an argument based on [Legendre's formula](https://en.wikipedia.org/wiki/Legendre%27s_formula).

**Theorem 1**: Legendre's formula gives the highest power of a prime $p$ dividing $n!$ by
$$\nu_p(n!) \coloneqq \sum_{i=1}^\infty \left\lfloor \frac n {p^i} \right\rfloor.$$

_Proof_: the proof is a straight-forward counting argument. In $\\{1, \dots, n\\}$, there are $\left\lfloor \frac n p \right\rfloor$ many numbers divisible by $p$.
Each of these contribute at least one power of $p$ to the factorial, but at first pass we count just one.
Then $\left\lfloor \frac n {p^2} \right\rfloor$ counts the numbers divisible by $p^2$.
Each of these contribute at least two powers of $p$ to the factorial, but we already counted one in the previous step, and at this step we only count one more.
We continue on this way, until all the powers of $p$ are counted.$\square$

**Theorem 2**: the multinomial coefficient ${n \choose a_1 a_2 \dots a_k}$ is always an integer.

_Proof_: we use Legendre's formula to show that the numerator has a higher prime power than the denominator, for any prime.
Using the intuitive inequality
$$\sum_{i=1}^k \lfloor x_i \rfloor \leq \left\lfloor \sum_{i=1}^k x_i \right\rfloor,$$
we have that
$$\sum_{i=1}^k \left\lfloor \frac {a_i} {p^j} \right\rfloor \leq \left\lfloor \frac n {p^j} \right\rfloor$$
(recalling that $a_1 + \dots + a_k = n$ in multinomial expressions).
Observing that $v_p(m!n!) = v_p(m!) + v_p(n!)$, we have that the max power of $p$ in the denominator of the multinomial
$$v_p(a_1!a_2!\cdots a_k!) = \sum_{i=1}^\infty \sum_{l=1}^k \left\lfloor \frac {a_i}{p^l} \right\rfloor \leq \sum_{l=1}^\infty \left\lfloor \frac n {p^l} \right\rfloor = v_p(n!),$$
which ends our proof.

## Why is the sum of the reciprocals of prime numbers divergent?

This is a classic result in number theory, going back to Euler.
We'll give a bounding argument due to [Ivan Niven](https://www.tandfonline.com/doi/abs/10.1080/00029890.1971.11992740) (which can be found in the more recent [_Euler: The Master of Us All_](https://bookstore.ams.org/dol-22/)).

**Theorem 3:** we have that
$$\sum_{p \leq n \text{ prime}} \frac 1 p > \log \log (n+1) - \log \frac {\pi^2} 6.$$

_Proof_: the outline of the proof is as follows
\begin{align}
\log(n+1) & < \sum_{i=1}^n \frac 1 i \\\
& \leq \prod_{p \leq n \text{ prime}} \left( 1 + \frac 1 p \right) \sum_{k=1}^n \frac 1 {k^2} \\\
& < \frac {\pi^2} 6 \prod_{p \leq n \text{ prime}} \exp \left( \frac 1 p \right) \\\
% & = \frac {\pi^2} 6 \exp \left( \sum\_{p \leq n \text{ prime}} \frac 1 p \right). \\\
\end{align}

Dividing through by $\pi^2/6$ and taking the log, gives the desired result.

The first inequality follows from the integral estimate for the harmonic series.

The second inequality follows from the fact that every integer $i$ can be written as a product of a square-free integer and a square, $i = (p_1 p_2 \cdots p_n) \cdot b^2$ (which follows from the fundamental theorem of arithmetic).
The first term in $(2)$ enumerates all the square-free integers and the second term enumerates all the squares.

The third inequality follows from the [Basel problem](https://en.wikipedia.org/wiki/Basel_problem) and the well known estimate $1 + x < \exp(x)$, which holds for $x > 0$.$\square$

Also, Euler's product formula because it's great.

**Theorem 4: Euler's product formula** gives a different representation of the Riemann zeta
$$\zeta(s) \coloneqq \sum_{n=1}^\infty \frac 1 {n^s} = \prod_{p \text{ prime}} \frac 1 {1 - \frac 1 {p^s}}.$$

_Proof_: Expanding the product on the right as a geometric series, we have
$$\prod_{p \text{ prime}} \frac 1 {1 - \frac 1 {p^s}} = \prod_{p \text{ prime}} \left( 1 + \frac 1 {p^s} + \frac 1 {p^{2s}} + \cdots \right).$$

Now we just need to note that each integer $n$ appears in the product on the left exactly once.
Indeed, by factoring $n=p_1^{j_1} p_2^{j_2} \cdots p_k^{j_k}$ (by the fundamental theorem of arithmetic), we see that this is exactly the term that comes from taking the product of the $j_1$th index of the sum of the first prime $p_1$, the $j_2$th index of the sum of the second prime $p_2$, and so on.

## Hex numbers

(From [_The Strong Law of Small Numbers_ by Richard Guy](https://en.wikipedia.org/wiki/Strong_law_of_small_numbers).)
[Hex numbers](https://en.wikipedia.org/wiki/Centered_hexagonal_number) are given by
$$H_n = 1 + 6 + \dots + 6n$$
Since $H_n = n^3 - (n-1)^3 = 3n(n-1) + 1$, the partial sums of $H_N$ are cubes.
You can see that each hexagonal number is the outer shell of a cube visually.

## The density of the primes compared to other common sequences

For a sequence $a_n$ defined by $a_n = f(n)$, we have the immediate relation that $f^{-1}(a_n) = n$.
For monotonically increasing integer sequences $a_n$, we can use this to get a count of sequence elements that are less than or equal to $n$.
We define the density of a sequence $a_n$ by
$$D(a_n) \coloneqq \frac{f^{-1}(a_n)} n$$
Here are a few examples
$$D(r^n) = \frac {\log_r n} n$$
$$D(n^r) = n^{\frac 1 r -1}$$
$$D(a + b n) = \frac{(n - a)} {b n}$$
$$D(p_n) = \frac {\pi(n)}n \sim \frac 1 {\log n}$$
where $p_n$ is the $n$th prime and $\pi(n)$ is the number of primes less than $N$.
Which demonstrates that the density of primes is just a little less than arithmetic and a bit more than geometric progression[^sequence-growth-rates].

## Future directions

- The [Euler characteristic](https://en.wikipedia.org/wiki/Euler_characteristic) $\chi$ for convex polyhedra is $2$, which satisfies the relation: $\chi = V - E + F$. At some point, we will prove this, in a simple case.

[^sequence-growth-rates]:
    A few useful sequence growth rates
    $$\lim_{n \to \infty} \frac {\log(n)^k} n \to 0, \forall k \geq 1$$
    $$\lim_{n \to \infty} \frac {\log(n)^{\log \log n}} n \to 0$$
    $$\lim_{n \to \infty} \frac{\log(n)^{\log(n)}} n \to \infty$$
