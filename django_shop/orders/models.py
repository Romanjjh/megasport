from django.db import models
from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=60, verbose_name="Імя")
    last_name = models.CharField(max_length=60, verbose_name="Фамілія")
    email = models.EmailField(verbose_name="Email")
    address = models.CharField(max_length=150, verbose_name="Адрес")
    postal_code = models.CharField(max_length=30, verbose_name="Почтовий індекс")
    city = models.CharField(max_length=100, verbose_name="Місто")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    paid = models.BooleanField(default=False, verbose_name="Чи оплачено замовлення")

    class Meta:
        ordering = ('-created',)
        verbose_name = 'замовлення'
        verbose_name_plural = 'замовлення'

    def __str__(self):
        return 'Замовлення {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Замовлення")
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name="Товар")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
