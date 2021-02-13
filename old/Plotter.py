import matplotlib.pyplot as plt
import matplotlib
from matplotlib.pyplot import ion
import numpy as np
import time


class Plotter:
    def __init__(self):

        self.a = -1
        self.b = 0
        self.c = 0
        self.d = 0

        self.labels = ["A", "B", "C", "D"]

        self.x = 0  # the label locations
        self.width = 0.10  # the width of the bars

        self.fig, self.ax = plt.subplots()
        # ion()


        plt.ion()
        plt.show()
        self.update()


    def update(self):
        while 1:

            with open("data.data") as f:
                text = f.readline()
                data = text.split(":")
                print(len(data))
                if len(data) < 4:
                    continue
                a = int(data[1])
                b = int(data[3])
                c = int(data[5])
                d = int(data[7])


            something_new = False
            if a != self.a:
                self.a = a
                something_new = True

            if b != self.b:
                self.b = b
                something_new = True

            if c !=self.c:
                self.c = c
                something_new = True

            if d != self.d:
                self.d = d
                something_new = True

            alle = a+b+c+d

            if alle != 0:

                plot_a = a / alle *100
                plot_b = b / alle *100
                plot_c = c / alle *100
                plot_d = d / alle *100

            else:
                plot_a = 0
                plot_b = 0
                plot_c = 0
                plot_d = 0


            if something_new:
                print("SOMETHING NEW")
                print(self.a, self.b, self.c, self.d)
                self.ax.clear()
                rects0 = self.ax.bar(
                    self.x - 3 * self.width,
                    plot_a,
                    self.width,
                    label='A',
                    color="b")
                rects1 = self.ax.bar(
                    self.x - 2 * self.width,
                    plot_b,
                    self.width,
                    label="B",
                    color="purple")
                rects2 = self.ax.bar(
                    self.x - self.width,
                    plot_c,
                    self.width,
                    label='C',
                    color="pink")
                rects3 = self.ax.bar(self.x, plot_d, self.width, label='D', color="red")
                

                plt.tick_params(
                    axis='x',          # changes apply to the x-axis
                    which='both',      # both major and minor ticks are affected
                    bottom=False,      # ticks along the bottom edge are off
                    top=False,         # ticks along the top edge are off
                    labelbottom=False) # labels along the bottom edge are off
                self.ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
                    ncol=3, fancybox=True, shadow=True)

                self.fig.tight_layout()
                self.ax.set_ylim([0, 120])
            plt.draw()
            plt.pause(0.1)
            plt.show()
p = Plotter()
p.update()