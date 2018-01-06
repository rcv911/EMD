from numpy import *
from matplotlib.pyplot import *
from scipy.signal import *
from scipy.interpolate import splrep, splev

f = 1
f2 = 1
t = linspace(0,10,10000)
x = zeros(len(t))
xmin = zeros(len(t))
xmax = zeros(len(t))

k = 4  # number of mod

newsi = zeros([k+1,len(x)])
mod = zeros([k,len(x)])


noise = random.uniform(-0.05,0.05,10000)
print(noise)
signal = sin (2*pi*f*t) + noise
x = signal
newsi[0,:] = x

for i in range(k):
    x = newsi[i,:]
    data1 = argrelmax(x)[0]
    xmax = x.take(data1)
    tmax = t.take(data1)
    data2 = argrelmin(x)[0]
    xmin = x.take(data2)
    tmin = t.take(data2)  

    coef = splrep(tmax,xmax)    
    resmax = splev(t,coef)
    coef = splrep(tmin,xmin)    
    resmin = splev(t,coef)

    mu = (resmax + resmin)/2
    mod[i,:] = x - mu
    newsi[i+1,:] = x - mod[i,:]
    

#draw graph
figure('Test Signal')
xlabel('t')
ylabel('Amplitude')
plot(t, newsi[0,:])
grid()

figure('Empirical Mode Decomposition')
xlabel('t')
ylabel('Amplitude')
for i in range(k):
    plot(t, mod[i,:])
grid()
    
figure('Result')
xlabel('t')
ylabel('Amplitude')
for i in range(k):
    plot(t, newsi[i,:])

# plot(t, newsi[0,:], 'y', label = 'all modes')
# plot(t, newsi[3,:], 'b', label = 'signal without first 3 modes')
# legend(loc = 'best')
grid()

show()

