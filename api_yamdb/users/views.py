from django.shortcuts import render

from .models import User

ROLES = {
    'user': 'user',
    'moderator': 'moderator',
    'admin': 'admin',
}


def import_users(request):
    template = "users/index.html"
    with open('static/data/users.csv', 'r') as file:
        for ind, row in enumerate(file):
            if ind == 0:
                continue
            row = row.split(',')
            bool_staff = False
            if row[3] == "admin":
                bool_staff = True
            new_user = User.objects.create_user(id=row[0],
                                                username=row[1],
                                                email=row[2],
                                                role=ROLES[row[3]],
                                                bio=row[4],
                                                first_name=row[5],
                                                last_name=row[6],
                                                is_staff=bool_staff,
                                                password="test")
            new_user.save()
    return render(request, template)
