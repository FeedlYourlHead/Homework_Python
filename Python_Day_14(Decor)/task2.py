def to_string(func):
    def wrapper():
        original_result = func()
        modified_result = str(original_result)
        return modified_result
    return wrapper

@to_string
def get_number():
    return 42

@to_string
def get_text():
    return "Hello, World!"

print(get_number())
print(type(get_number()))
print(get_text())
print(type(get_text()))
