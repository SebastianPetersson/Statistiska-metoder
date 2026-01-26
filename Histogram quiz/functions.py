import pygame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import random
import os

def start_screen(screen, W, H, fade_ms):
    font_large = pygame.font.SysFont('Arial',48)
    font_small = pygame.font.SysFont('Arial',30)
    title = font_large.render("Distribution Quiz", True, (255,255,255)).convert_alpha()
    hint  = font_small.render("Left click or press space", True, (200,200,200)).convert_alpha()
    clock = pygame.time.Clock(); start = pygame.time.get_ticks()
    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); exit()
            if e.type==pygame.KEYDOWN and e.key==pygame.K_SPACE: return
            if e.type==pygame.MOUSEBUTTONDOWN: return
        t = min(1.0, (pygame.time.get_ticks()-start)/fade_ms)
        a = int(255*t)
        screen.fill((10,10,40))
        tmp1, tmp2 = title.copy(), hint.copy()
        tmp1.set_alpha(a); tmp2.set_alpha(a)
        screen.blit(tmp1, (W//2-title.get_width()//2,300))
        screen.blit(tmp2, (W//2-hint.get_width()//2,360))
        pygame.display.flip(); clock.tick(60)


def make_plot(data, cumulative=False):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(6,4), dpi=100)
    if cumulative:
        ax.hist(data, bins=40, cumulative=True, density=True, histtype='barstacked')
        ax.set_title('Guess the distribution (ogive)', fontsize=16)
    else:
        ax.hist(data, bins=40, alpha=0.8, histtype='barstacked')
        ax.set_title('Guess the distribution (histogram)', fontsize=16)
    fig.tight_layout()

    canvas = FigureCanvas(fig)
    canvas.draw()
    raw_data = np.frombuffer(canvas.buffer_rgba(), dtype=np.uint8)
    raw_data = raw_data.reshape(fig.canvas.get_width_height()[::-1] + (4,))
    plt.close(fig)

    surface = pygame.image.frombuffer(raw_data.flatten(), fig.canvas.get_width_height(), "RGBA")
    return surface

def new_round(distributions, W, H):
    dist_name, generator = random.choice(list(distributions.items()))
    data = generator()
    plot_surface = make_plot(data, cumulative=random.choice([True, False]))
    x = W//2 - plot_surface.get_width()//2
    y = H//2 - plot_surface.get_height()//2 + 50
    input_box = pygame.Rect(W//2 - 150, y + plot_surface.get_height() + 20, 300, 40)
    return dist_name, plot_surface, x, y, input_box