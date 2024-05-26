from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя категорії')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категорії'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    """Модель товаров"""
    category = models.ForeignKey(Category, verbose_name='Категорія', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Назва')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Зображення')
    description = models.TextField(verbose_name='Опис', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Ціна')
    available = models.BooleanField(default=True, verbose_name='Доступність')

    class Meta:
        verbose_name = 'Товари'
        verbose_name_plural = 'Товари'
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.category.slug,
                                                    self.slug])

    def get_average_review_score(self):
        average_score = 0.0
        if self.reviews.count() > 0:
            total_score = sum([review.rating for review in self.reviews.all()])
            average_score = total_score / self.reviews.count()
        return round(average_score, 1)


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, verbose_name='Продукт')
    author = models.CharField(max_length=50, verbose_name='Автор')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Рейтинг')
    text = models.TextField(blank=True, verbose_name='Текст')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')

    class Meta:
        ordering = ('-created', )

    def save(self, *args, **kwargs):
        if self.rating > 5 or self.rating < 1:
            raise ValidationError("Неправильний рейтинг")
        super().save(*args, **kwargs)
