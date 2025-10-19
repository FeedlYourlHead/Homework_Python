def requires_permission(permission):
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_user_permissions = ['admin']
            if permission in current_user_permissions:
                return func(*args, **kwargs)
            else:
                return f'Ошибка: у пользователя {permission} нет прав доступа'
        return wrapper
    return decorator


@requires_permission('default_user')
def delete_user(user_id):
    return f"User {user_id} deleted"

@requires_permission('admin')
def edit_user(user_id):
    return f'User {user_id} was edited'

print(delete_user("123"))
print(edit_user('123'))
#Честно говоря не знаю, это ли требовалось в задании?
