from django.urls import path
from Job import views

app_name = "Job"


urlpatterns = [

    # Student Home Page 
    path('', views.home_view, name='home'),

    # Faculty Home Page 
    path('faculty/', views.faculty_home_view, name='faculty-home'),

    # List of All Jobs 
    path('jobs/', views.all_jobs, name='job-list'),

    # Create Job 
    path('job/create/', views.create_job, name='create-job'),

    # Single Job with job id = id 
    path('job/<int:id>/', views.single_job, name='single-job'),

    # Apply to Job with job id = id 
    path('apply-job/<int:id>/', views.apply_job, name='apply-job'),

    # Search Query result 
    path('result/', views.search_result, name='search_result'),

    # User Dashboard 
    path('dashboard/', views.dashboard, name='dashboard'),

    # Bookmark Job with job id = id URL
    path('bookmark-job/<int:id>/', views.bookmark_job_view, name='bookmark-job'),

    # See All Applications 
    path('dashboard/faculty/job/<int:id>/applicants/', views.all_applicants, name='applicants'),

    # Edit Job 
    path('dashboard/faculty/job/edit/<int:id>', views.job_edit, name='edit-job'),

    # View Applicant 
    path('dashboard/faculty/applicant/<int:id>/', views.applicant_details, name='applicant-details'),

    # Close Job
    path('dashboard/faculty/close/<int:id>/', views.job_complete, name='complete'),

    # Delete Job 
    path('dashboard/faculty/delete/<int:id>/', views.delete_job, name='del-job'),

]