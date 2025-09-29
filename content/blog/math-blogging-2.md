+++
title = "A Few Facts About Fibonacci Numbers"
date = "2019-12-05T14:04:04-08:00"
# toc = true
tags = [
	"math",
	"number theory"
]
math = true
+++

More [math blog testing](/blog/math-blogging). From a number theory course I graded a few years ago.

## Fibonacci Numbers

__Definition 1.__ The Fibonacci numbers are defined by $f_0 = 0, f_1 = 1$ and the recursive relation
$$f_n \coloneqq f_{n-1} + f_{n-2}, \ \ n \geq 1.$$

__Definition 2.__ A divisor of an integer $m$ is an integer $d$ such that $\exists b \in \Z$ with $b d = m$. The set of all divisors of $m$ is denoted by $D_m \coloneqq \\{ b | bk = m,\ k, b \in \Z \\}$.

__Definition 3.__ The greatest common divisor of two integers $m,n$ is
$$\gcd(m,n) \coloneqq \max (D_m \cap D_n).$$

__Theorem 1.__ $\gcd(f_n,f_m) = f_{\gcd(n,m)}$.

__Lemma 1.__ $\gcd(m,n) = \gcd(m,n \pm m)$.

_Proof_. Clearly, any divisor of both $m,n$ also divides $n \pm m$, so $\gcd(m,n) \leq \gcd(m,n \pm m)$. On the other hand, if we have a divisor $d$ of both $m = db$ and $n \pm m = dc$, then $n = db \mp dc = d(b \mp c)$, hence $\gcd(m,n \pm m) \leq \gcd(m,n)$.

__Lemma 2.__ For $n > 0$, $\gcd(f_n,f_{n-1}) = 1$.

_Proof_. We proceed by induction. The base case $n=1,2$ are clearly true ($0,1,1,2,3$). Now suppose the proposition is true for $k > 1$. We then have
$$\gcd(f_{k+1},f_{k}) = \gcd(f_k + f_{k-1},f_k) = \gcd(f_{k-1},f_k) = 1$$
where the first equality is by definition, the second is by Lemma 1, and the third is by the inductive hypothesis.

__Lemma 3.__ Given $m,n$ with $\gcd(m,n)=1$, for any $k \in \Z$, we have $\gcd(m,nk) = \gcd(m,k)$.

_Proof_. Any divisor of $m$ and $nk$ must divide $m$ and $k$ or else contradict the assumption.

__Lemma 4.__ For all $m,n \geq 0$ we have
$$f_{m+n} = f_{m+1} f_n + f_m f_{n-1}.$$

_Proof._ We fix $m$ and perform induction on $n$. For the base case, $n=1$, we have
$$f_{m+1} = f_{m+1} f_1 + f_m f_0 = f_{m+1}.$$
Now suppose that the proposition holds for $n$ (that is $f_{m+n} = f_{m+1} f_n + f_m f_{n-1}$). We then have
\begin{align*}
    f_{m+n+1} = f_{m+n} + f_{m+n-1} & = (f_{m+1} f_n + f_m f_{n-1}) + (f_{m+1} f_{n-1} + f_{m} f_{n-2}) \\\
    & = f_{m+1} f_{n+1} + f_m f_n.
\end{align*}

There is an alternate proof that revolves around the matrix
$$A \coloneqq \begin{bmatrix}
    0 & 1 \\\
    1 & 1
\end{bmatrix}$$
whose powers contain the Fibonacci sequence
$$A^{n} = \begin{bmatrix}
    f_{n-1} & f_n \\\
    f_n & f_{n+1}
\end{bmatrix}.$$
The proposition follows from inspecting the equality $A^m \times A^n = A^{m+n}$.

__Lemma 5.__ For $m,n \geq 1$, $f_m | f_{mn}$.

_Proof._ Fix $m \in \Z$ and proceed by induction. For the case $n=1$, this is trivial. Assume it holds for $n = k \geq 1$. Then
$$f_{m(k+1)} = f_{mk} f_{m+1} + f_{mk-1} f_{m}.$$
Since $f_m$ divides itself and $f_m$ divides $f_{mk}$ by the inductive hypothesis, we are done.

_Proof of Theorem 1._ Suppose $n = mk + r, 0 \leq r < m$. We then have
\begin{align*}
    \gcd(f_m,f_n) & \overset{(1)}{=} \gcd(f_m,f_{mk+1} f_r + f_{mk}f_{r-1}) \\\
    & \overset{(2)}{=} \gcd(f_m,f_{mk+1} f_r) \\\
    & \overset{(3)}{=} \gcd(f_m, f_r)
\end{align*}
where (1) follows from Lemma 4, (2) follows from Lemmas 1, 2, and 5, and (3) follows from Lemma 3.

Noting that this equality has produced Euclid's algorithm in the subscripts of the Fibonacci sequence, we see that eventually repeating this process we will have $\gcd(m,n) = \gcd(s,0) = s$. Hence,
$$\gcd(f_m,f_n) = \gcd(f_s,0) = f_s = f_{\gcd(m,n)}.$$
