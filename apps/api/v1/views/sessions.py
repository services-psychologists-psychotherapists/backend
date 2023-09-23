from rest_framework import generics, views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.session.selectors import get_free_slots, get_user_slots
from apps.session.services import delete_user_slot

from ..filters import SlotFilter
from ..mixins import PsychoBasedMixin
from ..permissions import IsPsychologistOnly
from ..serializers.sessions import SlotSerializer, FreeSlotsSerializer


class ListCreateSlotView(generics.ListCreateAPIView):
    """
    Создание слота и получение списка слотов психолога в ЛК.
    Фильтр 'since=DD.MM.YYYY' отдает слоты в диапазоне календаря с даты.
    """
    permission_classes = (IsPsychologistOnly,)
    serializer_class = SlotSerializer
    filterset_class = SlotFilter

    def get_queryset(self):
        return get_user_slots(self.request.user)

    def perform_create(self, serializer):
        serializer.save(psychologist=self.request.user.psychologists)


class DeleteSlotView(views.APIView):
    """Удаление слота из расписания в ЛК психолога."""
    permission_classes = (IsPsychologistOnly,)

    def delete(self, request, pk, format=None):
        delete_user_slot(request.user, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FreeSlotsView(PsychoBasedMixin, generics.ListAPIView):
    """
    Список свободных слотов.
    Фильтр 'since=DD.MM.YYYY' отдает слоты в диапазоне календаря с даты.
    """
    permission_classes = (AllowAny,)
    serializer_class = FreeSlotsSerializer
    filterset_class = SlotFilter

    def get_queryset(self):
        return get_free_slots(self.kwargs.get('psychologist_id'))
