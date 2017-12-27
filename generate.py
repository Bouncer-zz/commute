import json
import csv
import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# where is your locationhistory.json file located?
fname = 'locationhistory2.json'

# read json file
print 'reading file'
file = open(fname, "r")
content = file.read()
file.close()

# read json
print 'loading json'
data = json.loads(content)
data = data['locations']
count = len(data)
print count

import datetime

daily = {}
for loc in data:
    stamp = float(loc['timestampMs'])/1000
    
    day = int(datetime.datetime.fromtimestamp(stamp).strftime('%Y%m%d'))
    time = int(datetime.datetime.fromtimestamp(stamp).strftime('%H%M%S'))/10
    if time > 6000 and time < 10000:
        if day not in daily:
            daily[day] = {}
        daily[day][time] = {'y':float(loc['latitudeE7']) / 10000000, 'x':float(loc['longitudeE7']) / 10000000}
        #print datetime.datetime.fromtimestamp(day).strftime('%Y-%m-%d %H:%M:%S')




lines = []
fig = plt.figure()
ax = plt.axes()
line, = ax.plot([], [], lw=2)
plt.xlabel('Longitude')
plt.ylabel('Latitude')

frames = 0

days = []



for day in sorted(daily.keys())[-2:]:
    y = [daily[day][time]['y'] for time in sorted(daily[day].keys())]
    x = [daily[day][time]['x'] for time in sorted(daily[day].keys())]
    days.append({'x':x,'y':y})
    line = ax.plot([], [], color='k', lw=0.5, alpha=0.2)[0]
    lines.append(line)
    
    if len(x) > frames:
        frames = len(x)



def init():
	for line in lines:
		line.set_data([],[])
	return lines

def update(i):
    for l,line in enumerate(lines):
        line.set_data(days[l]['x'][:i], days[l]['y'][:i])
        line.axes.axis([4.7,5.3,52.25,52.45])
    return lines

ani = animation.FuncAnimation(fig, update, frames, init_func=init,
                              interval=100, blit=True)
ani.save('test.mp4', dpi=300)
#plt.show()
