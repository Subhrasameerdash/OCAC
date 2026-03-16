from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/transactions/', views.transaction_list, name='transaction-list'),
    path('api/transactions/create/', views.transaction_create, name='transaction-create'),
    path('api/transactions/<int:pk>/update/', views.transaction_update, name='transaction-update'),
    path('api/transactions/<int:pk>/delete/', views.transaction_delete, name='transaction-delete'),
    path('api/dashboard/', views.dashboard_summary, name='dashboard-summary'),
]
