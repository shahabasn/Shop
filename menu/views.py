from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import time
from .models import Category, MenuItem, ShopSetting, MenuView, SliderImage
from .forms import CategoryForm, MenuItemForm, ShopSettingForm, SliderImageForm

# Public Menu View
def menu_public(request):
    # Retrieve or create default shop settings
    settings = ShopSetting.objects.first()
    if not settings:
        settings = ShopSetting.objects.create(
            shop_name="മജീദിന്റെ ചായക്കട",
            phone_number="+91 8606756275",
            whatsapp_number="918606756275",
            google_map_link="https://maps.app.goo.gl/FkH6xP5m4bSdfG2",
            address="Majeedinte Chayakkada, Near Najath HSS School Peruvallur",
            opening_time=time(4, 30),
            closing_time=time(21, 0)
        )
    
    categories = Category.objects.all()
    slider_images = SliderImage.objects.filter(is_active=True).order_by('-created_at')
    
    # Query parameters
    search_query = request.GET.get('search', '').strip()
    category_id = request.GET.get('category', '').strip()
    
    items = MenuItem.objects.all().order_by('category', 'position')
    
    if search_query:
        items = items.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
        
    if category_id:
        items = items.filter(category_id=category_id)
        
    context = {
        'settings': settings,
        'categories': categories,
        'items': items,
        'slider_images': slider_images,
        'search_query': search_query,
        'selected_category_id': int(category_id) if category_id.isdigit() else None
    }
    return render(request, 'menu/menu.html', context)

# Login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'menu/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('menu_public')

# Admin Dashboard view
@login_required
def dashboard(request):
    total_items = MenuItem.objects.count()
    total_categories = Category.objects.count()
    available_items = MenuItem.objects.filter(is_available=True).count()
    unavailable_items = MenuItem.objects.filter(is_available=False).count()
    
    context = {
        'total_items': total_items,
        'total_categories': total_categories,
        'available_items': available_items,
        'unavailable_items': unavailable_items,
    }
    return render(request, 'menu/dashboard.html', context)

# Manage Categories - List & Edit/Delete/Add
@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'menu/category_list.html', {'categories': categories})

@login_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully.")
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'menu/category_form.html', {'form': form, 'title': 'Add Category'})

@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'menu/category_form.html', {'form': form, 'title': 'Edit Category'})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('category_list')
    return render(request, 'menu/category_confirm_delete.html', {'category': category})

# Manage Menu Items
@login_required
def item_list(request):
    items = MenuItem.objects.all().order_by('category', 'position')
    return render(request, 'menu/item_list.html', {'items': items})

@login_required
def item_add(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item added successfully.")
            return redirect('item_list')
    else:
        form = MenuItemForm()
    return render(request, 'menu/item_form.html', {'form': form, 'title': 'Add Menu Item'})

@login_required
def item_edit(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item updated successfully.")
            return redirect('item_list')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'menu/item_form.html', {'form': form, 'title': 'Edit Menu Item'})

@login_required
def item_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Menu item deleted successfully.")
        return redirect('item_list')
    return render(request, 'menu/item_confirm_delete.html', {'item': item})

# Shop Settings Edit
@login_required
def settings_edit(request):
    settings = ShopSetting.objects.first()
    if not settings:
        settings = ShopSetting.objects.create()
        
    if request.method == 'POST':
        form = ShopSettingForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, "Shop settings updated successfully.")
            return redirect('dashboard')
    else:
        form = ShopSettingForm(instance=settings)
    return render(request, 'menu/settings_form.html', {'form': form})


@csrf_exempt
def record_view(request):
    if request.method == 'POST':
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        MenuView.objects.create(ip_address=ip, user_agent=user_agent)
        return JsonResponse({'status': 'success', 'message': 'View recorded'})
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)


@login_required
def view_stats_api(request):
    now = timezone.now()
    # Handle localized start of day and start of month
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    total_views = MenuView.objects.count()
    today_views = MenuView.objects.filter(viewed_at__gte=today_start).count()
    month_views = MenuView.objects.filter(viewed_at__gte=month_start).count()
    
    return JsonResponse({
        'total_views': total_views,
        'today_views': today_views,
        'month_views': month_views
    })


def ensure_positions_sequenced(category):
    items = list(MenuItem.objects.filter(category=category).order_by('position', 'id'))
    for idx, item in enumerate(items, start=1):
        if item.position != idx:
            MenuItem.objects.filter(pk=item.pk).update(position=idx)


@login_required
def item_move_up(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    ensure_positions_sequenced(item.category)
    item.refresh_from_db()
    
    previous_item = MenuItem.objects.filter(
        category=item.category,
        position__lt=item.position
    ).order_by('-position').first()
    
    if previous_item:
        MenuItem.objects.filter(pk=item.pk).update(position=previous_item.position)
        MenuItem.objects.filter(pk=previous_item.pk).update(position=item.position)
        messages.success(request, f"Moved '{item.name}' up.")
    else:
        messages.info(request, f"'{item.name}' is already at the top.")
        
    return redirect('item_list')


@login_required
def item_move_down(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    ensure_positions_sequenced(item.category)
    item.refresh_from_db()
    
    next_item = MenuItem.objects.filter(
        category=item.category,
        position__gt=item.position
    ).order_by('position').first()
    
    if next_item:
        MenuItem.objects.filter(pk=item.pk).update(position=next_item.position)
        MenuItem.objects.filter(pk=next_item.pk).update(position=item.position)
        messages.success(request, f"Moved '{item.name}' down.")
    else:
        messages.info(request, f"'{item.name}' is already at the bottom.")
        
    return redirect('item_list')


@csrf_exempt
@login_required
def update_items_order(request):
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            item_ids = data.get('item_ids', [])
            for idx, item_id in enumerate(item_ids, start=1):
                MenuItem.objects.filter(pk=item_id).update(position=idx)
            return JsonResponse({'status': 'success', 'message': 'Ordering updated successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method.'}, status=400)


@login_required
def slider_list(request):
    sliders = SliderImage.objects.all().order_by('-created_at')
    if request.method == 'POST':
        form = SliderImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Slider image added successfully.")
            return redirect('slider_list')
    else:
        form = SliderImageForm()
    return render(request, 'menu/slider_list.html', {'sliders': sliders, 'form': form})


@login_required
def slider_delete(request, pk):
    slider = get_object_or_404(SliderImage, pk=pk)
    if request.method == 'POST':
        slider.delete()
        messages.success(request, "Slider image deleted successfully.")
    return redirect('slider_list')


