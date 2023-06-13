from django.db import models
from django.utils.translation import gettext as _


class Account(models.Model):
    image = models.ImageField(
        _("Image"), upload_to='profile_images', null=True, blank=True) 
    bio = models.CharField(_("Bio"), max_length=150) 
    user_name = models.CharField(_("User Name"), max_length=50)
    password = models.CharField(_("Password"), max_length=50)    
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    acctive = models.BooleanField(_("Is Active Account?"), default=False) 


    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Account")


    def __str__(self) -> str:
        return self.user_name   


class Follow(models.Model):
    following_user = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='followers')
    

