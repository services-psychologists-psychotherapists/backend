from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.psychologists.models import ProfilePsychologist
from apps.session.selectors import get_free_slots, get_user_slots

from ..filters import SlotFilter
from ..mixins import PsychoBasedMixin
from ..permissions import IsPsychologistOnly
from ..serializers.sessions import SlotSerializer, FreeSlotsSerializer


class ListCreateSlotView(generics.ListCreateAPIView):
    permission_classes = (IsPsychologistOnly,)
    serializer_class = SlotSerializer
    filterset_class = SlotFilter

    def get_queryset(self):
        return get_user_slots(self.request.user)

    def perform_create(self, serializer):
        serializer.save(psychologist=self.request.user.psychologists)


class FreeSlotsView(PsychoBasedMixin, generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FreeSlotsSerializer

    def get_queryset(self):
        return get_free_slots(self.get_psychologist())
