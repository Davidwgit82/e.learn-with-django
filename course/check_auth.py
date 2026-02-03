"""
    Attribuer des droits en fonction du rôle
    des users.
"""

def is_student_check(user):
    return user.is_authenticated and user.is_student

def is_instructor_check(user):
    return user.is_authenticated and user.is_instructor