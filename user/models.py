from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampMixin
from django.utils import timezone


class Account(AbstractUser):
    phone_number= models.CharField(
        _('Phone Number'),
        max_length=11,
        help_text=_("Phone Number of user"),  
        unique=False, 
        validators=[
            RegexValidator(regex="\A(09)(0|1|2|3)[0-9]{7}\d\Z", message="phone number is not correct")
        ])
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


    date_joined = models.DateTimeField(_('date joined'), default=timezone.now,
        blank= False, null=False                               
    )


    def get_followers_and_following(self):
        following_count = self.following.count()
        followers_count = self.followers.count()
        following = [(follow.to_user.username) for follow in self.following.all()]
        followers = [(follow.from_user.username) for follow in self.followers.all()]
        return following_count, following, followers_count, followers  


    class Meta:
        verbose_name, verbose_name_plural = _("User"), _("Users")    


class Follow(models.Model, TimeStampMixin):
    from_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='followers')  


    def __str__(self):
        return f'{self.from_user} following {self.to_user}'     