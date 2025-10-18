with open('data.txt', 'r') as file:
    lines = file.readlines()

unique_symbols = set()

for line in lines:
    cleaned_line = line.strip()
    unique_symbols.update(cleaned_line)

usless_symbols = {'>', '-', ' '}
unique_symbols -= usless_symbols

print("Размер алфавита: ",len(unique_symbols))
print("Алфавит:", unique_symbols)