#!/usr/bin/env python
import os
import sys
import django
from datetime import date

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mac.settings')
django.setup()

from shop.models import Product

# More products with 5-9 items per category
products_data = [
    # SHIRTS Category (7 items total including existing)
    {
        'product_name': 'Formal White Shirt',
        'category': 'shirts',
        'subcategory': 'formal',
        'price': 1199,
        'desc': 'Classic white formal shirt with slim fit. Perfect for office and business meetings.',
        'image': 'shop/images/1.jpg'
    },
    {
        'product_name': 'Casual Check Shirt',
        'category': 'shirts',
        'subcategory': 'casual',
        'price': 799,
        'desc': 'Comfortable checkered shirt in cotton blend. Great for weekend outings.',
        'image': 'shop/images/img4.jpg'
    },
    {
        'product_name': 'Denim Shirt',
        'category': 'shirts',
        'subcategory': 'casual',
        'price': 1099,
        'desc': 'Trendy denim shirt with modern fit. Perfect for casual and semi-formal occasions.',
        'image': 'shop/images/hero.png'
    },
    {
        'product_name': 'Linen Summer Shirt',
        'category': 'shirts',
        'subcategory': 'summer',
        'price': 1299,
        'desc': 'Breathable linen shirt perfect for hot weather. Light and comfortable.',
        'image': 'shop/images/1.jpg'
    },
    {
        'product_name': 'Printed Casual Shirt',
        'category': 'shirts',
        'subcategory': 'printed',
        'price': 899,
        'desc': 'Stylish printed shirt with unique patterns. Stand out in any crowd.',
        'image': 'shop/images/img4.jpg'
    },

    # JEANS Category (6 items)
    {
        'product_name': 'Skinny Fit Jeans',
        'category': 'jeans',
        'subcategory': 'skinny',
        'price': 1599,
        'desc': 'Modern skinny fit jeans with stretch fabric. Comfortable all-day wear.',
        'image': 'shop/images/hero.png'
    },
    {
        'product_name': 'Regular Fit Jeans',
        'category': 'jeans',
        'subcategory': 'regular',
        'price': 1199,
        'desc': 'Classic regular fit jeans in premium denim. Timeless style and comfort.',
        'image': 'shop/images/1.jpg'
    },
    {
        'product_name': 'Ripped Jeans',
        'category': 'jeans',
        'subcategory': 'ripped',
        'price': 1699,
        'desc': 'Trendy ripped jeans with distressed finish. Perfect for casual street style.',
        'image': 'shop/images/img4.jpg'
    },
    {
        'product_name': 'Black Jeans',
        'category': 'jeans',
        'subcategory': 'black',
        'price': 1399,
        'desc': 'Versatile black jeans that go with everything. Essential wardrobe piece.',
        'image': 'shop/images/hero.png'
    },
    {
        'product_name': 'Light Wash Jeans',
        'category': 'jeans',
        'subcategory': 'light',
        'price': 1249,
        'desc': 'Light wash denim jeans with vintage appeal. Relaxed and stylish.',
        'image': 'shop/images/1.jpg'
    },

    # WATCHES Category (8 items)
    {
        'product_name': 'Classic Analog Watch',
        'category': 'watches',
        'subcategory': 'analog',
        'price': 2999,
        'desc': 'Elegant analog watch with leather strap. Perfect for formal occasions.',
        'image': 'shop/images/img4.jpg'
    },
    {
        'product_name': 'Sports Digital Watch',
        'category': 'watches',
        'subcategory': 'sports',
        'price': 1999,
        'desc': 'Durable sports watch with multiple functions. Water resistant and shockproof.',
        'image': 'shop/images/hero.png'
    },
    {
        'product_name': 'Luxury Gold Watch',
        'category': 'watches',
        'subcategory': 'luxury',
        'price': 15999,
        'desc': 'Premium gold-plated watch with Swiss movement. Ultimate luxury timepiece.',
        'image': 'shop/images/1.jpg'
    },
    {
        'product_name': 'Casual Steel Watch',
        'category': 'watches',
        'subcategory': 'casual',
        'price': 3499,
        'desc': 'Stainless steel watch with modern design. Perfect for daily wear.',
        'image': 'shop/images/img4.jpg'
    },
    {
        'product_name': 'Vintage Style Watch',
        'category': 'watches',
        'subcategory': 'vintage',
        'price': 2799,
        'desc': 'Retro-inspired watch with classic design. Timeless elegance.',
        'image': 'shop/images/hero.png'
    },
    {
        'product_name': 'Fitness Tracker Watch',
        'category': 'watches',
        'subcategory': 'fitness',
        'price': 3999,
        'desc': 'Advanced fitness tracker with heart rate monitor and GPS.',
        'image': 'shop/images/1.jpg'
    },
    {
        'product_name': 'Minimalist Watch',
        'category': 'watches',
        'subcategory': 'minimal',
        'price': 2199,
        'desc': 'Clean, minimalist design watch. Simple elegance for modern lifestyle.',
        'image': 'shop/images/img4.jpg'
    },

    # SHOES Category (7 items)
    {
        'product_name': 'Formal Leather Shoes',
        'category': 'shoes',
        'subcategory': 'formal',
        'price': 2999,
        'desc': 'Premium leather formal shoes. Perfect for business and special occasions.',
        'image': 'shop/images/hero.png'
    },
    {
        'product_name': 'Casual Sneakers White',
        'category': 'shoes',
        'subcategory': 'casual',
        'price': 1799,
        'desc': 'Comfortable white sneakers for everyday wear. Classic and versatile.',
        'image': 'shop/images/1.jpg'
    },
    {
        'product_name': 'High-Top Sneakers',
        'category': 'shoes',
        'subcategory': 'sneakers',
        'price': 2299,
        'desc': 'Trendy high-top sneakers with street style appeal. Bold and comfortable.',
        'image': 'shop/images/img4.jpg'
    },
    {
        'product_name': 'Canvas Shoes',
        'category': 'shoes',
        'subcategory': 'canvas',
        'price': 1299,
        'desc': 'Lightweight canvas shoes perfect for casual outings. Breathable and stylish.',
        'image': 'shop/images/hero.png'
    },
    {
        'product_name': 'Hiking Boots',
        'category': 'shoes',
        'subcategory': 'boots',
        'price': 3499,
        'desc': 'Durable hiking boots with excellent grip. Perfect for outdoor adventures.',
        'image': 'shop/images/1.jpg'
    },
    {
        'product_name': 'Loafers Brown',
        'category': 'shoes',
        'subcategory': 'loafers',
        'price': 2599,
        'desc': 'Comfortable brown loafers for semi-formal occasions. Slip-on convenience.',
        'image': 'shop/images/img4.jpg'
    },

    # T-SHIRTS Category (6 items)
    {
        'product_name': 'Graphic T-Shirt',
        'category': 'tshirts',
        'subcategory': 'graphic',
        'price': 699,
        'desc': 'Cool graphic t-shirt with unique artwork. Express your personality.',
        'image': 'shop/images/hero.png'
    },
    {
        'product_name': 'Plain Black T-Shirt',
        'category': 'tshirts',
        'subcategory': 'plain',
        'price': 499,
        'desc': 'Essential plain black t-shirt. Versatile and comfortable for any occasion.',
        'image': 'shop/images/1.jpg'
    },
    {
        'product_name': 'V-Neck T-Shirt',
        'category': 'tshirts',
        'subcategory': 'vneck',
        'price': 649,
        'desc': 'Stylish v-neck t-shirt in premium cotton. Modern fit and comfort.',
        'image': 'shop/images/img4.jpg'
    },
    {
        'product_name': 'Long Sleeve T-Shirt',
        'category': 'tshirts',
        'subcategory': 'longsleeve',
        'price': 799,
        'desc': 'Comfortable long sleeve t-shirt. Perfect for layering or standalone wear.',
        'image': 'shop/images/hero.png'
    },
    {
        'product_name': 'Striped T-Shirt',
        'category': 'tshirts',
        'subcategory': 'striped',
        'price': 749,
        'desc': 'Classic striped t-shirt with timeless appeal. Casual and stylish.',
        'image': 'shop/images/1.jpg'
    },

    # ELECTRONICS Category (5 items)
    {
        'product_name': 'Bluetooth Speaker',
        'category': 'electronics',
        'subcategory': 'speaker',
        'price': 2999,
        'desc': 'Portable bluetooth speaker with excellent sound quality. Perfect for parties.',
        'image': 'shop/images/img4.jpg'
    },
    {
        'product_name': 'Smartphone Case',
        'category': 'electronics',
        'subcategory': 'accessories',
        'price': 599,
        'desc': 'Protective smartphone case with shock absorption. Keep your phone safe.',
        'image': 'shop/images/hero.png'
    },
    {
        'product_name': 'Power Bank 20000mAh',
        'category': 'electronics',
        'subcategory': 'powerbank',
        'price': 1999,
        'desc': 'High capacity power bank with fast charging. Never run out of battery.',
        'image': 'shop/images/1.jpg'
    },
    {
        'product_name': 'USB Cable Set',
        'category': 'electronics',
        'subcategory': 'cables',
        'price': 399,
        'desc': 'Set of premium USB cables for all your charging needs. Durable and fast.',
        'image': 'shop/images/img4.jpg'
    }
]

def add_products():
    print("Adding more products to create 5-9 items per category...")
    
    for product_data in products_data:
        # Check if product already exists
        if not Product.objects.filter(product_name=product_data['product_name']).exists():
            product = Product(
                product_name=product_data['product_name'],
                category=product_data['category'],
                subcategory=product_data['subcategory'],
                price=product_data['price'],
                desc=product_data['desc'],
                pub_date=date.today(),
                image=product_data['image']
            )
            product.save()
            print(f"✓ Added: {product.product_name} ({product.category})")
        else:
            print(f"- Skipped (already exists): {product_data['product_name']}")
    
    print(f"\nTotal products in database: {Product.objects.count()}")
    
    # Show products by category
    print("\nProducts by category:")
    categories = Product.objects.values_list('category', flat=True).distinct()
    for category in categories:
        count = Product.objects.filter(category=category).count()
        print(f"  {category.capitalize()}: {count} items")

if __name__ == '__main__':
    add_products() 