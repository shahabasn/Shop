from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from menu.models import Category, MenuItem, ShopSetting
from datetime import time

class Command(BaseCommand):
    help = 'Seeds the database with default categories, items, a superuser, and settings.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # 1. Create Superuser/Owner
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' created with password 'admin123'."))
        else:
            self.stdout.write("Superuser 'admin' already exists.")

        # 2. Setup Shop Settings
        settings, created = ShopSetting.objects.get_or_create(id=1)
        settings.shop_name = "Steaming Mug Cafe & Stationery"
        settings.phone_number = "+91 98765 43210"
        settings.whatsapp_number = "919876543210"  # WhatsApp link format without + or spaces
        settings.google_map_link = "https://maps.app.goo.gl/FkH6xP5m4bSdfG2"
        settings.opening_time = time(7, 30)
        settings.closing_time = time(21, 30)
        settings.address = "Steaming Mug Corner, Near Central Library, Town Junction"
        settings.save()
        self.stdout.write(self.style.SUCCESS("Shop settings initialized."))

        # 3. Create Categories
        categories_data = ["Tea & Coffee", "Snacks", "Cool Drinks", "Cool Bar", "Stationery"]
        categories = {}
        for name in categories_data:
            cat, cat_created = Category.objects.get_or_create(name=name)
            categories[name] = cat
            if cat_created:
                self.stdout.write(f"Category '{name}' created.")

        # 4. Create Sample Menu Items
        items_data = [
            # Tea & Coffee
            {"name": "Masala Chai", "category": "Tea & Coffee", "price": 1.50, "description": "Authentic Indian spiced tea brewed with fresh ginger, cardamom, and milk.", "is_available": True},
            {"name": "Filter Coffee", "category": "Tea & Coffee", "price": 1.80, "description": "Traditional South Indian frothy hot coffee brewed using a metal filter.", "is_available": True},
            {"name": "Green Tea", "category": "Tea & Coffee", "price": 1.20, "description": "Mild, organic green tea rich in antioxidants.", "is_available": True},
            
            # Snacks
            {"name": "Hot Samosa (2 pcs)", "category": "Snacks", "price": 2.00, "description": "Crispy fried pastries filled with spiced potato and peas served with sweet and spicy chutney.", "is_available": True},
            {"name": "Banana Fritters", "category": "Snacks", "price": 1.50, "description": "Crispy, sweet ripe banana slices dipped in batter and deep-fried.", "is_available": True},
            {"name": "Veg Puff", "category": "Snacks", "price": 1.80, "description": "Flaky puff pastry stuffed with mixed vegetables and spices.", "is_available": True},

            # Cool Drinks
            {"name": "Fresh Lime Juice", "category": "Cool Drinks", "price": 1.50, "description": "Refreshing freshly squeezed lime juice, salted or sweet.", "is_available": True},
            {"name": "Iced Tea", "category": "Cool Drinks", "price": 2.20, "description": "Chilled black tea with fresh lemon slices and mint leaves.", "is_available": True},

            # Cool Bar
            {"name": "Chocolate Milkshake", "category": "Cool Bar", "price": 3.50, "description": "Creamy chocolate shake topped with cocoa powder and chocolate sauce.", "is_available": True},
            {"name": "Mango Ice Cream", "category": "Cool Bar", "price": 2.50, "description": "Rich scoop of premium Alphonso mango ice cream.", "is_available": True},

            # Stationery
            {"name": "Premium Notebook (A4)", "category": "Stationery", "price": 2.80, "description": "120-page ruled notebook, high-quality thick pages.", "is_available": True},
            {"name": "Gel Pen (Blue/Black)", "category": "Stationery", "price": 1.00, "description": "Smooth flowing water-resistant gel pen.", "is_available": True},
        ]

        for item in items_data:
            menu_item, created = MenuItem.objects.get_or_create(
                name=item["name"],
                category=categories[item["category"]],
                defaults={
                    "price": item["price"],
                    "description": item["description"],
                    "is_available": item["is_available"]
                }
            )
            if created:
                self.stdout.write(f"Menu item '{item['name']}' added.")

        self.stdout.write(self.style.SUCCESS("Database seeding completed!"))
