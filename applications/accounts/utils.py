

def validate_password(password):
    """
    Validation check for strong password.
    :param password:
    :return:
    """
    min_length = 8

    # At least one letter and one non-letter
    first_isalpha = password[0].isalpha()
    if len(password) < min_length or all(c.isalpha() == first_isalpha for c in password):
        raise forms.ValidationError("Password must be at least %d characters long, and contain "
                                    "one letter and one digit or special character." % min_length)

    return password