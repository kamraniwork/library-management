import jwt
from rest_framework.viewsets import ViewSet
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .transactions import (
    register_user_with_email_or_phone_and_password,
    change_user_password,
    set_email,
    set_phone
)
from .tasks import (
    send_email_confirm,
    send_password_forget_token_email,
    send_sms_confirm,
    send_password_forget_token_sms,
)
from .utils import (
    check_send_email_or_phone_permission,
    validate_token,
    store_token_cache,
    check_phone_or_email
)

from .serializers import (
    RegisterEmailSerializer,
    RegisterPhoneSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    ChangePasswordWithForgotTokenSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ProfileUpdateSerializer,
    AddPhoneSerializer,
    AddEmailSerializer
)
from .models import Profile, User


class RegisterUser(ViewSet):
    """
    Register user with email and phone and send activate email
    use cache for handle time out activate email
    use @transactions.atomic for create user
    site can send activate email for per user 3 time in hours, handle by cache
    """

    @action(detail=False, methods=['post'], name='register user')
    def register_email(self, request):
        """
        register user by email and send activate email
        activate email contains jwt token and pk user
        and create access_token and refresh_token
        and store in redis with CACHE_STORE_TOKEN_{self.user.email} for 5 minutes( 60 * 5)
        """

        serializer = RegisterEmailSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            email = serializer.data['email'].lower()
            password = serializer.data['password']
            try:
                user = User.objects.get(username=username)
                if user and user.is_active:
                    return Response({'access denied': 'this email register before'}, status=403)
            except Exception:
                user = register_user_with_email_or_phone_and_password(
                    username=username,
                    email=email, password=password)
            # using cache for check limited send email
            # extension/utils.py
            check_send_email_or_phone_permission(username=username)
            user.set_password(password)
            user.save()
            token = RefreshToken.for_user(user=user)
            access_token = token.access_token
            token_jwt = {'username': user.username, 'email': user.email, 'refresh': str(token),
                         'access': str(access_token)}
            store_token_cache(token=token_jwt, username=user.username, time=settings.MAX_CONFIRM_REGISTER)
            send_email_confirm(email=email, token=str(access_token), inf=None, address='confirm')
            return Response({"success": "check email box"}, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)

    @action(detail=False, methods=['post'], name='register by phone')
    def register_phone(self, request):
        """
        register user by phone number and send activate sms
        activate sms contains jwt token and pk user
        and create access_token and refresh_token
        and store in redis with CACHE_STORE_TOKEN_{self.user.phone} for 5 minutes( 60 * 5)
        """
        serializer = RegisterPhoneSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            phone = serializer.data['phone']
            password = serializer.data['password']

            try:
                user = User.objects.get(username=username)
                if user and user.is_active:
                    return Response({'access denied': 'this email register before'}, status=403)

            except Exception:
                user = register_user_with_email_or_phone_and_password(
                    username=username,
                    phone=phone, password=password)

            # using cache for check limited send email
            # extension/utils.py
            check_send_email_or_phone_permission(username=username)
            user.set_password(password)
            user.save()

            token = RefreshToken.for_user(user=user)
            access_token = token.access_token
            token_jwt = {'username': user.username, 'phone': user.phone, 'refresh': str(token),
                         'access': str(access_token)}
            store_token_cache(token=token_jwt, username=user.username, time=settings.MAX_CONFIRM_REGISTER)

            send_sms_confirm(phone=phone, token=str(access_token), inf=None, address='confirm')

            return Response({"success": "check email box"}, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)


class ConfirmView(ViewSet):
    """
    confirm email, send confirm link to email or sms
    confirm link have a pk and token
    token is access token and pk is user.pk
    """

    @action(detail=False, methods=['get'], url_path=r'(?P<token>[a-zA-Z0-9._-]+)')
    def confirm_register(self, request, *args, **kwargs):
        """
        confirm register and user.is_active = True
        """
        token = kwargs.get('token')
        try:
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active and token == validate_token(username=user.username):
                user.is_active = True
                user.save()
                return Response({'success': 'your account is confirm'}, status=200)
        except Exception as e:
            return Response({'error': 'token is expire time'}, status=403)


