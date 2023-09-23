from django.shortcuts import get_object_or_404

from apps.psychologists.models import ProfilePsychologist


class PsychoBasedMixin:
    def get_psychologist(self):
        return get_object_or_404(
            ProfilePsychologist, id=self.kwargs.get('psychologist_id')
        )
