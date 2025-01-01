from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    # Add a full_name field
    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'})
    )

    class Meta:
        model = User
        fields = ['full_name', 'password1', 'password2']
        help_texts = {
            'password1': None,  # Remove password helper text
            'password2': None,  # Remove password confirmation helper text
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        # Set the username as the full_name (you might want to add logic to make it unique)
        user.username = self.cleaned_data['full_name']
        if commit:
            user.save()
        return user

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if User.objects.filter(username=full_name).exists():
            raise forms.ValidationError("A user with this full name already exists.")
        return full_name