class LoginView(ViewSet):
    """
    login user with email or phone
    and return access and refresh token
    """

    @action(detail=False, methods=['post'])
    def login_user(self, request):
        """
        login with email and password
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            user = User.objects.filter(username=username).first()
            if user is not None:
                if user.check_password(serializer.data['password']) and user.is_active:
                    token = RefreshToken.for_user(user=user)
                    access_token = token.access_token
                    token_jwt = {'username': user.username, 'refresh': str(token), 'access': str(access_token)}
                    store_token_cache(token=token_jwt, username=user.username,
                                      time=settings.MAX_STORE_TOKEN_TIME_OUT)
                    return Response({'tokens': token_jwt}, status=200)
                else:
                    return Response({'error': 'Password is invalid or user dont confirm'}, status=400)
            else:
                return Response({'error': 'username dont exist'}, status=400)
        else:
            return Response({'error': serializer.errors}, status=400)


class ForgotPassword(ViewSet):
    """
    handel forgot password user with phone or email.
    user give email or phone address and check if user with this email or phone number,
    send to for him(email,phone number), custom generate token,
    and user must write this token and email and new password for change password
    """

    @action(detail=False, methods=['post'])
    def forgot_password_email(self, request):
        """
        user send email address for send generate token to email
        """
        serialize_data = ForgotPasswordSerializer(data=request.data)
        if serialize_data.is_valid():
            username = serialize_data.data['username']
            user = User.objects.filter(username=username).first()
            if user is None:
                pass

            if user.is_active or user.email is not None:
                # per user can not this request more than 3 time in hours. extension/utils.py
                check_send_email_or_phone_permission(username=user.username)
                token = RefreshToken.for_user(user=user)
                access_token = token.access_token
                token_jwt = {'username': user.username, 'refresh': str(token), 'access': str(access_token)}
                store_token_cache(token=token_jwt, username=user.username,
                                  time=settings.MAX_CONFIRM_FORGOT_PASSWORD)
                send_password_forget_token_email(email=user.email, token=str(access_token))
                return Response({"success": "check email box"}, status=201)
            else:
                return Response({'error': 'This account is inactive.'}, status=403)
        else:
            return Response({"errors": serialize_data.errors}, status=400)

    @action(detail=False, methods=['post'])
    def forgot_password_phone(self, request):
        """
        user send phone number for send generate token with sms
        """
        serialize_data = ForgotPasswordSerializer(data=request.data)
        if serialize_data.is_valid(raise_exception=True):
            username = serialize_data.data['username']
            user = User.objects.filter(username=username).first()
            if user is None:
                return Response({'error': 'Phone number is invalid'}, status=400)

            if user.is_active or user.phone is not None:
                # per user can not this request more than 3 time in hours. extension/utils.py
                check_send_email_or_phone_permission(username=user.username)
                token = RefreshToken.for_user(user=user)
                access_token = token.access_token
                token_jwt = {'username': user.username, 'refresh': str(token), 'access': str(access_token)}
                store_token_cache(token=token_jwt, username=user.username,
                                  time=settings.MAX_CONFIRM_FORGOT_PASSWORD)
                # send token to sms. ./tasks.py
                send_password_forget_token_sms(phone=user.phone, token=str(access_token))

                return Response({"success": "check sms phone"}, status=201)
            else:
                return Response({'error': 'This account is inactive.'}, status=403)
        else:
            return Response({"errors": serialize_data.errors}, status=400)

    @action(detail=False, methods=['post'], url_path=r'forgot/(?P<token>[a-zA-Z0-9._-]+)')
    def change_password_after_forgot_password(self, request, *args, **kwargs):
        """
        user must enter email and new password and
        token that send to email
        """
        token = kwargs.get('token')
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            return Response({'error': 'token is invalid'}, status=400)

        if user.is_active and token == validate_token(user.username):
            serializer = ChangePasswordWithForgotTokenSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                # with @transaction.atomic in ./transactions.py
                password = serializer.data['password']
                change_user_password(user, password)
                token = RefreshToken.for_user(user=user)
                access_token = token.access_token
                token_jwt = {'username': user.username, 'refresh': str(token),
                             'access': str(access_token)}
                store_token_cache(token=token_jwt, username=user.username,
                                  time=settings.MAX_STORE_TOKEN_TIME_OUT)
                return Response({'tokens': token_jwt}, status=200)
            else:
                return Response({"errors": serializer.errors}, status=400)
        else:
            return Response({'error': 'Your account is inactive or token is expire time'}, status=403)


class ResetPassword(ViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if request.user.check_password(serializer.data['old_password']):
                if request.user.is_active:
                    change_user_password(request.user, serializer.data['password'])
                    token = RefreshToken.for_user(user=request.user)
                    access_token = token.access_token
                    token_jwt = {'username': request.user.username, 'refresh': str(token),
                                 'access': str(access_token)}

                    store_token_cache(token=token_jwt, username=request.user.username,
                                      time=settings.MAX_STORE_TOKEN_TIME_OUT)
                    return Response({'tokens': token_jwt}, status=200)
                else:
                    return Response({'error': 'user is deactivated, contact us.'}, status=403)
            else:
                return Response({'error': 'old password is wrong'}, status=403)
        else:
            return Response({"errors": serializer.errors}, status=400)


class ProfileViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(instance=profile, context={'request': request})
            return Response(serializer.data, status=200)
        except Exception:
            return Response({'error': 'serializer error'}, status=500)

    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileUpdateSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'error': serializer.errors})

        return Response({'success': 'update your information'}, status=200)


class AddEmailPhoneProfile(ViewSet):
    @action(detail=False, methods=['post'])
    def add_email(self, request):
        serializer = AddEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email'].lower()
            try:
                user = User.objects.filter(email=email).first()
                if user and user.is_active:
                    return Response({'access denied': 'this email register before'}, status=403)
            except Exception:
                # using cache for check limited send email
                # extension/utils.py
                check_send_email_or_phone_permission(username=email)

                token = RefreshToken.for_user(user=request.user)
                access_token = token.access_token
                token_jwt = {'username': request.user.username, 'refresh': str(token), 'access': str(access_token)}
                store_token_cache(token=token_jwt, username=request.user.username,
                                  time=settings.MAX_CONFIRM_REGISTER)

                send_email_confirm(email=email, token=str(access_token), address='add_field',
                                   inf=email)
                return Response({'success': 'check email for confirm email'}, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)

    @action(detail=False, methods=['post'])
    def add_phone(self, request):
        serializer = AddPhoneSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = serializer.data['phone']
            try:
                user = User.objects.filter(phone=phone).first()
                if user and user.is_active:
                    return Response({'access denied': 'this phone number register before'}, status=403)
            except Exception:
                # using cache for check limited send email
                # extension/utils.py
                check_send_email_or_phone_permission(username=phone)
                token = RefreshToken.for_user(user=request.user)
                access_token = token.access_token
                token_jwt = {'username': request.user.username, 'refresh': str(token), 'access': str(access_token)}
                store_token_cache(token=token_jwt, username=request.user.username,
                                  time=settings.MAX_CONFIRM_REGISTER)

                send_sms_confirm(phone=phone, token=str(access_token), address='add_field',
                                 inf=phone)
                return Response({'success': 'add new phone number for you'}, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)

    @action(detail=False, methods=['get'], url_path=r'(?P<token>[a-zA-Z0-9._-]+)/(?P<inf>[a-zA-Z0-9.@_]+)')
    def confirm_email_phone(self, request, *args, **kwargs):
        token = kwargs.get('token')
        inf = kwargs.get('inf')

        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        user = User.objects.get(id=payload['user_id'])
        if user.is_active:
            if check_phone_or_email(inf):
                set_phone(user, inf)
            else:
                set_email(user, inf)
            return Response({'success': 'your email or phone is confirm'}, status=200)
        else:
            return Response({'error': 'user is in active'}, status=403)
