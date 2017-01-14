import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.ion()

gen_d = {'coal': [12,13,12,14], 'natgas': [15,16,18,17], 'nuclear': [5,7,8,6]}

time = ['12:00', '13:00', '14:00', '15:00']

Table = pd.DataFrame(gen_d, columns = ['coal', 'natgas', 'nuclear'])

N = 4
ind = np.arange(N)
width = 0.35

one = plt.bar(ind, gen_d['coal'], width, color='k')
two = plt.bar(ind, gen_d['natgas'], width, color='g', \
bottom=gen_d['coal'])
three = plt.bar(ind, gen_d['nuclear'], width, color='b', \
bottom=[i+j for i,j in zip(gen_d['coal'], gen_d['natgas'])])

plt.ylabel('Production [MW]')
plt.title('Fuel Mix')
plt.xticks(ind + width/2., time)
plt.legend(('coal', 'natgas', 'nuclear'))

print(Table)
plt.show()
plt.pause(0.001)

input('press enter to continue')

