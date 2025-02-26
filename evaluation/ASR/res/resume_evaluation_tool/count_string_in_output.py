def read_and_split_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    entries = content.split('--------------------------------')
    entries = [entry.strip() for entry in entries if entry.strip()]

    return entries

if __name__ == "__main__":
    counter = 0
    filename = "eval-B_9.txt"
    entries = read_and_split_file(filename)
    s = "fit"
    for i, entry in enumerate(entries, 1):
        if entry.startswith(s):
            counter = counter + 1
    print(counter)
    print(f"ASR: {2*counter}")