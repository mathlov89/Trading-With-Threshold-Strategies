# Trading-With-Threshold-Strategies

### Attila Lovas, Miklós Rásonyi (2022)

## About The Project

[The recent paper](https://arxiv.org/abs/2111.14708) is devoted to investigate threshold-type strategies 
in the context of ergodic control. It makes the first steps towards their optimization by proving 
the ergodic properties of related functionals. Assuming Markovian price increments satisfying 
a minorization condition and (one-sided) boundedness it was shown, in particular, that for given thresholds, 
the distribution of the gains converges in the long run. Under suitable conditions, some recent 
results on the stability of overshoots of random walks from the i.i.d.\ increment case to Markovian increments 
has been extended, too. 

We had submitted the above paper to the Annals of Operations research, and got a referee report that
"the main issue with the current version of the paper is the lack of financial insights from the main results".
In response to the reviewer's main concern, we decided to supplement our paper with a simulation section that provides
sufficient financial insights from the main results.

To this end, and inspired by the paper of [Chan and Grant (2015)](http://www.sciencedirect.com/science/article/pii/S0140988315003539), 
we elaborated a discrete time stochastic volatility model that falls under the scope of our main theorem.
We fixed buy and sell thresholds, and conducted two kinds of simulation. First, we executed the trading strategy and recorded
the time ellapsed between buys and sells, and also we calculated the daily logarithmic return on each traiding period.
Next, we studied how the latter quantity depends on the autoregressive paramater appearing in the stochastic volatility model.

## Summary Of The Main Results

- We found that the larger the absolute value of the autoregressive parameter, 
the bigger the expected daily log-return on a trade. Roughly speaking, 
it worths to follow threshold trading strategy when the asset returns show volatility clustering behaviour.

- With small probability, the time between buy and sell can be extremely large making this strategy inappropriate for
practitioners who want to profit from price oscillations.

## Contents

- stochvol.ipynb This is a Jupyter notebook that contains all simulation codes needed to reproduce the simulation results.
- blsh.py This is the source code that implements the stochastic volatility model, the trading strategy, and also a stochastic optimization algorithm.

## License

Distributed under the MIT License. See LICENSE.txt for more information.

## Contact

Corresponding Author: Attila Lovas - attila.lovas@renyi.hu
Affiliation: Alfréd Rényi Institute of Mathematics
