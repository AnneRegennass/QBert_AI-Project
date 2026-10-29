import copy
import pygame
import sys
from collections import deque
import random
from jeu import *
from ia import *



HEADLESS = "--headless" in sys.argv
game_state = {"score": 0}


EPS = 0.9     # Epsilon initial pour l'exploration
GG = 20       # Gain pour une partie gagnée
MAX_DEP = 150 # Pour obliger l'IA a coloré



# --- Paramètres et fonction pour l'IA ---

optimizer = torch.optim.Adam(model.parameters(), lr=0.00001)


MEMORY_SIZE = 20000   # Taille de la mémoire de l'IA
BATCH_SIZE = 128      # Taille des batchs pour l'entraînement
memory = deque(maxlen=MEMORY_SIZE)

def train_step_batch():
    if len(memory) < BATCH_SIZE:
        return
    
    # On tire 128 souvenirs au hasard
    batch = random.sample(memory, BATCH_SIZE)

    states = []
    actions = []
    rewards = []
    next_states = []
    dones = []

    # Pour faire ne pas faire 128 batch séparés
    for state, action, reward, next_state, done in batch: 
        states.append(state)
        next_states.append(next_state)
        actions.append(action)
        rewards.append(reward)
        dones.append(done)

    states = torch.stack(states)           # Déjà un tenseur
    next_states = torch.stack(next_states) # Déjà un tenseur
    actions = torch.tensor(actions)
    rewards = torch.tensor(rewards, dtype=torch.float32)
    dones = torch.tensor(dones, dtype=torch.bool)

    # Entraînement du modèle
    model.train()
    q_values = model(states)
    current_q = q_values.gather(1, actions.unsqueeze(1)).squeeze()

    with torch.no_grad():
        next_q = target_model(next_states).max(1)[0]
        target_q = rewards + 0.95 * next_q * (~dones)

    loss = F.mse_loss(current_q, target_q)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


# --- Fonction pour l'affichage ---

# Pour afficher les cubes sur l'interface
def affiche_cube(colo,cj,cb,tour):
    pas = 64
    for i in range(8):
        for j in range(1,i+3):
            x, y = 600 - pas*i + 2*pas*j, 100 + i*88
            if colo[i][j-1] == 0:
                fenetre.blit(cj, (x, y))
            elif colo[i][j-1] == 1:
                fenetre.blit(cb, (x, y))
            elif colo[i][j-1] == 2 and j == 1:
                fenetre.blit(tour, (x+50, y-30))
            elif colo[i][j-1] == 2:
                fenetre.blit(tour, (x+30, y-30))

def affiche_perso(pos,perso,brouge,brose,serp,bverte):
    pas = 64
    x = 700 - pas + 2*pas
    y = 12
    fenetre.blit(perso, (x - pas*pos[0][0][0] + 2*pas*pos[0][0][1], y + pos[0][0][0]*88))
    for i in pos[1]:
        fenetre.blit(brouge, (x - pas*i[0] + 2*pas*i[1], y + i[0]*88))
    for i in pos[2]:
        if i[2] == 0:
            fenetre.blit(brose, (x - pas*i[0] + 2*pas*i[1], y + i[0]*88))
        else : 
            fenetre.blit(serp, (x - pas*i[0] + 2*pas*i[1], y + i[0]*88))
    for i in pos[3]:
        fenetre.blit(bverte, (x - pas*i[0] + 2*pas*i[1], y + i[0]*88))


# --- Boucle principale en mode headless pour entraîner l'IA et non headless pour lancer l'interface ---

colo_cube, pos, nbVie, t, tDepart, tpsEnnemisTouches = initJeu()

