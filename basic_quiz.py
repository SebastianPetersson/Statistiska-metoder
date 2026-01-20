import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
import seaborn as sns
import random
import numpy as np


root = tk.Tk()
root.withdraw()

score = 0
rounds = 2

rng = np.random.default_rng()

distributions = {
    'Integers' : lambda: rng.integers(100, size=100),
    'Uniform' : lambda: rng.uniform(size=100),
    'Normal' : lambda: rng.normal(size=100),
    'Binomial' : lambda: rng.binomial(n=10,p=0.3,size=100),
    'Gamma' : lambda: rng.gamma(shape=1.0, scale=0.9, size=100),
    'Geometric' : lambda: rng.geometric(p=0.31, size=100)
}

for i in range(rounds):
    
    dist_name, generator = random.choice(list(distributions.items()))
    data = generator()

    plt.figure(figsize=(12,8))
    plt.style.use('dark_background')
    if random.choice([True, False]):
        plt.hist(data, bins = 20, cumulative=True, density=True, histtype='stepfilled')
        plt.title('Guess the distribution (Ogive).')
    else:
        plt.hist(data, bins=20)
        plt.title('Guess the distribution (Histogram).')

    plt.show()
    guess = simpledialog.askstring('Histoquiz', f'Round {i+1}: Which distribution is this?')
    plt.close()

    if guess and guess.strip().lower() == dist_name.lower():
        score += 1
        messagebox.showinfo('Result', f'Correct, it was a {dist_name} distribution!')
    else:
        messagebox.showinfo('Result', f'Wrong, it was a {dist_name} distribution.')
messagebox.showinfo('Final Score:', f'You scored {score}/{rounds} points.')