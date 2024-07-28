from shop.models import Category


def common_variables(request):
    return {
        "categories": Category.objects.filter(parent__isnull=True).prefetch_related(
            "subcategories"
        )
    }
