import csv
import sys


def main():
    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    # TODO: Read database file into a variable
    data = {}
    with open(sys.argv[1], "r", newline="") as database_file:
        db_reader = csv.DictReader(database_file)
        for row in db_reader:
            # Create a generator that iterates over key-value in a row except the "name" key
            # Gets the value and converts them to ints before placing them into a tuple
            # Code from RoadRunner
            rows = tuple(int(v) for k, v in row.items() if k != "name")
            # Create a key value pair where key is a tuple of the three counts and value is the name
            data[rows] = row["name"]
        # Get list of Short Tandem Repeats from the csv fieldnames
        repeats = db_reader.fieldnames
        repeats.remove("name")

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r", newline="") as sequence_file:
        sequence = sequence_file.read()

    # TODO: Find longest match of each STR in DNA sequence
    repeat_values = []
    for repeat in repeats:
        repeat_values.append(longest_match(sequence, repeat))

    # TODO: Check database for matching profiles
    try:
        print(data[tuple(repeat_values)])
    except KeyError:
        print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):
        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:
            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
