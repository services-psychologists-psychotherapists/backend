from datetime import date
from typing import OrderedDict, Union

from django.db import transaction
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import exceptions

from apps.psychologists.models import (ProfilePsychologist, Institute,
                                       Service, Theme, Approach)
from apps.users.models import CustomUser


@transaction.atomic
def create_psychologist(user_data: OrderedDict,
                        psychologist_data: OrderedDict
                        ) -> tuple[CustomUser, ProfilePsychologist]:
    """
    user_data = {"email": str}
    psychologist_data содержит поля, обязательные для заполнения плюс:
    psychologist_data = {
        "themes": [{"title": str}],
        "approaches": [{"title": str}],
        "institutes" & "courses": [
            {"title": str,
            "speciality": str,
            "graduation_year": str,
            "document":  ContentFile,
            }
        ],
        "price": int,
        "experience": int,
    }
    """

    user = CustomUser.objects.create_user(
        is_client=False,
        is_psychologists=True,
        is_active=True,
        **user_data,
    )
    psychologist = create_profile(user, psychologist_data)
    return (user, psychologist)


def create_profile(user: CustomUser,
                   psychologist_data: OrderedDict,
                   ) -> ProfilePsychologist:
    themes = get_or_create_object(psychologist_data.pop('themes'), Theme)

    approaches = get_or_create_object(
        psychologist_data.pop('approaches'), Approach
    )

    institutes = get_or_create_education(
        psychologist_data.pop('institutes'), flag=True
    )

    courses = []
    if 'courses' in psychologist_data.keys():
        courses = get_or_create_education(
            psychologist_data.pop('courses'), flag=False
        )

    price = psychologist_data.pop('price')

    experience = psychologist_data.pop('experience')
    psychologist_data['started_working'] = count_started_working(experience)

    try:
        psychologist = ProfilePsychologist.objects.create(
            user=user,
            **psychologist_data,
        )
    except DjangoValidationError as e:
        raise exceptions.ValidationError(e.messages)

    psychologist.themes.add(*themes)
    psychologist.approaches.add(*approaches)
    for data in institutes + courses:
        education = data.pop('institute')
        psychologist.education.add(
            education, through_defaults=data
        )

    create_service(psychologist, price)

    return psychologist


@transaction.atomic
def update_psychologist(instance: ProfilePsychologist,
                        data: OrderedDict
                        ) -> ProfilePsychologist:
    """
    Образование можно только добавлять, предыдущий set не меняется.
    """

    if 'themes' in data:
        themes = get_or_create_object(data.pop('themes'), Theme)
        instance.themes.set(themes)
    if 'approaches' in data:
        approaches = get_or_create_object(data.pop('approaches'),
                                          Approach)
        instance.approaches.set(approaches)
    institutes = []
    if 'institutes' in data:
        institutes = get_or_create_education(data.pop('institutes'),
                                             flag=True)
    courses = []
    if 'courses' in data:
        courses = get_or_create_education(data.pop('courses'),
                                          flag=False)
    if 'price' in data:
        update_service(instance, data.pop('price'))

    for key, value in data.items():
        setattr(instance, key, value)
    instance.save()

    for data in institutes + courses:
        education = data.pop('institute')
        instance.education.add(
            education, through_defaults=data
        )

    return instance


def count_started_working(experience: int) -> date:
    """
    Считает год, с которого психолог начал рабочую практику
    """
    cur_year = date.today().year
    year = cur_year - experience
    return date(year, 1, 1)


def get_or_create_object(iterable: list[OrderedDict],
                         myclass: Union[Theme, Approach]
                         ) -> list[Union[Theme, Approach]]:
    """
    ("themes" | "approaches"): [{"title": str}],
    """
    for i, data in enumerate(iterable):
        obj, _ = myclass.objects.get_or_create(
            title=data['title'].title()
        )
        iterable[i] = obj
    return iterable


def get_or_create_education(iterable: list[OrderedDict],
                            flag: bool,
                            ) -> list[OrderedDict]:
    """
    ("institutes" | "courses"): [
            {"title": str,
            "speciality": str,
            "graduation_year": str,
            "document":  ContentFile,
            }
        ]
    """
    for data in iterable:
        title = data.pop('title')
        education, _ = Institute.objects.get_or_create(
            title=title,
            is_higher=flag,
        )
        data['institute'] = education
    return iterable


def create_service(psychologist: ProfilePsychologist,
                   price: int,
                   type: Service.Type = Service.Type.NOMATTER,
                   format: Service.Format = Service.Format.ONLINE,
                   ) -> Service:
    """
    Создает Service
    """
    service = Service.objects.create(
        psychologist=psychologist,
        price=price,
        type=type,
        format=format,
    )
    return service


def update_service(psychologist: ProfilePsychologist,
                   price: int,
                   type: Service.Type = Service.Type.NOMATTER,
                   format: Service.Format = Service.Format.ONLINE,
                   ) -> Service:
    """
    Изменяет Service
    """
    service = Service.objects.get(
        psychologist=psychologist,
        type=type,
        format=format,
    )
    service.price = price
    service.save()
    return service
