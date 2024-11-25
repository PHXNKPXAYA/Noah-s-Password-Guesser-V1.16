import itertools
import os
import time
from colorama import Fore, Style
import difflib  # For finding similar passwords

def print_green(text):
    """Print text in green for a hacker-style effect."""
    print(Fore.GREEN + text + Style.RESET_ALL)

def progress_bar(current, total, start_time, bar_length=40):
    """Display a progress bar with an ETA."""
    progress = current / total
    elapsed_time = time.time() - start_time
    eta = (elapsed_time / current) * (total - current) if current > 0 else 0
    eta_display = f"{int(eta // 60)}m {int(eta % 60)}s" if eta >= 60 else f"{int(eta)}s"

    bar = '=' * int(bar_length * progress) + '-' * (bar_length - int(bar_length * progress))
    print(f"\r[{bar}] {current}/{total} ({progress * 100:.2f}%) ETA: {eta_display}", end='')

def show_help():
    """Display help message."""
    print("\nHow to use Noah's Password Guesser:")
    print("1. Run the program.")
    print("2. Input up to 10 words when prompted (e.g., security question answers).")
    print("3. The program will generate up to 1 million password combinations.")
    print("4. A progress bar will show the generation status and estimated time.")
    print("5. Once complete, all passwords will be displayed.\n")
    print("Example: Enter words like 'dog', 'school', '1987', etc., when prompted.")
    print("Press Enter without typing to stop entering words.\n")

def find_similar_passwords(passwords, search_query):
    """Use difflib to find the closest matches for a password."""
    return difflib.get_close_matches(search_query, passwords, n=10, cutoff=0.6)

def highlight_and_scroll(passwords_to_highlight, all_passwords):
    """Clear the screen and scroll to the highlighted password."""
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
    
    print(Fore.GREEN + "\nHighlighted Passwords:")
    for idx, password in enumerate(passwords_to_highlight, start=1):
        print(f"{idx}. {Fore.YELLOW}{password}{Style.RESET_ALL}")

    # Scroll the list to show the selected password
    start_idx = max(0, all_passwords.index(passwords_to_highlight[0]) - 5)
    end_idx = min(len(all_passwords), start_idx + 10)
    
    print(Fore.GREEN + "\nFull List of Passwords (scrolling to selected):")
    for i in range(start_idx, end_idx):
        print(f"{i+1}. {all_passwords[i]}")

    print(Fore.GREEN + "\nYou can now view the highlighted password within the list.")

def handle_search(passwords):
    """Allow user to search for a password."""
    search_query = input(Fore.YELLOW + "\nEnter a password to search for: ")
    matches = [p for p in passwords if search_query.lower() in p.lower()]
    
    print(Fore.GREEN + f"\nFound {len(matches)} matches for '{search_query}':")
    for match in matches:
        print(match)
    
    if len(matches) == 0:
        print(Fore.RED + "No exact matches found.")
        offer_similar_search(passwords, search_query)
    else:
        select_from_list(matches, "exact", passwords)

def offer_similar_search(passwords, search_query):
    """Offer the user the option to search for similar passwords."""
    print(Fore.YELLOW + "\nNo exact matches. Would you like to search for similar passwords? (y/n): ")
    similar_option = input()
    if similar_option.lower() == 'y':
        similar_passwords = find_similar_passwords(passwords, search_query)
        if similar_passwords:
            print(Fore.GREEN + "\nSimilar passwords found:")
            for sim in similar_passwords:
                print(sim)
            select_from_list(similar_passwords, "similar", passwords)
        else:
            print(Fore.RED + "No similar passwords found.")

def select_from_list(passwords, match_type, all_passwords):
    """Allow user to select a password from the list."""
    print(Fore.GREEN + f"\nSelect a password from the {match_type} list by entering its number:")
    for idx, password in enumerate(passwords, start=1):
        print(f"{idx}. {password}")
    
    try:
        selected = int(input(Fore.YELLOW + "\nEnter the number of the password to highlight (or 0 to cancel): "))
        if selected == 0:
            return
        elif selected <= len(passwords):
            highlight_and_scroll([passwords[selected - 1]], all_passwords)
        else:
            print(Fore.RED + "Invalid selection.")
            select_from_list(passwords, match_type, all_passwords)
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a number.")
        select_from_list(passwords, match_type, all_passwords)

def generate_passwords(user_words, max_combinations=1_000_000):
    """Generate passwords based on user input."""
    passwords = []
    total_combinations = min(max_combinations, sum(len(list(itertools.permutations(user_words, r))) for r in range(1, len(user_words) + 1)))
    count = 0
    start_time = time.time()
    
    try:
        for r in range(1, len(user_words) + 1):
            for combination in itertools.permutations(user_words, r):
                password = ''.join(combination)
                passwords.append(password)
                count += 1
                progress_bar(count, total_combinations, start_time)
                if count >= total_combinations:
                    raise StopIteration
    except StopIteration:
        pass
    
    return passwords

def main():
    # Display cool intro text
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
    print_green("Noah's Password Guesser v1.06\n")
    time.sleep(0.5)

    # Check for help flag
    print("Type 'h' or '--help' for instructions, or press Enter to continue.")
    user_input = input("> ").strip().lower()
    if user_input in ('h', '--help'):
        show_help()
        return

    print("Welcome to the Password Guesser!")
    print("Input up to 10 words to generate possible password combinations.\n")

    # Get up to 10 words from the user
    user_words = []
    for i in range(10):
        word = input(f"Enter word {i + 1} (or press Enter to finish): ").strip()
        if not word:
            break
        user_words.append(word)

    if not user_words:
        print("No words provided. Exiting.")
        return

    print("\nGenerating passwords from your input words...\n")

    # Generate passwords and show progress
    passwords = generate_passwords(user_words)

    # Completion message and display generated passwords
    print("\nPassword generation complete!")

    # After generation, let the user decide how to view the passwords
    view_option = input(Fore.YELLOW + "\nWould you like to view all generated passwords? (y/n): ")
    if view_option.lower() == 'y':
        print(f"\nGenerated {len(passwords)} possible passwords:")
        for password in passwords:
            print(password)

        # Allow user to search and highlight passwords
        handle_search(passwords)

if __name__ == "__main__":
    main()
