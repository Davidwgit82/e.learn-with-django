from django.urls import path
from . import views

urlpatterns = [
    # 1. Accueil
    path('', views.IndexView.as_view(), name='index'),

    # 2. Authentification (Généralement groupé)
    path('auth/register/', views.register_view, name='register'),

    # 3. Actions spécifiques et Listes (Toujours AVANT les slugs)
    path('courses/', views.CourseListView.as_view(), name='list_course'),
    path('courses/create/', views.CreateCourseView.as_view(), name='create_course'),
    path('courses/me/', views.MyCourseListView.as_view(), name='my_course'),
    path('courses/my-reservations/', views.MyReservationListView.as_view(), name='my_reservation'),

    # 4. Détails et Actions sur un objet précis (Via Slug)
    # On met le détail en dernier ou juste avant les actions spécifiques au slug
    path('courses/<slug:slug>/', views.DetailCourseView.as_view(), name='detail_course'),
    path('courses/<slug:slug>/reserver/', views.CreateReservationView.as_view(), name='reserve_a_course'),
    path('courses/<slug:slug>/delete/', views.DeleteReservationView.as_view(), name='delete_my_reservation'),
]