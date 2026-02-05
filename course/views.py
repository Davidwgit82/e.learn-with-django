from .check_auth import (
    is_instructor_check, is_student_check
)
from django.db.models import Count
from django.views import View
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
        context['courses'] = Course.objects.filter(is_active=True)[:4]\
            .select_related('category', 'teacher')\
            .annotate(nb_inscrits=Count('reserve_course'))
        context['reservations'] = Reservation.objects.count()
        return context

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "compte créé.")
            return redirect('login')
        else:
            messages.error(request, "corriger les erreurs.")
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

class CourseListView(ListView):
    model = Course
    template_name = 'course/list_course.html'
    context_object_name = 'courses'
    paginate_by = 3

    def get_queryset(self):
        queryset = Course.objects.filter(is_active=True).select_related(
            'teacher',
            'category'
        )
        queryset = queryset.annotate(nb_inscrits=Count('reserve_course'))
        category_slug = self.request.GET.get('category')
        
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        return context
    
class DetailCourseView(DetailView):
    model = Course
    template_name = 'course/detail_course.html'
    context_object_name = 'course'

    def get_queryset(self):
        return Course.objects.annotate(
            nb_inscrits=Count('reserve_course')
        ).select_related('teacher', 'category')\
            .prefetch_related('reserve_course__student')\

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object
        context['nb_places_restantes'] = max(course.places - course.nb_inscrits, 0)

        return context

'''def is_instructor_check(user):
    return user.is_instructor

@user_passes_test(is_instructor_check)
def get_my_course(request):
    my_course = request.user.course_teacher.all()
    return render(request, 'course/my_course_list.html', {'course' : my_course})'''


""" seul l'instructeur crée et publie ses cours """
class CreateCourseView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CreateCourseForm
    template_name = 'course/create_course.html'
    success_url = reverse_lazy('list_course')
    raise_exception = True

    def test_func(self):
        return self.request.user.is_instructor

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        messages.success(self.request, 'votre cours a été crée et publié.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('list_course')

class MyCourseListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = 'login'
    model = Course
    template_name = 'course/my_course_list.html'
    context_object_name = 'courses'
    raise_exception = False

    def test_func(self):
        return self.request.user.is_instructor
    
    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user).select_related(
            'category'
        ).annotate(nb_inscrits=Count('reserve_course')) \
        .order_by('-created_at')

"""
seul les etudiants participent aux cours 
""" 
class MyReservationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = 'login'
    model = Reservation
    template_name = 'course/my_reservation_list.html'
    context_object_name = 'reservation'
    raise_exception = False

    def test_func(self):
        return self.request.user.is_student
    
    def get_queryset(self):
        return Reservation.objects.filter(student=self.request.user).select_related(
            'course',          
            'course__category' 
        )
    
class ReserveCourseView(LoginRequiredMixin, UserPassesTestMixin, View):
    raise_exception = True 

    def test_func(self):
        return self.request.user.is_student

    def post(self, request, slug):
        course = get_object_or_404(
            Course,
            slug=slug,
            is_active=True
        )
        student = request.user

        if Reservation.objects.filter(
            student=student,
            course=course
        ).exists():
            messages.warning(
                request,
                "Vous avez déjà réservé ce cours."
            )

        elif course.reserve_course.count() >= course.places:
            messages.warning(
                request,
                "Ce cours est complet."
            )

        else:
            Reservation.objects.create(
                student=student,
                course=course
            )
            messages.success(
                request,
                "Réservation effectuée."
            )

        return redirect(course.get_absolute_url())


