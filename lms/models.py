from django.db import models


class Courses(models.Model):
    """Класс для создания модели Курса"""
    title = models.CharField(max_length=150, verbose_name='название курса')
    preview = models.ImageField(upload_to='image/', verbose_name='изображение', blank=True, null=True)
    description = models.TextField(verbose_name='описание курса', blank=True, null=True)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name='создатель курса', blank=True, null=True)

    def __str__(self):
        return f'{self.title} {self.preview} {self.description}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lessons(models.Model):
    """Класс для создания модели урока"""
    title = models.CharField(max_length=150, verbose_name='название урока')
    description = models.TextField(verbose_name='описание урока', blank=True, null=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, blank=True, null=True, verbose_name='курс')
    preview = models.ImageField(upload_to='image/', verbose_name='изображение', blank=True, null=True)
    link = models.URLField(null=True, blank=True)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name='создатель урока', blank=True,
                              null=True)

    def __str__(self):
        return f'{self.title} {self.description} {self.preview} {self.link}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ['title']



