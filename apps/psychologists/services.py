from datetime import date
from typing import OrderedDict

from django.db import transaction
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import exceptions

from apps.psychologists.models import (ProfilePsychologist, Institute,
                                       Service)
from apps.users.models import CustomUser


@transaction.atomic
def create_psychologist(user_data: OrderedDict,
                        psychologist_data: OrderedDict
                        ) -> tuple[CustomUser, ProfilePsychologist]:
    """
    user_data = {"email": str}
    psychologist_data содержит поля, обязательные для заполнения плюс:
    psychologist_data = {
        "themes": [Theme],
        "approaches": [Approach],
        "institutes": [
            {"title": str,
            "speciality": str,
            "graduation_year": str,
            "file":  ContentFile,
            }
        ],
        "courses": [
            {"title": str,
            "speciality": str,
            "graduation_year": str,
            "file":  ContentFile,
            }
        ],
        "price": int,
        "experience": int,
    }
    """

    user = CustomUser.objects.create_user(
        is_client=False,
        is_psychologists=True,
        **user_data,
    )
    psychologist = create_profile(user, psychologist_data)
    return (user, psychologist)


def create_profile(user: CustomUser,
                   psychologist_data: OrderedDict,
                   ) -> ProfilePsychologist:
    themes = psychologist_data.pop('themes')
    approaches = psychologist_data.pop('approaches')
    institutes = get_or_create_institute(psychologist_data.pop('institutes'))
    courses = []
    if 'courses' in psychologist_data.keys():
        courses = get_or_create_courses(psychologist_data.pop('courses'))
    price = psychologist_data.pop('price')
    experience = psychologist_data.pop('experience')
    psychologist_data['started_working'] = count_started_working(experience)
    try:
        psychologist = ProfilePsychologist.objects.create(
            user=user,
            **psychologist_data,
        )
    except DjangoValidationError as e:
        raise exceptions.ValidationError(e.message_dict)
    psychologist.themes.add(*themes)
    psychologist.approaches.add(*approaches)
    for data in institutes + courses:
        education = data.pop('institute')
        psychologist.education.add(
            education, through_defaults=data
        )
    create_service(psychologist, price)
    return psychologist


def count_started_working(experience: int) -> date:
    """
    Считает год, с которого психолог начал рабочую практику
    """
    cur_year = date.today().year
    year = cur_year - experience
    return date(year, 1, 1)


def get_or_create_institute(institutes: list[OrderedDict]
                            ) -> list[OrderedDict]:
    """
    "institutes": [
            {"title": str,
            "speciality": str,
            "graduation_year": str,
            "file":  ContentFile,
            }
        ]
    """
    for education in institutes:
        title = education.pop('title')
        institute, _ = Institute.objects.get_or_create(
            title=title,
            is_higher=True,
        )
        education['institute'] = institute
    return institutes


def get_or_create_courses(courses: list[OrderedDict]) -> list[OrderedDict]:
    """
    "courses": [
            {"title": str,
            "speciality": str,
            "graduation_year": str,
            "file":  ContentFile,
            }
        ],
    """
    for education in courses:
        title = education.pop('title')
        course, _ = Institute.objects.get_or_create(
            title=title,
            is_higher=False,
        )
        education['institute'] = course
    return courses


def create_service(psychologist: ProfilePsychologist, price: int) -> Service:
    """
    Создает Service
    """
    service = Service.objects.create(
        psychologist=psychologist,
        price=price
    )
    return service
