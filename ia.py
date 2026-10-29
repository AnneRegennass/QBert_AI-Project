from random import *
from jeu import *
import torch
import torch.nn as nn
import torch.nn.functional as F 


EPS_MIN = 0.05
EPS_DECAY = 0.9995
class DQN(nn.Module):
    def __init__(self, input_size=12, output_size=4):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, output_size)
        )
    def forward(self, x): # permet au réseau de ne pas rester linéaire
        return self.net(x) # retourne 4 nombres qui correspondent à chaque action (les scores pour chaque action)

model = DQN()
try:
    model.load_state_dict(torch.load("dqn_qbert.pth"))
    # Mode évaluation si on a un document qui a enregistré d'anciennes parties
    model.eval()  
except FileNotFoundError:
    print("Modèle pré-entraîné non trouvé, démarrage avec un modèle aléatoire.")

# Encode l'état actuel en un tenseur (position du bonhomme, cases qui l'entourent, invincibilité, positions des ennemis)
def encodeEtat(grille, position):
    px = position[0][0][0]
    py = position[0][0][1]
    inv = position[0][1] * 50
    g = grille[px][py-1]*100 if py > 0 else -5
    d = grille[px][py+1]*100    if py <= px else -5
    h = grille[px+1][py]*100   if px +1 < len(grille) else -5
    b = grille[px-1][py]*100  if px > 0 and py <= px - 1 else -5
    lr = len(position[1])
    r1x = px - position[1][0][0] if lr >=1 else 0
    r1y = py - position[1][0][1] if lr >=1 else 0
    r2x = px - position[1][1][0] if lr >=2 else 0
    r2y = py - position[1][1][1] if lr >=2 else 0
    ls = len(position[2])
    tserpent = position[2][0][3] if ls >=1 else 0
    xserpent = px - position[2][0][0] if ls >=1 else 0
    yserpent = py - position[2][0][1] if ls >=1 else 0
    return torch.tensor([h,b,g,d,inv,r1x,r1y,r2x,r2y,tserpent,xserpent,yserpent], dtype=torch.float32)


def mouvementIA(grille, position, state,eps):
    sta = encodeEtat(grille, position)
    # Pour permettre l'exploration de l'IA, qu'elle ne tourne pas en rond dans ce qu'elle connaît déjà
    if random() < eps:
        action = randint(0,3)
    else :
        with torch.no_grad():
            q_values = model(sta)
            action = torch.argmax(q_values).item()
    if eps > EPS_MIN:
        eps *= EPS_DECAY
    pos, state = mouvementBonhomme(position, action, state)
    return pos, state, action, eps





