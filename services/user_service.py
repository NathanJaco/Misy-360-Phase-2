def validate_login(users, email, password):
    for user in users:
        if user["email"] == email and user["password"] == password:
            return user

    return None


def email_exists(users, email):
    for user in users:
        if user["email"] == email:
            return True

    return False


def register_user(users, name, email, password, role):
    new_user = {
        "name": name,
        "email": email,
        "password": password,
        "role": role
    }

    users.append(new_user)

    return new_user