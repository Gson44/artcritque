from django import forms 
from .models import ArtUser, ArtEntry
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User  # Import the User model
class Sign_Up_Form(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1"]

    def __init__(self, *args, **kwargs):
        super(Sign_Up_Form, self).__init__(*args, **kwargs)
        
        # Remove help_text for all fields
        for field in self.fields.values():
            field.help_text = None

class Art_Entry_Form(forms.ModelForm):
    class Meta:
        model = ArtEntry 
        fields = ['art_name', 'image', 'likes']
  