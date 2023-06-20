from django.db import models
from django.utils.translation import gettext as _
from core.models import BaseModel, TimeStampMixin


class Post(BaseModel, TimeStampMixin):
    user = models.ForeignKey("user.Account",
                                verbose_name=_("Account"),
                                on_delete=models.CASCADE
                                )
    text = models.TextField(_("Post")) 
    title = models.CharField(_("Title"), max_length=100) 
    is_archived = models.BooleanField(_("Is Post Archive?"), default=False)      
    tags = models.ManyToManyField("Tag", verbose_name=_("Tag"), related_name='posts_tags')


    def is_liked_by_user(self, user):
        self.like_set.filter(user= user).exists()


    def get_like_count(self):
        return self.likes.count()


    def get_comment_count(self):
        return self.comments.count()


    def get_comments_and_users(self):
        comment_users = {}
        comments = self.comments.all()
        for comment in comments:
            user = comment.user
            if user.username not in comment_users:
                comment_users[user.username] = [comment.text]
            else:
                comment_users[user.username].append(comment.text)
        return comment_users, comments.count()    


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


class Tag(BaseModel, TimeStampMixin):
    name = models.CharField(_("Name"), max_length=50)


    def __str__(self) -> str:
        return self.name   


class Image(BaseModel, TimeStampMixin):
    name = models.CharField(_("Name"), max_length=50)
    alt = models.CharField(_("Alternative Text"), max_length=100)
    Post = models.ForeignKey("Post",
                                verbose_name=_("Post"),
                                on_delete=models.CASCADE)
    image = models.FileField(
        _("Image"), 
        upload_to="uploads/photos", blank= True, null= True
    )    


class Comment(BaseModel, TimeStampMixin):
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
    post = models.ForeignKey(Post,
                            verbose_name=_("Post"),
                            on_delete=models.CASCADE)



    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comment")    


class Like(BaseModel, TimeStampMixin):
    like = models.BooleanField(_("Is Like?"), default=False) 
    post = models.ForeignKey("Post",
                                verbose_name=_("Post"),
                                on_delete=models.CASCADE)
    user = models.ForeignKey("user.Account",
                        verbose_name=_("Account"),
                        on_delete=models.CASCADE
                        ) 


    def __str__(self):
        return f'{self.user} likes {self.post}'                             