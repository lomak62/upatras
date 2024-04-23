def print_pattern(rows):
    for i in range(rows):
        stars = '*' * (i + 1)  # Αυξάνεται ο αριθμός των αστερίσκων σε κάθε γραμμή
        spaces = ' ' * (2 * (rows - i) - 1)  # Μειώνεται ο αριθμός των κενών σε κάθε γραμμή
        print(stars + spaces + stars)


def main():
    while True:
        try:
            n = int(input("Δώστε το n (1-20): "))
            if n not in range(1, 21):
                continue
            print_pattern(n)
        except ValueError:
            print("Τέλος προγράμματος")
            break


if __name__ == "__main__":
    main()
