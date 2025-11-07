from collections import Counter
import string

def is_palindrome(s):
    if isinstance(s, int):
        s = str(s)
    s = s.upper()
    s2 = ''.join(reversed(s))
    if s == s2:
        return True
    else:
        return False

def word_counts(s):
    translator = str.maketrans('', '', string.punctuation)
    clean_text = s.translate(translator).lower()

    words = clean_text.split()

    return dict(Counter(words))

print(word_counts('Привет мир!'))
print(word_counts(''))
    


