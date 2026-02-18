import pygame
from functions import make_plot, start_screen, new_round
import numpy as np
import random
import os
import json, time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(SAVE_DIR, exist_ok=True)
SAVE_PATH = os.path.join(SAVE_DIR, "Played_games.json")

os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"
rng = np.random.default_rng()
clock = pygame.time.Clock()
showing_feedback = False

pygame.init()

W, H = 1200, 800
screen = pygame.display.set_mode((W, H))
font = pygame.font.SysFont("Arial", 24)
background_path = os.path.join(SAVE_DIR, "analyst.png")
background_img = pygame.image.load(background_path).convert()
background_img = pygame.transform.scale(background_img, (W, H))


distributions = {
    'Uniform' : lambda: rng.uniform(size=1000),
    'Normal' : lambda: rng.normal(size=1000),
    'Binomial' : lambda: rng.binomial(n=10,p=0.3,size=1000),
    'Negative Binomial' : lambda: rng.negative_binomial(n=10, p=0.3, size=1000),
    'Gamma' : lambda: rng.gamma(shape=1.0, scale=0.9, size=1000),
    'Geometric' : lambda: rng.geometric(p=0.31, size=1000)
}

score = 0
rounds = 20
current_round = 1
running = True

dist_name, plot_surface, x, y, input_box = new_round(distributions=distributions, W=W, H=H)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_active
input_text = ""
feedback = ""
active_box = True

start_screen(screen, W, H, fade_ms=2000, background_img=background_img)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            active_box = input_box.collidepoint(event.pos)
            color = color_active if active_box else color_inactive

        if event.type == pygame.KEYDOWN and active_box:
            if event.key == pygame.K_RETURN:

                if not showing_feedback:
                    correct = input_text.lower() == dist_name.lower()
                    if correct:
                        feedback = "Correct!"
                        score += 1
                    else:
                        feedback = f"Wrong! It was {dist_name}"

                    showing_feedback = True

                else:
                    if current_round >= rounds:
                        running = False
                    else:
                        current_round += 1
                        dist_name, plot_surface, x, y, input_box = new_round(
                            distributions=distributions, W=W, H=H
                        )
                        input_text = ""
                        feedback = ""
                        showing_feedback = False
                        active_box = True
                        color = color_active

            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]

            else:
                if len(input_text) < 20:
                    input_text += event.unicode


    screen.blit(background_img, (25,0))
    darken = pygame.Surface((W, H))
    darken.set_alpha(120)
    darken.fill((0, 0, 0))
    screen.blit(darken, (0,0))
    screen.blit(plot_surface, (x, y))

    pygame.draw.rect(screen, color, input_box, 2)
    text_surface = font.render(input_text, True, (255,255,255))
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

    if feedback:
        fb_color = (0,255,0) if feedback.startswith("Correct") else (255,0,0)
        fb_surface = font.render(feedback, True, fb_color)
        screen.blit(fb_surface, (W//2 - fb_surface.get_width()//2, input_box.y + 50))

    round_surface = font.render(f"Round {current_round} / {rounds}", True, (200,200,200))
    screen.blit(round_surface, (10,10))

    pygame.display.flip()
    clock.tick(30)

screen.blit(background_img, (25,0))
end_surface = font.render(f"Quiz finished! Score: {score}/{rounds}", True, (255,255,255))
screen.blit(end_surface, (W//2 - end_surface.get_width()//2, H//2))

game_data = {
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    "rounds": rounds,
    "score": score
}


with open(SAVE_PATH, "a", encoding="utf-8") as f:
    f.write(json.dumps(game_data) + "\n")

pygame.display.flip()
pygame.time.wait(3000)
pygame.quit()
