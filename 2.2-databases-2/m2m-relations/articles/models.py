from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['name']  # сортировка по алфавиту

    def __str__(self):
        return self.name


class Scope(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='scopes')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes')
    is_main = models.BooleanField(default=False, verbose_name='Основной')

    class Meta:
        verbose_name = 'Связь статьи и раздела'
        verbose_name_plural = 'Связи статей и разделов'
        # Чтобы не было дубликатов: одна статья + один тег = уникальная связь
        unique_together = ('article', 'tag')

    def __str__(self):
        return f'{self.article.title} - {self.tag.name} ({"основной" if self.is_main else "дополнительный"})'


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение')

    # Связь с тегами через промежуточную модель Scope
    tags = models.ManyToManyField(Tag, through=Scope, related_name='articles')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']  # сортировка по дате (свежие сверху)

    def __str__(self):
        return self.title