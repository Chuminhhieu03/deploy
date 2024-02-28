from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from .models import UserUpgrade
from .models import FeedBack
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import generate_token
from django.views.generic import View
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from datetime import datetime
# Create your views here.


def handleLogin(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username).first()
        if user is None:
            messages.warning(request, "Tài khoản không tồn tại")
            return render(request, 'login.html')
        if not user.is_active:
            messages.warning(request, "Tài khoản chưa được kích hoạt")
            return render(request, 'login.html')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.warning(request, "Mật khẩu không chính xác")
            return render(request, 'login.html')
        login(request, user)
        return redirect('/')


def logout(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    auth_logout(request)
    messages.info(request, "Đăng xuất thành công")
    return redirect('/user/login')


def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # check username is already exist or not
        if User.objects.filter(username=username).exists():
            messages.warning(request, "Tài khoản này đã tồn tại trong hệ thống")
            return render(request, 'signup.html')
        # check email is already exist or not
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email này đã tồn tại")
            return render(request, 'signup.html')
        # check password is match or not
        if pass1 != pass2:
            messages.warning(request, "Mật khẩu không khớp")
            return render(request, 'signup.html')
        # create
        user = User.objects.create_user(
            username=username, email=email, password=pass1)
        user.first_name = f"Người dùng #{user.id}"
        user.is_active = False
        user.userprofile = UserProfile()
        user.userprofile.save()
        user.userupgrade = UserUpgrade()
        user.userupgrade.save()
        user.save()
        email_subject = "Kích hoạt tài khoản"
        message = render_to_string('activate_account.html', {
            'user': user,
            'domain': '127.0.0.1:8000',
            'uid':  urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        email_message = EmailMessage(
            email_subject, message, settings.EMAIL_HOST_USER, [email])
        email_message.send()
        messages.success(
            request, "Tài khoản của bạn đã được tạo thành công, vui lòng kích hoạt")
        return render(request, 'login.html')


def resetPassword(request):
    if request.method == "GET":
        return render(request, 'resetPassword.html')
    if request.method == "POST":
        email = request.POST['email']
        users = User.objects.filter(email=email)
        if users.exists():
            user = users.first()  # Lấy người dùng đầu tiên trong danh sách
            email_subject = '[Lấy lại mật khẩu]'
            message = render_to_string('reset-user-password.html', {
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': PasswordResetTokenGenerator().make_token(user)
            })
            email_message = EmailMessage(
                email_subject, message, settings.EMAIL_HOST_USER, [email])
            email_message.send()
            messages.success(
                request, "Kiểm tra email của bạn để lấy lại mật khẩu")
            return render(request, 'login.html')
        else:
            messages.warning(request, "Email không tồn tại trong hệ thống")
            return render(request, 'login.html')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Kích hoạt tài khoản thành công")
            return redirect('/user/login')
        messages.warning(request, "Bạn đã kích hoạt tài khoản rồi")
        return render(request, 'login.html')


class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.warning(
                    request, "Link này không còn hiệu luực, vui lòng thử lại với link mới")
                return render(request, 'login.html')
        except DjangoUnicodeDecodeError as identifier:
            pass
        messages.success(request, "Vui lòng nhập mật khẩu mới")
        return render(request, 'set_new_password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        if password != confirm_password:
            messages.warning(request, "Mật khẩu không khớp")
            return render(request, 'set_new_password.html', context)
        # check valid password with condition that password must have at least 1 uppercase, 1 lowercase, 1 number and 1 special character
        if not any(char.isupper() for char in password):
            messages.warning(
                request, "Mật khẩu phải có ít nhất 1 ký tự viết hoa")
            return render(request, 'set_new_password.html', context)
        if not any(char.islower() for char in password):
            messages.warning(
                request, "Mật khẩu phải có ít nhất 1 ký tự viết thường")
            return render(request, 'set_new_password.html', context)
        if not any(char.isdigit() for char in password):
            messages.warning(request, "Mật khẩu phải có ít nhất 1 chữ số")
            return render(request, 'set_new_password.html', context)
        if not any(not char.isalnum() for char in password):
            messages.warning(
                request, "Mật khẩu phải có ít nhất 1 ký tự đặc biệt")
            return render(request, 'set_new_password.html', context)
        if len(password) < 8:
            messages.warning(
                request, "Mật khẩu phải có ít nhất 8 ký tự")
            return render(request, 'set_new_password.html', context)
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(
                request, "Mật khẩu của bạn đã được thay đổi thành công")
            return redirect('/user/login/')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, "Một lỗi đã xảy ra, vui lòng thử lại")
            return render(request, 'set_new_password.html', context)


def index(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    return render(request, 'profile.html')


def edit_profile(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == "GET":
        return render(request, 'editprofile.html')
    if request.method == "POST":
        user = request.user
        avatar = request.FILES.get('avatar', "")
        fullname = request.POST['full_name']
        address = request.POST['address']
        phone = request.POST['phone']
        dob = request.POST['birth']
        # check avatar is not a image file



        if avatar:
            user.userprofile.avatar = avatar
        user.first_name = fullname
        user.userprofile.address = address
        user.userprofile.phone = phone
        user.date_joined = datetime.strptime(dob, '%d/%m/%Y')
        user.userprofile.save()
        user.save()
        messages.success(request, "Cập nhật thông tin thành công")
        return render(request, 'editprofile.html')


def feedback_user(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == "GET":
        return render(request, 'feedback.html')
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        feedback = FeedBack(user=request.user, title=title, content=content,email=request.user.email,phone=request.user.userprofile.phone)
        feedback.save()
        messages.success(request, "Gửi phản hồi thành công, chúng tôi sẽ liên hệ với bạn sớm nhất")
        return render(request, 'feedback.html')


def changepassword(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.method == "GET":
        return render(request, 'changepassword.html')
    if request.method == "POST":
        old_password = request.POST['oldPassword']
        new_password = request.POST['newPassword']
        confirm_password = request.POST['confirmNewPassword']
        user = request.user
        if not user.check_password(old_password):
            messages.warning(request, "Mật khẩu cũ không chính xác")
            return render(request, 'changepassword.html')
        if new_password != confirm_password:
            messages.warning(request, "Mật khẩu mới không khớp")
            return render(request, 'changepassword.html')
        # check valid password with condition that password must have at least 1 uppercase, 1 lowercase, 1 number and 1 special character
        if not any(char.isupper() for char in new_password):
            messages.warning(
                request, "Mật khẩu phải có ít nhất 1 ký tự viết hoa")
            return render(request, 'changepassword.html')
        if not any(char.islower() for char in new_password):
            messages.warning(
                request, "Mật khẩu phải có ít nhất 1 ký tự viết thường")
            return render(request, 'changepassword.html')
        if not any(char.isdigit() for char in new_password):
            messages.warning(request, "Mật khẩu phải có ít nhất 1 chữ số")
            return render(request, 'changepassword.html')
        if not any(not char.isalnum() for char in new_password):
            messages.warning(
                request, "Mật khẩu phải có ít nhất 1 ký tự đặc biệt")
            return render(request, 'changepassword.html')
        if len(new_password) < 8:
            messages.warning(
                request, "Mật khẩu phải có ít nhất 8 ký tự")
            return render(request, 'changepassword.html')
        user.set_password(new_password)
        user.save()
        messages.success(
            request, "Mật khẩu của bạn đã được thay đổi thành công")
        return redirect('/user/login')


def upgrade(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userupgrade.state == "2":
        messages.warning(request, "Yêu cầu nâng cấp tài khoản của bạn đang chờ duyệt")
        return redirect('upgrade_success')
    if request.user.userupgrade.state == "1":
        messages.warning(request, "Tài khoản của bạn đã được nâng cấp")
        return redirect('upgrade_success')
    if request.method == "GET":
        return render(request, 'upgrade.html')
    if request.method == "POST":
        return render(request, 'upgrade_checkout.html')


def upgrade_checkout(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    if request.user.userupgrade.state == "2":
        messages.warning(request, "Yêu cầu nâng cấp tài khoản của bạn đang chờ duyệt")
        return redirect('upgrade_success')
    if request.user.userupgrade.state == "1":
        messages.warning(request, "Tài khoản của bạn đã được nâng cấp")
        return redirect('upgrade_success')
    if request.method == "GET":
        return render(request, 'upgrade_checkout.html')
    if request.method == "POST":
        user = request.user
        if user is None:
            messages.warning(request, "Tài khoản không tồn tại")
            return redirect('upgrade')
        user.userupgrade.state = '2'
        user.userupgrade.save()
        messages.success(request, "Yêu cầu nâng cấp tài khoản đã được gửi")
        return redirect('upgrade_success')
        
def upgrade_success(request):
    if request.user.is_authenticated == False:
        messages.warning(request, "Bạn chưa đăng nhập")
        return redirect('login')
    return render(request, 'upgrade_success.html')
