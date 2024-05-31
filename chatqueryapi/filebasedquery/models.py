from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from uuid import uuid4

from .file_uploader import upload_bytesfile

def get_uuid6():
    return uuid4().hex

class ApiUser(AbstractUser):
    pass

class UserFiles(models.Model):

    user = models.ForeignKey(ApiUser, on_delete=models.CASCADE, null = True, related_name="user_files")
    file = models.FileField(blank=True, null=True)
    openai_fileid = models.CharField(blank=True, null=True, max_length=100)
    file_name = models.UUIDField(primary_key=True, default=get_uuid6)


@receiver(pre_save, sender = UserFiles)
def upload_to_openai(instance, *args, **kwargs):
    if instance.file:
        try:
            print(type(instance.file.file.file))
            print(instance.file.file.__dict__)
            print(instance.file.__dict__ ,instance.file.name )
            f_type = instance.file.name
            file_object = upload_bytesfile(instance.file.file.file, f_type)
            print(file_object)
            instance.openai_fileid = file_object.id
            instance.file.file.file.seek(0)
        except Exception as e:
            raise Exception(f"File upload failed {e.args}")
    else:
        raise Exception("File is required") 
    
