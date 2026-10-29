import random as rd
import time as tps

TIMER = 300
FINJEU = False

TPSENNEMIS = 60
PROCSERPENT = 1/8
PROCBALLER = 1/3
PROCBALLEV = 1/4

NBSERPENTSMAX = 1
NBBALLERMAX = 3
NBBALLEVMAX = 1

TDEPART = 120
TPSENNEMISELIMINE = 60

JUMPLIFE = 0.2
ENNEMILIFE = 0.05
NBPOINTCASE = 0.5
NBPOINTSERPENT = 0
NBPOINTSBOULER = 0
DEPLACEMENT = 0.005

DELAISIA = 30

def initJeu():
    '''
    initialise le jeu
    :param entrée: void
    :param sortie:  grille : grille de jeu
                    positions : liste des positions :   positions[0] coordonnées du perso jouable + état (0 = normal ou 1 = invisible avec balle)
                                                        positions[1] liste des coordonnées des balles rouges
                                                        positions[2] coordonnées du serpent et état du serpent (balle ou serpent)
                                                        positions[3] liste des coordonnées des balles vertes (bonus)
    '''
    nbVies = 3 
    grille = [  [-1,-1],
                [-1,0,-1], 
                [-1,0,0,-1], 
                [-1,0,0,0,-1], 
                [ 2,0,0,0,0,2 ], 
                [-1,0,0,0,0,0,-1], 
                [-1,0,0,0,0,0,0,-1], 
                [-1,0,0,0,0,0,0,0,-1], 
                [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1] ]
    
    positions = [[[1,1],0], [], [], []]
    tDepart = TDEPART
    tpsEnnemisTouches = TPSENNEMISELIMINE
    return grille, positions, nbVies, 0, tDepart, tpsEnnemisTouches

def mouvementBalle(position, numBalle, colo):
    '''
    Fait bouger la balle donnée en paramètre
    :param entrée: coordonnées de la balle à bouger (xballe, yballe)
    :param entrée: colo = 1 si boule ennemis rouge, 3 si boule alliée verte
    :param sortie: (x,y) : nouvelles coordonnées de la balle
    '''
    # On vérifie si l'une ou l'autre des cases est libre
    if caseLibre(position, position[colo][numBalle][0]+1, position[colo][numBalle][1]):
        if caseLibre(position, position[colo][numBalle][0]+1, position[colo][numBalle][1]+1):
            # si les deux sont libres :
            if position[colo][numBalle][1] != 7 :
                position[colo][numBalle][0] +=1
                direction = rd.uniform(0,1)
                if direction > 0.5 :
                    position[colo][numBalle][1] += 1
            position[colo][numBalle][2] = TPSENNEMIS
            return position
        else :
            position[colo][numBalle][0] +=1
            position[colo][numBalle][2] = TPSENNEMIS
            return position
    else :
        if caseLibre(position, position[colo][numBalle][0]+1, position[colo][numBalle][1]+1):
            position[colo][numBalle][0] +=1
            position[colo][numBalle][1] += 1
            position[colo][numBalle][2] = TPSENNEMIS
            return position
        else:
            return position

def disparitionBalle(position, colo):
    l = len(position[colo])
    i = 0
    while i < l :
        if position[colo][i][0] == 8 :
            position[colo].pop(i)
            l -= 1
        else :
            i +=1  
    return position

def apparitionBalle(positions, colo):
    '''
    Gérère l'apparition d'une nouvelle balle
    :param d'entrée: void
    :param sortie: grille des positions mise à jour
    '''
    if caseLibre(positions,2,1):
        if caseLibre(positions, 2,2):
            pos = rd.uniform(0,1)
            if pos > 0.5:
                positions[colo].append([2,2,TPSENNEMIS])
            else:
                positions[colo].append([2,1,TPSENNEMIS])
        else :
            positions[colo].append([2,1,TPSENNEMIS])
    else :
        if caseLibre(positions, 2,2):
            positions[colo].append([2,2,TPSENNEMIS])
    return positions

def apparitionSerpent(positions):
    '''
    Gérère l'apparition d'unnouveau serpent
    :param d'entrée: void
    :param sortie: grille des positions mise à jour
    '''
    if caseLibre(positions,2,1):
        if caseLibre(positions, 2,2):
            pos = rd.uniform(0,1)
            if pos > 0.5:
                positions[2].append([2,2,0,TPSENNEMIS])
            else:
                positions[2].append([2,1,0,TPSENNEMIS])
        else :
            positions[2].append([2,1,0,TPSENNEMIS])
    else :
        if caseLibre(positions, 2,2):
            positions[2].append([2,2,0,TPSENNEMIS])
    return positions

