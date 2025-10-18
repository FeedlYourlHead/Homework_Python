def requires_permission(permission):
    def wrapper():
        pass
    return wrapper


@requires_permission
def delete_user(user_id):
    return f"User {user_id} deleted"
