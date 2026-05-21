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
# =========================
    # SCHERMATA: MENU PRINCIPALE
    # =========================
    if stato == "menu":
        screen.fill(NERO)
        
        titolo = font_grande.render("SKY RUSH", True, CIANO)
        screen.blit(titolo, (LARGHEZZA // 2 - titolo.get_width() // 2, 200))

        best = font.render(f"MIGLIOR PUNTEGGIO: {best_score}", True, BIANCO)
        screen.blit(best, (LARGHEZZA // 2 - best.get_width() // 2, 320))

        info = font.render("Premi SPAZIO per iniziare", True, BIANCO)
        screen.blit(info, (LARGHEZZA // 2 - info.get_width() // 2, 380))

        pygame.display.update()
        continue

    # =========================
    # LOGICA DI GIOCO (Stato Game)
    # =========================
    if stato == "game":
        frame += 1

        # gravità applicata alla coordinata Y del player
        player[2] += gravita
        player[1] += player[2]

        # movimento manuale veloce verso il basso
        if tasti[pygame.K_DOWN]:
            player[1] += 5

        # limiti dello schermo per il player
        if player[1] < 0:
            player[1] = 0
            player[2] = 0

        if player[1] > ALTEZZA - dimensione_player:
            player[1] = ALTEZZA - dimensione_player
            player[2] = 0

        # Movimento nuvole
        for n in nuvole:
            n[0] -= n[2]
            if n[0] < -120:
                n[0] = LARGHEZZA + 50
                n[1] = random.randint(40, 220)

        # Generazione bilanciata ostacoli
        if frame % 75 == 0:
            gap = random.randint(140, 170)  
            altezza_top = random.randint(60, ALTEZZA - gap - 60) 
            ostacoli.append([LARGHEZZA, altezza_top, gap, False])

        # Aggiornamento ostacoli
        for o in ostacoli:
            o[0] -= velocita * 1.4

            # Assegnazione punti al superamento dell'ostacolo
            if not o[3] and o[0] < player[0]:
                o[3] = True
                punteggio += 1
                conta_ostacoli += 1

                if punteggio % 5 == 0:
                    velocita += 0.25

                if conta_ostacoli % 15 == 0:
                    notte = not notte

        # Gestione Collisioni di precisione
        px, py = player[0], player[1]
        for o in ostacoli:
            if px < o[0] + 50 and px + dimensione_player > o[0]:
                if py < o[1] or py + dimensione_player > o[1] + o[2]:
                    crea_particelle(px + dimensione_player//2, py + dimensione_player//2)
                    stato = "gameover"

                    if punteggio > best_score:
                        best_score = punteggio
                        open(FILE_SCORE, "w").write(str(best_score))

        # Rimozione ostacoli vecchi passati a sinistra
        ostacoli = [o for o in ostacoli if o[0] > -100]
        # =========================
    # AGGIORNAMENTO PARTICELLE
    # =========================
    for p in particelle:
        p[0] += p[2]
        p[1] += p[3]
        p[4] -= 1
    particelle = [p for p in particelle if p[4] > 0]

    # =========================
    