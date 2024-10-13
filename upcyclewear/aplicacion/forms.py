from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UsuarioRegisterForm(UserCreationForm):
    direccion = forms.CharField(max_length=255, required=False)
    telefono = forms.CharField(max_length=20, required=False)
    foto_perfil = forms.ImageField(required=False)
    descripcion = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefono', 'direccion', 'foto_perfil', 'password1', 'password2', 'descripcion']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
            'foto_perfil': forms.FileInput(),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def save(self, commit=True):
        user = super().save(commit)
        
        # Cambiar el nombre del archivo de la foto de perfil
        if self.cleaned_data.get('foto_perfil'):
            foto = self.cleaned_data['foto_perfil']
            # Cambia el nombre del archivo
            foto.name = f"{user.username}.jpg"  # O el formato que prefieras
            user.foto_perfil = foto
        
        if commit:
            user.save()
        
        return user
