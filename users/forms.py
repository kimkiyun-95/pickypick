from django import forms
from . import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.forms import PasswordResetForm
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class LoginForm(forms.Form):
    username = forms.CharField(label="아이디", max_length=100,
        widget=forms.TextInput(attrs={'placeholder': '아이디를 입력해주세요', 'style': 'height:50px'}))
    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 입력해주세요'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = models.User.objects.get(username=username)
            if user.check_password(password):
                return self.cleaned_data
            else:
                raise ValidationError("비밀번호가 틀렸습니다")
        except models.User.DoesNotExist:
            raise ValidationError("존재하지 않는 아이디입니다")


GENDER_CHOICES = {
    ("male", "남성"),
    ("female", "여성"),
}


class SignUpForm(forms.Form):
    username = forms.CharField(label="아이디", max_length=100, label_suffix='', widget=forms.TextInput(attrs={'placeholder': '6자 이상의 영문 혹은 영문과 숫자를 조합'}))
    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 입력하세요'}), label_suffix='')
    password_re = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput(attrs={'placeholder': '비밀번호를 한번 더 입력하세요'}), label_suffix='')

    last_name = forms.CharField(label="성", max_length=25, label_suffix='')
    first_name = forms.CharField(label="이름", max_length=50, label_suffix='')

    nickname = forms.CharField(label="닉네임", max_length=100, label_suffix='', widget=forms.TextInput(attrs={'placeholder': '부적절한 닉네임은 제재를 받을 수 있습니다'}))
    email = forms.EmailField(label="이메일", label_suffix='')

    gender = forms.ChoiceField(label="성별", choices=GENDER_CHOICES, widget=forms.RadioSelect, label_suffix='')
    birth = forms.DateField(label="생년월일", widget=forms.SelectDateWidget, label_suffix='')

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            user = models.User.objects.get(username=username)
            raise ValidationError("중복된 아이디 입니다. 사용하실 수 없습니다")
        except ObjectDoesNotExist:
            return username

    def clean_password_re(self):
        password = self.cleaned_data.get("password")
        password_re = self.cleaned_data.get("password_re")
        if password == password_re:
            return password_re
        else:
            raise ValidationError("비밀번호가 일치하지 않습니다")

    def save(self):
        username = self.cleaned_data.get("username")
        password_re = self.cleaned_data.get("password_re")
        last_name = self.cleaned_data.get("last_name")
        first_name = self.cleaned_data.get("first_name")
        nickname = self.cleaned_data.get("nickname")
        email = self.cleaned_data.get("email")
        gender = self.cleaned_data.get("gender")
        birth = self.cleaned_data.get("birth")

        user = models.User.objects.create_user(username, email=email, password=password_re)

        user.first_name=first_name
        user.last_name=last_name
        user.nickname=nickname
        user.gender=gender
        user.birth=birth

        user.save()


class FindMyIdForm(forms.Form):
    name = forms.CharField(label='이름', widget=forms.TextInput(attrs={'placeholder': '이름을 입력해주세요'}))
    email = forms.EmailField(label="이메일", widget=forms.TextInput(attrs={'placeholder': '이메일을 입력해주세요'}))
    

class MyPasswordResetForm(PasswordResetForm):
    username = forms.CharField(
        label="아이디",
        widget=forms.TextInput(attrs={'placeholder': '아이디를 입력해주세요'})
    )

    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'placeholder': '이메일을 입력해주세요'})
    )

# farm 입점 관련
class FarmEnrollForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = models.Farmer
        fields = ('farm_name', 'farmer_profile', 'farm_profile', 'profile_title', 'profile_desc', 'sub_count', 'farm_news', 'farm_cat',)
        widgets = {
            'farm_cat': forms.RadioSelect,
            'profile_title': forms.TextInput(attrs={'placeholder': '농장을 한 문장으로 소개해주세요'})
        }
        labels = {
            'farm_name': '농장 이름',
            'farmer_profile': '프로필 사진',
            'farm_profile': '농장 사진',
            'profile_title': '농장 한 줄 소개',
            'profile_desc': '농장 상세 소개',
            'farm_cat': '해시 태그 선택', 
        }

class FarmApplyForm(forms.ModelForm):
     class Meta:
        model = models.Farm_Apply
        fields = ('name', 'phone_num', 'farm_name', 'farm_cat', 'detail_cat', 'desc',)
        widgets = {
            'farm_cat': forms.RadioSelect,
            'detail_cat': forms.TextInput(attrs={'placeholder': '세부품목을 작성해주세요'}),
        }
        labels = {
            'name': '이름',
            'phone_num': '휴대폰 번호',
            'farm_name': '농장 이름',
            'farm_cat': '품종',
            'detail_cat':'',
            'desc': '추가 전달 사항',
        }

class FarmerStoryForm(forms.ModelForm):
    class Meta:
        model = models.Farmer_Story
        fields = ('title', 'content',)
        widgets = {
            'content': SummernoteWidget(),
        }