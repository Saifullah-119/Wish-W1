import random
import json
import os

# Character Pools
five_star_pool = ['Azmas', 'Feia', 'Newkie', 'Mou', 'Yaugh', 'Reama', 'Araech', 'Rawtis', 'Agrathe', 'Sappha', 'Jadin', 'Rubia', 'Diam', 'Arean', 'Valka', 'Thaelec', 'Aizha', 'Mwuk', 'Kriana']
four_star_pool = ['Zapza', 'Barem', 'Finala', 'Equill', 'Barem', 'Henceproveth', 'Thythagoras', 'Rosetha', 'Minna', 'Marie', 'Manty', 'Relikh', 'Fanky', 'Naita', 'Zaima', 'Imat']
three_star_pool = ['Ranja', 'Dize', 'Budin', 'Nott', 'Galax', 'Ohem', 'Sola', 'Nebeuna', 'Perra']

# History File
HISTORY_FILE = "wish_history.json"
MAX_HISTORY = 1000

# Wishing chances
def pull_character():
    chance = random.random()
    if chance < 0.10:
        return random.choice(five_star_pool), 5
    elif chance < 0.50:
        return random.choice(four_star_pool), 4
    else:
        return random.choice(three_star_pool), 3

# Saving and loading history
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[-MAX_HISTORY:], f)

# Math problem generator
def easy_math_problem():
    a, b = random.randint(1, 10), random.randint(1, 10)
    return f"{a} + {b} = ?", a + b

def hard_math_problem():
    a, b = random.randint(10, 50), random.randint(10, 50)
    return f"{a} * {b} = ?", a * b

# Wishing function
def wish(num_wishes):
    history = load_history()
    if num_wishes == 1:
        problem, answer = easy_math_problem()
    else:
        problem, answer = hard_math_problem()
    
    print(f"Math problem to proceed: {problem}")
    user_answer = int(input("Enter answer: "))
    
    if user_answer != answer:
        print("Incorrect math answer. Try again later.")
        return

    pulled_characters = []
    for _ in range(num_wishes):
        char, rarity = pull_character()
        pulled_characters.append((char, rarity))
    
    history.extend(pulled_characters)
    save_history(history)

    # Dialogue
    if any(rarity == 5 for _, rarity in pulled_characters):
        print("Unbelievable... You have pulled the following:")
    else:
        print("You have pulled the following:")
    
    # Display pulls
    for char, rarity in pulled_characters:
        print(f"{char} {'*' * rarity}")

# View history
def view_history():
    history = load_history()
    for i, (char, rarity) in enumerate(history, 1):
        print(f"{i}: {char} {'*' * rarity}")

# Calculate stats
def calculate_stats():
    history = load_history()
    if not history:
        print("No history available.")
        return

    num_pulls = len(history)
    num_five_star = sum(1 for _, rarity in history if rarity == 5)
    num_four_star = sum(1 for _, rarity in history if rarity == 4)

    avg_5_star_pity = num_pulls / num_five_star if num_five_star > 0 else float('inf')
    avg_4_star_pity = num_pulls / num_four_star if num_four_star > 0 else float('inf')
    
    five_stars_per_100 = (num_five_star / num_pulls) * 100
    four_stars_per_100 = (num_four_star / num_pulls) * 100

    # Luck rating
    if five_stars_per_100 > 20:
        luck_rating = "Excellent"
    elif five_stars_per_100 > 10:
        luck_rating = "Good"
    elif five_stars_per_100 == 10:
        luck_rating = "Average"
    elif five_stars_per_100 > 5:
        luck_rating = "Bad"
    else:
        luck_rating = "Horrendous"

    print(f"Avg 5-star pity: {avg_5_star_pity:.2f}")
    print(f"Avg 4-star pity: {avg_4_star_pity:.2f}")
    print(f"5 stars in 100 pulls: {five_stars_per_100:.2f}")
    print(f"4 stars in 100 pulls: {four_stars_per_100:.2f}")
    print(f"Luck rating: {luck_rating}")

# Main loop
def main():
    while True:
        print("\nChoose an option: ")
        print("1: Wish")
        print("2: View History")
        print("3: View Stats")
        print("4: Exit")
        
        choice = input("Enter choice: ")
        if choice == "1":
            print("Wish for 1 or 10?")
            num_wishes = int(input("Enter 1 or 10: "))
            if num_wishes in [1, 10]:
                wish(num_wishes)
            else:
                print("Invalid number of wishes.")
        elif choice == "2":
            view_history()
        elif choice == "3":
            calculate_stats()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
