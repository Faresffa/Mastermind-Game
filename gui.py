#voir la video youtube enregistré sur la bib stark
#voir c'est quoi le probleme de l'execution infinie 
#continuer le code 
import pygame
from main import generate_win_combination, compare_combinations, COLORS, LENGTH, TRIES

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mastermind")

# Couleurs Pygame
COLOR_MAP = {
    'r': (255, 0, 0),  # Rouge
    'b': (0, 0, 255),  # Bleu
    'g': (0, 255, 0),  # Vert
    'w': (255, 255, 255),  # Blanc
    'y': (255, 255, 0),  # Jaune
    'o': (255, 165, 0)  # Orange
}
BACKGROUND_COLOR = (210, 180, 140)
TEXT_COLOR = (0, 0, 0)

# Autres constantes
FONT = pygame.font.SysFont("Arial", 24)
LARGE_FONT = pygame.font.SysFont("Arial", 36)

def draw_difficulty_selection():
    """Affiche l'écran de sélection de difficulté."""
    screen.fill(BACKGROUND_COLOR)

    # Diviser l'écran en deux sections
    pygame.draw.rect(screen, (255, 100, 100), (0, 0, WIDTH // 2, HEIGHT))  # Côté gauche (Hard)
    pygame.draw.rect(screen, (100, 255, 100), (WIDTH // 2, 0, WIDTH // 2, HEIGHT))  # Côté droit (Easy)

    # Ajouter le texte
    hard_text = LARGE_FONT.render("HARD", True, TEXT_COLOR)
    easy_text = LARGE_FONT.render("EASY", True, TEXT_COLOR)
    screen.blit(hard_text, (WIDTH // 4 - hard_text.get_width() // 2, HEIGHT // 2 - hard_text.get_height() // 2))
    screen.blit(easy_text, (3 * WIDTH // 4 - easy_text.get_width() // 2, HEIGHT // 2 - easy_text.get_height() // 2))

    pygame.display.update()

def handle_difficulty_click(pos):
    """Détecte les clics pour choisir la difficulté."""
    x, _ = pos
    if x < WIDTH // 2:
        return 'hard'
    else:
        return 'easy'

def draw_board(attempts, current_colors, feedback, selected_color):
    """Affiche le plateau de jeu avec un tableau structuré."""
    screen.fill(BACKGROUND_COLOR)  # Fond

    # Dessiner le tableau des essais
    table_x = 200
    table_y = 10
    cell_width = 100
    cell_height = 40

    # Dessiner les lignes et colonnes
    for i in range(TRIES):
        for j in range(LENGTH):
            rect_x = table_x + j * cell_width
            rect_y = table_y + i * cell_height
            pygame.draw.rect(screen, (200, 200, 200), (rect_x, rect_y, cell_width, cell_height), 1)

            # Remplir la case avec la couleur si elle existe
            if i < len(attempts) and j < len(attempts[i]):
                color = attempts[i][j]
                pygame.draw.circle(screen, COLOR_MAP[color], (rect_x + cell_width // 2, rect_y + cell_height // 2), 15)

    # Afficher les couleurs en cours de sélection
    for j, color in enumerate(current_colors):
        pygame.draw.circle(screen, COLOR_MAP[color], (table_x + j * cell_width + cell_width // 2, table_y + len(attempts) * cell_height + cell_height // 2), 15)

    # Affiche la couleur actuellement sélectionnée
    if selected_color:
        pygame.draw.circle(screen, COLOR_MAP[selected_color], (WIDTH - 100, HEIGHT - 150), 30)

    # Affiche les retours
    if feedback:
        feedback_text = f"Bien placés : {feedback[0]} - Mal placés : {feedback[1]}"
        text = FONT.render(feedback_text, True, TEXT_COLOR)
        screen.blit(text, (100, HEIGHT - 50))
    # Calcul de la largeur totale des cercles
    total_width = len(COLORS) * 100

    # Position de départ pour centrer les cercles
    start_x = (WIDTH - total_width) // 2

    # Affiche les couleurs disponibles pour la sélection
    for i, color in enumerate(COLORS):
     pygame.draw.circle(screen, COLOR_MAP[color], (start_x + i * 100, HEIGHT - 100), 20)

    pygame.display.update()

def handle_color_click(pos):
    """Détecte les clics pour sélectionner une couleur."""
    x, y = pos
    if y > HEIGHT - 120:
        index = (x - 50) // 100
        if 0 <= index < len(COLORS):
            return COLORS[index]
    return None

def draw_end_screen(win, win_combination):
    """Affiche l'écran de fin."""
    screen.fill(BACKGROUND_COLOR)
    if win:
        end_text = "Félicitations, vous avez gagné !"
    else:
        end_text = "Désolé, vous avez perdu !"

    text = LARGE_FONT.render(end_text, True, TEXT_COLOR)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))

    # Affiche la combinaison gagnante
    for i, color in enumerate(win_combination):
        pygame.draw.circle(screen, COLOR_MAP[color], (WIDTH // 2 - (LENGTH * 30) + i * 60, HEIGHT // 2), 20)

    # Dessiner les boutons
    quit_button = pygame.Rect(WIDTH // 4 - 50, 3 * HEIGHT // 4, 100, 50)
    retry_button = pygame.Rect(3 * WIDTH // 4 - 50, 3 * HEIGHT // 4, 130, 50)

    pygame.draw.rect(screen, (200, 0, 0), quit_button)
    pygame.draw.rect(screen, (0, 200, 0), retry_button)

    quit_text = FONT.render("Quitter", True, TEXT_COLOR)
    retry_text = FONT.render("Recommencer", True, TEXT_COLOR)

    screen.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))
    screen.blit(retry_text, (retry_button.centerx - retry_text.get_width() // 2, retry_button.centery - retry_text.get_height() // 2))

    pygame.display.update()

    return quit_button, retry_button

def main():
    """Boucle principale du jeu."""
    running = True
    difficulty = None
    win_combination = []
    attempts = []
    current_attempt = []
    feedback = None
    selected_color = None  # Variable pour la couleur sélectionnée

    # Écran de sélection de difficulté
    while running:
        draw_difficulty_selection()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                difficulty = handle_difficulty_click(event.pos)
                if difficulty:
                    win_combination = generate_win_combination(difficulty == 'hard')
                    running = False

    running = True
    win = False
    while running:
        # Passer selected_color à la fonction de dessin
        draw_board(attempts, current_attempt, feedback, selected_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                color = handle_color_click(event.pos)
                if color:
                    selected_color = color  # Mettre à jour la couleur sélectionnée
                    current_attempt.append(color)
                    if len(current_attempt) == LENGTH:
                        well_placed, misplaced = compare_combinations(win_combination, current_attempt)
                        feedback = (well_placed, misplaced)
                        attempts.append(current_attempt)

                        if well_placed == LENGTH:
                            win = True
                            running = False

                        current_attempt = []

        # Conditions de fin
        if len(attempts) >= TRIES and not win:
            running = False

    quit_button, retry_button = draw_end_screen(win, win_combination)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    return
                elif retry_button.collidepoint(event.pos):
                    main()

if __name__ == "__main__":
    main()
