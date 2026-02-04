from django.db import models
from .utils import SlugBaseModel, TimeStamp
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class User(AbstractUser):
    is_instructor = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

class Category(SlugBaseModel, TimeStamp):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Course(SlugBaseModel, TimeStamp):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_teacher')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_course')

    title = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=6, decimal_places=0, default=0)
    places = models.IntegerField()
    is_active = models.BooleanField(default=True, verbose_name='ouvert aux inscriptions')

    @property
    def is_available(self):
        # un cours est dispo si il est ouvert aux inscription et places dispo
        dispo_places = self.reserve_course.count() < self.places
        return self.is_active and dispo_places

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Cours'
    
    def get_absolute_url(self):
        return reverse('detail_course', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.title} (par: {self.teacher.username})'

class Reservation(TimeStamp):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reserve_course')

    """ empêcher l'etudiant de reserver un même cours deux fois. """
    class Meta:
        unique_together = ['student', 'course']

    def __str__(self):
        return f'student {self.student.username} has reserved this course -> {self.course.title}'
    
