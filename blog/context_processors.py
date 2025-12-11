from .models import Category

def categories_in_context(request):
    return {
        'all_categories': Category.objects.all().order_by('name')
    }
