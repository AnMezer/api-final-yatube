from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey('Group', on_delete=models.SET_NULL, null=True)
    ordered_by = ('-pub_date')

    def __str__(self):
        return self.text

    if TYPE_CHECKING:
        comments: models.Manager['Comment']


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Group(models.Model):
    title = models.CharField('Название сообщества', max_length=20)
    slug = models.SlugField('Слаг', unique=True)
    description = models.TextField('Описание сообщества', blank=True)

    class Meta:
        verbose_name = 'сообщество'
        verbose_name_plural = 'Сообщества'

    def __str__(self):
        return self.title

    def save(self, *args, ** kwargs):
        """Автоматически получает slug из названия сообщества.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        self.full_clean()
        super().save(*args, **kwargs)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='following')

    class Meta:
        models.UniqueConstraint(fields=('user', 'following'),
                                name='unique_follow')
        models.CheckConstraint(condition=~models.Q(user=models.F('following')),
                               name='disable_self_follow')
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