def mouvementSerpent(position, numSerpent):
    if position[2][numSerpent][2] == 0 :
        if position[2][numSerpent][0] == 7 :
            position[2][numSerpent][2] = 1
        else :
            if caseLibre(position, position[2][numSerpent][0]+1, position[2][numSerpent][1]):
                if caseLibre(position, position[2][numSerpent][0]+1, position[2][numSerpent][1]+1):
                    position[2][numSerpent][0] +=1
                    direction = rd.uniform(0,1)
                    if direction > 0.5 :
                        position[2][numSerpent][1] +=1
                else :
                    position[2][numSerpent][0] +=1
            else :
                if caseLibre(position, position[2][numSerpent][0]+1, position[2][numSerpent][1]+1):
                    position[2][numSerpent][0] +=1
                    position[2][numSerpent][1] +=1
                else :
                    return position   
    else :
        serpentSuit(position, numSerpent)
    position[2][numSerpent][3] = TPSENNEMIS
    return position

def estMort(positions, grille, nbVie):
    '''
    return 0 si mort par le vide, 1 si mort par un ennemis
    '''
    if positions[0][1] == 0 :
        # si le bonhomme n'est pas invincible
        for i in range(len(positions[1])):
            if positions[0][0][0] == positions[1][i][0] and positions[0][0][1] == positions[1][i][1] :
                nbVie -= 1
                return True, nbVie, 1
        for i in range(len(positions[2])):
            if positions[0][0][0] == positions[2][i][0] and positions[0][0][1] == positions[2][i][1]:
                nbVie -= 1
                return True, nbVie, 1
    if grille[positions[0][0][0]][positions[0][0][1]]==-1:
        nbVie -= 1 
        return True, nbVie, 0
    if positions[0][0][1]>8:
        nbVie -= 1
        return True, nbVie, 0
    return False, nbVie, 0

def mouvementTeleport(grille, position):
    grille[position[0][0][0]][position[0][0][1]] = -1
    grille [1][1] = 1
    position[0][0][0] = 1
    position[0][0][1] = 1
    return grille, position

def mouvementBonhomme(position, mouv,state):
    '''
    mouv = 0 pour haut, 1 pour bas, 2 pour gauche, 3 pour droite
    '''
    match mouv :
        case 0 :
            position[0][0][0] -= 1
            position[0][0][1] -= 1
        case 1 :
            position[0][0][0] += 1
            position[0][0][1] += 1
        case 2 :
            position[0][0][0] += 1
        case 3 :
            position[0][0][0] -= 1
    return position, state

def serpentSuit(position, numSerpent):
    distx = position[2][numSerpent][0]-position[0][0][0]
    disty = position[2][numSerpent][1]-position[0][0][1]
    if abs(distx)>abs(disty):
        if distx>=0 and position[2][numSerpent][0]-1 > 0 and caseLibre(position, position[2][numSerpent][0]-1, position[2][numSerpent][1]):
                    position[2][numSerpent][0] -= 1
        else :
            if position[2][numSerpent][0]+1 < 8 and caseLibre(position, position[2][numSerpent][0]+1, position[2][numSerpent][1]):
                    position[2][numSerpent][0] += 1
    else :
        if disty>=0 and position[2][numSerpent][1]-1 > 0 and caseLibre(position, position[2][numSerpent][0], position[2][numSerpent][1]-1):
                if 1<=position[2][numSerpent][1]-1<=position[2][numSerpent][0]-1 :
                    position[2][numSerpent][1] -= 1
                    position[2][numSerpent][0]-=1
        else :
            if position[2][numSerpent][1]+1 < position[2][numSerpent][0]+1 <8 and caseLibre(position, position[2][numSerpent][0],position[2][numSerpent][1]+1):
                position[2][numSerpent][1] += 1
                position[2][numSerpent][0] +=1
    return position

