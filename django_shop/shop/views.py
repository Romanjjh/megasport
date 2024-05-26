from loguru import logger

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, FormView, DetailView
from .forms import RegisterUserForm, LoginUserForm, FeedbackForm, ReviewForm
from .models import *
from .utils import DataMixin
from cart.forms import CartAddProductForm

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB")


class ShopHome(DataMixin, ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Головна"
        return dict(list(context.items()))

    def get_queryset(self):
        return Product.objects.all().select_related('category')


class ProductDetailView(DataMixin, DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        context['review_form'] = ReviewForm()
        context['cart_product_form'] = CartAddProductForm()
        context = self.get_user_context(**context)
        return context

    def post(self, request, category_slug, slug):
        product = self.get_object()
        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            cleaned_form = review_form.cleaned_data
            author_name = "Анонімний користувач"
            Review.objects.create(
                product=product,
                author=author_name,
                rating=cleaned_form['rating'],
                text=cleaned_form['text']
            )
            return redirect('shop:product_detail', category_slug=category_slug, slug=slug)

        context = self.get_context_data()
        context['review_form'] = review_form
        return self.render_to_response(context)


class ShopCategory(DataMixin, ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Категорія - ' + str(context['products'][0].category).upper()
        return dict(list(context.items()))

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['category_slug'])


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'shop/product/register.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Реєстрація')
        context['form_first'] = RegisterUser.form_class
        return dict(list(context.items()) + list(user_context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('shop:product_list')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'shop/product/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Війти')
        return dict(list(context.items()) + list(user_context.items()))

    def get_success_url(self):
        return reverse_lazy('shop:product_list')


class FeedbackFormView(DataMixin, FormView):
    form_class = FeedbackForm
    template_name = 'shop/product/feedback.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title='Зворотній звязок')
        context['form_feedback'] = FeedbackFormView.form_class
        return dict(list(context.items()) + list(user_context.items()))

    def form_valid(self, form):
        logger.debug(form.cleaned_data)
        return redirect('shop:product_list')


def about(request):
    return render(request, 'shop/product/about.html')


def logout_user(request):
    logout(request)
    return redirect('shop:login')
