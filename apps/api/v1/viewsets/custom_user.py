from base64 import urlsafe_b64encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from djoser import signals
from djoser.conf import settings

from apps.users.models import CustomUser
from ..serializers.custom_user import CustomUserSerializer


class CustomUsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ['post', 'get']

    @action(
        detail=False,
        methods=['get'],
        url_path='me',
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'],
        url_path='activation'
    )
    def activation(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        if not settings.EMAIL.activation:
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if not user.is_active:
            context = {'user': user}
            signals.activation.send(
                sender=self.__class__, user=user, request=request,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['post'],
        url_path='resend_activation'
    )
    def resend_activation(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        if not settings.EMAIL.activation:
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        if not user.is_active:
            context = {'user': user}
            signals.activation.send(
                sender=self.__class__, user=user, request=request,
                context=context
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['post'],
        url_path='reset_password'
    )
    def reset_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        context = {
            'user': user,
            'uid': urlsafe_b64encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        }

        signals.reset_password.send(
            sender=self.__class__, user=user, request=request, context=context
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['post'],
        url_path='reset_password_confirm'
    )
    def reset_password_confirm(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        new_password = serializer.validated_data['new_password']

        user.set_password(new_password)
        user.save()

        signals.password_reset.send(
            sender=self.__class__, user=user, request=request
        )

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['post'],
        url_path='set_password',
        permission_classes=[IsAuthenticated]
    )
    def set_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        new_password = serializer.validated_data['new_password']

        user.set_password(new_password)
        user.save()

        signals.set_password.send(sender=self.__class__, user=user,
                                  request=request)

        return Response(status=status.HTTP_204_NO_CONTENT)