def contactBonhomme(position, t, tpsEnnemisTouches, state):
    for i in range (len(position[3])):
        if position[3][i][0] == position[0][0][0] and position[3][i][1] == position[0][0][1]:
            # Le joueur attrape une boule verte
            position[0][1] = 1
            t = TIMER # temps d'invincibilité
            position[3].pop(i)
            return position, t , tpsEnnemisTouches, state
    # On traite ici que les contacts quand le joueur élimine les ennemis, 
    # les autres sont traité lorsqu'on vérifie la mort
    if position[0][1] == 1 :
        for i in range (len(position[1])) :
            if position[1][i][0] == position[0][0][0] and position[1][i][1] == position[0][0][1] :
                position[1].pop(i)
                state["score"]+= NBPOINTSBOULER
                return position, t , TPSENNEMISELIMINE, state
        for i in range (len(position[2])) :
            if position[2][i][0] == position[0][0][0] and position[2][i][1] == position[0][0][1] :
                position[2].pop(i)
                state["score"]+= NBPOINTSERPENT
                return position, t , TPSENNEMISELIMINE, state
    return position, t , tpsEnnemisTouches, state

def caseLibre(position, x, y):
    '''
    :param entrée:  grille des positions
                    x de la case que l'on vérifie
                    y de la case que l'on vérifie
    :param sortie:  bool si la case est libre ou non
    '''
    for i in position[1]:
        if i[0]==x and i[1]==y:
            return False
    for i in position[2]:
        if i[0]==x and i[1]==y:
            return False
    for i in position[3]:
        if i[0]==x and i[1]==y:
            return False
    return True

def majEtat(position, t):
    if t == 0 and position[0][1] == 1 :
        position[0][1] = 0
        return position

def majGame (grille, position, nbVie, t, tDepart, state, tpsEnnemisTouches):
    if position[0][0][0]>0 and position[0][0][0]<8 and position[0][0][1]>0 and position[0][0][1] < 8 :
        if grille[position[0][0][0]][position[0][0][1]] == 0 :
            # Mise à jour de la couleur d'une case
            grille[position[0][0][0]][position[0][0][1]] = 1
            state["score"] += NBPOINTCASE
        else :
            if state["score"] > 0 :
                state["score"] += DEPLACEMENT 
        
    
    majEtat(position, t)
    if t!=0:
        t -= 1

    if tpsEnnemisTouches!=0:
        tpsEnnemisTouches-=1
    
    # mouvement des ennemis
    for i in range(len(position[1])) :
        if position[1][i][2] == 0:
            position = mouvementBalle(position, i, 1)
        else :
            position[1][i][2] -= 1 
    position = disparitionBalle(position, 1)

    for i in range(len(position[2])) :
        if position[2][i][3] == 0 :
            position = mouvementSerpent(position, i)
        else :
            position[2][i][3] -= 1 
    
    for i in range(len(position[3])) :
        if position[3][i][2] == 0:
            position = mouvementBalle(position, i, 3)
        else :
            position[3][i][2] -= 1 
    position = disparitionBalle(position, 3)

    position, t, tpsEnnemisTouches, state = contactBonhomme(position, t, tpsEnnemisTouches, state)

    if grille[position[0][0][0]][position[0][0][1]] == 2 :
        grille, position = mouvementTeleport(grille, position)

    # si le bonhomme meurt
    mort, nbVie, typeMort = estMort(position, grille, nbVie)
    if mort :
        if nbVie == 0 :
            state["score"] -= JUMPLIFE
            return grille, position, -1, t, tDepart, tpsEnnemisTouches
        else :
            if typeMort == 0:
                state["score"] -= JUMPLIFE
                position[0] = [[1,1],0]
            else :
                state["score"] -= ENNEMILIFE
                position[0] = [position[0][0], 0]
            position[1] = []
            position[2] = []
            position[3] = []
            t = 0
            return grille, position, nbVie, t, TDEPART, tpsEnnemisTouches

    # On ajoute des ennemis
    if tDepart == 0 : 
        if tpsEnnemisTouches==0 :
            if len(position[1]) < NBBALLERMAX :
                nb = rd.uniform(0,1)
                if nb < PROCBALLER :
                    position = apparitionBalle(position, 1)
            if len(position[3]) < NBBALLEVMAX :
                nb = rd.uniform(0,1)
                if nb < PROCBALLEV :
                    position = apparitionBalle(position, 3)
            if len(position[2]) < NBSERPENTSMAX :
                nb = rd.uniform(0,1)
                if nb < PROCSERPENT :
                    position = apparitionSerpent(position)
    else :
        tDepart -= 1

    return grille, position, nbVie, t, tDepart, tpsEnnemisTouches

def partieGagnee(grille):
    for i in range (8):
        for j in range(i+1):
            if grille[i][j] == 0 :
                return False
    return True
