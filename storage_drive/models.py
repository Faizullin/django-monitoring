from django.db import models
from dashboard.models import CustomUser
from django.urls import reverse

# class Folder(models.Model):
#     name = models.CharField(max_length=128)
#     parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
#     owner = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         full_name = f'{self.name}'
#         if self.parent:
#             full_name = f'{self.parent}::' + full_name
#         return full_name

#     @property
#     def depth(self):
#         if not self.parent:
#             return 0
#         else:
#             return self.parent.depth + 1

#     @property
#     def get_list_url(self):
#         return reverse('storage_drive:index')

#     def parent_url(self):
#         url_list = []
#         temp = self
#         while(temp.parent):
#             temp = temp.parent
#             url_list.append(reverse('storage_drive:index') + '?id=' + str(temp.pk))
#         return 
    

def user_directory_path(instance, filename):
    return f'uploads/user_{instance.owner.pk}/{filename}'

class File(models.Model):
    name = models.CharField(max_length=128)
    file = models.FileField(upload_to=user_directory_path)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    @property
    def get_download_url(self):
        return reverse('storage_drive:download', args=[self.pk])
    
    @property
    def get_location(self):
        return user_directory_path(self,self.name)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
        return super().save(*args, **kwargs)

    @property
    def icon(self):
        location = str(self.get_location)
        if '.' in location.split('/')[-1]:
            self.extension = location.split('/')[-1].split('.')[-1]
        else:
            self.extension = 'folder'
            return 'folder'
        if self.extension == 'txt':
            return 'file-alt'
        elif self.extension == 'pdf':
            return 'file-pdf'
        elif self.extension in ['doc', 'docs', 'docx', 'odt', 'dot', 'dotm', 'dotx']:
            return 'file-word'
        elif self.extension in ['xls', 'xlsx', 'xlt']:
            return 'file-excel'
        elif self.extension in ['ppt', 'pptx', 'ppsx']:
            return 'file-powerpoint'
        elif self.extension in ['png', 'jpg', 'jpeg']:
            return 'file-image'
        elif self.extension in ['mp4', 'mkv', 'flv', 'vob', 'avi', 'wmv']:
            return 'file-video'
        elif self.extension in ['mp3', 'aa', 'aac', 'act', 'mmf', 'mpc']:
            return 'file-audio'
        elif self.extension in ['py', 'js', 'java', 'php', 'rb', 'html', 'css', 'htm']:
            return 'file-code'
        elif self.extension in ['zip', 'rar', 'iso', '7z', 'apk']:
            return 'file-archive'
        elif self.extension == 'csv':
            return 'file-csv'
        else:
            return ''