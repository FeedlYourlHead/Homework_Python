text = input("Введите текст: ")

reserved_words= input("Введите зарезервированные слова через запятую(пример: слово1, слово2,): ").split(", ")

words = text.split()
result_words = []

for word in words:
    is_reserved = False
    for r_word in reserved_words:
        if word.lower() == r_word.lower():
            is_reserved = True
            break
    
    if is_reserved:
        new_word = ""
        for char in word:
            new_word += char.upper()
        result_words.append(new_word)
    else:
        result_words.append(word)

result_text = " ".join(result_words)

print(f"Результат: {result_text}")