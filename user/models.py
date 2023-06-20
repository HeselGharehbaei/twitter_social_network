from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel, TimeStampMixin


class Account(AbstractBaseUser, BaseModel, TimeStampMixin):
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
    is_verify = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    image = models.FileField(
        _("Image"), 
        upload_to="uploads/photos",
        blank= True, 
        null= True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'email']


    def __str__(self):
        return self.username


    def delete(self):
        self.deleted = True
        self.save()


    def undelete(self):
        self.deleted = False
        self.save()


    def has_perm(self, perm, obj=None):
        return self.is_admin


    def has_module_perms(self, app_label):
        return True


    def get_followers_and_following_count(self):
        following_count = self.following.count()
        followers_count = self.followers.count()
        following = [(follow.to_user.username, follow.to_user.image.url) for follow in self.following.all()]
        followers = [(follow.from_user.username, follow.from_user.image.url) for follow in self.followers.all()]
        return following_count, following, followers_count, followers 


class Follow(BaseModel, TimeStampMixin):
    from_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='followers')  


    def __str__(self):
        return f'{self.from_user} following {self.to_user}'     