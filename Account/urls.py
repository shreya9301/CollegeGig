from django.urls import path
from Account import views

app_name = "Account"

urlpatterns = [

    # Student Registration URL
    path('student/register/', views.student_registration, name='student-registration'),

    # Faculty Registration URL
    path('faculty/register/', views.faculty_registration, name='faculty-registration'),

    # Edit Student Profile URL
    #path('profile/edit/<int:id>/', views.student_edit_profile, name='edit-profile'),

    # Login URL
    path('login/', views.UserLogin, name='login'),

    # Logout URL
    path('logout/', views.UserLogout, name='logout'),

]