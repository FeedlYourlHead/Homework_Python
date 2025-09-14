user_input = input("Введите ваше выражение: ")
if "+" in user_input:
    user_list = user_input.split("+")
    result = int(user_list[0]) + int(user_list[1])
elif '-' in user_input:
    user_list = user_input.split("-")
    result = int(user_list[0]) - int(user_list[1])
elif '*' in user_input:
    user_list = user_input.split("*")
    result = int(user_list[0]) * int(user_list[1])
elif '/' in user_input:
    user_list = user_input.split("/")
    result = int(user_list[0]) / int(user_list[1])
print(f"Результат: {int(result)}")