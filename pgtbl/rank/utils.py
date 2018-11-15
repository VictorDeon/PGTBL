from groups.models import Group


def get_group_grades(discipline):
    """
    Get the grades of tbl groups
    """

    groups = Group.objects.filter(discipline=discipline)

    groups_grade = []
    for group in groups:
        final_grade = calcule_final_grade(group)

        group = {
            'id': group.id,
            'group': group.title,
            'grade': final_grade
        }
        groups_grade.append(group)

    return groups_grade


def calcule_final_grade(group):
    """
    Calcule group final grade.
    """

    grades = 0.0
    final_grade = 0.0

    for grade in group.grades.all():
        grades += grade.calcule_session_grade()

    if group.grades.count() > 0:
        final_grade = grades / group.grades.count()

    return final_grade