from django.db.models import Q
from django.views.generic import DetailView, ListView

from .models import Product


class ProductListView(ListView):
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 9

    def get_queryset(self):  # type: ignore[override]
        queryset = Product.objects.filter(is_active=True)
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):  # type: ignore[override]
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        return context


class ProductDetailView(DetailView):
    template_name = "products/product_detail.html"
    context_object_name = "product"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    queryset = Product.objects.filter(is_active=True)
