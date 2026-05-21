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
# Font per testo normale e grande
font = pygame.font.SysFont("Arial", 22)
font_grande = pygame.font.SysFont("Arial", 50)

# =========================
# COLORI (TUPLE IMMUTABILI)
# =========================
BIANCO = (255, 255, 255)
NERO = (0, 0, 0)
CIANO = (0, 229, 255)
VERDE = (0, 200, 83)
AZZURRO = (79, 195, 247)
SCURO = (5, 8, 20)

# =========================
# BEST SCORE SALVATO SU FILE
# =========================
FILE_SCORE = "best_score.txt"

if os.path.exists(FILE_SCORE):
    try:
        best_score = int(open(FILE_SCORE).read())
    except:
        best_score = 0
else:
    best_score = 0

# =========================
# STATO DEL GIOCO
# =========================
stato = "menu"   # menu / game / gameover
# =========================
# PLAYER (x, y, velocità verticale)
# =========================
player = [70, 320, 0.0]
dimensione_player = 26

gravita = 0.38       # forza che spinge verso il basso
spinta = -6.5        # salto verso l'alto

# =========================
# VARIABILI DI GIOCO
# =========================
punteggio = 0
velocita = 3.5
frame = 0
notte = False
conta_ostacoli = 0

ostacoli = []
particelle = []

# =========================
# STELLE (TUPLE IMMUTABILI)
# =========================
stelle = tuple(
    (random.randint(0, LARGHEZZA),
     random.randint(0, ALTEZZA),
     random.randint(1, 2))
    for _ in range(120)
)

# =========================
# NUVOLE (LISTE MODIFICABILI)
# =========================
nuvole = [
    [random.randint(0, LARGHEZZA),
     random.randint(40, 220),
     random.uniform(0.6, 1.4)]
    for _ in range(7)
]

# =========================
# RESET GIOCO
# =========================
def reset():
    global player, punteggio, velocita, frame, notte, conta_ostacoli
    global ostacoli, particelle

    player = [70, 320, 0.0]
    punteggio = 0
    velocita = 3.5
    frame = 0
    notte = False
    conta_ostacoli = 0
    ostacoli = []
    particelle = []
    
# =========================
# SISTEMA PARTICELLE (EFFETTO MORTE)
# =========================
def crea_particelle(x, y):
    for _ in range(22):
        particelle.append([
            x, y,
            random.uniform(-3, 3),
            random.uniform(-3, 3),
            random.randint(25, 45)
        ])

# =========================
# DISEGNO NUVOLE
# =========================
def disegna_nuvola(x, y, scala):
    pygame.draw.circle(screen, BIANCO, (int(x), int(y)), int(18 * scala))
    pygame.draw.circle(screen, BIANCO, (int(x + 20 * scala), int(y - 10 * scala)), int(22 * scala))
    pygame.draw.circle(screen, BIANCO, (int(x + 45 * scala), int(y)), int(20 * scala))
    pygame.draw.circle(screen, BIANCO, (int(x + 25 * scala), int(y + 10 * scala)), int(22 * scala))

# =========================
# LOOP PRINCIPALE
# =========================
gioco_attivo = True

while gioco_attivo:

    clock.tick(60)

    # =========================
    # EVENTI INPUT
    # =========================
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            gioco_attivo = False

        if evento.type == pygame.KEYDOWN:
            if stato == "menu":
                if evento.key == pygame.K_SPACE:
                    reset()
                    stato = "game"

            elif stato == "gameover":
                if evento.key == pygame.K_r:
                    reset()
                    stato = "game"
                if evento.key == pygame.K_h:
                    stato = "menu"

            elif stato == "game":
                if evento.key == pygame.K_UP:
                    player[2] = spinta

    tasti = pygame.key.get_pressed()