if HEADLESS:
    import random
    eps = EPS
    eps = 0.07 # A commenter si l'IA n'a pas appris
    tour = 0
    partie_count = 0
    best_score = 0
    hab_score = 0
    win = 0
    # Pour avoir un réseau cible stable
    target_model = copy.deepcopy(model) 
    for step in range(300000):
        x = pos[0][0][0]
        y = pos[0][0][1]

        # Avant le mouvement de l'IA
        state = encodeEtat(colo_cube, pos)
        pos,game_state,mouv, eps = mouvementIA(colo_cube, pos, game_state, eps)
        init_score = game_state["score"]
        # Pour coller à la vitesse du jeu
        for _ in range(DELAISIA):
            colo_cube, pos, nbVie, t, tDepart, tpsEnnemisTouches = majGame(
                colo_cube, pos, nbVie, t, tDepart, game_state, tpsEnnemisTouches
            )
            if nbVie == -1 or partieGagnee(colo_cube):
                break

        # Après le mouvement de l'IA
        next_state = encodeEtat(colo_cube, pos)

        # Pour que l'IA n'abuse pas des déplacements inutiles
        if (game_state["score"]-init_score == DEPLACEMENT):
            hab_score += 1
        else:
            hab_score = 0
        if(hab_score >= 8):
            game_state["score"] -= 0.05
            hab_score = 0

        # Pour forcer la fin de partie si trop de déplacements
        if tour >= MAX_DEP:
            done = True
            game_state["score"] -= 10
        else :
            done = False
        tour += 1

        # Mise à jour du modèle cible toutes les 1000 étapes
        if (step % 1000) == 0:
            target_model.load_state_dict(model.state_dict())

        # Gestion de la fin de partie si perdue ou gagnée
        if nbVie == -1 or tour >= MAX_DEP :
            tour = 0
            if(win > 0):
                win -= 1
            partie_count += 1
            print("Perdu , Step:", step, "Score:", game_state["score"], "Eps:", eps)
            colo_cube, pos, nbVie, t, tDepart, tpsEnnemisTouches = initJeu()
            if (game_state["score"] > best_score and game_state["score"] > 5) or game_state["score"] > 15:
                best_score = game_state["score"]
                torch.save(model.state_dict(), "dqn_qbert.pth")
            game_state["score"] = 0
            
        if partieGagnee(colo_cube):
            game_state["score"] += GG
            win += 20
            partie_count += 1
            print("Partie gagnée! Score:", game_state["score"])
            torch.save(model.state_dict(), "dqn_qbert.pth")
            memory.append((state, mouv, game_state["score"]-init_score, next_state, True))
            colo_cube, pos, nbVie, t, tDepart, tpsEnnemisTouches = initJeu()
            print("gg\n")
            torch.save(model.state_dict(), "dqn_qbert.pth")
            target_model.load_state_dict(model.state_dict())

            for _ in range(10):
                train_step_batch()
            eps = max(eps * 0.995, 0.001)
            if(win > 100):
                eps = 0
            game_state["score"] = 0
        else:
            if(win == 0):
                if nbVie == -1:
                    memory.append((state, mouv, game_state["score"]-init_score, next_state, True))
                else:
                    memory.append((state, mouv, game_state["score"]-init_score, next_state, done))
        if(step % 4 == 0):
            train_step_batch()

            
