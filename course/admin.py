from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count

from .models import User, Category, Course, Reservation

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('rôles', {
            'fields': ('is_instructor', 'is_student')
        }),
    )

    list_display = (
        'username', 'email',
        'is_instructor', 'is_student',
        'is_staff'
    )

    list_filter = (
        'is_instructor', 'is_student',
        'is_staff', 'is_superuser'
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'teacher',
        'category',
        'is_active',
        'nb_inscrits_display',
        'places',
        'availability_display',
        'prix',
        'video_file',
    )

    list_filter = ('is_active', 'category')
    list_editable = ('is_active',)

    readonly_fields = (
        'availability_display',
        'nb_inscrits_display',
    )

    fieldsets = (
        ('controle ad', {
            'fields': ('is_active', 'availability_display'),
        }),
        ('Info general', {
            'fields': ('title', 'teacher', 'category', 'description', 'video_file'),
        }),
        ('Logistique & prix', {
            'fields': ('prix', 'places', 'nb_inscrits_display'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(nb_inscrits=Count('reserve_course'))

    @admin.display(description="Nb inscrits", ordering='nb_inscrits')
    def nb_inscrits_display(self, obj):
        return getattr(obj, 'nb_inscrits', 0)

    @admin.display(boolean=True, description="Disponible")
    def availability_display(self, obj):
        return obj.is_available
    
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'created_at')
    search_fields = (
        'student__username',
        'course__title'
    )
    list_filter = ('course',)


