from .check_auth import (
    is_instructor_check, is_student_check
)
from django.shortcuts import (
   get_object_or_404, redirect, render
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin
)
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views.generic import (
    TemplateView, ListView, DetailView, CreateView
)
from .forms import RegistrationForm, CreateCourseForm
from .models import (
    Category, Course, Reservation, User
)
from django.contrib.auth.decorators import login_required, user_passes_test

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all()
        context['courses'] = Course.objects.all()[:4]
        context['reservations'] = Reservation.objects.count()
        return context

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(
        request, 'registration/register.html', {'form': form}
    )

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

'''def is_instructor_check(user):
    return user.is_instructor

@user_passes_test(is_instructor_check)
def get_my_course(request):
    my_course = request.user.course_teacher.all()
    return render(request, 'course/my_course_list.html', {'course' : my_course})'''


@user_passes_test(is_instructor_check)
def create_course(request):
    if request.method == 'POST':
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            return redirect('list_course')
    else:
        form = CreateCourseForm()
    return render(
        request, 'course/create_course.html', {'form': form}
    )

class CreateCourseView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CreateCourseForm
    template_name = 'course/create_course.html'

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_instructor
    
    def form_valid(self, form):
        form.instance.teacher = self.request.user
        messages.success(self.request, 'cours publié.')
        
        super().form_valid(form)
        return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', reverse('list_course'))

class MyCourseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = 'login' # reidrection si non connecté
    model = Course
    template_name = 'course/my_course_list.html'
    context_object_name = 'courses'
    raise_exception = False

    def test_func(self):
        return self.request.user.is_instructor
    
    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user)
    
class MyReservationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = 'login'
    model = Reservation
    template_name = 'course/my_reservation.html'
    context_object_name = 'reservation'
    raise_exception = False

    def test_func(self):
        return self.request.user.is_student
    
    def get_queryset(self):
        return Reservation.objects.filter(student=self.request.user)

""" reserver un cours """
@user_passes_test(is_student_check)
def reserver(request, slug):
    course = get_object_or_404(Course, slug=slug)
    student = request.user

    if Reservation.objects.filter(student=student, course=course).exists():
        messages.warning(request, 'vous avez deja reservé ce cours')

    elif not course.is_available:
        messages.warning(request, "ce cours est complet")

    else:
        Reservation.objects.create(student=student, course=course)
        messages.success(request, 'vous avez reservé ce cours.')

    return redirect(course.get_absolute_url())
