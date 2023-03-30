from django import forms
from dashboard.models import CustomUser

class UserForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = [ 'username', 'email','age','address']