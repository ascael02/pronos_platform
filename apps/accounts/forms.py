# ─── apps/accounts/forms.py ───────────────────────────────────────────────────
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User


class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfilForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'bio', 'avatar', 'pays', 'telephone']


class ChangerMotDePasseForm(PasswordChangeForm):
    pass
