#!/usr/bin/env python3
import random

from PyQt5 import QtCore, QtWidgets, uic
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import collections
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')

np.set_printoptions(suppress=True)


def SIR(population, days_before_treatment, contacts_per_human, contacts_per_human_with_treatment, recovery_days,
        recovery_days_with_treatment, probability_of_transmission,
        probability_of_transmission_with_treatment, infected_at_day1):
    # susceptible, infected, recovered population
    days_simulated = 0
    total_infected = infected_at_day1

    Y = np.zeros((recovery_days,), dtype=int)  # Initialize the array with R ints
    Y[0] = total_infected

    people_susceptible = population - total_infected  # people can be infected
    total_recovered = 0

    total_sum_run = total_infected

    while np.count_nonzero(Y) != 0:  # while something is in Y array
        if days_simulated == days_before_treatment:
            contacts_per_human = contacts_per_human_with_treatment
            recovery_days = recovery_days_with_treatment
            probability_of_transmission = probability_of_transmission_with_treatment

        if days_simulated >= days_before_treatment:
            probability_of_transmission *= 0.95

        prob1 = total_infected / (population - 1)  # probability of contacting with infected
        prob2 = prob1 * probability_of_transmission  # probability of being infected after contact
        prob_after_one_contact = 1 - prob2  # probability of being not infected after contact
        prob_after_mult_contacts = prob_after_one_contact ** contacts_per_human  # probability of being not infected
        # after multiple contacts

        probability_of_becoming_infected = \
            1 - prob_after_mult_contacts
        new_infected = np.random.binomial(people_susceptible, probability_of_becoming_infected)

        total_sum_run += new_infected
        people_susceptible -= new_infected
        total_recovered = total_recovered + Y[
            recovery_days - 1]  # increase num recovered by last spot of time sick array

        # shift the time sick array (Y) over by one, put new num infected at beginning
        Y = np.roll(Y, 1)
        Y[0] = new_infected

        total_infected += Y[len(Y) - 1]

        days_simulated += 1
    return days_simulated, total_sum_run


def graph(durations):
    counter = collections.Counter(durations)  # create counter for data
    counter_array = np.array(list(sorted(counter.items())))  # convert counter to 2d array

    # split 2d array into 2 1d arrays
    duration, counts = counter_array.T

    plt.plot(duration, counts, 'bo-')

    plt.xlabel('duration (days)')
    plt.ylabel('num instances')
    plt.title('Virus Simulation')
    plt.grid(True)

    plt.savefig("test.png")
    plt.show()


def runner(num_sims, population, days_before_treatment, contacts_per_human, contacts_per_human_with_treatment,
           recovery_days, recovery_days_with_treatment, probability_of_transmission,
           probability_of_transmission_with_treatment, infected_at_day1):
    sum_duration = 0
    total_infected = 0

    durations = np.array([])  # array of durations

    print('\nSimulation'.ljust(15, ' ') + 'Duration'.ljust(15, ' ') + 'Infected'.ljust(15, ' '))
    print('-' * 45)
    for i in range(num_sims):
        duration, sum_infected = \
            SIR(population, days_before_treatment, contacts_per_human, contacts_per_human_with_treatment, recovery_days,
                recovery_days_with_treatment, probability_of_transmission,
                probability_of_transmission_with_treatment, infected_at_day1)

        durations = np.append(durations, [duration])  # adds run duration to durations array

        sum_duration += duration
        total_infected += sum_infected
        print('{}'.format(i + 1).ljust(15, ' ') + '{}'.format(duration).ljust(15, ' ')
              + '{}'.format(sum_infected).ljust(15, ' '))

    print('-' * 45)
    mean_duration = float(sum_duration) / num_sims
    mean_infected = float(total_infected) / num_sims
    print('mean duration = ', mean_duration, ' mean infected = ', mean_infected)

    graph(durations)


def main():
    num_sims = 100

    population = 1500000
    days_before_treatment = 50
    contacts_per_human = 5
    contacts_per_human_with_treatment = 3
    recovery_days = 14
    recovery_days_with_treatment = 7
    probability_of_transmission = 0.1
    probability_of_transmission_with_treatment = 0.05
    infected_at_day1 = 2

    runner(num_sims, population, days_before_treatment, contacts_per_human, contacts_per_human_with_treatment,
           recovery_days, recovery_days_with_treatment, probability_of_transmission,
           probability_of_transmission_with_treatment, infected_at_day1)


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)

        n_data = 50
        self.xdata = list(range(n_data))
        self.ydata = [random.randint(0, 10) for i in range(n_data)]

        self.show()


if __name__ == "__main__":
    main()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()

app.exec_()
