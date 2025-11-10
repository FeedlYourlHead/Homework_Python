
def even_numbers(start, end):
    for number in range(start, end + 1):
        if number % 2 == 0:
            yield number
    

if __name__ == '__main__':
    while True:
        try:
            start = int(input('Введите начальное число: '))
            end = int(input('Введите конечное число: '))
            if start > end:
                raise ValueError
            for num in even_numbers(start, end):
                print(num)
            break
        except ValueError:
            print("введите корректное число")



