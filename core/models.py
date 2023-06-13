from django.db import models
from django.utils.translation import gettext as _


class Like(models.Model):
    like = models.BooleanField(_("Is Like?"), default=False) 
    Post = models.ForeignKey("post.Post",
                                verbose_name=_("Post"),
                                on_delete=models.CASCADE)
