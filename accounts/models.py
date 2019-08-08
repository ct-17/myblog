from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self, email, fullname=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError(_("User must have an Email address."))
        if not password:
            raise ValueError(_("User must have an Password"))
        user_obj = self.model(
            email = self.normalize_email(email),
            fullname=fullname
        )
        user_obj.set_password(password) # thay đổi mật khẩu người dùng
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email,fullname=None, password=None):
        user = self.create_user(
                email,
                fullname=fullname,
                password=password,
                is_staff=True
        )
        return user

    def create_superuser(self, email, fullname=None, password=None):
        user = self.create_user(
                email,
                fullname=fullname,
                password=password,
                is_staff=True,
                is_admin=True
        )
        return user


class User(AbstractBaseUser):
    email           = models.EmailField( max_length=255, unique=True, verbose_name=_("Email"))
    fullname        = models.CharField(max_length=255, verbose_name=_('Fullname'))
    is_active       = models.BooleanField(default=True) # có thể đăng nhập
    staff           = models.BooleanField(default=False) # là người quản trị nhưng ko phải superuser
    admin           = models.BooleanField(default=False) # superuser
    timestamp       = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email' # đăng nhập bằng email
    REQUIRED_FIELDS = ['fullname'] # .\manage.py createsuperuser

    objects = UserManager()
    
    def __str__(self):
        return self.email

    def get_fullname(self):
        if self.fullname:
            return self.fullname
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('User')