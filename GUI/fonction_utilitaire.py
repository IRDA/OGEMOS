def is_decimal_number(string):
    if "." not in string and string.isdigit():
        return True
    if "." in string:
        decimal_parts = string.split(".")
        if len(decimal_parts) == 2 and decimal_parts[0].isdigit() and (
                decimal_parts[1].isdigit() or decimal_parts[1] == ""):
            return True
        else:
            return False
    return False


def is_valid_string(string):
    is_valid = True
    for character in string:
        if character.isalnum():
            pass
        else:
            if character in ["-", "/", " ", ",", "'", ".", "(", ")", "+"]:
                pass
            else:
                is_valid = False
    return is_valid
