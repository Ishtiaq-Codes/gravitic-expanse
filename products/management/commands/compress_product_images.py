"""
Management command to compress all existing product images.
Run once on the server to fix old large images:

    python manage.py compress_product_images --settings=kamalia_store.settings_prod

Options:
    --dry-run    Show what would be compressed without actually doing it
    --max-size   Max dimension in pixels (default: 800)
    --quality    JPEG quality 1-95 (default: 85)
"""

import os
from django.core.management.base import BaseCommand
from django.conf import settings
from PIL import Image
from products.models import Product


class Command(BaseCommand):
    help = 'Compress and resize all existing product images'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Show results without changing files')
        parser.add_argument('--max-size', type=int, default=800, help='Max image dimension (default: 800)')
        parser.add_argument('--quality', type=int, default=85, help='JPEG quality 1-95 (default: 85)')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        max_size = options['max_size']
        quality = options['quality']

        products = Product.objects.filter(image__isnull=False).exclude(image='')
        total = products.count()

        self.stdout.write(f'\n🔍 Found {total} products with images\n')

        if dry_run:
            self.stdout.write('⚠️  DRY RUN — no files will be changed\n')

        compressed = 0
        skipped = 0
        errors = 0

        for product in products:
            try:
                img_path = product.image.path

                if not os.path.exists(img_path):
                    self.stdout.write(self.style.WARNING(f'  ⚠ MISSING: {product.name} → {img_path}'))
                    skipped += 1
                    continue

                # Get original size
                original_size = os.path.getsize(img_path)
                original_kb = original_size / 1024

                if not dry_run:
                    img = Image.open(img_path)

                    # Convert to RGB if needed
                    if img.mode in ('RGBA', 'P', 'LA'):
                        img = img.convert('RGB')

                    # Resize
                    img.thumbnail((max_size, max_size), Image.LANCZOS)

                    # Save compressed
                    img.save(img_path, format='JPEG', quality=quality, optimize=True)

                    new_size = os.path.getsize(img_path)
                    new_kb = new_size / 1024
                    saved_pct = int((1 - new_size / original_size) * 100)

                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  ✓ {product.name[:40]:<40} '
                            f'{original_kb:.0f}KB → {new_kb:.0f}KB '
                            f'(-{saved_pct}%)'
                        )
                    )
                else:
                    self.stdout.write(f'  → Would compress: {product.name} ({original_kb:.0f}KB)')

                compressed += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ ERROR {product.name}: {e}'))
                errors += 1

        self.stdout.write(f'\n{"─" * 60}')
        self.stdout.write(f'✅ Done: {compressed} compressed, {skipped} skipped, {errors} errors\n')
