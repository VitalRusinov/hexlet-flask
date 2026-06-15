def filter_users_by_name_contains(users, search_term):
    """Фильтрует пользователей, у которых search_term содержится где угодно в имени"""
    if not search_term:
        return users

    search_term_lower = search_term.lower()
    return [
        user for user in users
        if search_term_lower in user["name"].lower()
    ]

def validate_user(user):
    errors = {}

    if not user.get('name'):
        errors['name'] = "Can't be blank"
    elif len(user['name']) <= 4:
        errors['name'] = "Nickname must be greater than 4 characters"

    if not user.get('email'):
        errors['email'] = "Can't be blank"

    return errors

def generate_id(users):
    return max((u["id"] for u in users), default=0) + 1