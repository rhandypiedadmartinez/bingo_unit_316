import streamlit as st
from collections import defaultdict
from bingo_simulator import print_card
from bingo_simulator import convert_letter_to_letter_index
from bingo_simulator import convert_letter_index_to_letter
from bingo_simulator import check_bingo
from bingo_simulator import convert_number_to_letter
import csv
import os

# Get the absolute path of the script directory
cwd = os.getcwd()

# Read the CSV file
csv_path = os.path.join(cwd, "bingo.csv")

def update_cards(cards, letter_index, number):
    letter = convert_number_to_letter(number)
    is_changed = False 
    changes = f"{letter}: "

    for card_number, card in cards.items():
        for row in card:
            try:
                if row[str(number)] != None:
                    row[str(number)] = True
                    is_changed = True 
                    changes += f"{card_number}, "
            except:
                pass
    
    return cards, is_changed, changes

def display_card_data(card_number, card_data):
    st.write(f"Card Number: {card_number}")
    st.write("Card Data:")
    for row in card_data:
        st.write(row)

def main():

    st.title("")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "used_numbers" not in st.session_state:
        st.session_state.used_numbers = []

    if "cards" not in st.session_state:        
        with open(csv_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header

            # Group rows by card number
            cards = defaultdict(list)
            for row in reader:
                card_number = row[-1]
                numbers = {num: num == '0' for num in row[:-1]}  # Mark '0' as True initially
                cards[card_number].append(numbers)

        st.session_state.cards = cards
      
    winning = None

    # Display card data when button is clicked
    if number_input := st.chat_input("Find Card"):
      
        number_input = int(number_input)
        st.session_state.used_numbers.append(number_input)

        letter = convert_number_to_letter(number_input)

        # Convert letter to number
        letter_index = convert_letter_to_letter_index(letter)

        st.session_state.cards, is_changed, changes = update_cards(st.session_state.cards, letter_index, number_input)
        
        responses = ""

        if is_changed:
            responses = [changes]
        else:
            st.error(f"Card {number_input} not found.")

        cards = st.session_state.cards 
        # for card_number, card in cards.items():
        #    print(f"\nCard {card_number}:")
        #    print_card(card)
        #    pass

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            for response in responses:
                print(response)
                st.markdown(f"{response}")

        for card_number, card in cards.items():
            if check_bingo(card):
                winning = card_number
                print(f"Winning is {card_number}")
                st.success(f"Bingo on Card {card_number}!") 


if __name__ == "__main__":
    main()
