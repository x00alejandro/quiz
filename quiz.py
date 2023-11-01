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
            if row:
                if len(row) == 3:
                    english, spanish, consecutive_correct = row
                    consecutive_correct = int(consecutive_correct) if consecutive_correct else 0
                    dictionary.append([english, spanish, consecutive_correct])
                elif len(row) == 2:
                    english, spanish = row
                    dictionary.append([english, spanish, 0])
    return dictionary

def save_dictionary(filename, dictionary):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for english, spanish, consecutive_correct in dictionary:
            writer.writerow([english, spanish, consecutive_correct])

def update_progress(progress_filename, score, total_words, no_count):
    current_date = datetime.date.today()
    today_entry = None

    try:
        with open(progress_filename, 'r', newline='') as file:
            reader = csv.reader(file)
            first_row = next(reader, None)  # Read the first row (title row)
            if first_row and not all(value.isdigit() for value in first_row[1:3]):
                first_row = next(reader, None)  # Skip title row if not numeric
            progress = list(reader)
            today_entry = next((entry for entry in progress if entry and entry[0] == str(current_date)), None)
    except FileNotFoundError:
        pass

    if today_entry:
        today_date, total, correct, _, trials_of_day = today_entry[:5]  # Unpack the first five values
        counter = int(trials_of_day) if no_count else 1

        total = int(total) if total.isdigit() else 0
        correct = int(correct) if correct.isdigit() else 0
        percent_correct = f"{round(correct / total * 100)}%" if total > 0 else "0%"
        today_entry = [today_date, total, score, percent_correct, counter]
        with open(progress_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            if first_row:
                writer.writerow(first_row)  # Write back the title row
            for entry in progress:
                if entry and entry[0] == str(current_date):
                    writer.writerow(today_entry)
                else:
                    writer.writerow(entry)
    else:
        percent_correct = f"{round(score / total_words * 100)}%" if total_words > 0 else "0%"
        today_entry = [str(current_date), total_words, score, percent_correct, 1]
        with open(progress_filename, 'a', newline='') as file:
            writer = csv.writer(file)
            if not os.path.getsize(progress_filename):  # Check if the file is empty
                writer.writerow(["Date", "Words", "Correct", "Percent Correct", "Trials Of Day"])
            writer.writerow(today_entry)

def ask_question(dictionary, no_count):
    score = 0
    wrong_attempts = 0
    total_words = len(dictionary)
    random.shuffle(dictionary)

    for i, (english, spanish, consecutive_correct) in enumerate(dictionary):
        is_english_to_spanish = random.choice([True, False])
        if is_english_to_spanish:
            user_answer = input(f"What is the Spanish translation of '{english}': ").strip().lower()
        else:
            user_answer = input(f"What is the English translation of '{spanish}': ").strip().lower()

        if (is_english_to_spanish and user_answer == spanish.lower()) or (not is_english_to_spanish and user_answer == english.lower()):
            if not no_count:
                consecutive_correct += 1
            score += 1
        else:
            print(f"Wrong! The correct answer is '{spanish if is_english_to_spanish else english}'.")
            consecutive_correct = 0
            wrong_attempts += 1
        dictionary[i][2] = consecutive_correct

    return score, total_words

def main():
    parser = argparse.ArgumentParser(description="Dictionary Quiz")
    parser.add_argument("--file", help="Specify the CSV file for the dictionary", default="all.csv")
    parser.add_argument("--no-count", action="store_true", help="Run in no-count mode")
    args = parser.parse_args()

    dictionary_filename = args.file
    progress_filename = "progress.csv"
    no_count = args.no_count

    if not os.path.exists(dictionary_filename):
        print(f"The dictionary file '{dictionary_filename}' does not exist.")
        return

    if not os.path.exists(progress_filename):
        with open(progress_filename, 'w', newline=''):  # Create progress file if it doesn't exist
            pass

    dictionary = read_dictionary(dictionary_filename)

    print("Welcome to the Dictionary Quiz!")

    total_words = len(dictionary)  # Count the total words for the actual quiz

    score, _ = ask_question(dictionary, no_count)  # Use _ for total_words since it's already calculated

    print(f"Quiz ended. Your score: {score}/{total_words}")

    if not no_count:
        for i in range(len(dictionary) - 1, -1, -1):
            if dictionary[i][2] >= 5:
                dictionary.pop(i)  # Remove words with consecutive count >= 5

    update_progress(progress_filename, score, len(dictionary), no_count)

    save_dictionary(dictionary_filename, dictionary)


if __name__ == "__main__":
    main()

