def is_teacher(user):
    if user.is_teacher() and user.is_authenticated:
        return True
    else:
        return False
