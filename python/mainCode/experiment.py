import time
from plotter import Plotter
import sys
import os
import pandas as pd
from os import listdir
from os.path import isfile, join
import numpy as np


def getSin(time):
    # period is 8 seconds, amplitude is 4000, gaussian noise
    return float(4000*np.sin(2*np.pi*time/8) + np.random.normal(0, 500, 1)[0])


window_size = 30
hop_size = 2

# Define the target range (breaths per minute)
target_range = (4, 12)


samplingPeriod = 0.1
duration = 60
target_range = (4, 12)

sample_rate = 1/samplingPeriod

setupComplete = False
data = []
windowData = []
startIndex = 1
currentIndex = startIndex

window_size_samples = int(window_size * sample_rate)
hop_size_samples = int(hop_size * sample_rate)


plotter = Plotter(window_size, hop_size, samplingPeriod,
                  duration, target_range)

(canvas1, line1, ax1, fig1) = plotter.createCanvas("rawData")
(canvas2, line2, ax2, fig2) = plotter.createCanvas("biofeedback")


def experimentCode():
    global counter
    global data
    global windowData
    global startIndex
    global currentIndex

    while True:
        # v = device.getSensorsData('Respiration', 1)
        v = getSin(now)
        if v == False:
            next
        if v != False:
            variable = float(str(v))
            data.append(variable)
            currentIndex = currentIndex + 1

            plotter.updateRawData(data, line1, fig1)

            if (currentIndex - startIndex) >= hop_size_samples:

                plotter.updateBiofeedback(windowData, line2, fig2, ax2)

                startIndex = currentIndex

                index = startIndex - window_size_samples
                if (index <= 0):
                    index = 0

                windowData = data[index: startIndex]

            plotter.mainDraw()

            break


start = time.time()
now = start


def runExperiment(duration, samplingPeriod):
    global now
    global start

    while True:
        if (time.time() - now) >= samplingPeriod:
            now = time.time()
            experimentCode()

        if time.time() - start >= duration:
            saveData()
            break


def saveData():
    mypath = "C:/Users/ollie/Documents/Arduino/sketch_oct7a/python/mainCode/data"
    dataFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    if not dataFiles:
        # dataFiles is empty, initialize name at "data1.csv"
        latestFilename = "data1.csv"

    else:
        # Take the latest filename (i.e. data3.csv), isolate the number, increment the next filename
        latestFilename = max(dataFiles)

        # isolate the number after "data" and before ".csv"
        number = int(latestFilename.split(".")[0][4:])
        number += 1  # increment the number
        latestFilename = f"data{number}.csv"
    df = pd.DataFrame(data)
    df.to_csv('data/'+latestFilename)


if __name__ == '__main__':
    try:
        runExperiment(duration, samplingPeriod)
    except KeyboardInterrupt:
        saveData()
        print('Interrupted')
