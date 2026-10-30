<p align="center">
  🌐 <b>Select language / Choisir la langue :</b><br>
  <a href="#lang-en"><b>🇬🇧 English</b></a> • <a href="#lang-fr"><b>🇫🇷 Français</b></a>
</p>

# Q*bert - Deep Q-Network (DQN)

---

<a id="lang-en"></a>
# 🇬🇧 English version

## 📌 Project Overview

This project is a Python-based implementation of the classic arcade game **Q*bert**, featuring an AI agent trained via **Deep Q-Learning (DQN)** with **PyTorch**.

The agent autonomously learns to navigate the isometric pyramid, change cube colors, and avoid enemies (such as snakes and red balls) while utilizing flying discs for teleportation.

Developed as an academic project, its main objective is to explore **Deep Reinforcement Learning (DRL)**, evaluate neural network design decisions, and optimize agent decision-making in a discrete state-action space environment.

---

## 🧠 AI Architecture & Rationale

The agent's decision-making system relies on a **Deep Q-Network (DQN)** architecture:

* **Inputs (12 features):** Encoded state representing:
  * Immediate neighboring tiles (Up, Down, Left, Right).
  * Relative positions of active enemies (Coily, falling red balls).
  * Player state (e.g., invincibility status, position on the board).
* **Hidden Layers:** 3 Fully Connected (Linear) layers:
  * Structure: `128 → 256 → 128` neurons with **ReLU** activation functions.
* **Outputs (4 neurons):** Estimated Q-values for the 4 isometric diagonal actions (Top-Left, Top-Right, Bottom-Left, Bottom-Right).

### Why these Hyperparameters & Network Choices?

