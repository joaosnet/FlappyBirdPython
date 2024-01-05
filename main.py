import pygame
import os
import random

# Definindo a tela
TELA_LARGURA = 500
TELA_ALTURA = 800

# Definido imagens
CANO = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
FUNDO = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]

# Definindo fonte
pygame.font.init()
PONTOS = pygame.font.SysFont("arial", 50)