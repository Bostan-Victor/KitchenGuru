from rest_framework import generics, status
from authorization import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from users import models
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.core.signing import Signer
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse


class RegisterView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer


@api_view(['POST'])
def login_view(request):
    data = request.data
    try:
        user = models.Users.objects.get(username=data['username_email'])
    except models.Users.DoesNotExist:
        try:
            user = models.Users.objects.get(email=data['username_email'])
        except:
            return Response({"message": "Username or Email invalid!"}, status=status.HTTP_404_NOT_FOUND)
    try:
        profile = models.Profiles.objects.get(user_id=user.id)
        profile.last_login = datetime.now()
        profile.save()
    except:
        return Response({"message": "Profile does not exist!"}, status=status.HTTP_404_NOT_FOUND)
    if check_password(data['password'], user.password):
        refresh = RefreshToken.for_user(user)
        access_token =  str(refresh.access_token)
        if user.is_superuser:
            return Response({"message": "Admin logged in",
                             "access_token": access_token,
                             "refresh_token": str(refresh)}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User logged in!",
                    "access_token": access_token,
                    "refresh_token": str(refresh) }, status=status.HTTP_200_OK)
    return Response({"message": "Password invalid!"}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        if check_password(data['password'], user.password):
            if len(data['new_password']) < 8:
                return Response({"message": "Password shorter than 8 characters"}, status=status.HTTP_400_BAD_REQUEST)
            if data['new_password'] != data['confirm_new_password']:
                return Response({"message": "New password fields do not match!"}, status=status.HTTP_400_BAD_REQUEST)
            new_password = data['new_password']
            user.set_password(new_password)
            user.save()
            profile = models.Profiles.objects.get(user_id=user.id)
            profile.updated = datetime.now()
            profile.save()
            return Response({"message": "Password updated succesfully!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Old password is incorrect!"}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
def password_recovery_request_view(request):
    data = request.data
    try:
        user = models.Users.objects.get(email=data['email'])
    except:
        return Response({'message': 'There is no account created with this email!'}, status=status.HTTP_404_NOT_FOUND)
    pass_recovery_object = models.PasswordRecovery.objects.get(user_id=user.id)
    pass_recovery_object.created_at = datetime.now()
    pass_recovery_object.is_used = False
    pass_recovery_object.save()
    link = request.build_absolute_uri(reverse('password-recovery-change') + f'?user_id={user.id}')
    send_mail(
        'KitchenGuru - Password Recovery',
        f'Click this link to change your password:\n{link}',
        'KitchenGuru@mail.com',
        [data['email']],
        fail_silently=False
    )
    return Response({'message': 'Email sent succesfully!'}, status=status.HTTP_200_OK)
            

class PasswordRecoveryChangeView(generics.UpdateAPIView):
    serializer_class = serializers.PasswordRecoveryChange

    def update(self, request, *args, **kwargs):
        data = request.data
        user_id = request.query_params.get('user_id')
        user = models.Users.objects.get(id=user_id)
        pass_recovery_object = models.PasswordRecovery.objects.get(user_id=user_id)
        created_at = pass_recovery_object.created_at
        now = timezone.now()
        delta = timedelta(minutes=15)

        if pass_recovery_object.is_used:
            return Response({"message": "The link has been used already!"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if now - created_at > delta:
                return Response({"message": "The link has expired!"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                if len(data['new_password']) < 8:
                    return Response({"message": "Password shorter than 8 characters"}, status=status.HTTP_400_BAD_REQUEST)
                if data['new_password'] != data['confirm_new_password']:
                    return Response({"message": "New password fields do not match!"}, status=status.HTTP_400_BAD_REQUEST)
                new_password = data['new_password']
                user.set_password(new_password)
                user.save()
                profile = models.Profiles.objects.get(user_id=user.id)
                profile.updated = datetime.now()
                profile.save()
                pass_recovery_object.is_used = True
                pass_recovery_object.save()
                return Response({"message": "Password updated succesfully!"}, status=status.HTTP_200_OK)
