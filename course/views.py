from django.shortcuts import (
    render, get_object_or_404, redirect
)
from django.contrib import messages
from django.views.generic import (
    TemplateView, ListView, DetailView
)
from .models import (
    Category, Course, Reservation
)
from django.contrib.auth.decorators import login_required

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all()
        context['courses'] = Course.objects.all()[:3]
        context['reservations'] = Reservation.objects.count()

        return context


class CourseListView(ListView):
    model = Course
    template_name = 'course/list_course.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class DetailCourse(DetailView):
    model = Course
    template_name = 'course/detail_course.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # recupere l'instance : course
        course = self.get_object()
        context['nb_places_restantes'] = course.places - course.reserve_course.count()

        return context

""" reserver un cours """
@login_required
def reserver(request, slug):
    course = get_object_or_404(Course, slug=slug)
    student = request.user

    if Reservation.objects.filter(student=student, course=course):
        messages.warning(request, 'vous avez deja reservé ce cours')

    # optionnel : car dans la views detail_course.html 
    # le bouton est 'disabled' quand il n ya plus de places
    elif not course.is_available:
        messages.warning(request, "ce cours est complet")

    else:
        Reservation.objects.create(student=student, course=course)

    return redirect(course.get_absolute_url())
