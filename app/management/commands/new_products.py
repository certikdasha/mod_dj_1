from django.core.management.base import BaseCommand
from app.models import Product


class Command(BaseCommand):
    help = "Add 2 products"

    def handle(self, *args, **options):
        Product.objects.create(name='Burger', text='big', price=34.5, stock=6)
        Product.objects.create(name='Soup', text='soup', price=25.8, stock=10)
