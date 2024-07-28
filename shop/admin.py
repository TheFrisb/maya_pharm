from django import forms
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Product, Order, OrderItem, Category, Brand, RedirectImage


# Register your models here.
class ParentCategoryFilter(SimpleListFilter):
    title = "parent category"
    parameter_name = "parent"

    def lookups(self, request, model_admin):
        return [(cat.id, cat.name) for cat in Category.objects.filter(parent=None)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(parent__id=self.value())
        else:
            return queryset


class ProductAdminForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.exclude(parent=None),
        widget=FilteredSelectMultiple(verbose_name="Categories", is_stacked=False),
    )

    class Meta:
        model = Product
        fields = "__all__"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    list_display = ("product__title", "quantity", "price")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "parent"]
    list_filter = [ParentCategoryFilter]
    readonly_fields = ("slug",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Category.objects.filter(parent=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        # Only top-level categories for the filter list in admin
        qs = super().queryset(request)
        return qs.filter(parent=None)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = (
        "title",
        "status",
    )
    list_filter = ("status",)
    search_fields = ("title",)
    readonly_fields = ("slug",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ("status",)
    search_fields = ("first_name", "last_name", "shipping_address", "phone_number")
    inlines = [OrderItemInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(RedirectImage)
class RedirectImageAdmin(admin.ModelAdmin):
    pass
