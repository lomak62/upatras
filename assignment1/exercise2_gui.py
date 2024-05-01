import tkinter as tk
import json
import exercise2


class CardIssuerIdentifier:
    """Επιστρέφει τον Credit card issuer"""
    def __init__(self, issuers_file):
        self.issuers_file = issuers_file
        self.issuers_data = self.load_issuers_data()

    def load_issuers_data(self):
        try:
            with open(self.issuers_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Error: issuers file not found")
            return None
        except json.JSONDecodeError:
            print("Error: issuers file is not a valid JSON")
            return None

    def identify(self, card_number):
        if self.issuers_data is None:
            return "Error: issuers data not loaded"
        for issuer, prefixes in sorted(self.issuers_data.items(), key=lambda x: max(len(p) for p in x[1]), reverse=True):
            for prefix in sorted(prefixes, key=len, reverse=True):
                if '-' in prefix:
                    start, end = map(int, prefix.split('-'))
                    if int(card_number[:len(str(start))]) in range(start, end + 1):
                        return issuer
                else:
                    if card_number.startswith(prefix):
                        return issuer
        return None


class CardValidator:
    """Ελέγχει τη δοθείσα από το χρήστη συμβολοσειρά"""
    def __init__(self, input_string):
        self.input_string = input_string

    def extract_digits(self):
        # Αφαιρούμε τα κενά και τις παύλες από τη συμβολοσειρά
        return ''.join(char for char in self.input_string if char.isdigit())

    def format_card_number(self, digits):
        # Μορφοποιούμε τον αριθμό στη μορφή xxxx-xxxx-xxxx-xxxx
        return f"{digits[:4]}-{digits[4:8]}-{digits[8:12]}-{digits[12:]}"

    def has_valid_characters(self):
        invalid_character = exercise2.check_invalid_characters(self.input_string)
        if invalid_character:
            self.invalid_character = invalid_character
            return False
        return True

    def has_valid_length(self):
        return len(self.extract_digits()) == 16

    def is_luhn_valid(self):
        return exercise2.is_luhn_valid(self.extract_digits())

    def is_valid(self):
        if not self.has_valid_characters():
            return "Η συμβολοσειρά περιέχει τον μη επιτρεπτό χαρακτήρα '{}'".format(self.invalid_character)
        if not self.has_valid_length():
            return "Ο αριθμός πρέπει να έχει 16 ψηφία"
        if not self.is_luhn_valid():
            return "Ο αριθμός {} είναι ΑΚΥΡΟΣ".format(self.format_card_number(self.extract_digits()))
        return "Ο αριθμός {} είναι ΕΓΚΥΡΟΣ".format(self.format_card_number(self.extract_digits()))

    def identify_issuer(self):
        card_issuer_identifier = CardIssuerIdentifier("exercise2_iss.json")
        return card_issuer_identifier.identify(self.extract_digits())


class GUI:
    """Δημιουργεί το γραφικό περιβάλλον"""
    def __init__(self, root):
        self.root = root
        self.root.title('Bank card number validation - v1.2024')
        self.root.geometry("600x350")
        self.root.resizable(False, False)

        self.fg_color = None
        self.spritesheet = tk.PhotoImage(file="exercise2_art.png")

        self.visa_image = self._subimage(0, 0, 149, 48, self.spritesheet)
        self.mastercard_image = self._subimage(150, 0, 298, 48, self.spritesheet)

        self.create_widgets()

    def create_widgets(self):
        # Create and pack widgets for input and validation

        self.f1 = tk.Frame(self.root)
        self.f1.pack(anchor='nw', padx=40, pady=(40, 60))

        self.entry_title = tk.Label(self.f1, text="Card number", font=("Helvetica", 8), justify="left")
        self.entry_title.pack(anchor='w')

        self.entry = tk.Entry(self.f1, font=("Helvetica", 16))
        self.entry.pack(side='left')
        self.entry.bind("<1>", self.clear_label)
        self.entry.bind("<Return>", self.check_entry)
        self.entry.focus_force()

        self.button = tk.Button(self.f1, text="Check", command=self.check_entry, font=("Helvetica", 16))
        self.button.pack(padx=40)

        # Create and pack widgets for validation result

        self.f2 = tk.Frame(self.root)
        self.f2.pack(anchor='w', padx=(40, 0))

        self.label_title = tk.Label(self.f2, text="Validation", font=("Helvetica", 8), justify="left")
        self.label_title.pack(anchor='w')

        self.label = tk.Label(self.f2, text="", font=("Helvetica", 16))
        self.label.pack(anchor='w')

        # Create and pack widgets for issuer information

        self.f3_f4_frame = tk.Frame(self.root, padx=40)
        self.f3_f4_frame.pack(expand=1, fill='x')

        self.f3 = tk.Frame(self.f3_f4_frame)
        self.f3.pack(side='left')

        self.issuer_title = tk.Label(self.f3, text="Issuer", font=("Helvetica", 8), justify="left")
        self.issuer_title.pack(anchor='w')

        self.issuer_label = tk.Label(self.f3, text="", font=("Helvetica", 16), justify="left")
        self.issuer_label.pack(anchor='w')

        self.f4 = tk.Frame(self.f3_f4_frame)
        self.f4.pack(side='right')

        self.issuer_image = tk.Label(self.f4, image='')
        self.issuer_image.pack()

    def _subimage(self, l, t, r, b, spritesheet):
        dst = tk.PhotoImage()
        dst.tk.call(dst, 'copy', spritesheet, '-from', l, t, r, b, '-to', 0, 0)
        return dst

    def check_entry(self, event=None):
        self.clear_label(event)
        entry_str = self.entry.get().strip()
        if not entry_str:
            return False
        validator = CardValidator(entry_str)
        validation_result = validator.is_valid()
        if 'ΕΓΚΥΡΟΣ' in validation_result:
            self.fg_color = "#000000"
            self.update_issuer_label(validator)
        self.update_label(validation_result)

    def update_label(self, validation_result):
        self.label.config(text=validation_result, fg=self.fg_color)

    def update_issuer_label(self, validator):
        issuer = validator.identify_issuer()
        if issuer:
            self.issuer_label.config(text=issuer)
            self.issuer_artwork(issuer)

    def issuer_artwork(self, issuer):
        issuer_images = {'Visa': self.visa_image, 'MasterCard': self.mastercard_image}
        self.issuer_image.config(image=issuer_images.get(issuer, ''))

    def clear_label(self, event=None):
        self.label.config(text="")
        self.issuer_label.config(text="")
        self.issuer_image.config(image='')
        self.fg_color = "#8b0000"


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
