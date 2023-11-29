from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    """
        Модель представляет курс в онлайн школе.
    """
    title = models.CharField(max_length=50, verbose_name='название')
    preview = models.ImageField(upload_to='course/', verbose_name='превью', null=True)
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'


class Lesson(models.Model):
    """
        Модель представляет урок в онлайн школе.
    """
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lesson/', verbose_name='превью', null=True)
    url = models.URLField(verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="курс")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'


class Subscription(models.Model):
    """
        Модель подписки на курс.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="пользователь")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="курс")

    def __str__(self):
        return f'{self.user.email} подписан на {self.course.title}'
