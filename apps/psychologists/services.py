from datetime import date
from typing import OrderedDict

from django.db import transaction
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
    ObjectDoesNotExist,
)
from django.http import HttpRequest
from rest_framework import exceptions

from apps.core.models import UploadFile
from apps.psychologists.models import (
    ProfilePsychologist,
    Institute,
    Service,
    Theme,
    Approach,
)
from apps.psychologists.threads import PsychoConfirmationFormEmailThread
from apps.users.models import CustomUser


@transaction.atomic
def create_psychologist(
    validated_data: OrderedDict,
    request: HttpRequest,
) -> tuple[CustomUser, ProfilePsychologist]:
    """
    psychologist_data содержит поля, обязательные для заполнения плюс:
    validated_data = {
        "themes": [{"title": str}],
        "approaches": [{"title": str}],
        "institutes" & "courses": [
            {"title": str,
            "speciality": str,
            "graduation_year": str,
            "document": str,
            }
        ],
        "price": int,
        "experience": int,
    }
    """
    email = validated_data.pop("email")

    user = CustomUser.objects.create_user(
        is_client=False,
        is_psychologists=True,
        is_active=True,
        email=email,
    )
    psychologist = create_profile(user, validated_data)

    PsychoConfirmationFormEmailThread(request, user).start()

    return (user, psychologist)


@transaction.atomic
def create_profile(
    user: CustomUser,
    psychologist_data: OrderedDict,
) -> ProfilePsychologist:
    themes = get_themes(psychologist_data.pop("themes"))

    approaches = get_or_create_approaches(psychologist_data.pop("approaches"))

    institutes = get_or_create_education(psychologist_data.pop("institutes"), flag=True)

    courses = []
    if "courses" in psychologist_data.keys():
        courses = get_or_create_education(psychologist_data.pop("courses"), flag=False)

    price = psychologist_data.pop("price")

    experience = psychologist_data.pop("experience")
    psychologist_data["started_working"] = count_started_working(experience)

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
        education = data.pop("institute")
        psychologist.education.add(education, through_defaults=data)

    create_service(psychologist, price)

    return psychologist


@transaction.atomic
def update_psychologist(
    instance: ProfilePsychologist, data: OrderedDict
) -> ProfilePsychologist:
    """
    Образование можно только добавлять, предыдущий set не меняется.
    """

    if "themes" in data:
        themes = get_themes(data.pop("themes"))
        instance.themes.set(themes)
    if "approaches" in data:
        approaches = get_or_create_approaches(data.pop("approaches"))
        instance.approaches.set(approaches)
    institutes = []
    if "institutes" in data:
        institutes = get_or_create_education(data.pop("institutes"), flag=True)
    courses = []
    if "courses" in data:
        courses = get_or_create_education(data.pop("courses"), flag=False)
    if "price" in data:
        update_service(instance, data.pop("price"))

    for key, value in data.items():
        setattr(instance, key, value)
    instance.save()

    for data in institutes + courses:
        education = data.pop("institute")
        instance.education.add(education, through_defaults=data)

    return instance


def count_started_working(experience: int) -> date:
    """
    Считает год, с которого психолог начал рабочую практику
    """
    cur_year = date.today().year
    year = cur_year - experience
    return date(year, 1, 1)


def get_themes(iterable: list[OrderedDict]) -> list[Theme]:
    """
    ("themes"): [{"title": str}].
    """
    output = []
    for data in iterable:
        try:
            obj = Theme.objects.get(title=data["title"].title())
            output.append(obj)
        except ObjectDoesNotExist:
            pass
    return output


def get_or_create_approaches(iterable: list[OrderedDict]) -> list[Approach]:
    """
    ("approaches"): [{"title": str}].
    """
    for i, data in enumerate(iterable):
        obj, _ = Approach.objects.get_or_create(title=data["title"].title())
        iterable[i] = obj
    return iterable


def get_or_create_education(
    iterable: list[OrderedDict],
    flag: bool,
) -> list[OrderedDict]:
    """
    ("institutes" | "courses"): [
            {"title": str,
            "speciality": str,
            "graduation_year": str,
            "document":  str,
            }
        ]
    """
    for data in iterable:
        title = data.pop("title")
        education, _ = Institute.objects.get_or_create(
            title=title,
            is_higher=flag,
        )
        data["institute"] = education
        document = data.pop("document")
        file = UploadFile.objects.get(id=document)
        data["document"] = file
    return iterable


def create_service(
    psychologist: ProfilePsychologist,
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


def update_service(
    psychologist: ProfilePsychologist,
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
