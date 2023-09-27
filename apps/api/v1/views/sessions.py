from rest_framework import generics, status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.session.selectors import get_free_slots, get_user_slots
from apps.session.services import delete_user_slot, cancel_session

from ..filters import SlotFilter
from ..permissions import IsClientOnly, IsParticipant, IsPsychologistOnly
from ..serializers.sessions import (CreateSessionSerializer,
                                    FreeSlotsSerializer, SlotSerializer)


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


class FreeSlotsView(generics.ListAPIView):
    """
    Список свободных слотов.
    Фильтр 'since=DD.MM.YYYY' отдает слоты в диапазоне 14 дней с даты.
    """
    permission_classes = (AllowAny,)
    serializer_class = FreeSlotsSerializer
    filterset_class = SlotFilter

    def get_queryset(self):
        return get_free_slots(self.kwargs.get('psychologist_id'))


class CreateSessionView(generics.CreateAPIView):
    """Создание сессии."""
    permission_classes = (IsClientOnly,)
    serializer_class = CreateSessionSerializer


class CancelSessionView(views.APIView):
    """
    Отмена сессии. При отмене клиентом ответ содержит информацию о
    возврате денежных средств.
    """
    permission_classes = (IsParticipant,)

    def delete(self, request, pk, format=None):
        details = cancel_session(request.user, pk)
        return Response(details, status=status.HTTP_204_NO_CONTENT)
