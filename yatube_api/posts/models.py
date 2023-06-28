from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField('Ссылка', unique=True)
    description = models.TextField('Описание')

    def __str__(self):
        return self.title


class Post(models.Model):
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    text = models.TextField('Текст поста')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts', blank=True, null=True,
        verbose_name='Группа'
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments',
    )
    post = models.ForeignKey(
        Post,
        verbose_name='Пост',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField('Текст комментария')
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
