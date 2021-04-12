from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.handleLogin, name='login'),
    path('dashboard/', views.dash, name="dashboard"),
    path('logout/', views.Logout, name='logout'),
    path('adminList/', views.adminList, name='adminList'),
    path('teacherList/', views.teacherList, name='teacherList'),
    path('studentList/', views.studentList, name='studentList'),
    path('deleteUser/<int:pk>', views.deleteUser, name='deleteUser'),
    path('addAdmin/', views.addAdmin, name='addAdmin'),
    path('addTeacher/', views.addTeacher, name='addTeacher'),
    path('addStudent/', views.addStudent, name='addStudent'),
    path('editAdmin/<int:pk>', views.editAdmin, name='editAdmin'),
    path('editTeacher/<int:pk>', views.editTeacher, name='editTeacher'),
    path('editStudent/<int:pk>', views.editStudent, name='editStudent'),
    path('changePassword/<int:pk>', views.changePassword, name='changePassword'),
    path('profile/<int:pk>', views.profile, name='profile'),
    

    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password-reset/password_reset_form.html',
             subject_template_name='password-reset/password_reset_subject.txt',
             email_template_name='password-reset/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),
        
#     path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

#     path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password-reset/password_reset_done.html'),
#      name='password_reset_done'),

#     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
#     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password-reset/password_reset_complete.html'),
#      name='password_reset_complete'),
]