from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('courses/', views.CourseListView.as_view(), name='list-course'),
    path('courses/<slug:slug>/', views.DetailCourse.as_view(), name='detail-course'),
    path('courses/<slug:slug>/reserver/', views.reserver, name='reserve-a-course')
]