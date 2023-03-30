import factory
from django.contrib.auth.models import Group
from django.utils import timezone
from .models import CustomUser, SystemData
from django.core.files.uploadedfile import SimpleUploadedFile
import random

class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: f"group{n}")
    
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_staff = False
    is_active = True
    date_joined = factory.LazyFunction(timezone.now)
    password = factory.PostGenerationMethodCall('set_password',
                                                'defaultpassword')
    address = factory.Sequence(lambda n: f"user-address-{n}")
    age = 19

class SuperuserFactory(UserFactory):
    is_staff = True
    is_superuser = True
