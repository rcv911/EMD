from numpy import *
from matplotlib.pyplot import *
from scipy.signal import *
from scipy.interpolate import splrep, splev
from scipy.integrate import odeint

f = 1
f2 = 1
t = linspace(0, 10, 10000)
per = linspace(0, 100, 100000)
x = zeros(len(t))
xmin = zeros(len(t))
xmax = zeros(len(t))

k = 4 # number of mod

newsi = zeros([k+1, len(x)])
mod = zeros([k, len(x)])


def wanda01(x,t):
    rx = 9
    wx = 33
    nx0 = x[1]
    nx1 = (rx - x[0]**2) * x[1] - wx*x[0] 
    res = array([nx0, nx1])
    return res


res=odeint(wanda01, [-0.2, 0.1, 0.4, 0.2], per)
noise = random.uniform(-0.15, 0.15, 10000)
x = noise + res[:,0] [90000:]
newsi[0,:] = x

for i in range(k):
    x = newsi[i,:]
    data1 = argrelmax(x)[0]
    xmax = x.take(data1)
    tmax = t.take(data1)
    data2 = argrelmin(x)[0]
    xmin = x.take(data2)
    tmin = t.take(data2)  

    coef = splrep(tmax, xmax)    
    resmax = splev(t, coef)
    coef = splrep(tmin, xmin)    
    resmin = splev(t, coef)

    mu = (resmax + resmin)/2
    mod[i, :] = x - mu
    newsi[i+1, :] = x - mod[i, :]
        
    

#draw graph
figure('EMD Van der Pol oscillator')
subplot(3,1,1)
xlabel('t')
ylabel('Amplitude')
plot(t, newsi[0,:])
grid()

subplot(3,1,2)
xlabel('t')
ylabel('Amplitude')
for i in range(k):
    plot(t, mod[i,:])
grid()    
    
subplot(3,1,3)
xlabel('t')
ylabel('Amplitude')
for i in range(k):
    plot(t, newsi[i,:])
grid()
    
show()