"""
    attribution des rôles
"""

def is_student(user):
    return user.is_authenticated and user.groups.filter(
        name="student-group"
    ).exists()


def is_instructor(user):
    return user.is_authenticated and user.groups.filter(
        name="instructor-group"
    ).exists()
