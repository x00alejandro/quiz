import csv
import random
import datetime
import os
import argparse
    
def read_dictionary(filename):
    dictionary = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:
                english, spanish, consecutive_correct = row
                consecutive_correct = int(consecutive_correct) if consecutive_correct else 0
                dictionary.append([english, spanish, consecutive_correct])
            elif len(row) == 2:
                english, spanish = row
                dictionary.append([english, spanish, 0])  # Add a 0 if the 3rd column is missing
    return dictionary



def save_dictionary(filename, dictionary):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for english, spanish, consecutive_correct in dictionary:
            writer.writerow([english, spanish, consecutive_correct])
            
def move_to_removed(removed_filename, removed_word):
    with open(removed_filename, 'a', newline='') as removed_file:
        writer = csv.writer(removed_file)
        writer.writerow(removed_word)

def ask_question(dictionary, no_count):
    score = 0
    wrong_attempts = 0
    total_words = len(dictionary)
    random.shuffle(dictionary)
    
    for i, (english, spanish, consecutive_correct) in enumerate(dictionary):
        user_answer = input(f"What is the Spanish translation of '{english}': ").strip().lower()
        if user_answer == spanish.lower():
            print("Correct!")
            if not no_count:
                consecutive_correct += 1
                if consecutive_correct >= 5:
                    move_to_removed(removed_filename, dictionary[i])  # Move the word to the removed file
                    del dictionary[i]  # Remove the word from the dictionary
            score += 1
        else:
            print(f"Wrong! The correct answer is '{spanish}'.")
            consecutive_correct = 0
            wrong_attempts += 1
        dictionary[i][2] = consecutive_correct

    if not no_count:
        score = total_words - wrong_attempts
    
    return score, total_words


def main():
    parser = argparse.ArgumentParser(description="Dictionary Quiz")
    parser.add_argument("--file", help="Specify the CSV file for the dictionary", default="all.csv")
    parser.add_argument("--no-count", action="store_true", help="Do not update progress or remove words")
    args = parser.parse_args()

    dictionary_filename = args.file
    progress_filename = "progress.csv"
    removed_filename = "removed.csv"

    if not os.path.exists(dictionary_filename):
        print(f"The dictionary file '{dictionary_filename}' does not exist.")
        return
    
    if not os.path.exists(progress_filename):
        with open(progress_filename, 'w', newline=''):  # Create progress file if it doesn't exist
            pass
    
    if not os.path.exists(removed_filename):
        with open(removed_filename, 'w', newline=''):  # Create removed file if it doesn't exist
            pass

    dictionary = read_dictionary(dictionary_filename)
    
    print("Welcome to the Dictionary Quiz!")
    
    score, total_words = ask_question(dictionary, args.no_count)
    
    print(f"Quiz ended. Your score: {score}/{total_words}")
    
    if not args.no_count:
        with open(progress_filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.date.today(), total_words, score])
    
    save_dictionary(dictionary_filename, dictionary)

if __name__ == "__main__":
    main()

