from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id and self.position == 0:
            max_pos = MenuItem.objects.filter(category=self.category).aggregate(models.Max('position'))['position__max']
            self.position = (max_pos or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ShopSetting(models.Model):
    shop_name = models.CharField(max_length=200, default="Tea & Snacks Corner")
    phone_number = models.CharField(max_length=20, default="+1234567890")
    whatsapp_number = models.CharField(max_length=20, default="+1234567890")
    google_map_link = models.URLField(max_length=500, blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.shop_name


class MenuView(models.Model):
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"View from {self.ip_address} at {self.viewed_at}"


class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider_images/')
    title = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Slider Image {self.id}"

