from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login, get_user_model

User = get_user_model()
class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": _("Password")
    }))
    password2 = forms.CharField(label=_('Pasword (again)'), widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": _("Password (again)")
    }))

    class Meta:
        model = User
        widgets = {
            'fullname' : forms.TextInput(attrs={"placeholder": _("Full Name")}),
            'email' : forms.TextInput(attrs={"placeholder": _("Email")}),
        }
        fields = ('fullname','email',)

    def clean_fullname(self):
        fullname = self.cleaned_data.get("fullname")
        qs = User.objects.filter(fullname=fullname)
        if qs.exists():
            raise forms.ValidationError(_("That User is already taken."))
        return fullname
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError(_("That Email is already taken."))
        return email

    def clean_password2(self):
        # Kiểm tra xem hai mục nhập mật khẩu có trùng khớp không
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Your passwords didn't match."))
        return password2

    def save(self, commit=True):
        # Lưu mật khẩu được cung cấp ở định dạng băm
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={
        "class": "form-control", "placeholder": _("Email")
    }))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": _("Password")
    }))

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if not qs.exists():
            raise forms.ValidationError(_("Email address does not exist."))
        return email

    def clean(self):
        request = self.request
        #data = self.cleaned_data
        #email = data.get("email")
        #password = data.get("password")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
        else:
            raise forms.ValidationError(_("Email or Password don't exist."))   
        #self.user = user