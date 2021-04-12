from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(_("Email Address"), unique=True)
    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="Related User", on_delete=models.CASCADE)
    teacher_id = models.IntegerField(primary_key=True, unique=True)
    phone_no = models.CharField(max_length=10, null=False, blank=False)
    department = models.CharField(max_length=30,null=False, blank=False)

    def __str__(self):
        return self.user.email

    # Custom Properties
    @property
    def email(self):
        return self.user.email
        
    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def password(self):
        return self.user.password

    @property
    def active(self):
        return self.user.is_active

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="Related User", on_delete=models.CASCADE)
    # user = models.OneToOneField(User, verbose_name="Related User", on_delete=models.CASCADE,  parent_link=True)
    rollno = models.IntegerField(primary_key=True, unique=True)
    phone_no = models.CharField(max_length=10, null=False, blank=False)
    course = models.CharField(max_length=30)
    department = models.CharField(max_length=30,null=False, blank=False,default="")
    # is_student = models.BooleanField('student status', default=True)

    def __str__(self):
        return self.user.email
    
    # Custom Properties
    @property
    def email(self):
        return self.user.email
        
    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def password(self):
        return self.user.password

    @property
    def active(self):
        return self.user.is_active