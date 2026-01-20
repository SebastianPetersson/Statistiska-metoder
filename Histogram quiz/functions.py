import pygame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import random
import os

def start_screen(screen, WIDTH, HEIGHT):
    font_large = pygame.font.SysFont('Arial', 48)
    font_small = pygame.font.SysFont('Arial', 30)
    waiting=True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        screen.fill((10,10,40))
        title = font_large.render("Distribution Quiz", True, (255,255,255))
        hint = font_small.render("Left click or click space to continue", True, (200,200,200))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 300))
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, 360))
        pygame.display.flip()

def make_plot(data, cumulative=False):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(6,4), dpi=100)
    if cumulative:
        ax.hist(data, bins=20, cumulative=True, density=True, histtype='step')
        ax.set_title('Guess the distribution (ogive)', fontsize=16)
    else:
        ax.hist(data, bins=20, alpha=0.8)
        ax.set_title('Guess the distribution (histogram)', fontsize=16)
    fig.tight_layout()

    canvas = FigureCanvas(fig)
    canvas.draw()
    raw_data = np.frombuffer(canvas.buffer_rgba(), dtype=np.uint8)
    raw_data = raw_data.reshape(fig.canvas.get_width_height()[::-1] + (4,))
    plt.close(fig)

    surface = pygame.image.frombuffer(raw_data.flatten(), fig.canvas.get_width_height(), "RGBA")
    return surface

def new_round(distributions, WIDTH, HEIGHT):
    dist_name, generator = random.choice(list(distributions.items()))
    data = generator()
    plot_surface = make_plot(data, cumulative=random.choice([True, False]))
    x = WIDTH//2 - plot_surface.get_width()//2
    y = HEIGHT//2 - plot_surface.get_height()//2 + 50
    input_box = pygame.Rect(WIDTH//2 - 150, y + plot_surface.get_height() + 20, 300, 40)
    return dist_name, plot_surface, x, y, input_box