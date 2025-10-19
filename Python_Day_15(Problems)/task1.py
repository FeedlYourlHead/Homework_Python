def roman_to_int(s) -> int:
    symbols = {
        'I': 1,
        'V': 5,
        'X':10,
        'L':50,
        'C':100,
        'D':500,
        'M':1000
    }
    number = 0
    s = s.replace('IV', 'IIII').replace('IX', 'VIIII')
    s = s.replace('XL', 'XXXX').replace('XC', 'LXXXX')
    s = s.replace('CD', 'CCCC').replace('CM', 'DCCCC')
    for char in s:
        number += symbols[char]
    return number

print(roman_to_int('III'))
print(roman_to_int('LVIII'))
print(roman_to_int("MCMXCIV"))

print(roman_to_int('MCMLXXXIV'))
print(roman_to_int('MCCXXXIV'))
print(roman_to_int('MCMXC'))

#Возможно здесь ожидалось другое решение, но я уже решал эту задачу на LeetCode

