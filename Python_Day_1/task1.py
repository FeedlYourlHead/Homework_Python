type_ed_mat = input("Введите тип учебного материала(книга/видео): ")
while True:
    try:
        cost_mat = int(input("Введите стоимость материала: "))
        if cost_mat <= 0:
            print('Введите положительное число')
            continue
        break
    except ValueError:
        print('Введите целое число')
cat_mat = input("Введите категорию материала: ")

print(f"Материал добавлен: Тип - {type_ed_mat}, Стоимость - {cost_mat}, Категория - {cat_mat}")