from django.db import models
from django.utils.translation import gettext as _
from core.models import TimeStampMixin


class Post(models.Model, TimeStampMixin):
    user = models.ForeignKey(
        "user.Account",
        verbose_name=_("Account"),
        on_delete=models.CASCADE,
        related_name='post'
    )
    text = models.TextField(
        _("Post"),
        help_text=_("Text of the post"),
    ) 
    title = models.CharField(
        _("Title"), 
        max_length=100,
        help_text=_("Title of the post"),
    ) 
    is_archived = models.BooleanField(
        _("Is Post Archive?"), 
        default=False
    )      
    tags = models.ManyToManyField(
        "Tag", 
        verbose_name=_("Tag"), 
        related_name='posts_tags'
    )


    def is_liked_by_user(self, user):
        self.like_set.filter(user= user).exists()


    def get_like(self):
        likes = self.like.all()
        likes_count= self.like.count()
        return likes, likes_count


    def get_comments(self):
        comments = self.comments.all()
        comments_count = self.comments.count() 
        return comments, comments_count  


    @classmethod
    def get_posts_by_tag(cls, tag_name):
        return cls.objects.filter(tags__name=tag_name) 


    @classmethod
    def get_posts_by_user(cls, user):
        return cls.objects.filter(user=user)       


    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Post")


    def __str__(self) -> str:
        return self.title


class Tag(models.Model, TimeStampMixin):
    name = models.CharField(
        _("Name"), 
        max_length=50,
        help_text=_("Name of the tag for the post"),
    )


    def __str__(self) -> str:
        return self.name   


class Image(models.Model, TimeStampMixin):
    name = models.CharField(_("Name"), max_length=50)
    alt = models.CharField(_("Alternative Text"), max_length=100)
    post = models.ForeignKey(Post,
                                related_name=_("image"),
                                on_delete=models.CASCADE)
    image = models.FileField(
        _("Image"), 
        upload_to="uploads/photos", 
        help_text=_("Name of image for the post"),
        blank= True, 
        null= True,
    )    


class Comment(models.Model, TimeStampMixin):
    text = models.TextField(_("Text"))
    parent = models.ForeignKey("self",
                               related_name=_("parent_comment"),
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True
                               )
    user = models.ForeignKey("user.Account",
                        related_name=_("comments"),
                        on_delete=models.CASCADE
                        )   
    post = models.ForeignKey(Post,
                            related_name=_("comments"),
                            on_delete=models.CASCADE)



    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comment")    


class Like(models.Model, TimeStampMixin):
    like = models.BooleanField(_("Is Like?"), default=False) 
    post = models.ForeignKey(Post,
                        related_name=_("like"),
                        on_delete=models.CASCADE)
    user = models.ForeignKey("user.Account",
                        related_name=_("like"),
                        on_delete=models.CASCADE
                        ) 


    def __str__(self):
        return f'{self.user} likes {self.post}'                             