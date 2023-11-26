import csv
from collections import defaultdict
import random

def generate_random_number(used_numbers):
    remaining_numbers = set(range(1, 76)) - set(used_numbers)
    
    if not remaining_numbers:
        raise ValueError("All numbers have been used")

    return random.sample(remaining_numbers, 1)[0]

def print_card(card):
    print("B  I  N  G  O")
    for row in card:
        print(' '.join(f"{num}:{called}" for num, called in row.items()))

def convert_letter_to_letter_index(letter):
    letter_mapping = {'B': 0, 'I': 1, 'N': 2, 'G': 3, 'O': 4}
    return letter_mapping.get(letter, -1)

def convert_letter_index_to_letter(index_number):
    number_mapping = {0: 'B', 1:'I', 2: 'N', 3: 'G', 4: 'O'}
    return number_mapping.get(index_number, -1)

def convert_number_to_letter(number_input):
    letter = ""
    if 1 <= number_input <= 15:
        letter = 'B'
    elif 16 <= number_input <= 30:
        letter = 'I'
    elif 31 <= number_input <= 45:
        letter = 'N'
    elif 46 <= number_input <= 60:
        letter = 'G'
    elif 61 <= number_input <= 75:
        letter = 'O'
    return letter

def update_cards(cards, letter_index, number):
    letter = convert_letter_index_to_letter(letter_index)
    for card_number, card in cards.items():
        for row in card:
            try:
                if row[str(number)] != None:
                    row[str(number)] = True
                    print(f"\tChange Card #{card_number} at {letter}-{number}" )
            except:
                pass
    
    return cards

def check_bingo(card):
    for row in card:
        if not all(row.values()):
            return False
    return True

def main():
    # Example usage
    used_numbers = []

    winning = None

    # Read the CSV file
    csv_path = 'bingo.csv'  # Set the default path to 'bingo.csv'
    
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header

        # Group rows by card number
        cards = defaultdict(list)
        for row in reader:
            card_number = row[-1]
            numbers = {num: num == '0' for num in row[:-1]}  # Mark '0' as True initially
            cards[card_number].append(numbers)

    # Print each card
    # for card_number, card in cards.items():
    #     print(f"\nCard {card_number}:")
    #     print_card(card)
        
    
    # Simulation loop
    for _ in range(60):  # Adjust the number of iterations as needed
        random_number = generate_random_number(used_numbers)
        
        used_numbers.append(random_number)
        
        letter = None

        if 1 <= random_number <= 15:
            letter = 'B'
        elif 16 <= random_number <= 30:
            letter = 'I'
        elif 31 <= random_number <= 45:
            letter = 'N'
        elif 46 <= random_number <= 60:
            letter = 'G'
        elif 61 <= random_number <= 75:
            letter = 'O'

        print(f"Generated Number: {random_number}, Letter: {letter}")

        # Convert letter to number
        letter_number = convert_letter_to_letter_index(letter)

        # Update cards
        cards = update_cards(cards, letter_number, random_number)

        stop_loop = False

        # Check for Bingo
        for card_number, card in cards.items():
            if check_bingo(card):
                winning = card_number
                #print(f"Bingo on Card {card_number}!")    
                stop_loop = True
                break

        if stop_loop == True:
            break

        
    #for card_number, card in cards.items():
    #    print(f"\nCard {card_number}:")
    #    print_card(card)
    #    pass

    #print(f"Bingo on Card {winning}!")

    if winning==None:
        print("Not winning")
        return False
    else: 
        print(f"Bingo on Card {winning}!")
        return True   
    
                

if __name__ == "__main__":
#    main()
    count = 1
    while True:
        if main():
            print(1/count)
            break
        else:
            print(count)
            count+=1

