from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
from .models import User, Teacher, Student

# Register your models here.



""" For Inline Teacher in user table"""
class TeacherInline(admin.TabularInline):
    model = Teacher

""" For Inline Student in user table"""
class StudentInline(admin.TabularInline):
    model = Student

class CustomUserAdmin(UserAdmin):
    model = User
    # inlines = [TeacherInline]
    inlines = [StudentInline, TeacherInline]
    list_display = ('email','first_name', 'is_staff', 'is_active', 'is_superuser','is_student','is_teacher',)
    list_filter = ('email', 'is_staff', 'is_active',)
    readonly_field = ('date_joined','last_login',)
    fieldsets = (
        (None, {'fields': ('email', 'first_name','last_name', 'password')}),
        # ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser','is_teacher')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser','is_student','is_teacher')}),
        ('Groups', {'fields': ('groups',)}),
        ('User Permissions', {'fields': ('user_permissions',)}),
        ('Last Login', {'fields': ('last_login',)}),
        ('Date Joined', {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # 'fields': ('email', 'first_name','last_name', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser','is_teacher','groups','user_permissions')}
            'fields': ('email', 'first_name','last_name', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser','is_student','is_teacher','groups','user_permissions')}
        ),
    )
    search_fields = ('email','first_name',)
    ordering = ('email',)


class TeacherAdmin(ModelAdmin):
    model = Teacher
    list_display = ('email','first_name','teacher_id', 'phone_no', 'department','active')
    list_filter = ('teacher_id', 'department',)
    search_fields = ('email','first_name','department','teacher_id',)
    ordering = ('department',)


class StudentAdmin(ModelAdmin):
    model = Student
    list_display = ('email','first_name','rollno', 'phone_no', 'course','active')
    list_filter = ('rollno', 'course',)
    search_fields = ('email','first_name','course','rollno',)
    ordering = ('rollno',)


admin.site.register(User, CustomUserAdmin)

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)

