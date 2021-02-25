from django.urls import path

from .views import ProductView, ProductReviewView, CategoryView

urlpatterns = [
    path('', ProductView.as_view()),
    path('/<int:product_id>/review', ProductReviewView.as_view()),
    path('/category', CategoryView.as_view()),
    ]
