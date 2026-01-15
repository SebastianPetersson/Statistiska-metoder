
import pygame
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import random
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Distribution Quiz")

font = pygame.font.SysFont("Arial", 24)

rng = np.random.default_rng()


distributions = {
    'Integers' : lambda: rng.integers(100, size=100),
    'Uniform' : lambda: rng.uniform(size=100),
    'Normal' : lambda: rng.normal(size=100),
    'Binomial' : lambda: rng.binomial(n=10,p=0.3,size=100),
    'Gamma' : lambda: rng.gamma(shape=1.0, scale=0.9, size=100),
    'Geometric' : lambda: rng.geometric(p=0.31, size=100)
}

def make_plot(data, cumulative=False):
    plt.style.use('dark_background')
    plt.figure(figsize=(6,4))
    if cumulative:
        plt.hist(data, bins=20, cumulative=True, density=True, histtype='step')
        plt.title('Guess the distribution (ogive).')
    else:
        plt.hist(data, bins=20, alpha=0.8)
        plt.title('Guess the distribution (histogram).')
    plt.tight_layout()

    plt.savefig('distribution_plot.png')
    plt.close()
    return pygame.image.load('distribution_plot.png')

score = 0
rounds = 5
current_round = 1
running = True

dist_name, generator = random.choice(list(distributions.items()))
data = generator()
plot_surface = make_plot(data, cumulative=random.choice([True, False]))




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))
    screen.blit(plot_surface, (300, 200))
    pygame.display.flip()

pygame.quit()























# root = tk.Tk()
# root.withdraw()

# score = 0
# rounds = 2

# for i in range(rounds):
    
#     dist_name, generator = random.choice(list(distributions.items()))
#     data = generator()

#     plt.figure(figsize=(12,8))
#     plt.style.use('dark_background')
#     if random.choice([True, False]):
#         plt.hist(data, bins = 20, cumulative=True, density=True, histtype='stepfilled')
#         plt.title('Guess the distribution (Ogive).')
#     else:
#         plt.hist(data, bins=20)
#         plt.title('Guess the distribution (Histogram).')

#     plt.show()
#     guess = simpledialog.askstring('Histoquiz', f'Round {i+1}: Which distribution is this?')
#     plt.close()

#     if guess and guess.strip().lower() == dist_name.lower():
#         score += 1
#         messagebox.showinfo('Result', f'Correct, it was a {dist_name} distribution!')
#     else:
#         messagebox.showinfo('Result', f'Wrong, it was a {dist_name} distribution.')
# messagebox.showinfo('Final Score:', f'You scored {score}/{rounds} points.')