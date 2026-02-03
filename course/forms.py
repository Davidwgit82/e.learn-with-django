from django import forms
from .models import User, Course
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    ROLE = (
        ('student', 'etudiant'),
        ('instructor', 'enseignant'),
    )

    role = forms.ChoiceField(
        choices=ROLE,
        widget=forms.RadioSelect,
        label='Je suis un'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    
    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')

        if role == 'instructor':
            user.is_instructor = True
        elif role == 'student':
            user.is_student = True

        if commit:
            user.save()
        return user
    
class CreateCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('category', 'title', 'description', 'prix', 'places', 'is_active')
        widgets = {
            # On utilise un RadioSelect mais avec des vraies valeurs booléennes
            'is_active': forms.RadioSelect(choices=[(True, 'Disponible'), (False, 'Indisponible')]),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Décrivez votre cours...'}),
        }