* **Fully Connected Layers (MLP) over CNNs:** Since the visual environment can be simplified into exact spatial coordinates and relative positions, using a 12-feature vector input significantly reduces computational complexity compared to feeding raw image frames into a Convolutional Neural Network (CNN). This allows for dramatically faster training while maintaining strong policy convergence.
* **Layer Sizing (128 → 256 → 128):** The bottleneck-like expansion and reduction allow the model to learn non-linear spatial relationships between Q*bert and moving hazards before collapsing them down to 4 actionable directional Q-values.
* **Epsilon-Greedy Strategy:** Balances exploration (random actions) and exploitation (using trained weights). Decay ensures the agent slowly transitions from random trials to strategic play.
* **Replay Buffer (Capacity: 20,000):** Stores transition tuples $(s, a, r, s')$ to break temporal correlation between consecutive frames during mini-batch sampling.
* **Batch Size (128):** Balances gradient stability and GPU memory throughput during backpropagation.

---

## 🎮 Game Modes

The application supports two runtime environments:

1. **Headless Mode (`--headless`):** Runs the game without GUI rendering to drastically speed up training iterations and experience accumulation.
2. **Graphical Mode (Pygame):** Renders the visual environment to evaluate performance or play manually.
   * Press **`J`**: Switch to Manual Mode (Human control).
   * Press **`I`**: Switch to Demonstration Mode (AI plays using loaded model weights).

---

## 🕹️ Controls (Manual Mode)

Movement mimics isometric diagonals:

* **`E`**: Top-Left
* **`R`**: Top-Right
* **`S`**: Bottom-Left
* **`D`**: Bottom-Right

---

## 📂 File Structure

* **`main.py`:** Application entry point, main loop execution, and DQN training loop logic.
* **`jeu.py`:** Game engine, physics, collision detection, entity behaviors, and state encoding.
* **`dqn_qbert.pth`:** Saved PyTorch model checkpoint (generated/updated during training).
* **`assets/` or `*.png`:** Graphic sprites for Pygame interface rendering.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* PyTorch
* Pygame
* NumPy

### Installation & Execution

```bash
# Create a virtual environment
python3 -m venv C:/path/to/new/virtual/environment

# Activate your virtual environment
source C:/path/to/new/virtual/environment/bin/activate

# Install dependencies
pip install torch pygame numpy

# Run graphical evaluation
python3 main.py

# Run fast training mode
python3 main.py --headless
```
<p align="right">
  <a href="#top">⬆️ <b>Back to top</b></a>
</p>

---

<a id="lang-fr"></a>
# 🇫🇷 Version Français

## 📌 Présentation du Projet

Ce projet est une implémentation complète en **Python** du jeu d'arcade classique **Q*bert**, intégrant un agent autonome entraîné par **Apprentissage par Renforcement Profond (Deep Q-Learning - DQN)** avec **PyTorch**.

L'agent apprend par lui-même à colorier l'intégralité de la pyramide tout en évitant les ennemis (serpents, boules rouges) et en exploitant intelligemment les téléporteurs.

Réalisé dans un cadre académique, l'objectif principal de ce projet est d'étudier l'application des réseaux de neurones au contrôle séquentiel, de justifier les choix d'architecture réseau et d'analyser le compromis exploration/exploitation.

---

## 🧠 Architecture de l'IA & Choix Techniques

L'intelligence artificielle repose sur une architecture **Deep Q-Network (DQN)** :

* **Entrées (12 variables) :** État de l'environnement encodé vectoriellement :
  * État des cases adjacentes (Haut, Bas, Gauche, Droite).
  * Position relative des ennemis dangereux.
  * Statut du joueur (ex: position sur la grille, invincibilité).
* **Couches cachées :** 3 couches linéaires interconnectées :
  * Structure : `128 → 256 → 128` neurones avec activations **ReLU**.
* **Sorties (4 neurones) :** Prédictions des Q-values pour les 4 déplacements diagonaux possibles.

### Pourquoi ces choix d'architecture et de paramètres ?

* **Vecteur d'état vs Réseau Convolutif (CNN) :** Plutôt que d'alimenter un CNN avec les images brutes du jeu (coûteux en calcul), l'état du jeu est résumé sous forme de features spatiales directes. Cela réduit drastiquement la complexité computationnelle, permettant un entraînement rapide et une meilleure convergence.
* **Dimensionnement des couches (128 → 256 → 128) :** La montée en capacité à 256 neurones permet de modéliser les relations spatiales complexes entre Q*bert et plusieurs entités mobiles avant de projeter ces informations vers la prise de décision (4 actions).
* **Stratégie Epsilon-Greedy :** Assure une phase d'exploration (actions aléatoires) au début pour découvrir la carte, puis favorise progressivement l'exploitation des connaissances acquises.
* **Replay Memory (Capacité 20 000) :** Stocke les expériences passées $(s, a, r, s')$ et tire des mini-batchs aléatoires pour casser la corrélation temporelle entre étapes successives.
* **Batch Size (128) :** Assure un bon équilibre entre la stabilité de la descente de gradient et la vitesse d'exécution sur GPU/CPU.

---

## 🎮 Modes de Jeu

Le programme propose deux modes de fonctionnement :

1. **Mode Headless (`--headless`) :** Entraînement accéléré sans rendu graphique. L'IA joue à grande vitesse pour accumuler de l'expérience et ajuster ses poids.
2. **Mode Graphique (Pygame) :** Permet d'observer le comportement de l'IA ou de jouer manuellement.
   * **Touche `J`** : Mode Manuel (Humain).
   * **Touche `I`** : Mode Démonstration (L'IA contrôle le personnage avec les poids du modèle chargé).

---

## 🕹️ Contrôles (Mode Manuel)

Les déplacements simulent l'axe isométrique du jeu :

* **`E`** : Haut-Gauche
* **`R`** : Haut-Droite
* **`S`** : Bas-Gauche
* **`D`** : Bas-Droite

---

## 📂 Structure des Fichiers

* **`main.py` :** Point d'entrée de l'application, gestion de la boucle d'entraînement et de jeu.
* **`jeu.py` :** Moteur de jeu, physique, détection de collisions et encodage de l'état.
* **`dqn_qbert.pth` :** Sauvegarde des poids PyTorch du modèle entraîné.
* **`assets/` ou `*.png` :** Sprites et éléments visuels pour l'affichage Pygame.

---

## 🚀 Installation & Lancement

```bash
# Créer un environnement virtuel
python3 -m venv C:/chemin/du/nouveau/environnement/virtuel

# Activer votre environnement virtuel
source C:/chemin/du/nouveau/environnement/virtuel/bin/activate

# Installer les dépendances
pip install torch pygame numpy

# Lancer le jeu / mode démonstration
python3 main.py

# Lancer l'entraînement rapide sans interface
python3 main.py --headless
```
<p align="right">
  <a href="#top">⬆️ <b>Retour en haut</b></a>
</p> 