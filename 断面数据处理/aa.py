#coding=utf-8
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
t = np.arange(0.0,2.0,0.1)
s = np.sin(t*np.pi)
plt.subplot(2,2,1)
plt.plot(t,s,'b--')
plt.ylabel('y1')
plt.subplot(2,2,2)
plt.plot(2*t,s,'r--')
plt.ylabel('y2')
plt.subplot(2,2,3)
plt.plot(3*t,s,'m--')
plt.subplot(2,2,4)
plt.plot(4*t,s,'k--')
plt.show()

