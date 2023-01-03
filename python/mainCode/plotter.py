import matplotlib.pyplot as plt
import tkinter
from scipy.fft import rfft, rfftfreq
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np


### Drawing functions
class Plotter:
    
    def __init__(self, window_size, hop_size, samplingPeriod, duration, target_range):
        self.window_size = window_size
        self.hop_size = hop_size
        self.samplingPeriod = samplingPeriod
        self.sample_rate = 1/samplingPeriod
        self.duration = duration
        self.target_range = target_range

        self.dominant_frequency = 0
        self.dominant_period = 0
        self.biofeedback_score = 0

        self.canvases = []


        self.root = tkinter.Tk()
        self.root.wm_title("Embedding in Tk")

        button_quit = tkinter.Button(master=self.root, text="Quit", command=self.root.destroy)


        b2 = tkinter.Button(self.root, text='b2')

        self.text_display = tkinter.Text(self.root)
        self.text_display.pack(side = tkinter.BOTTOM, fill = tkinter.BOTH)


        b2.pack(side = tkinter.RIGHT)


    def createCanvas(self, type):
        # You probably won't need this if you're embedding things in a tkinter plot...
        # plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        line1, = ax.plot([], [], 'r-') # Returns a tuple of line objects, thus the comma

        if (type == "rawData"):
            # set the scale 
            ax.set_ylim(0, 5000)
            ax.set_xlim(0, 60)

        if (type == "biofeedback"):
            # set the scale 
            target_range_breaths_per_second = [bpm / 60 for bpm in self.target_range]
            ax.axvspan(target_range_breaths_per_second[0], target_range_breaths_per_second[1], alpha=0.1, color='red')

            ax.set_ylim(0, 1000)
            ax.set_xlim(0, 1)

        canvas = FigureCanvasTkAgg(fig, master=self.root)  # A tk.DrawingArea.
        canvas.draw()

        canvas.mpl_connect("key_press_event", lambda event: print(f"you pressed {event.key}"))
        canvas.mpl_connect("key_press_event", key_press_handler)

        self.canvases.append(canvas)

        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)


        return canvas, line1, ax, fig
    


    def __calculate_biofeedback_score(self, power_spectrum, target_range):
        # Convert the target range to breaths per second
        target_range_breaths_per_second = [bpm / 60 for bpm in target_range]

        # Extract the frequencies and power values from the power spectrum
        frequencies = power_spectrum[:, 0]
        power = power_spectrum[:, 1]

        # Calculate the area under the curve (AUC) of the power spectrum within the
        # target range
        auc_target = np.trapz(power[(frequencies >= target_range[0]) & (frequencies <= target_range[1])], frequencies[(
            frequencies >= target_range[0]) & (frequencies <= target_range[1])])

        # Calculate the AUC of the power spectrum outside of the target range
        auc_outside = np.trapz(power[(frequencies < target_range[0]) | (frequencies > target_range[1])], frequencies[(
            frequencies < target_range[0]) | (frequencies > target_range[1])])

        # Calculate the biofeedback score as the ratio of the AUC within the target range
        # to the AUC outside of the target range
        biofeedback_score = auc_target / auc_outside

        return biofeedback_score


    def __calculate_power_spectrum(self, signal):

        # Calculate the FFT of the signal
        N = len(signal)
        yf = rfft(signal)
        yf = np.abs(yf) ** 2
        
        xf = rfftfreq(N, 1/self.sample_rate)

        yf[0] = 0
        xf[0] = 0

        # scale yf to be in the range of 0 to 1000
        yf = yf / np.max(yf) * 1000

        return np.array([xf, yf]).T


    def __process_breathing_data(self, data):
        # Calculate the power spectrum of the window
        power_spectrum = self.__calculate_power_spectrum(data)

        xf = power_spectrum[:, 0]
        yf = power_spectrum[:, 1]

        dominant_freq = np.argmax(np.abs(yf))

        # Calculate the biofeedback score from the power spectrum and target range
        biofeedback_score = self.__calculate_biofeedback_score(power_spectrum, self.target_range)

        return [xf, yf, xf[dominant_freq], biofeedback_score]
    

    def __draw(self, x, y, line, fig):
        
        line.set_xdata(x)
        line.set_ydata(np.abs(y))
        fig.canvas.draw()
        fig.canvas.flush_events()


    def updateBiofeedback(self, data, line, fig, ax):
        if (len(data) < self.window_size):
            return
        biofeedback = self.__process_breathing_data(data)
        xf = biofeedback[0]
        yf = biofeedback[1]
        self.dominant_frequency = biofeedback[2]
        self.dominant_period = 1 / self.dominant_frequency

        self.biofeedback_score = biofeedback[3]

        # Clear the Text widget
        self.text_display.delete("1.0", tkinter.END)
        
        # Set the text and color based on the value of self.dominant_period
        self.text_display.insert("1.0", f"Dominant period is {self.dominant_period} seconds", "red")

        # self.text_display.tag_configure("red", foreground="red", background="red", font=("Arial", 16), justify=tkinter.LEFT)
        
        self.__draw(xf, yf, line, fig)


    def updateRawData(self, data, line, fig):
        if (len(data) < self.window_size):
            return
        # create suitable y for data, and x for time
        y = data
        x = [i*self.samplingPeriod for i in range(len(data))] 
        self.__draw(x, y, line, fig)


    def mainDraw(self):
        self.root.update_idletasks()
        self.root.update()