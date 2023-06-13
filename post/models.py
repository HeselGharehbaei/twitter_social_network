from django.db import models
from django.utils.translation import gettext as _


class Post(models.Model):
    user = models.ForeignKey("user.Account",
                                verbose_name=_("Account"),
                                on_delete=models.CASCADE
                                )
    text = models.TextField(_("Post")) 
    title = models.CharField(_("Title"), max_length=100) 
    acctive = models.BooleanField(_("Is Post Archive?"), default=False)      
    create_at = models.DateTimeField(
        _("create at"), auto_now=False, auto_now_add=True)
    tag = models.ManyToManyField(_("Tag"),
                                    verbose_name=_("Tags"),
                                    )  


    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Post")


    def __str__(self) -> str:
        return self.title


class Tag(models.Model):
    name = models.CharField(_("Name"), max_length=50)


class Image(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    alt = models.CharField(_("Alternative Text"), max_length=100)
    Post = models.ForeignKey("Post",
                                verbose_name=_("Post"),
                                on_delete=models.CASCADE)
    image = models.ImageField(_("Image"), upload_to='Post',)


class Comment(models.Model):
    title = models.CharField(_("Title"), max_length=150)
    text = models.TextField(_("Text"))
    parent = models.ForeignKey("self",
                               verbose_name=_("Parent Comment"),
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True
                               )
    user = models.ForeignKey("user.Account",
                        verbose_name=_("Account"),
                        on_delete=models.CASCADE
                        )   
    Post = models.ForeignKey("Post",
                            verbose_name=_("Post"),
                            on_delete=models.CASCADE)


    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comment")


    def __str__(self) -> str:
        return self.title
