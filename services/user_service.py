def validate_login(users, email, password):
    clean_email = email.strip()

    for user in users:
        if user["email"].strip() == clean_email and user["password"] == password:
            return user

    return None


def email_exists(users, email):
    clean_email = email.strip()

    for user in users:
        if user["email"].strip() == clean_email:
            return True

    return False


def register_user(users, name, email, password, role):
    new_user = {
        "user_id": str(len(users) + 1),
        "name": name.strip(),
        "email": email.strip(),
        "password": password,
        "role": role
    }

    users.append(new_user)

    return new_user