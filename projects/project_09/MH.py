import random
# import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class MH:
    def __init__(self) -> None:
        self.n_doors = 3
        self.n_trials = 0
        self.n_sw = 0
        self.sw_w_n = 0
        self.sw_w = []
        self.st_w_n = 0
        self.st_w = []

    def __str__(self) -> str:
        return (f'MH problem\n'
                f'  n_doors = {self.n_doors}\n'
                f'  n_trials = {self.n_trials}\n'
                f'  n_sw = {self.n_sw}\n'
                f'  sw_w_n = {self.sw_w_n}\n'
                f'  sw_w [{self.n_trials}] = {self.sw_w}...\n'
                f'  st_w_n = {self.st_w_n}\n'
                f'  st_w [{self.n_trials}] = {self.st_w}...')

    def trial(self): #verbose argument fixes test file bug
        doors = [i for i in range(1, self.n_doors + 1)]
        self.n_trials += 1
        correct = False
        #select chosen door, car door, and open goat door
        car = random.randint(1, self.n_doors)
        chosen = random.randint(1, self.n_doors)
        goat = random.randint(1, self.n_doors)
        while goat == car or goat == chosen:
            goat = random.randint(1, self.n_doors)
        if chosen == car: correct = True
        #randomly decide to switch
        switched = bool(random.randint(0,1))
        sw_d = None
        if switched:
            doors.remove(chosen)
            doors.remove(goat)
            sw_d = doors[0]
            if sw_d == car:
                correct = True
            else:
                correct = False
        self.update(switched, chosen, correct, sw_d)

    def update(self, switched, chosen, correct, sw_d):
        if switched:
            self.n_sw += 1
            if correct:
                self.sw_w_n += 1
        elif correct:
            self.st_w_n += 1
        self.sw_w.append(self.sw_w_n/max(self.n_sw,1))
        self.st_w.append(self.st_w_n/max(self.n_trials-self.n_sw,1))

    def experiment(self, nt=10):
        for i in range(nt):
            self.trial()

    def plot(self):
        x = [i for i in range(self.n_trials)]
        fig, ax = plt.subplots()
        ax.set_xlim([0,self.n_trials])
        ax.set_ylim([0,1])
        ax.plot(x,self.sw_w,self.st_w)
        plt.show()

    def animate_plot(self):
        x = []
        y = []
        z = []

        def animate(i):
            ax.clear()
            ax.set_xlim([0,self.n_trials])
            ax.set_ylim([0,1])
        
            x.append(i)
            y.append(self.sw_w[i])
            z.append(self.st_w[i])
            ax.plot(x,y,z)

        fig, ax = plt.subplots()
        ani = FuncAnimation(fig, animate, frames=self.n_trials, interval=30, repeat=False)
        plt.show()

if __name__ == "__main__":
    random.seed(42)
    mh = MH()
    print(mh)

    mh.trial()
    print(mh)
    mh.trial()
    print(mh)
    mh.trial()
    print(mh)
    mh.experiment(1000)
    print(mh)

    # mh.plot()

    mh.animate_plot()
