from django.shortcuts import get_object_or_404

from apps.users.models import CustomUser

from .models import Slot
from .threads import SessionCancelEmailThread


def delete_user_slot(user: CustomUser, pk: int) -> None:
    """
    Удаление психологом слота из расписания.
    Если слот занят сессией, участники получают уведомление по почте.
    """
    slot = get_object_or_404(Slot, psychologist__user=user, pk=pk)

    if not slot.is_free:
        SessionCancelEmailThread(slot.session, 'psycholohist', False).run()

    slot.delete()
    return None
