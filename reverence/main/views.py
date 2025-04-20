from django.db.models import Q
from django.shortcuts import render
from .models import Category, Size, ClothingItem
from django.views.generic import ListView, DetailView


class CatalogView(ListView):
    model = ClothingItem
    template_name = 'main/product/list.html'
    context_object_name = 'clothing_items'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slugs = self.request.Get.getlist('category')
        size_names = self.request.Get.getlist('size')
        min_price = self.request.Get.get('min_price')
        max_price = self.request.Get.get('max_price')

        if category_slugs:
            queryset = queryset.filter(category__slug__in=category_slugs)

        if size_names:
            queryset = queryset.filter(
                Q(sizez__name__in=size_names) & Q(sizes_clothingitemsize__available=True)
            )

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__gte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['sizes'] = Size.objects.all()
        context['selected_categories'] = self.request.GET.getlist('category')
        context['selected_sizes'] = self.request.GET.getlist('size')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')

        return context


class ClothingItemDetailView(DetailView):
    model = ClothingItem
    template_name = 'main/product/detail.html'
    context_object_name = 'clothing_item'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
