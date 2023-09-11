from datetime import date

from django.db import transaction

from apps.psychologists.models import (ProfilePsychologist, Institute,
                                       Service)
# from apps.psychologists.selectors import get_themes, get_approaches
from apps.users.models import CustomUser


@transaction.atomic
def create_psychologist(user_data, psychologist_data):
    user = CustomUser.objects.create_user(
        is_client=False,
        is_psychologists=True,
        **user_data,
    )
    psychologist = create_profile(user, psychologist_data)
    return psychologist


def create_profile(user, psychologist_data):
    themes = psychologist_data.pop('themes')
    approaches = psychologist_data.pop('approaches')
    institutes = get_or_create_institute(psychologist_data.pop('institutes'))
    courses = get_or_create_courses(psychologist_data.pop('courses'))
    price = psychologist_data.pop('price')
    experience = psychologist_data.pop('experience')
    psychologist_data['started_working'] = count_started_working(experience)
    psychologist = ProfilePsychologist.objects.create(
        user=user,
        **psychologist_data,
    )
    psychologist.themes.add(*themes)
    psychologist.approaches.add(*approaches)
    for data in institutes + courses:
        education = data.pop('institute')
        psychologist.education.add(
            education, through_defaults=data
        )
    create_service(psychologist, price)
    return psychologist


def count_started_working(experience):
    cur_year = date.today().year
    year = cur_year - experience
    return date(year, 1, 1)


def get_or_create_institute(institutes):
    for education in institutes:
        title = education.pop('title')
        institute, _ = Institute.objects.get_or_create(
            title=title,
            is_higher=True,
        )
        education['institute'] = institute
    return institutes


def get_or_create_courses(courses):
    for education in courses:
        title = education.pop('title')
        course, _ = Institute.objects.get_or_create(
            title=title,
            is_higher=False,
        )
        education['institute'] = course
    return courses


def create_service(psychologist, price):
    service = Service.objects.create(
        psychologist=psychologist,
        price=price
    )
    return service
