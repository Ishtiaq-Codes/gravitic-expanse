from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from PIL import Image
import os


class Product(models.Model):
    CATEGORY_CHOICES = getattr(settings, 'PRODUCT_CATEGORIES', [])

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='suits')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    suite_code = models.CharField(max_length=50, blank=True, null=True, unique=True, help_text="Unique code for the suit/product")
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-generate slug
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

        # Auto-compress and resize image after saving
        if self.image:
            img_path = self.image.path
            if os.path.exists(img_path):
                img = Image.open(img_path)

                # Convert RGBA/palette images to RGB (required for JPEG)
                if img.mode in ('RGBA', 'P', 'LA'):
                    img = img.convert('RGB')

                # Resize to max 800x800 while keeping aspect ratio
                max_size = (800, 800)
                img.thumbnail(max_size, Image.LANCZOS)

                # Save as JPEG at 85% quality (reduces file size by 70-90%)
                img.save(img_path, format='JPEG', quality=85, optimize=True)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    @property
    def effective_price(self):
        """Return discount price if available, otherwise regular price."""
        if self.discount_price and self.discount_price < self.price:
            return self.discount_price
        return self.price

    @property
    def discount_percentage(self):
        """Return percentage off if discount exists."""
        if self.discount_price and self.discount_price < self.price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0
