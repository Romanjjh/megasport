from django.core.mail import send_mail
from .models import OrderItem
from .forms import OrderCreateForm
from cart.views import *
from cart.cart_services import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear_cart()
            send_mail('Замовлення Оформлено',
                      'Увійдіть в адмін панель, щоб переглянути нове замовлення.',
                      'roman.melnuk@icloud.com',
                      ['roman.melnuk@icloud.com '], fail_silently=True)
        return render(request, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create.html', {'form': form})
