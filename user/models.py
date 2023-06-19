from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class Account(AbstractBaseUser):
    phone_number= models.CharField(
        _('Phone Number'),
        max_length=11, unique=True, 
        validators=[
            RegexValidator(regex="\A(09)(0|1|2|3)[0-9]{7}\d\Z", message="phone number is not correct")
        ])
    username = models.CharField(
        _('User Name'),
        max_length=50, unique=True)
    email = models.EmailField(
        _('email address'),
        max_length= 254,
        unique=True
    )
    bio = models.CharField(
        _("Biography"), 
        max_length=150, 
        help_text=_("Biography is a written account of a person's life"), 
        blank= True, 
        null= True,
    )
    image = models.FileField(
        _("Image"), 
        upload_to="uploads/photos", blank= True, null= True
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    first_name = models.CharField(
        _('First Name'),
        max_length=50, 
        blank=True, 
        null=True)
    last_name = models.CharField(
        _('Last Name'),
        max_length=50, 
        blank=True, 
        null=True)
    is_active = models.BooleanField(default=True)
    image = models.FileField(
        _("Image"), 
        upload_to="uploads/photos",
        blank= True, 
        null= True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'email']
    

    def __str__(self):
        return self.username