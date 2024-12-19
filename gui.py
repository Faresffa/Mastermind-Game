#voir la video youtube enregistré sur la bib stark
#voir c'est quoi le probleme de l'execution infinie 
#continuer le code 
# 4h du matin note pour demain en haut 
import pygame
import random
from main import generate_win_combination, get_user_input, compare_combinations, COLORS_TEXT, COLORS, LENGTH, TRIES

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mastermind")

# Couleurs Pygame
COLOR_MAP = {
    'r': (255, 0, 0),  # Rouge
    'b': (0, 0, 255),  # Bleu
    'g': (0, 255, 0),  # Vert
    'w': (255, 255, 255),  # Blanc
    'y': (255, 255, 0),  # Jaune
    'o': (255, 165, 0),  # Orange
}

# Fonction pour dessiner le plateau de jeu
def draw_board(attempts, feedback):
    screen.fill((255, 255, 255))  # Fond blanc

    # Affichage des tentatives
    for i, attempt in enumerate(attempts):
        for j, color in enumerate(attempt):
            pygame.draw.circle(screen, COLOR_MAP[color], (100 + j * 120, 100 + i * 40), 20)

    # Affichage du feedback
    font = pygame.font.SysFont("Arial", 24)
    if feedback:
        feedback_text = f"Bien placées : {feedback[0]} - Mal placées : {feedback[1]}"
        text = font.render(feedback_text, True, (0, 0, 0))
        screen.blit(text, (100, HEIGHT - 50))

    pygame.display.update()

# Fonction pour gérer les clics de souris
def handle_click(pos):
    x, y = pos
    if y > HEIGHT - 80:  # Si le clic est dans la zone des couleurs
        index = (x - 50) // 100
        if 0 <= index < len(COLORS):
            return COLORS[index]
    return None

def main():
    print("Bienvenue au Mastermind avec Pygame!")
    
    # Choisir la difficulté
    while True:
        difficulty = input("Choisissez la difficulté ('easy'  sans doublons, 'hard'  avec doublons) : ").lower()
        if difficulty in ['easy', 'hard']:
            allow_duplicates = (difficulty == 'hard')
            break
        print("Erreur : Veuillez entrer 'easy' ou 'hard'.")

    win_combination = generate_win_combination(allow_duplicates)
    attempts = []
    feedback = None

    # Boucle principale
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                color = handle_click(pygame.mouse.get_pos())
                if color:
                    attempts.append([color])  # Ajouter la couleur sélectionnée

                    # Lorsque l'utilisateur a fait une tentative complète (LENGTH couleurs)
                    if len(attempts) == LENGTH:
                        # Vérifier la combinaison
                        well_placed, misplaced = compare_combinations(win_combination, attempts)
                        feedback = (well_placed, misplaced)
                        
                        if well_placed == LENGTH:
                            print("Félicitations, vous avez trouvé la combinaison secrète !")
                            running = False
                        else:
                            attempts.clear()  # Réinitialiser les tentatives
                            draw_board(attempts, feedback)

        draw_board(attempts, feedback)  # Afficher les tentatives et le feedback

    pygame.quit()

if __name__ == "__main__":
    main()
