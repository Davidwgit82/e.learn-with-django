from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Course

class RegistrationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Étudiant'),
        ('instructor', 'Enseignant'),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
        label='Je suis'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if role not in dict(self.ROLE_CHOICES):
            raise forms.ValidationError("rôle invalide.")
        return role

    def save(self, commit=True):
        user = super().save(commit=False)

        user.is_student = False
        user.is_instructor = False

        role = self.cleaned_data['role']
        if role == 'student':
            user.is_student = True
        elif role == 'instructor':
            user.is_instructor = True

        if commit:
            user.save()
        return user

class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('category', 'title', 'description', 'prix', 'places', 'is_active')
        widgets = {
            'is_active': forms.RadioSelect(
                choices=[(True, 'Disponible'), (False, 'Indisponible')]
            ),
            'description': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Décrivez votre cours...'}
            ),
        }

    def clean_prix(self):
        prix = self.cleaned_data.get('prix')
        if prix is not None and prix < 0:
            raise forms.ValidationError("Le prix ne peut pas être négatif.")
        return prix

    def clean_places(self):
        places = self.cleaned_data.get('places')
        if places is not None and places < 1:
            raise forms.ValidationError("Le nombre de places doit être supérieur à 0.")
        return places

    def clean_is_active(self):
        value = self.cleaned_data.get('is_active')
        if not isinstance(value, bool):
            raise forms.ValidationError("Valeur invalide.")
        return value

