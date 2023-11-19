# Django에서 제공하는 forms 모듈과 Django 인증 관련 폼들을 가져옵니다.
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm as AuthPasswordChangeForm, AuthenticationForm
# 사용자 프로필 모델을 가져옵니다.
from .models import Profile
# 사용자 모델을 가져옵니다.
from django.contrib.auth import get_user_model
# 비밀번호 체크를 위한 함수를 가져옵니다.
from django.contrib.auth.hashers import check_password

# 사용자 생성을 위한 커스텀 폼입니다. Django의 기본 UserCreationForm을 상속받아 사용합니다.
class CustomUserCreationForm(UserCreationForm):
    # 사용자의 닉네임을 입력받기 위한 필드를 추가합니다.
    nickname = forms.CharField(max_length=50)

    class Meta(UserCreationForm.Meta):
        # 기본 UserCreationForm의 필드에 닉네임 필드를 추가합니다.
        fields = UserCreationForm.Meta.fields + ('nickname',)

    # 폼에서 입력받은 데이터를 바탕으로 사용자를 생성하고 저장합니다.
    def save(self, commit=True):
        # super().save(commit=False)를 호출하여 사용자 객체를 생성합니다. commit=False는 데이터베이스에 바로 저장하지 않습니다.
        user = super().save(commit=False)
        user.save()
        # 사용자 객체에 프로필이 연결되어 있지 않다면 프로필을 생성합니다.
        if not hasattr(user, 'profile'):
            Profile.objects.create(user=user)
        # 생성한 프로필의 닉네임을 폼에서 입력받은 닉네임으로 설정합니다.
        user.profile.nickname = self.cleaned_data['nickname']
        # commit이 True라면 프로필을 데이터베이스에 저장합니다.
        if commit:
            user.profile.save()
        return user

# 사용자의 닉네임을 변경하기 위한 폼입니다.
class NicknameChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname']

    # 폼에서 입력받은 닉네임을 바탕으로 사용자의 닉네임을 변경하고 저장합니다.
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile

# 사용자의 비밀번호를 변경하기 위한 폼입니다. Django의 기본 PasswordChangeForm을 상속받아 사용합니다.
class PasswordChangeForm(AuthPasswordChangeForm):
    # 현재 비밀번호를 확인하기 위한 필드를 추가합니다.
    password_check = forms.CharField(max_length=32, widget=forms.PasswordInput, label='현재 비밀번호 확인')

    # 입력받은 현재 비밀번호가 실제 비밀번호와 일치하는지 검증합니다.
    def clean_password_check(self):
        old_password = self.cleaned_data.get('이전 비밀번호')
        password_check = self.cleaned_data.get('비밀번호 체크')
        if password_check != old_password:
            raise forms.ValidationError('현재 비밀번호와 일치하지 않습니다.')
        return password_check

# 사용자 계정을 삭제하기 위한 폼입니다. Django의 기본 AuthenticationForm을 상속받아 사용합니다.
class UserDeleteForm(AuthenticationForm):
    # 비밀번호를 입력받기 위한 필드를 추가합니다.
    password = forms.CharField(widget=forms.PasswordInput)

    # 폼의 인스턴스가 생성될 때 실행되는 메소드입니다. request 인자를 받아 저장합니다.
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserDeleteForm, self).__init__(*args, **kwargs)

    # 입력받은 비밀번호가 실제 비밀번호와 일치하는지 검증합니다.
    def clean_password(self):
        password = self.cleaned_data.get('비밀번호')
        user = get_user_model().objects.get(pk=self.request.user.pk)
        if not check_password(password, user.set_password):
            raise forms.ValidationError('비밀번호가 일치하지 않습니다.')
        return password