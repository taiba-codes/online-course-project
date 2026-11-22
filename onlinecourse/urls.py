from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    path('', views.popular_course_list, name='index'),
    path('<int:course_id>/', views.course_details, name='course_details'),
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),
    path('<int:course_id>/submit/', views.submit, name='submit'),
    path('course/<int:course_id>/exam_result/', views.show_exam_result, name='exam_result'),
]