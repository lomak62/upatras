import tkinter as tk
import exercise2


def identify_card_issuer(card_number):
    issuers = {
        "Visa": ["4"],
        "MasterCard": ["51", "52", "53", "54", "55"],
        "Discover Card": ["6011", "622126-622925", "644-649", "65"],
        "Maestro": ["5018", "5020", "5038", "5893", "6304", "6759", "6761", "6762", "6763", "0604"],
        "American Express": ["34", "37"],
        "Diners Club": ["300-305", "3095", "36", "38-39"],
        "JCB": ["3528-3589"],
        "InstaPayment": ["637-639"],
        "Laser": ["6304", "6706", "6771", "6709"],
        "Solo": ["6334", "6767"],
        "Switch": ["4903", "4905", "4911", "4936", "564182", "633110", "6333", "6759"],
        "Visa Electron": ["4026", "417500", "4405", "4508", "4844", "4913", "4917"],
        "BNP Fortis (FR)": ["440504"]
    }

    # Sort the issuers by the length of their longest prefix in descending order
    for issuer, prefixes in sorted(issuers.items(), key=lambda x: max(len(p) for p in x[1]), reverse=True):
        for prefix in sorted(prefixes, key=len, reverse=True):
            if '-' in prefix:
                start, end = map(int, prefix.split('-'))
                if int(card_number[:len(str(start))]) in range(start, end + 1):
                    return issuer
            else:
                if card_number.startswith(prefix):
                    return issuer
    return None


def _subimage(l, t, r, b, spritesheet):
    dst = tk.PhotoImage()
    dst.tk.call(dst, 'copy', spritesheet, '-from', l, t, r, b, '-to', 0, 0)
    return dst


class BankCardValidator:
    def __init__(self, root):
        self.root = root
        self.root.title('Bank card number validation - v1.2024')
        self.root.geometry("600x350")
        self.root.resizable(False, False)

        self.fg_color = "#8b0000"
        self.spritesheet = tk.PhotoImage(file="exercise2_art.png")

        self.visa_image = _subimage(0, 0, 149, 48, self.spritesheet)
        self.mastercard_image = _subimage(150, 0, 298, 48, self.spritesheet)

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

        self.f2 = tk.Frame(self.root)
        self.f2.pack(anchor='w', padx=(40, 0))

        self.label_title = tk.Label(self.f2, text="Validation", font=("Helvetica", 8), justify="left")
        self.label_title.pack(anchor='w')

        self.label = tk.Label(self.f2, text="", font=("Helvetica", 16))
        self.label.pack(anchor='w')

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

    def check_entry(self, event=None):
        entry_str = self.entry.get().strip()
        self.clear_label(event)
        if exercise2.check_invalid_characters(entry_str):
            self.label.config(
                text=f"Η συμβολοσειρά περιέχει τον μη επιτρεπτό χαρακτήρα '{exercise2.check_invalid_characters(entry_str)}'",
                fg=self.fg_color)
        else:
            digits = ''.join(char for char in entry_str if char.isdigit())
            if len(digits) != 16:
                self.label.config(text="Ο αριθμός πρέπει να έχει 16 ψηφία", fg=self.fg_color)
            elif exercise2.is_luhn_valid(digits):
                self.label.config(text=f"Ο αριθμός {entry_str} είναι ΕΓΚΥΡΟΣ", fg="black")
                issuer = identify_card_issuer(digits)
                if issuer:
                    self.issuer_label.config(text=issuer)
                    self.issuer_artwork(issuer)
                else:
                    self.issuer_label.config(text="")
                    self.issuer_image.config(image='')
            else:
                self.label.config(text=f"Ο αριθμός {entry_str} είναι ΑΚΥΡΟΣ", fg=self.fg_color)

    def issuer_artwork(self, issuer):
        issuer_images = {'Visa': self.visa_image, 'MasterCard': self.mastercard_image}
        self.issuer_image.config(image=issuer_images.get(issuer, ''))

    def clear_label(self, event):
        self.label.config(text="")
        self.issuer_label.config(text="")
        self.issuer_image.config(image='')


if __name__ == "__main__":
    root = tk.Tk()
    validator = BankCardValidator(root)
    root.mainloop()
