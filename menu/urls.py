from django.urls import path
from . import views

urlpatterns = [
    # Public route
    path('', views.menu_public, name='menu_public'),
    
    # Auth routes
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Admin Dashboard & Settings
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/settings/', views.settings_edit, name='settings_edit'),
    
    # Categories CRUD
    path('dashboard/categories/', views.category_list, name='category_list'),
    path('dashboard/categories/add/', views.category_add, name='category_add'),
    path('dashboard/categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('dashboard/categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Menu Items CRUD
    path('dashboard/items/', views.item_list, name='item_list'),
    path('dashboard/items/add/', views.item_add, name='item_add'),
    path('dashboard/items/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('dashboard/items/<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('dashboard/items/<int:pk>/move-up/', views.item_move_up, name='item_move_up'),
    path('dashboard/items/<int:pk>/move-down/', views.item_move_down, name='item_move_down'),
    path('dashboard/items/reorder/', views.update_items_order, name='update_items_order'),
    
    # Slider Images CRUD
    path('dashboard/sliders/', views.slider_list, name='slider_list'),
    path('dashboard/sliders/<int:pk>/delete/', views.slider_delete, name='slider_delete'),
    
    # API endpoints
    path('api/views/record/', views.record_view, name='record_view'),
    path('api/views/stats/', views.view_stats_api, name='view_stats_api'),
]
