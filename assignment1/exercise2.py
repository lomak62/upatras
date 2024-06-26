def check_invalid_characters(input_string):
    """ Έλεγχος αν η συμβολοσειρά περιέχει μη επιτρεπτούς χαρακτήρες """
    return next((char for char in input_string if not (char.isdigit() or char.isspace() or char == '-')), None)


def is_luhn_valid(card_number):
    """ Έλεγχος εγκυρότητας του αριθμού της πιστωτικής κάρτας με τον αλγόριθμο του Luhn """

    # Τα ψηφία στις άρτιες θέσεις
    digits_at_even_positions = [int(card_number[i]) for i in range(1, 16, 2)]
    # Τα ψηφία στις περιττές θέσεις διπλασιασμένα
    digits_at_odd_positions = [int(card_number[i]) * 2 for i in range(0, 16, 2)]
    # Προσθέτουμε τα ψηφία των διψήφιων διπλασιασμένων αριθμών ώστε να γίνουν μονοψήφιοι
    digits_at_odd_positions_converted = [sum(int(digit) for digit in str(num)) if num >= 10 else num
                                         for num in digits_at_odd_positions]
    # Άθροισμα των ψηφίων στις άρτιες θέσεις με το άθροισμα των διπλασιασμένων ψηφίων στις περιττές θέσεις
    total_sum = sum(digits_at_even_positions) + sum(digits_at_odd_positions_converted)
    # Έλεγχος του τελικού αθροίσματος
    return total_sum % 10 == 0


def prompt_user_to_reenter():
    """ Ζητάει από τον χρήστη να επαναλάβει την εισαγωγή του αριθμού της κάρτας """
    print("Παρακαλώ επαναλάβετε την εισαγωγή.")


def main():
    while True:
        input_string = input("Πληκτρολογήστε τον αριθμό της κάρτας: ")

        # Έλεγχος για μη επιτρεπτούς χαρακτήρες
        invalid_char = check_invalid_characters(input_string)
        if invalid_char:
            print(f"Η συμβολοσειρά περιέχει τον μη επιτρεπτό χαρακτήρα '{invalid_char}'.")
            prompt_user_to_reenter()
            continue

        # Αφαιρούμε τα κενά και τις παύλες από τη συμβολοσειρά
        digits = ''.join(char for char in input_string if char.isdigit())

        # Έλεγχος αν έχουν εισαχθεί ακριβώς 16 ψηφία
        if len(digits) != 16:
            print("Ο αριθμός πρέπει να έχει 16 ψηφία.")
            prompt_user_to_reenter()
            continue

        # Μορφοποιούμε τον αριθμό στη μορφή xxxx-xxxx-xxxx-xxxx
        card_number = f"{digits[:4]}-{digits[4:8]}-{digits[8:12]}-{digits[12:]}"

        # Έλεγχος εγκυρότητας σύμφωνα με τον αλγόριθμο Luhn
        if is_luhn_valid(digits):
            print(f"Ο αριθμός {card_number} είναι ΕΓΚΥΡΟΣ.")
            print("Τέλος προγράμματος.")
            break
        else:
            print(f"Ο αριθμός {card_number} είναι ΑΚΥΡΟΣ.")
            prompt_user_to_reenter()


if __name__ == "__main__":
    main()
