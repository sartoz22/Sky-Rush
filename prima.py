import pygame
import random
import os
import sys

# =========================
# INIZIALIZZAZIONE PYGAME
# =========================
pygame.init()

# Dimensioni finestra di gioco ALLARGATA
LARGHEZZA = 480
ALTEZZA = 720

screen = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Sky Rush")

clock = pygame.time.Clock()
