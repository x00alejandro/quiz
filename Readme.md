# Dictionary Quiz Script

This Python script allows you to take a dictionary quiz using a CSV file containing English and Spanish word pairs. You can specify the CSV file to use and track your progress over time.

## Features

- Supports customizable CSV files for your dictionary.
- Keeps track of your quiz progress, including date, total words, and score.
- Removes words from the dictionary if you answer them correctly five times consecutively.
- Allows you to specify the dictionary file to use with the `--file` flag.
- Provides usage information with the `--help` argument.

## Usage

To run the script, simply execute it in your terminal, and you can provide the `--file` flag to specify the CSV file for the dictionary. If you don't provide the flag, it will default to "all.csv".

```bash
python quiz.py
python quiz.py --file example.csv
```

To display usage information, you can use the --help argument:

bash
Copy code
python quiz.py --help
Requirements
Python 3.x
argparse library (usually included in standard Python installations)
Example CSV File Format
The CSV file should contain pairs of English and Spanish words, like this:

Feel free to customize and use it for your language learning needs!