# --- Initialisation de Pygame ---
else:
    pygame.init()
    # --- Création de la fenêtre ---
    LARGEUR, HAUTEUR = 1600, 1600
    fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Q*bert")

    cube_jaune = pygame.image.load("Sprites/Cube.png").convert_alpha()
    cube_bleu = pygame.image.load("Sprites/Cube2.png").convert_alpha()
    tour = pygame.image.load("Sprites/tourne.png").convert_alpha()
    brose = pygame.image.load("Sprites/boule_rose.png").convert_alpha()
    brouge = pygame.image.load("Sprites/boule_rouge.png").convert_alpha()
    bverte = pygame.image.load("Sprites/boule_verte.png").convert_alpha()
    serp = pygame.image.load("Sprites/serpent.png").convert_alpha()
    perso = pygame.image.load("Sprites/Q*bert.png").convert_alpha()
    perso_inv = pygame.image.load("Sprites/Q*bert_inv.png").convert_alpha()
    go = pygame.image.load("Sprites/game_over.jpg").convert_alpha()
    
    game = 0

    while game == 0 :
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j :
                    game = 1
                elif event.key == pygame.K_i :
                    game = 2
    
    if game == 1 :
        # --- Boucle principale ---
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s :
                        pos, game_state = mouvementBonhomme(pos, 2, game_state)
                    elif event.key == pygame.K_d :
                        pos, game_state = mouvementBonhomme(pos, 1, game_state)
                    elif event.key == pygame.K_e :
                        pos, game_state = mouvementBonhomme(pos, 0, game_state)
                    elif event.key == pygame.K_r :
                        pos, game_state = mouvementBonhomme(pos, 3, game_state)

            colo_cube, pos, nbVie, t, tDepart, tpsEnnemisTouches = majGame(colo_cube, pos, nbVie, t, tDepart,game_state, tpsEnnemisTouches)

            fenetre.fill((0, 0, 0))  # Couleur de fond (noir ici)
            if nbVie == -1 :
                # Game Over
                fenetre.blit(go, (20, 20))
                pygame.time.wait(3000)
                print(game_state["score"])
                pygame.quit()
                sys.exit()

            if partieGagnee(colo_cube) :
                # Fin de partie, on réinitialise la grille en conservant le nombre de vie et le score
                nbVieBis = 0
                colo_cube, pos, nbVieBis, t, tDepart, tpsEnnemisTouches = initJeu()

            affiche_cube(colo_cube,cube_jaune,cube_bleu,tour)
            if pos[0][1] == 0:
                affiche_perso(pos,perso,brouge,brose,serp,bverte)
            else :
                affiche_perso(pos,perso_inv,brouge,brose,serp,bverte)

            font_vie = pygame.font.Font(None, 74)
            texte = font_vie.render(str(nbVie), True, (255, 255, 255))
            fenetre.blit(texte, (170, 100))


            # Mise à jour de l'affichage
            pygame.display.flip()
            # Limite la boucle à 60 images/seconde
            clock.tick(60)

    elif game == 2 :
        # --- Boucle principale ---
        clock = pygame.time.Clock()
        # Pour que l'IA ne joue pas trop vite (à la vitesse d'un joueur humain)
        tIA = DELAISIA
        EPS = 0
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if tIA == 0 :
                position, game_state, action, eps = mouvementIA(colo_cube, pos, game_state, 0)
                tIA = DELAISIA

            else :
                tIA -=1

            colo_cube, pos, nbVie, t, tDepart, tpsEnnemisTouches = majGame(colo_cube, pos, nbVie, t, tDepart,game_state, tpsEnnemisTouches)

            fenetre.fill((0, 0, 0))
            if nbVie == -1 :
                # Game Over
                fenetre.blit(go, (20, 20))
                print(game_state["score"])
                colo_cube, pos, nbVie, t, tDepart, tpsEnnemisTouches = initJeu()
                game_state["score"] = 0

            if partieGagnee(colo_cube) :
                # Fin de partie, on réinitialise la grille en conservant le nombre de vie et le score
                print("partie gagnée", game_state["score"])
                nbVieBis = 0
                colo_cube, pos, nbVieBis, t, tDepart, tpsEnnemisTouches = initJeu()

            affiche_cube(colo_cube,cube_jaune,cube_bleu,tour)
            if pos[0][1] == 0:
                affiche_perso(pos,perso,brouge,brose,serp,bverte)
            else :
                affiche_perso(pos,perso_inv,brouge,brose,serp,bverte)

            font_vie = pygame.font.Font(None, 74)
            texte = font_vie.render(str(nbVie), True, (255, 255, 255))
            fenetre.blit(texte, (170, 100))


            # Mise à jour de l'affichage
            pygame.display.flip()
            # Limite la boucle à 90 images/seconde
            clock.tick(90)
