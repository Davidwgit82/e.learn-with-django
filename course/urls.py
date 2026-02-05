from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('auth/register/', views.register_view, name='register'),

    path('courses/', views.CourseListView.as_view(), name='list_course'),
    path('courses/create/', views.CreateCourseView.as_view(), name='create_course'),
    path('courses/me/', views.MyCourseListView.as_view(), name='my_course'),
    path('courses/my-reservations/', views.MyReservationListView.as_view(), name='my_reservation'),

    path('courses/<slug:slug>/', views.DetailCourseView.as_view(), name='detail_course'),
    path('courses/<slug:slug>/reserver/', views.CreateReservationView.as_view(), name='reserve_a_course'),
    path('courses/<slug:slug>/delete/', views.DeleteReservationView.as_view(), name='delete_my_reservation'),
    path('courses/<slug:slug>/edit/', views.UpdateCourseView.as_view(), name='update_my_course'),
]