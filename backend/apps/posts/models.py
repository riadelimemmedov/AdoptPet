from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField, SlugField
from django_extensions.db.models import TimeStampedModel

# Create your models here.


# !Category
class Category(TimeStampedModel):
    name = models.CharField(_("Category name"), max_length=100, null=True, unique=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, null=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# !Post
class Post(TimeStampedModel):
    title = models.CharField(_("Post title"), max_length=250)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Author post"),
        related_name="posts_author",
        null=True,
        on_delete=models.SET_NULL,
    )
    slug = models.SlugField(max_length=100, unique=True, db_index=True, null=True)
    post_photo_url = models.FileField(
        _("Post photo"),
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpg", "jpeg"])],
    )
    categories = models.ManyToManyField(
        Category,
        verbose_name=_("Categories"),
        related_name="posts_categories",
        blank=True,
    )
    body = models.TextField(_("Post body"))
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Likes"),
        related_name="post_likes",
        blank=True,
    )

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.author.username}"


# !Comment
class Comment(TimeStampedModel):
    post = models.ForeignKey(
        Post,
        verbose_name=_("Post"),
        related_name="comment_post",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("Author comment"),
        related_name="comment_author",
        null=True,
        on_delete=models.SET_NULL,
    )
    body = models.TextField(_("Comment body"))

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"{self.body[:20]} by {self.author.username}"
