# Buy Low and Sell High

import numpy as np
from scipy.stats import norm

Phi= lambda z: norm.cdf(z)  # Standard Gaussian CDF

def AR1_stac(rho: float):
    """
    rho: autoregressive coefficient in the volatility process
    """
    
    x = np.random.normal()/np.sqrt(1-rho**2.0)  # stationary initialization
    
    while True:
        yield x 
        x=rho*x+np.random.normal()  # AR(1) iteration

def log_return(sigma, M: float):
    """
    sigma: the stochastic volatility process
    M: upper bound of the daily log-return (large positive number)
    """
    
    def calc_X():
        s = np.abs(next(sigma)) # next stochastic volatility
        x = np.min([s*np.random.normal(),M])  # truncated daily log-return
        Ex = M*(1-Phi(M/s))-s/np.sqrt(2*np.pi)*np.exp(-0.5*(M/s)**2.0) # expectation of x conditioned on s
        
        return x-Ex  # centralized and truncated daily log-return
    
    while True:
        yield calc_X()

def random_walk(X, S0):
    """
    S0: starting value
    X: increment process
    """
    
    S = S0  # The martingale part of the price process 
    while True:
        yield S
        S+=next(X)
        
def dynamic_trading(S):
    """
    S: fluctuations of the logarithmic price
    """
    
    s = next(S)
    L, T = 0, 0  # buying and selling time
    sL, sT = s, s  # buy and sell price
    
    def next_trade(th_low: float, th_high: float)->tuple:
        """
        Calculates time ellapsed between the next buy and sell, 
        and also calculates the daily logarithmic return over 
        the trading period.
        
        theta_low, theta_high: buy and sell thresholds
        """
        
        nonlocal L, T, sL, sT
        
        if th_low>th_high:  # don't trigger unfavourable trades
            return 0, 0.0
        
        L = T
        sL = sT
        while sL>=th_low: # wait until the price goes below th_low
            sL = next(S)
            L = L+1
        
        T = L
        sT = sL
        while sT<=th_high:  # wait until the price reaches th_up
            sT = next(S)
            T = T+1
            
        return T-L, (sT-sL)/(T-L)
        
    return next_trade

def KW_SPSA(L, th0: np.ndarray):
    """
    Kiefer-Wolfowitz Simultaneous Perturbation Stochastic Algorithm
    aiming to finding the minimum of 
    L: the loss function
    th0: initial guess (2d vector)
    
    This algorithm operates with decreasing step-size.
    """
    
    assert th0[0] < th0[1], "The lower threshold should be strictly lower than the upper one."
    
    th = th0
    k = 1

    while True:
        yield th
        
        while True:
            # next stepsize
            a = 1/k
            c = a**0.5
        
            # calculate the stochastic gradient
            Dlt = c*np.random.choice([-1,1],size=(2,))
            H = 0.5*(L(th+Dlt)-L(th-Dlt))/Dlt
        
            # update th
            th_new = th - a*H
            if th_new[0]<th_new[1]:  # ensure that th[0]<th[1]
                th = th_new
                break
            k+=1
            
def get_trader(rho: float):
    # set objective function
    sigma = AR1_stac(rho=rho)
    X = log_return(sigma, M=1.0)
    S = random_walk(X, S0=0.0)
    
    return dynamic_trading(S)
            
def find_optimal_theta(rho: float)->np.ndarray:
    """
    Find optimal threshold trading strategy for a given value 
    of the autoregressive coefficient in the volatility process.
    """
    
    # set objective function
    trader = get_trader(rho)
    objfcn = lambda th: -trader(th[0],th[1])[1]
    
    # set optimizer
    th = np.array([-1,1])
    optimizer = KW_SPSA(L=objfcn, th0=th)
    
    # perform optimization
    for i in range(50): # maxIter is 50
        thnew = next(optimizer)        
        if i>0 and np.allclose(th, thnew, rtol=1e-3, atol=1e-6):
            return th
        th = thnew
     
    print("Warning: Maximum Number of Iterations reached.")
    return th 