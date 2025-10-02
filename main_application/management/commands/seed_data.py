"""
Django management command to seed the database with Kenyan agricultural data
Usage: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from decimal import Decimal
import random
from datetime import datetime, timedelta, date
import uuid

# Import all models
from main_application.models import *


class Command(BaseCommand):
    help = 'Seeds the database with sample Kenyan agricultural data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()
        
        self.stdout.write('Starting data seeding...')
        
        # Seed data in order of dependencies
        self.seed_counties()
        self.seed_subcounties()
        self.seed_wards()
        self.seed_users()
        self.seed_locations()
        self.seed_farmer_profiles()
        self.seed_buyer_profiles()
        self.seed_farms()
        self.seed_crop_categories()
        self.seed_crops()
        self.seed_product_units()
        self.seed_products()
        self.seed_product_reviews()
        self.seed_market_prices()
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))

    def clear_data(self):
        """Clear existing data (use with caution)"""
        models_to_clear = [
            ProductReview, MarketPrice, Product, Farm, FarmerProfile, BuyerProfile, 
            Location, CustomUser, Crop, CropCategory, 
            ProductUnit, Ward, SubCounty, County,
        ]
        
        for model in models_to_clear:
            try:
                model.objects.all().delete()
                self.stdout.write(f'Cleared {model.__name__}')
            except Exception as e:
                self.stdout.write(f'Error clearing {model.__name__}: {e}')

    def seed_counties(self):
        """Seed Kenyan counties"""
        counties_data = [
            {'name': 'Nairobi', 'code': '001', 'population': 4397073, 'area_sq_km': 696.0},
            {'name': 'Kiambu', 'code': '023', 'population': 2417735, 'area_sq_km': 2449.0},
            {'name': 'Murang\'a', 'code': '022', 'population': 1056640, 'area_sq_km': 2325.0},
            {'name': 'Nakuru', 'code': '033', 'population': 2162202, 'area_sq_km': 7496.0},
            {'name': 'Meru', 'code': '013', 'population': 1545714, 'area_sq_km': 6930.0},
            {'name': 'Nyeri', 'code': '021', 'population': 759164, 'area_sq_km': 3337.0},
            {'name': 'Kirinyaga', 'code': '024', 'population': 610411, 'area_sq_km': 1478.0},
            {'name': 'Embu', 'code': '014', 'population': 608599, 'area_sq_km': 2555.0},
            {'name': 'Machakos', 'code': '029', 'population': 1421932, 'area_sq_km': 6281.0},
            {'name': 'Uasin Gishu', 'code': '035', 'population': 1163186, 'area_sq_km': 3345.0},
        ]
        
        for county_data in counties_data:
            County.objects.get_or_create(
                code=county_data['code'],
                defaults=county_data
            )
        
        self.stdout.write(f'✓ Seeded {len(counties_data)} counties')

    def seed_subcounties(self):
        """Seed sub-counties"""
        subcounties_data = [
            # Nairobi (4 sub-counties)
            {'county_code': '001', 'name': 'Westlands', 'code': '001001'},
            {'county_code': '001', 'name': 'Dagoretti North', 'code': '001002'},
            {'county_code': '001', 'name': 'Langata', 'code': '001003'},
            {'county_code': '001', 'name': 'Embakasi South', 'code': '001004'},
            
            # Kiambu (5 sub-counties)
            {'county_code': '023', 'name': 'Thika Town', 'code': '023001'},
            {'county_code': '023', 'name': 'Ruiru', 'code': '023002'},
            {'county_code': '023', 'name': 'Limuru', 'code': '023003'},
            {'county_code': '023', 'name': 'Kikuyu', 'code': '023004'},
            {'county_code': '023', 'name': 'Gatundu South', 'code': '023005'},
            
            # Murang'a (4 sub-counties)
            {'county_code': '022', 'name': 'Kangema', 'code': '022001'},
            {'county_code': '022', 'name': 'Mathioya', 'code': '022002'},
            {'county_code': '022', 'name': 'Kiharu', 'code': '022003'},
            {'county_code': '022', 'name': 'Maragwa', 'code': '022004'},
            
            # Nakuru (3 sub-counties)
            {'county_code': '033', 'name': 'Nakuru Town East', 'code': '033001'},
            {'county_code': '033', 'name': 'Rongai', 'code': '033002'},
            {'county_code': '033', 'name': 'Naivasha', 'code': '033003'},
            
            # Meru (3 sub-counties)
            {'county_code': '013', 'name': 'Imenti North', 'code': '013001'},
            {'county_code': '013', 'name': 'Imenti South', 'code': '013002'},
            {'county_code': '013', 'name': 'Tigania East', 'code': '013003'},
        ]
        
        for subcounty_data in subcounties_data:
            county = County.objects.get(code=subcounty_data['county_code'])
            SubCounty.objects.get_or_create(
                county=county,
                code=subcounty_data['code'],
                defaults={'name': subcounty_data['name']}
            )
        
        self.stdout.write(f'✓ Seeded {len(subcounties_data)} sub-counties')

    def seed_wards(self):
        """Seed wards"""
        # Generate 2-3 wards per sub-county
        subcounties = SubCounty.objects.all()
        ward_count = 0
        
        for subcounty in subcounties:
            num_wards = random.randint(2, 3)
            for i in range(num_wards):
                Ward.objects.get_or_create(
                    subcounty=subcounty,
                    code=f'{subcounty.code}{i+1:02d}',
                    defaults={'name': f'{subcounty.name} Ward {i+1}'}
                )
                ward_count += 1
        
        self.stdout.write(f'✓ Seeded {ward_count} wards')

    def seed_users(self):
        """Seed users - 25 farmers, 15 buyers, 1 admin"""
        first_names = ['John', 'Mary', 'Peter', 'Jane', 'David', 'Sarah', 'James', 'Lucy', 'Michael', 'Grace',
                      'Daniel', 'Ann', 'Joseph', 'Faith', 'Samuel', 'Ruth', 'Brian', 'Joyce', 'Kevin', 'Alice',
                      'Patrick', 'Rose', 'Simon', 'Catherine', 'Paul', 'Margaret', 'Stephen', 'Elizabeth', 'Moses', 'Hannah']
        
        last_names = ['Mwangi', 'Wanjiku', 'Kamau', 'Njeri', 'Kariuki', 'Waithera', 'Kimani', 'Muthoni', 'Omondi', 'Akinyi',
                     'Otieno', 'Adhiambo', 'Kipchoge', 'Chepkemoi', 'Mutua', 'Nduku', 'Ochieng', 'Atieno', 'Wekesa', 'Nekesa']
        
        # Create 25 farmers
        for i in range(25):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f'{first_name.lower()}_{last_name.lower()}_{i}'
            
            CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': f'{username}@farm.ke',
                    'phone_number': f'+2547{random.randint(10000000, 99999999)}',
                    'user_type': 'farmer',
                    'national_id': f'{random.randint(10000000, 99999999)}',
                    'is_verified': random.choice([True, True, True, False]),  # 75% verified
                    'password': make_password('password123'),
                    'date_of_birth': date(random.randint(1970, 2000), random.randint(1, 12), random.randint(1, 28)),
                }
            )
        
        # Create 15 buyers
        for i in range(15):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f'buyer_{first_name.lower()}_{i}'
            
            CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': f'{username}@buyer.ke',
                    'phone_number': f'+2547{random.randint(10000000, 99999999)}',
                    'user_type': 'buyer',
                    'national_id': f'{random.randint(10000000, 99999999)}',
                    'is_verified': True,
                    'password': make_password('password123'),
                    'date_of_birth': date(random.randint(1975, 2000), random.randint(1, 12), random.randint(1, 28)),
                }
            )
        
        # Create admin
        CustomUser.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'email': 'admin@farm.ke',
                'phone_number': '+254700000000',
                'user_type': 'admin',
                'national_id': '99999999',
                'is_verified': True,
                'is_staff': True,
                'is_superuser': True,
                'password': make_password('admin123'),
                'date_of_birth': date(1980, 1, 1),
            }
        )
        
        self.stdout.write('✓ Seeded 41 users (25 farmers, 15 buyers, 1 admin)')

    def seed_locations(self):
        """Seed locations for all users"""
        users = CustomUser.objects.filter(user_type__in=['farmer', 'buyer'])
        wards = list(Ward.objects.all())
        
        for user in users:
            ward = random.choice(wards)
            
            Location.objects.get_or_create(
                user=user,
                name='Home',
                defaults={
                    'county': ward.subcounty.county,
                    'subcounty': ward.subcounty,
                    'ward': ward,
                    'village': f'{user.first_name} Village',
                    'detailed_address': f'Plot {random.randint(1, 500)}, {ward.name}',
                    'latitude': Decimal(str(round(random.uniform(-4.5, 1.5), 6))),
                    'longitude': Decimal(str(round(random.uniform(33.5, 41.5), 6))),
                    'is_default': True,
                }
            )
        
        self.stdout.write(f'✓ Seeded {users.count()} locations')

    def seed_farmer_profiles(self):
        """Seed farmer profiles"""
        farmer_users = CustomUser.objects.filter(user_type='farmer')
        farming_types = ['crop', 'livestock', 'mixed', 'poultry', 'horticulture']
        experiences = ['beginner', 'intermediate', 'experienced', 'expert']
        
        for user in farmer_users:
            FarmerProfile.objects.get_or_create(
                user=user,
                defaults={
                    'farm_name': f'{user.first_name} {user.last_name} Farm',
                    'farming_type': random.choice(farming_types),
                    'years_of_experience': random.choice(experiences),
                    'total_farm_size': Decimal(str(round(random.uniform(0.5, 20.0), 2))),
                    'farming_methods': random.sample(['organic', 'conventional', 'mixed'], k=random.randint(1, 2)),
                    'certifications': random.sample(['GAP', 'Organic', 'GlobalGAP', 'None'], k=random.randint(0, 2)),
                    'bank_account_number': f'{random.randint(1000000000, 9999999999)}',
                    'bank_name': random.choice(['Equity Bank', 'KCB', 'Cooperative Bank', 'NCBA']),
                    'mpesa_number': user.phone_number,
                    'is_cooperative_member': random.choice([True, False]),
                }
            )
        
        self.stdout.write(f'✓ Seeded {farmer_users.count()} farmer profiles')

    def seed_buyer_profiles(self):
        """Seed buyer profiles"""
        buyer_users = CustomUser.objects.filter(user_type='buyer')
        buyer_types = ['individual', 'restaurant', 'hotel', 'retailer', 'wholesaler']
        
        for user in buyer_users:
            buyer_type = random.choice(buyer_types)
            BuyerProfile.objects.get_or_create(
                user=user,
                defaults={
                    'buyer_type': buyer_type,
                    'business_name': f'{user.first_name} {buyer_type.title()}' if buyer_type != 'individual' else '',
                    'preferred_payment_method': random.choice(['mpesa', 'bank_transfer', 'cash']),
                    'credit_limit': Decimal(str(random.randint(10000, 100000))),
                }
            )
        
        self.stdout.write(f'✓ Seeded {buyer_users.count()} buyer profiles')

    def seed_farms(self):
        """Seed 2-4 farms per farmer"""
        farmer_profiles = FarmerProfile.objects.all()
        farm_count = 0
        
        for farmer in farmer_profiles:
            user_location = farmer.user.locations.first()
            num_farms = random.randint(1, 3)
            
            for i in range(num_farms):
                Farm.objects.get_or_create(
                    farmer=farmer,
                    name=f'{farmer.farm_name}-plot-{i+1}-{farmer.user.username}',
                    defaults={
                        'location': user_location,
                        'size': Decimal(str(round(random.uniform(0.5, 10.0), 2))),
                        'soil_type': random.choice(['Loam', 'Clay', 'Sandy', 'Volcanic']),
                        'water_source': random.choice(['Borehole', 'River', 'Rain', 'Municipal']),
                        'irrigation_method': random.choice(['Drip', 'Sprinkler', 'Flood', 'None']),
                        'elevation': random.randint(800, 2500),
                        'description': f'Quality farm in {user_location.county.name}',
                        'is_active': True,
                    }
                )
                farm_count += 1
        
        self.stdout.write(f'✓ Seeded {farm_count} farms')

    def seed_crop_categories(self):
        """Seed crop categories"""
        categories_data = [
            {'name': 'cereals', 'description': 'Cereal crops like maize, wheat, rice'},
            {'name': 'vegetables', 'description': 'Vegetable crops'},
            {'name': 'fruits', 'description': 'Fruit crops'},
            {'name': 'legumes', 'description': 'Beans, peas, and other legumes'},
            {'name': 'tubers', 'description': 'Root and tuber crops'},
            {'name': 'cash-crops', 'description': 'Export and cash crops'},
        ]
        
        for category_data in categories_data:
            CropCategory.objects.get_or_create(
                name=category_data['name'],
                defaults=category_data
            )
        
        self.stdout.write(f'✓ Seeded {len(categories_data)} crop categories')

    def seed_crops(self):
        """Seed diverse crops"""
        categories = {cat.name: cat for cat in CropCategory.objects.all()}
        
        crops_data = [
            # Cereals
            {'name': 'maize', 'scientific_name': 'Zea mays', 'category': 'cereals', 'maturity': 120},
            {'name': 'wheat', 'scientific_name': 'Triticum aestivum', 'category': 'cereals', 'maturity': 140},
            {'name': 'rice', 'scientific_name': 'Oryza sativa', 'category': 'cereals', 'maturity': 150},
            
            # Vegetables
            {'name': 'tomatoes', 'scientific_name': 'Solanum lycopersicum', 'category': 'vegetables', 'maturity': 75},
            {'name': 'cabbage', 'scientific_name': 'Brassica oleracea', 'category': 'vegetables', 'maturity': 60},
            {'name': 'kale-sukuma-wiki', 'scientific_name': 'Brassica oleracea', 'category': 'vegetables', 'maturity': 45},
            {'name': 'spinach', 'scientific_name': 'Spinacia oleracea', 'category': 'vegetables', 'maturity': 40},
            {'name': 'onions', 'scientific_name': 'Allium cepa', 'category': 'vegetables', 'maturity': 90},
            
            # Fruits
            {'name': 'bananas', 'scientific_name': 'Musa acuminata', 'category': 'fruits', 'maturity': 270},
            {'name': 'avocado', 'scientific_name': 'Persea americana', 'category': 'fruits', 'maturity': 365},
            {'name': 'mangoes', 'scientific_name': 'Mangifera indica', 'category': 'fruits', 'maturity': 365},
            
            # Legumes
            {'name': 'beans', 'scientific_name': 'Phaseolus vulgaris', 'category': 'legumes', 'maturity': 90},
            {'name': 'peas', 'scientific_name': 'Pisum sativum', 'category': 'legumes', 'maturity': 75},
            
            # Tubers
            {'name': 'potatoes', 'scientific_name': 'Solanum tuberosum', 'category': 'tubers', 'maturity': 105},
            {'name': 'sweet-potatoes', 'scientific_name': 'Ipomoea batatas', 'category': 'tubers', 'maturity': 120},
            
            # Cash crops
            {'name': 'coffee', 'scientific_name': 'Coffea arabica', 'category': 'cash-crops', 'maturity': 365},
            {'name': 'tea', 'scientific_name': 'Camellia sinensis', 'category': 'cash-crops', 'maturity': 365},
        ]
        
        for crop_data in crops_data:
            category = categories.get(crop_data['category'])
            if category:
                Crop.objects.get_or_create(
                    name=crop_data['name'],
                    defaults={
                        'scientific_name': crop_data['scientific_name'],
                        'category': category,
                        'maturity_period_days': crop_data['maturity'],
                        'growing_season': random.choice(['Long rains', 'Short rains', 'Year-round']),
                    }
                )
        
        self.stdout.write(f'✓ Seeded {len(crops_data)} crops')

    def seed_product_units(self):
        """Seed product units"""
        units_data = [
            {'name': 'Kilogram', 'abbreviation': 'kg', 'conversion_factor': Decimal('1.0')},
            {'name': 'Bag (90kg)', 'abbreviation': 'bag', 'conversion_factor': Decimal('90.0')},
            {'name': 'Crate', 'abbreviation': 'crate', 'conversion_factor': Decimal('10.0')},
            {'name': 'Piece', 'abbreviation': 'pc', 'conversion_factor': Decimal('1.0')},
            {'name': 'Bunch', 'abbreviation': 'bunch', 'conversion_factor': Decimal('5.0')},
            {'name': 'Sack (50kg)', 'abbreviation': 'sack', 'conversion_factor': Decimal('50.0')},
        ]
        
        for unit_data in units_data:
            ProductUnit.objects.get_or_create(
                abbreviation=unit_data['abbreviation'],
                defaults=unit_data
            )
        
        self.stdout.write(f'✓ Seeded {len(units_data)} product units')

    def seed_products(self):
        """Seed 3-8 products per farm"""
        farms = Farm.objects.all()
        crops = list(Crop.objects.all())
        units = list(ProductUnit.objects.all())
        quality_grades = ['premium', 'grade_a', 'grade_b', 'standard']
        statuses = ['active', 'active', 'active', 'sold_out', 'draft']
        product_count = 0
        
        for farm in farms:
            num_products = random.randint(3, 8)
            selected_crops = random.sample(crops, min(num_products, len(crops)))
            
            for crop in selected_crops:
                unit = random.choice(units)
                harvest_date = timezone.now().date() - timedelta(days=random.randint(1, 60))
                
                Product.objects.get_or_create(
                    farmer=farm.farmer,
                    crop=crop,
                    farm=farm,
                    name=f'{crop.name}-{farm.farmer.user.username}-{product_count}',
                    defaults={
                        'description': f'Fresh {crop.name} from {farm.name} in {farm.location.county.name}',
                        'quantity_available': Decimal(str(random.randint(10, 500))),
                        'unit': unit,
                        'price_per_unit': Decimal(str(random.randint(30, 300))),
                        'minimum_order': Decimal(str(random.choice([1, 2, 5, 10]))),
                        'quality_grade': random.choice(quality_grades),
                        'harvest_date': harvest_date,
                        'expiry_date': harvest_date + timedelta(days=random.randint(30, 180)),
                        'organic_certified': random.choice([True, False]),
                        'status': random.choice(statuses),
                        'featured': random.choice([True, False, False, False]),  # 25% featured
                        'views_count': random.randint(0, 500),
                    }
                )
                product_count += 1
        
        self.stdout.write(f'✓ Seeded {product_count} products')

    def seed_product_reviews(self):
        """Seed reviews for active products"""
        active_products = Product.objects.filter(status='active')[:50]  # Review first 50 active products
        buyers = list(CustomUser.objects.filter(user_type='buyer'))
        review_count = 0
        
        for product in active_products:
            num_reviews = random.randint(0, 5)
            reviewers = random.sample(buyers, min(num_reviews, len(buyers)))
            
            for buyer in reviewers:
                rating = random.randint(3, 5)  # Mostly positive reviews
                comments = [
                    "Great quality produce!",
                    "Fresh and well packaged.",
                    "Good value for money.",
                    "Would buy again.",
                    "Excellent service from the farmer.",
                    "Product as described.",
                    "Fast delivery and good quality.",
                ]
                
                ProductReview.objects.get_or_create(
                    product=product,
                    buyer=buyer,
                    defaults={
                        'rating': rating,
                        'title': f'{rating} stars - {random.choice(["Satisfied", "Good", "Excellent"])}',
                        'comment': random.choice(comments),
                        'is_verified_purchase': True,
                        'helpful_votes': random.randint(0, 20),
                    }
                )
                review_count += 1
        
        self.stdout.write(f'✓ Seeded {review_count} product reviews')

    def seed_market_prices(self):
        """Seed historical market prices"""
        crops = Crop.objects.all()
        counties = County.objects.all()
        units = list(ProductUnit.objects.all())
        price_count = 0
        
        # Create price records for the last 90 days
        for days_ago in range(0, 90, 7):  # Weekly prices
            date_recorded = timezone.now().date() - timedelta(days=days_ago)
            
            for crop in crops:
                for county in random.sample(list(counties), min(3, len(counties))):
                    base_price = random.randint(40, 200)
                    variation = random.uniform(0.9, 1.1)
                    
                    MarketPrice.objects.get_or_create(
                        crop=crop,
                        location=county,
                        date_recorded=date_recorded,
                        defaults={
                            'price_per_unit': Decimal(str(round(base_price * variation, 2))),
                            'unit': random.choice(units),
                            'quality_grade': random.choice(['Grade A', 'Grade B', 'Standard']),
                            'supply_level': random.choice(['High', 'Medium', 'Low']),
                            'demand_level': random.choice(['High', 'Medium', 'Low']),
                            'price_trend': random.choice(['Rising', 'Stable', 'Falling']),
                            'source': random.choice(['Market Survey', 'County Agriculture Office', 'Cooperative']),
                        }
                    )
                    price_count += 1
        
        self.stdout.write(f'✓ Seeded {price_count} market price records')