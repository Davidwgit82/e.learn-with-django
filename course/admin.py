from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import Category, Course, Reservation, User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # On ajoute tes champs spécifiques dans l'interface admin
    fieldsets = UserAdmin.fieldsets + (
        ('rôles', 
        {'fields': 
            ('is_instructor', 'is_student')
        }),
    )
    list_display = ('username', 'email', 'is_instructor', 'is_student', 'is_staff')
    list_filter = ('is_instructor', 'is_student', 'is_staff', 'is_superuser')

""" tables principales """

""" inline """
class ReservationInline(admin.TabularInline):
    model = Reservation
    extra = 1

class CourseInline(admin.TabularInline):
    model = Course
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ['name']
    inlines = [CourseInline]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'get_availability', 'prix', 'places')
    list_editable = ('is_active',)
    
    readonly_fields = ('get_availability',)

    fieldsets = (
        ('control administratif', {
            'fields': ('is_active', 'get_availability'),
            'description': 'Suspendez le cours manuellement ici.'
        }),
        ('info général', {
            'fields': ('title', 'teacher', 'category', 'description')
        }),
        ('logitsic & prix', {
            'fields': ('prix', 'places'),
        }),
    )

    def get_availability(self, obj):
        return obj.is_available
    get_availability.boolean = True
    get_availability.short_description = 'statut' 

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('student', 'course',)
    search_fields = ['student']