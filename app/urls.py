from django.urls import path
from django.conf.urls.static import static 

from .views import *
# from django.contrib.auth.decorators import login_required
# from login.views import signin_view  # adjust based on your file


urlpatterns = [
    path('', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('admin_page/', admin_page, name='admin_page'),
    path('dashboard/', dashboard, name='dashboard'),
    path('section/go/', section_redirect_view, name='section_redirect'),
    path('section/<str:section_name>/', section_detail_view, name='section_detail'),
    path('add-section/', add_section, name='add_section'),
   
    path('logout/', logout_view, name='logout'),
    path('profile/',profile_view, name='profile'),

    # editign the post
    path('delete-post/<int:post_id>/', delete_post, name='delete_post'),
    path('edit-post/<int:post_id>/', edit_post, name='edit_post'),

    path('edit-section/<int:section_id>/', edit_section, name='edit_section'),
    path('delete-section/<int:section_id>/', delete_section, name='delete_section'),

    path('dashboard/', dashboard, name='dashboard'),
    path('community/join/<int:section_id>/', join_community, name='join_community'),
    path('community/leave/<int:section_id>/', leave_community, name='leave_community'),
    path('community/chat/<int:section_id>/',community_chat, name='community_chat'),
    path('filter-jobs/', filter_jobs, name='filter_jobs'),
    path('repo-filter/',repo_filter, name='repo_filter'),


    # delete and edit the repo and job openings
    path('edit-job/<int:job_id>/', edit_jobopening, name='edit_job'),
    path('delete-job/<int:job_id>/',delete_jobopening, name='delete_job'),

    path('edit-repo/<int:repo_id>/', edit_repo, name='edit_repo'),
    path('delete-repo/<int:repo_id>/', delete_repo, name='delete_repo'),



    # your other paths...   

    # feedback
    path('submit-feedback/', submit_feedback, name='submit_feedback'),
    path('delete-feedback/<int:feedback_id>/', delete_feedback, name='delete_feedback'),

]

