import pygame
from functions import make_plot, start_screen, new_round
import numpy as np
import random
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"
rng = np.random.default_rng()

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Distribution Quiz")
font = pygame.font.SysFont("Arial", 24)

distributions = {
    'Integers' : lambda: rng.integers(100, size=100),
    'Uniform' : lambda: rng.uniform(size=100),
    'Normal' : lambda: rng.normal(size=100),
    'Binomial' : lambda: rng.binomial(n=10,p=0.3,size=100),
    'Gamma' : lambda: rng.gamma(shape=1.0, scale=0.9, size=100),
    'Geometric' : lambda: rng.geometric(p=0.31, size=100)
}

score = 0
rounds = 5
current_round = 1
running = True

dist_name, plot_surface, x, y, input_box = new_round()
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_active
input_text = ""
feedback = ""
active_box = True

start_screen(screen)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active_box = True
            else:
                active_box = False
            color = color_active if active_box else color_inactive

        if event.type == pygame.KEYDOWN and active_box:
            if event.key == pygame.K_RETURN:
                if input_text.lower() == dist_name.lower():
                    feedback = "Correct!"
                    score += 1
                else:
                    feedback = f"Wrong! It was {dist_name}"
                active_box = False

            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                if len(input_text) < 15:
                    input_text += event.unicode

        elif event.type == pygame.KEYDOWN and not active_box:
            current_round += 1
            if current_round > rounds:
                running = False
            else:
                dist_name, plot_surface, x, y, input_box = new_round()
                input_text = ""
                feedback = ""
                active_box = True
                color = color_active

    screen.fill((0,0,0))
    screen.blit(plot_surface, (x, y))

    pygame.draw.rect(screen, color, input_box, 2)
    text_surface = font.render(input_text, True, (255,255,255))
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

    if feedback:
        fb_color = (0,255,0) if feedback.startswith("Correct") else (255,0,0)
        fb_surface = font.render(feedback, True, fb_color)
        screen.blit(fb_surface, (WIDTH//2 - fb_surface.get_width()//2, input_box.y + 50))

    round_surface = font.render(f"Round {current_round} / {rounds}", True, (200,200,200))
    screen.blit(round_surface, (10,10))

    pygame.display.flip()

screen.fill((0,0,0))
end_surface = font.render(f"Quiz finished! Score: {score}/{rounds}", True, (255,255,255))
screen.blit(end_surface, (WIDTH//2 - end_surface.get_width()//2, HEIGHT//2))
pygame.display.flip()
pygame.time.wait(5000)
pygame.quit()

hej
