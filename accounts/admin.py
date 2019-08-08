from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _

from .models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password (again):"), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('fullname', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Your passwords didn't match."))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
    site_title = _("CT Bog")

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('fullname','email', 'password', 'is_active', 'admin')

    def clean_password(self):
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'fullname', 'admin')
    list_filter = ('admin', 'staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('fullname','email','password')}),
        # ('Personal info', {'fields': ('fullname',)}),
        ('Permissions', {'fields': ('admin', 'staff', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'fullname',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.site_header = _("Account Admin")
admin.site.site_title = _("CT Admin")
admin.site.index_title = ""

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)