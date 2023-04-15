from django.forms import ModelForm, CharField, IntegerField
from .models import File

class FileForm(ModelForm):
    name = CharField(max_length=255, required=False)   

    class Meta:
        model = File
        fields = ['file', 'name']


# class FolderForm(ModelForm):
#     class Meta:
#         model = Folder
#         fields = ['name', 'parent']