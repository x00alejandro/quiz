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

def ask_question(dictionary):
    score = 0
    wrong_attempts = 0
    total_words = len(dictionary)
    random.shuffle(dictionary)
    
    for i, (english, spanish, consecutive_correct) in enumerate(dictionary):
        user_answer = input(f"What is the Spanish translation of '{english}': ").strip().lower()
        if user_answer == spanish.lower():
            print("Correct!")
            consecutive_correct += 1
            if consecutive_correct >= 5:
                del dictionary[i]  # Remove the word if answered correctly 5 times consecutively
        else:
            print(f"Wrong! The correct answer is '{spanish}'.")
            consecutive_correct = 0
            wrong_attempts += 1
        dictionary[i][2] = consecutive_correct

    score = total_words - wrong_attempts  # Calculate the score based on the number of correct answers before the last question
    
    return score, total_words


def main():
    progress_filename = "progress.csv"

    parser = argparse.ArgumentParser(description="Dictionary Quiz")
    parser.add_argument("--file", help="Specify the CSV file for the dictionary", default="all.csv")
    args = parser.parse_args()

    dictionary_filename = args.file

    if not os.path.exists(dictionary_filename):
        print(f"The dictionary file '{dictionary_filename}' does not exist.")
        return
    
    dictionary = read_dictionary(dictionary_filename)
    
    print("Welcome to the Dictionary Quiz!")
    
    score, total_words = ask_question(dictionary)
    
    print(f"Quiz ended. Your score: {score}/{total_words}")
    
    with open(progress_filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.date.today(), total_words, score])
    
    save_dictionary(dictionary_filename, dictionary)

if __name__ == "__main__":
    main()


