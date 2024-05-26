from .models import Category


def get_categories_from_shop(request):
    categories = Category.objects.all()
    return {'categories': categories}
