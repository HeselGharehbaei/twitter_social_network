from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        _('email address'),
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
        upload_to="uploads/photos"
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
    verbose_name = _("Account")
    verbose_name_plural = _("Account")


    def __str__(self):
    return self.email     


class Follow(models.Model):
    following_user = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='followers')
    

