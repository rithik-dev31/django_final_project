from django.urls import path
from .views import *


urlpatterns = [
    path('', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('admin_page/', admin_page, name='admin_page'),
    path('dashboard/', dashboard, name='dashboard'),
    path('section/go/', section_redirect_view, name='section_redirect'),
    path('section/<str:section_name>/', section_detail_view, name='section_detail'),
    path('add-section/', add_section, name='add_section'),
   
    path('logout/', logout_view, name='logout'),
    # your other paths...
]

