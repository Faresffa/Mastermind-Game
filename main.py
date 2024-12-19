
#------------------------------------MASTERMIND GAME BY-----------------------------------------------------------
#------------------------------------HAFIANE Fares-and-Shaima---------------------------------------------------------------
import random

# Constantes du jeu
COLORS = ['r', 'b', 'g', 'w', 'y', 'o']  # Couleurs disponibles
COLORS_TEXT = {
    'r': 'red',
    'b': 'blue',
    'g': 'green',
    'w': 'white',
    'y': 'yellow',
    'o': 'orange'
}  # Dictionnaire pour afficher les couleurs en texte
LENGTH = 4  # Longueur de la combinaison
TRIES = 10  # Nombre maximum de tentatives

def generate_win_combination(allow_duplicates):
    """Génère une combinaison secrète aléatoire."""
    if allow_duplicates:
        return [random.choice(COLORS) for _ in range(LENGTH)]
    else:
        return random.sample(COLORS, LENGTH)

def get_user_input(difficulty):
    """Demande une saisie utilisateur et la valide."""
    while True:
        user_input = input(
            f"Entrez {LENGTH} noms de couleurs parmi {', '.join(COLORS_TEXT.values())} (séparés par des espaces)(Entrez (quit) si vous voulez abondonnez) : "
        ).lower()
        if user_input == "quit":
            return "quit"

        # Diviser la saisie en mots
        colors = user_input.split()

        # Vérifier le nombre de couleurs saisies
        if len(colors) != LENGTH:
            print(f"Erreur : Vous devez entrer exactement {LENGTH} couleurs.")
            continue

        # Extraire les premières lettres
        first_letters = [color[0] for color in colors]
        #print(first_letters)
        # Vérifier si les lettres sont valides
        if any(letter not in COLORS for letter in first_letters):
            print(f"Erreur : Les couleurs doivent être parmi {', '.join(COLORS_TEXT.values())}.")
            continue

        # Vérifier les doublons en mode easy
        if difficulty == 'easy' and len(set(first_letters)) != LENGTH:
            print("Erreur : Les couleurs ne doivent pas contenir de doublons.")
            continue

        return first_letters

def compare_combinations(win, guess):
    """Compare la combinaison secrète avec celle de l'utilisateur et retourne les indices."""
    well_placed = 0
    misplaced = 0

    win_copy = win[:]
    guess_copy = guess[:]

    # Vérifier les couleurs bien placées
    for current_index in range(LENGTH):
        if guess[current_index] == win[current_index]:
            well_placed += 1
            win_copy[current_index] = guess_copy[current_index] = None

    # Vérifier les couleurs mal placées
    for color in guess_copy:
        if color and color in win_copy:
            misplaced += 1
            win_copy[win_copy.index(color)] = None

    return well_placed, misplaced

def main():
    """Boucle principale du jeu."""
    print("Bienvenue au Mastermind !")
    print("Devinez la combinaison secrète de 4 couleurs.")
    print(f"Les couleurs possibles sont : {', '.join(f'{value} ({key})' for key, value in COLORS_TEXT.items())}")

    # Choisir la difficulté
    while True:
        difficulty = input("Choisissez la difficulté ('easy'  sans doublons, 'hard'  avec doublons) : ").lower()
        #print(difficulty)
        if difficulty in ['easy', 'hard']:
            allow_duplicates = (difficulty == 'hard')
            break
        print("Erreur : Veuillez entrer 'easy' ou 'hard'.")

    win_combination = generate_win_combination(allow_duplicates)

    for attempt in range(1, TRIES + 1):
        print(f"\nTentative {attempt}/{TRIES}")
        guess = get_user_input(difficulty)

        if guess == "quit":
            print("\nVous avez choisi d'abandonner. Merci d'avoir joué !")
            break

        well_placed, misplaced = compare_combinations(win_combination, guess)
        print(f"\u2713 Bien placé(s) : {well_placed}, \u274C Mal placé(s) : {misplaced}")

        if well_placed == LENGTH:
            print("\nFélicitations ! Vous avez trouvé la combinaison secrète :", ' '.join(COLORS_TEXT[letter] for letter in win_combination))
            break
    else:
        print("\nDésolé, vous avez épuisé toutes vos tentatives.")
        print("La combinaison gagnante était :", ' '.join(COLORS_TEXT[letter] for letter in win_combination))

if __name__ == "__main__":
    main()
