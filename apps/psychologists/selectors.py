from django.db.models import Prefetch, F
from django.shortcuts import get_object_or_404

from apps.psychologists.models import (ProfilePsychologist, Institute,
                                       Service)
from apps.users.models import CustomUser


def get_psychologist(user: CustomUser) -> ProfilePsychologist:
    queryset = ProfilePsychologist.objects.all().select_related(
        'user').prefetch_related(
            Prefetch('themes'),
            Prefetch('approaches'),
            Prefetch('education'),
        )
    return get_object_or_404(queryset, user=user)


def get_education(user: ProfilePsychologist,
                  flag: bool) -> list[Institute]:
    education = user.education.filter(is_higher=flag)
    education = education.annotate(
            speciality=F('psychoeducation__speciality'),
            graduation_year=F('psychoeducation__graduation_year'),
            document=F('psychoeducation__document'),
        )
    return education


def get_service(psychologist: ProfilePsychologist,
                type: Service.Type = Service.Type.NOMATTER,
                format: Service.Format = Service.Format.ONLINE,
                ) -> Service:
    return get_object_or_404(
        Service,
        psychologist=psychologist,
        type=type,
        format=format
    )
