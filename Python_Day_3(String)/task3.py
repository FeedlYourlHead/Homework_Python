s = input("Введите вашу строку: ")

substrings = [s[i:j] for i in range(len(s)) for j in range(i+1, len(s)+1)]

print(substrings)