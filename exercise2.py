def check_invalid_characters(input_string):
    """
    Έλεγχος αν η συμβολοσειρά περιέχει μη επιτρεπτούς χαρακτήρες
    """
    return next((char for char in input_string if not (char.isdigit() or char.isspace() or char == '-')), None)


def is_luhn_valid(card_number):
    """
    Έλεγχος του αριθμού της πιστωτικής κάρτας με τον αλγόριθμο του Luhn
    """
    # Τα ψηφία στις άρτιες θέσεις
    digits_at_even_positions = [int(card_number[i]) for i in range(1, 16, 2)]
    # Διπλασιάζουμε τα ψηφία στις περιττές θέσεις
    digits_at_odd_positions = [int(card_number[i]) * 2 for i in range(0, 16, 2)]
    # Προσθέτουμε τα ψηφία των διψήφιων διπλασιασμένων αριθμών ώστε να γίνουν μονοψήφιοι
    single_digits = [sum(int(digit) for digit in str(num)) if num >= 10 else num for num in digits_at_odd_positions]
    # Άθροισμα των άρτιων ψηφίων με το άθροισμα των περιττών ψηφίων που διπλασιάστηκαν
    total_sum = sum(digits_at_even_positions) + sum(single_digits)
    # Έλεγχος του τελικού αθροίσματος
    if total_sum % (digits_at_even_positions[-1] + 2) == 0:
        return True
    return False


def prompt_user_to_reenter():
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
        card_number_wo_spaces_and_dashes = ''.join(char for char in input_string if char.isdigit())

        # Έλεγχος αν έχουν εισαχθεί ακριβώς 16 ψηφία
        if len(card_number_wo_spaces_and_dashes) != 16:
            print("Ο αριθμός πρέπει να έχει 16 ψηφία.")
            prompt_user_to_reenter()
            continue

        # Μορφοποιούμε τον αριθμό στη μορφή xxxx-xxxx-xxxx-xxxx
        formatted_card_number = (f"{card_number_wo_spaces_and_dashes[:4]}-{card_number_wo_spaces_and_dashes[4:8]}-"
                                 f"{card_number_wo_spaces_and_dashes[8:12]}-{card_number_wo_spaces_and_dashes[12:]}")

        # Έλεγχος εγκυρότητας σύμφωνα με τον αλγόριθμο Luhn
        if is_luhn_valid(card_number_wo_spaces_and_dashes):
            print(f"Ο αριθμός {formatted_card_number} είναι ΕΓΚΥΡΟΣ.")
            print("Τέλος προγράμματος.")
            break
        else:
            print(f"Ο αριθμός {formatted_card_number} είναι ΑΚΥΡΟΣ.")
            prompt_user_to_reenter()


if __name__ == "__main__":
    main()
