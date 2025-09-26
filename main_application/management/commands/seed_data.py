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
from main_application.models import *  # Adjust import path based on your app structure


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
        self.seed_user_profiles()
        self.seed_farmer_profiles()
        self.seed_buyer_profiles()
        self.seed_farms()
        self.seed_crop_categories()
        self.seed_crops()
        self.seed_product_units()
        self.seed_products()
        self.seed_product_images()
        self.seed_product_reviews()
        self.seed_wishlists()
        self.seed_carts()
        self.seed_cart_items()
        self.seed_orders()
        self.seed_order_items()
        self.seed_order_status_history()
        self.seed_payment_methods()
        self.seed_payments()
        self.seed_delivery_zones()
        self.seed_delivery_partners()
        self.seed_deliveries()
        self.seed_market_prices()
        self.seed_crop_calendar()
        self.seed_market_demand_forecasts()
        self.seed_input_categories()
        self.seed_input_suppliers()
       
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded database with Kenyan agricultural data!'))

    def clear_data(self):
        """Clear existing data (use with caution)"""
        # Clear in reverse dependency order
        models_to_clear = [
            SystemConfiguration, AuditLog, AppVersion, MobileDevice,
            SchemeApplication, GovernmentScheme, TrainingEnrollment,
            TrainingSession, TrainingCourse, TrainingProvider,
            QualityInspection, QualityInspector, QualityStandard,
            StorageBooking, Warehouse, InsuranceClaim, InsurancePolicy,
            InsuranceProduct, InsuranceProvider, LoanApplication,
            LoanProduct, FinancialInstitution, CooperativeMembership,
            Cooperative, ConsultationRequest, Advisory, ExtensionAgent,
            AgriculturalInput, InputSupplier, InputCategory,
            MarketDemandForecast, CropCalendar, MarketPrice,
            Delivery, DeliveryPartner, DeliveryZone, Payment,
            PaymentMethod, OrderStatusHistory, OrderItem, Order,
            CartItem, Cart, Wishlist, ProductReview, ProductImage,
            Product, Farm, FarmerProfile, BuyerProfile, Location,
            UserProfile, CustomUser, Crop, CropCategory, ProductUnit,
            Ward, SubCounty, County,
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
            {'name': 'Mombasa', 'code': '002', 'population': 1208333, 'area_sq_km': 295.0},
            {'name': 'Kwale', 'code': '003', 'population': 866820, 'area_sq_km': 8270.0},
            {'name': 'Kilifi', 'code': '004', 'population': 1453787, 'area_sq_km': 12246.0},
            {'name': 'Tana River', 'code': '005', 'population': 315943, 'area_sq_km': 38437.0},
            {'name': 'Lamu', 'code': '006', 'population': 143920, 'area_sq_km': 6273.0},
            {'name': 'Taita Taveta', 'code': '007', 'population': 340671, 'area_sq_km': 17084.0},
            {'name': 'Garissa', 'code': '008', 'population': 841353, 'area_sq_km': 45720.0},
            {'name': 'Wajir', 'code': '009', 'population': 781263, 'area_sq_km': 56501.0},
            {'name': 'Mandera', 'code': '010', 'population': 1025756, 'area_sq_km': 26465.0},
            {'name': 'Marsabit', 'code': '011', 'population': 459785, 'area_sq_km': 66923.0},
            {'name': 'Isiolo', 'code': '012', 'population': 268002, 'area_sq_km': 25336.0},
            {'name': 'Meru', 'code': '013', 'population': 1545714, 'area_sq_km': 6930.0},
            {'name': 'Tharaka Nithi', 'code': '014', 'population': 393177, 'area_sq_km': 2609.0},
            {'name': 'Embu', 'code': '015', 'population': 608599, 'area_sq_km': 2821.0},
            {'name': 'Kitui', 'code': '016', 'population': 1136187, 'area_sq_km': 24385.0},
            {'name': 'Machakos', 'code': '017', 'population': 1421932, 'area_sq_km': 6208.0},
            {'name': 'Makueni', 'code': '018', 'population': 987653, 'area_sq_km': 8008.0},
            {'name': 'Nyandarua', 'code': '019', 'population': 596268, 'area_sq_km': 3304.0},
            {'name': 'Nyeri', 'code': '020', 'population': 759164, 'area_sq_km': 3356.0},
            {'name': 'Kirinyaga', 'code': '021', 'population': 610411, 'area_sq_km': 1478.0},
            {'name': 'Murang\'a', 'code': '022', 'population': 1056640, 'area_sq_km': 2325.0},
            {'name': 'Kiambu', 'code': '023', 'population': 2417735, 'area_sq_km': 2449.0},
            {'name': 'Turkana', 'code': '024', 'population': 926976, 'area_sq_km': 77000.0},
            {'name': 'West Pokot', 'code': '025', 'population': 621241, 'area_sq_km': 9169.0},
            {'name': 'Samburu', 'code': '026', 'population': 310327, 'area_sq_km': 20182.0},
            {'name': 'Trans Nzoia', 'code': '027', 'population': 990341, 'area_sq_km': 2469.0},
            {'name': 'Uasin Gishu', 'code': '028', 'population': 1163186, 'area_sq_km': 3345.0},
            {'name': 'Elgeyo Marakwet', 'code': '029', 'population': 454480, 'area_sq_km': 3049.0},
            {'name': 'Nandi', 'code': '030', 'population': 885711, 'area_sq_km': 2884.0},
            {'name': 'Baringo', 'code': '031', 'population': 666763, 'area_sq_km': 11075.0},
            {'name': 'Laikipia', 'code': '032', 'population': 518560, 'area_sq_km': 9229.0},
            {'name': 'Nakuru', 'code': '033', 'population': 2162202, 'area_sq_km': 7496.0},
            {'name': 'Narok', 'code': '034', 'population': 1157873, 'area_sq_km': 17921.0},
            {'name': 'Kajiado', 'code': '035', 'population': 1117840, 'area_sq_km': 21903.0},
            {'name': 'Kericho', 'code': '036', 'population': 901777, 'area_sq_km': 2454.0},
            {'name': 'Bomet', 'code': '037', 'population': 875689, 'area_sq_km': 1882.0},
            {'name': 'Kakamega', 'code': '038', 'population': 1867579, 'area_sq_km': 3033.0},
            {'name': 'Vihiga', 'code': '039', 'population': 590013, 'area_sq_km': 531.0},
            {'name': 'Bungoma', 'code': '040', 'population': 1670570, 'area_sq_km': 2069.0},
            {'name': 'Busia', 'code': '041', 'population': 893681, 'area_sq_km': 1691.0},
            {'name': 'Siaya', 'code': '042', 'population': 993183, 'area_sq_km': 2530.0},
            {'name': 'Kisumu', 'code': '043', 'population': 1155574, 'area_sq_km': 2009.0},
            {'name': 'Homa Bay', 'code': '044', 'population': 1131950, 'area_sq_km': 3154.0},
            {'name': 'Migori', 'code': '045', 'population': 1116436, 'area_sq_km': 2586.0},
            {'name': 'Kisii', 'code': '046', 'population': 1266860, 'area_sq_km': 649.0},
            {'name': 'Nyamira', 'code': '047', 'population': 605576, 'area_sq_km': 899.0},
        ]
        
        for county_data in counties_data:
            County.objects.get_or_create(
                code=county_data['code'],
                defaults=county_data
            )
        
        self.stdout.write('Seeded counties')

    def seed_subcounties(self):
        """Seed sub-counties for selected counties"""
        subcounties_data = [
            # Nairobi
            {'county_code': '001', 'name': 'Westlands', 'code': '001001'},
            {'county_code': '001', 'name': 'Dagoretti North', 'code': '001002'},
            {'county_code': '001', 'name': 'Dagoretti South', 'code': '001003'},
            {'county_code': '001', 'name': 'Langata', 'code': '001004'},
            {'county_code': '001', 'name': 'Kibra', 'code': '001005'},
            {'county_code': '001', 'name': 'Roysambu', 'code': '001006'},
            {'county_code': '001', 'name': 'Kasarani', 'code': '001007'},
            {'county_code': '001', 'name': 'Ruaraka', 'code': '001008'},
            {'county_code': '001', 'name': 'Embakasi South', 'code': '001009'},
            {'county_code': '001', 'name': 'Embakasi North', 'code': '001010'},
            {'county_code': '001', 'name': 'Embakasi Central', 'code': '001011'},
            {'county_code': '001', 'name': 'Embakasi East', 'code': '001012'},
            {'county_code': '001', 'name': 'Embakasi West', 'code': '001013'},
            {'county_code': '001', 'name': 'Makadara', 'code': '001014'},
            {'county_code': '001', 'name': 'Kamukunji', 'code': '001015'},
            {'county_code': '001', 'name': 'Starehe', 'code': '001016'},
            {'county_code': '001', 'name': 'Mathare', 'code': '001017'},
            
            # Kiambu
            {'county_code': '023', 'name': 'Thika Town', 'code': '023001'},
            {'county_code': '023', 'name': 'Juja', 'code': '023002'},
            {'county_code': '023', 'name': 'Gatundu South', 'code': '023003'},
            {'county_code': '023', 'name': 'Gatundu North', 'code': '023004'},
            {'county_code': '023', 'name': 'Ruiru', 'code': '023005'},
            {'county_code': '023', 'name': 'Githunguri', 'code': '023006'},
            {'county_code': '023', 'name': 'Kiambu Town', 'code': '023007'},
            {'county_code': '023', 'name': 'Kiambaa', 'code': '023008'},
            {'county_code': '023', 'name': 'Kabete', 'code': '023009'},
            {'county_code': '023', 'name': 'Kikuyu', 'code': '023010'},
            {'county_code': '023', 'name': 'Limuru', 'code': '023011'},
            {'county_code': '023', 'name': 'Lari', 'code': '023012'},
            
            # Murang'a
            {'county_code': '022', 'name': 'Kangema', 'code': '022001'},
            {'county_code': '022', 'name': 'Mathioya', 'code': '022002'},
            {'county_code': '022', 'name': 'Kiharu', 'code': '022003'},
            {'county_code': '022', 'name': 'Kigumo', 'code': '022004'},
            {'county_code': '022', 'name': 'Maragwa', 'code': '022005'},
            {'county_code': '022', 'name': 'Kandara', 'code': '022006'},
            {'county_code': '022', 'name': 'Gatanga', 'code': '022007'},
        ]
        
        for subcounty_data in subcounties_data:
            county = County.objects.get(code=subcounty_data['county_code'])
            SubCounty.objects.get_or_create(
                county=county,
                code=subcounty_data['code'],
                defaults={'name': subcounty_data['name']}
            )
        
        self.stdout.write('Seeded sub-counties')

    def seed_wards(self):
        """Seed wards for selected sub-counties"""
        wards_data = [
            # Thika Town Sub-county
            {'subcounty_code': '023001', 'name': 'Township', 'code': '023001001'},
            {'subcounty_code': '023001', 'name': 'Kamenu', 'code': '023001002'},
            {'subcounty_code': '023001', 'name': 'Hospital', 'code': '023001003'},
            {'subcounty_code': '023001', 'name': 'Gatuanyaga', 'code': '023001004'},
            {'subcounty_code': '023001', 'name': 'Ngoliba', 'code': '023001005'},
            
            # Kangema Sub-county
            {'subcounty_code': '022001', 'name': 'Kangema', 'code': '022001001'},
            {'subcounty_code': '022001', 'name': 'Muguru', 'code': '022001002'},
            {'subcounty_code': '022001', 'name': 'Rwathia', 'code': '022001003'},
            
            # Westlands Sub-county
            {'subcounty_code': '001001', 'name': 'Kitisuru', 'code': '001001001'},
            {'subcounty_code': '001001', 'name': 'Parklands/Highridge', 'code': '001001002'},
            {'subcounty_code': '001001', 'name': 'Karura', 'code': '001001003'},
            {'subcounty_code': '001001', 'name': 'Kangemi', 'code': '001001004'},
            {'subcounty_code': '001001', 'name': 'Mountain View', 'code': '001001005'},
        ]
        
        for ward_data in wards_data:
            subcounty = SubCounty.objects.get(code=ward_data['subcounty_code'])
            Ward.objects.get_or_create(
                subcounty=subcounty,
                code=ward_data['code'],
                defaults={'name': ward_data['name']}
            )
        
        self.stdout.write('Seeded wards')

    def seed_users(self):
        """Seed users with different types"""
        users_data = [
            {
                'username': 'john_farmer',
                'first_name': 'John',
                'last_name': 'Mwangi',
                'email': 'john.mwangi@farmer.ke',
                'phone_number': '+254712345678',
                'user_type': 'farmer',
                'national_id': '12345678',
                'is_verified': True,
            },
            {
                'username': 'mary_farmer',
                'first_name': 'Mary',
                'last_name': 'Wanjiku',
                'email': 'mary.wanjiku@farmer.ke',
                'phone_number': '+254723456789',
                'user_type': 'farmer',
                'national_id': '23456789',
                'is_verified': True,
            },
            {
                'username': 'peter_buyer',
                'first_name': 'Peter',
                'last_name': 'Kamau',
                'email': 'peter.kamau@buyer.ke',
                'phone_number': '+254734567890',
                'user_type': 'buyer',
                'national_id': '34567890',
                'is_verified': True,
            },
            {
                'username': 'sarah_buyer',
                'first_name': 'Sarah',
                'last_name': 'Njoki',
                'email': 'sarah.njoki@buyer.ke',
                'phone_number': '+254745678901',
                'user_type': 'buyer',
                'national_id': '45678901',
                'is_verified': True,
            },
            {
                'username': 'agent_james',
                'first_name': 'James',
                'last_name': 'Kinyua',
                'email': 'james.kinyua@extension.ke',
                'phone_number': '+254756789012',
                'user_type': 'agent',
                'national_id': '56789012',
                'is_verified': True,
            },
            {
                'username': 'supplier_grace',
                'first_name': 'Grace',
                'last_name': 'Wangui',
                'email': 'grace.wangui@supplier.ke',
                'phone_number': '+254767890123',
                'user_type': 'supplier',
                'national_id': '67890123',
                'is_verified': True,
            },
            {
                'username': 'admin_david',
                'first_name': 'David',
                'last_name': 'Kiprotich',
                'email': 'david.kiprotich@admin.ke',
                'phone_number': '+254778901234',
                'user_type': 'admin',
                'national_id': '78901234',
                'is_verified': True,
                'is_staff': True,
                'is_superuser': True,
            },
        ]
        
        for user_data in users_data:
            user_data['password'] = make_password('password123')
            user_data['date_of_birth'] = date(1985, random.randint(1, 12), random.randint(1, 28))
            CustomUser.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
        
        self.stdout.write('Seeded users')

    def seed_locations(self):
        """Seed locations for users"""
        users = CustomUser.objects.all()[:5]  # First 5 users
        counties = County.objects.filter(code__in=['001', '022', '023'])
        
        location_names = ['Home', 'Farm', 'Office', 'Warehouse', 'Market']
        villages = ['Kiambu Road', 'Thika Road', 'Ruiru Town', 'Kangema Center', 'Westlands']
        
        for i, user in enumerate(users):
            county = counties[i % len(counties)]
            subcounty = county.subcounties.first()
            ward = subcounty.wards.first() if subcounty else None
            
            if ward:
                Location.objects.get_or_create(
                    user=user,
                    name=location_names[i % len(location_names)],
                    defaults={
                        'county': county,
                        'subcounty': subcounty,
                        'ward': ward,
                        'village': villages[i % len(villages)],
                        'detailed_address': f'Plot {random.randint(1, 100)}, {villages[i % len(villages)]}',
                        'latitude': Decimal(str(-1.0 + random.uniform(-0.5, 0.5))),
                        'longitude': Decimal(str(37.0 + random.uniform(-0.5, 0.5))),
                        'is_default': True,
                    }
                )
        
        self.stdout.write('Seeded locations')

    def seed_user_profiles(self):
        """Seed user profiles"""
        users = CustomUser.objects.all()
        
        for user in users:
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': f'Agricultural enthusiast from {user.last_name} family',
                    'preferred_language': 'en',
                    'notification_preferences': {
                        'email': True,
                        'sms': True,
                        'push': True,
                        'market_updates': True,
                        'weather_alerts': True,
                    },
                    'privacy_settings': {
                        'show_phone': True,
                        'show_location': False,
                        'allow_messages': True,
                    }
                }
            )
        
        self.stdout.write('Seeded user profiles')

    def seed_farmer_profiles(self):
        """Seed farmer profiles"""
        farmer_users = CustomUser.objects.filter(user_type='farmer')
        
        farming_types = ['crop', 'mixed', 'horticulture']
        experience_levels = ['intermediate', 'experienced', 'expert']
        
        for i, user in enumerate(farmer_users):
            FarmerProfile.objects.get_or_create(
                user=user,
                defaults={
                    'farm_name': f'{user.first_name} {user.last_name} Farm',
                    'farming_type': farming_types[i % len(farming_types)],
                    'years_of_experience': experience_levels[i % len(experience_levels)],
                    'total_farm_size': Decimal(str(random.uniform(0.5, 10.0))),
                    'farming_methods': ['organic', 'conventional'][i % 2:i % 2 + 1],
                    'certifications': ['GAP', 'Organic'][i % 2:i % 2 + 1],
                    'bank_account_number': f'12345678{i:02d}',
                    'bank_name': ['KCB Bank', 'Equity Bank', 'Cooperative Bank'][i % 3],
                    'mpesa_number': user.phone_number,
                    'is_cooperative_member': i % 2 == 0,
                    'cooperative_name': 'Murang\'a Coffee Cooperative' if i % 2 == 0 else '',
                }
            )
        
        self.stdout.write('Seeded farmer profiles')

    def seed_buyer_profiles(self):
        """Seed buyer profiles"""
        buyer_users = CustomUser.objects.filter(user_type='buyer')
        
        buyer_types = ['individual', 'restaurant', 'retailer']
        
        for i, user in enumerate(buyer_users):
            BuyerProfile.objects.get_or_create(
                user=user,
                defaults={
                    'buyer_type': buyer_types[i % len(buyer_types)],
                    'business_name': f'{user.first_name}\'s {buyer_types[i % len(buyer_types)].title()}' if buyer_types[i % len(buyer_types)] != 'individual' else '',
                    'business_registration': f'BZ{random.randint(1000, 9999)}' if buyer_types[i % len(buyer_types)] != 'individual' else '',
                    'tax_pin': f'P{random.randint(100000000, 999999999)}' if buyer_types[i % len(buyer_types)] != 'individual' else '',
                    'preferred_payment_method': 'mpesa',
                    'credit_limit': Decimal(str(random.uniform(10000, 100000))),
                    'delivery_instructions': 'Call before delivery',
                }
            )
        
        self.stdout.write('Seeded buyer profiles')

    def seed_farms(self):
        """Seed farms for farmers"""
        farmer_profiles = FarmerProfile.objects.all()
        
        for i, farmer in enumerate(farmer_profiles):
            user_location = farmer.user.locations.first()
            if user_location:
                Farm.objects.get_or_create(
                    farmer=farmer,
                    name=f'{farmer.farm_name} Plot {i+1}',
                    defaults={
                        'location': user_location,
                        'size': Decimal(str(random.uniform(0.25, 5.0))),
                        'soil_type': ['Clay', 'Loam', 'Sandy'][i % 3],
                        'water_source': ['Borehole', 'River', 'Rain'][i % 3],
                        'irrigation_method': ['Drip', 'Sprinkler', 'Furrow'][i % 3],
                        'elevation': random.randint(1200, 2000),
                        'description': f'A productive farm in {user_location.county.name}',
                        'photos': ['farm1.jpg', 'farm2.jpg'],
                    }
                )
        
        self.stdout.write('Seeded farms')

    def seed_crop_categories(self):
        """Seed crop categories"""
        categories_data = [
            {'name': 'cereals', 'description': 'Cereal crops like maize, wheat, rice'},
            {'name': 'legumes', 'description': 'Legume crops like beans, peas, groundnuts'},
            {'name': 'vegetables', 'description': 'Vegetable crops like tomatoes, onions, cabbages'},
            {'name': 'fruits', 'description': 'Fruit crops like mangoes, oranges, bananas'},
            {'name': 'cash-crops', 'description': 'Cash crops like coffee, tea, sugarcane'},
            {'name': 'roots-tubers', 'description': 'Root and tuber crops like potatoes, cassava'},
        ]
        
        for category_data in categories_data:
            CropCategory.objects.get_or_create(
                name=category_data['name'],
                defaults=category_data
            )
        
        self.stdout.write('Seeded crop categories')

    def seed_crops(self):
        """Seed common Kenyan crops"""
        categories = CropCategory.objects.all()
        
        crops_data = [
            {
                'name': 'maize',
                'scientific_name': 'Zea mays',
                'category': 'cereals',
                'variety': 'H614',
                'growing_season': 'Long rains (March-July)',
                'maturity_period_days': 120,
                'ideal_temperature_min': 18.0,
                'ideal_temperature_max': 27.0,
                'ideal_rainfall': 500.0,
                'storage_requirements': 'Dry, well-ventilated storage',
            },
            {
                'name': 'beans',
                'scientific_name': 'Phaseolus vulgaris',
                'category': 'legumes',
                'variety': 'Rosecoco',
                'growing_season': 'Long & Short rains',
                'maturity_period_days': 90,
                'ideal_temperature_min': 15.0,
                'ideal_temperature_max': 25.0,
                'ideal_rainfall': 400.0,
                'storage_requirements': 'Cool, dry place',
            },
            {
                'name': 'coffee',
                'scientific_name': 'Coffea arabica',
                'category': 'cash-crops',
                'variety': 'SL28',
                'growing_season': 'Year-round',
                'maturity_period_days': 365,
                'ideal_temperature_min': 15.0,
                'ideal_temperature_max': 24.0,
                'ideal_rainfall': 1500.0,
                'storage_requirements': 'Proper drying and storage',
            },
            {
                'name': 'tomatoes',
                'scientific_name': 'Solanum lycopersicum',
                'category': 'vegetables',
                'variety': 'Anna F1',
                'growing_season': 'Year-round with irrigation',
                'maturity_period_days': 75,
                'ideal_temperature_min': 18.0,
                'ideal_temperature_max': 29.0,
                'ideal_rainfall': 600.0,
                'storage_requirements': 'Cool, humid conditions',
            },
            {
                'name': 'potatoes',
                'scientific_name': 'Solanum tuberosum',
                'category': 'roots-tubers',
                'variety': 'Shangi',
                'growing_season': 'Long rains',
                'maturity_period_days': 100,
                'ideal_temperature_min': 15.0,
                'ideal_temperature_max': 20.0,
                'ideal_rainfall': 500.0,
                'storage_requirements': 'Cool, dark, ventilated',
            },
            {
                'name': 'bananas',
                'scientific_name': 'Musa acuminata',
                'category': 'fruits',
                'variety': 'Cavendish',
                'growing_season': 'Year-round',
                'maturity_period_days': 270,
                'ideal_temperature_min': 26.0,
                'ideal_temperature_max': 30.0,
                'ideal_rainfall': 1200.0,
                'storage_requirements': 'Room temperature until ripe',
            },
        ]
        
        for crop_data in crops_data:
            category_name = crop_data.pop('category')
            category = categories.get(name=category_name)
            Crop.objects.get_or_create(
                name=crop_data['name'],
                defaults={**crop_data, 'category': category}
            )
        
        self.stdout.write('Seeded crops')

    def seed_product_units(self):
        """Seed product units"""
        units_data = [
            {'name': 'Kilogram', 'abbreviation': 'kg', 'conversion_factor': Decimal('1.0')},
            {'name': 'Gram', 'abbreviation': 'g', 'conversion_factor': Decimal('0.001')},
            {'name': 'Tonne', 'abbreviation': 't', 'conversion_factor': Decimal('1000.0')},
            {'name': 'Bag (90kg)', 'abbreviation': 'bag', 'conversion_factor': Decimal('90.0')},
            {'name': 'Crate', 'abbreviation': 'crate', 'conversion_factor': Decimal('10.0')},
            {'name': 'Piece', 'abbreviation': 'pc', 'conversion_factor': Decimal('0.5')},
            {'name': 'Bunch', 'abbreviation': 'bunch', 'conversion_factor': Decimal('2.0')},
            {'name': 'Liter', 'abbreviation': 'l', 'conversion_factor': Decimal('1.0')},
        ]
        
        kg_unit = None
        for unit_data in units_data:
            unit, created = ProductUnit.objects.get_or_create(
                abbreviation=unit_data['abbreviation'],
                defaults=unit_data
            )
            if unit_data['abbreviation'] == 'kg':
                kg_unit = unit
        
        # Set base unit for other units
        if kg_unit:
            ProductUnit.objects.filter(abbreviation__in=['g', 't', 'bag']).update(base_unit=kg_unit)
        
        self.stdout.write('Seeded product units')

    def seed_products(self):
        """Seed products from farmers"""
        farmer_profiles = FarmerProfile.objects.all()
        crops = Crop.objects.all()
        units = ProductUnit.objects.all()
        
        product_names = {
            'maize': ['Fresh Maize Cobs', 'Dry Maize Grain', 'Maize Flour'],
            'beans': ['Fresh Beans', 'Dry Beans', 'Bean Flour'],
            'coffee': ['Coffee Cherries', 'Coffee Beans', 'Roasted Coffee'],
            'tomatoes': ['Fresh Tomatoes', 'Cherry Tomatoes', 'Roma Tomatoes'],
            'potatoes': ['Fresh Potatoes', 'Seed Potatoes', 'Baby Potatoes'],
            'bananas': ['Sweet Bananas', 'Cooking Bananas', 'Banana Bunch'],
        }
        
        for farmer in farmer_profiles:
            farm = farmer.farms.first()
            if farm:
                # Create 2-3 products per farmer
                farmer_crops = random.sample(list(crops), min(3, len(crops)))
                
                for i, crop in enumerate(farmer_crops):
                    crop_products = product_names.get(crop.name, [f'{crop.name} Product'])
                    product_name = random.choice(crop_products)
                    
                    unit = random.choice(units)
                    harvest_date = timezone.now().date() - timedelta(days=random.randint(1, 30))
                    
                    Product.objects.get_or_create(
                        farmer=farmer,
                        crop=crop,
                        farm=farm,
                        name=f"{product_name} - {farmer.user.first_name}",
                        defaults={
                            'description': f'High quality {crop.name} from {farm.name}. Grown using sustainable farming methods.',
                            'quantity_available': Decimal(str(random.uniform(10, 500))),
                            'unit': unit,
                            'price_per_unit': Decimal(str(random.uniform(50, 300))),
                            'minimum_order': Decimal(str(random.uniform(1, 10))),
                            'quality_grade': random.choice(['premium', 'grade_a', 'standard']),
                            'harvest_date': harvest_date,
                            'expiry_date': harvest_date + timedelta(days=random.randint(30, 365)),
                            'organic_certified': i % 2 == 0,
                            'certification_body': 'Kenya Organic Agriculture Network' if i % 2 == 0 else '',
                            'storage_condition': 'Cool, dry place',
                            'packaging_options': ['25kg bags', '50kg bags', 'bulk'],
                            'images': [f'{crop.name}1.jpg', f'{crop.name}2.jpg'],
                            'status': 'active',
                            'featured': i == 0,
                            'views_count': random.randint(10, 100),
                            'likes_count': random.randint(1, 20),
                        }
                    )
        
        self.stdout.write('Seeded products')

    def seed_product_images(self):
        """Seed product images"""
        products = Product.objects.all()
        
        for i, product in enumerate(products[:5]):  # First 5 products
            ProductImage.objects.get_or_create(
                product=product,
                image=f'products/{product.crop.name}_{i+1}.jpg',
                defaults={
                    'caption': f'{product.name} main image',
                    'is_primary': True,
                    'order': 1,
                }
            )
        
        self.stdout.write('Seeded product images')

    def seed_product_reviews(self):
        """Seed product reviews"""
        products = Product.objects.all()[:3]  # First 3 products
        buyer_users = CustomUser.objects.filter(user_type='buyer')
        
        for product in products:
            for i, buyer in enumerate(buyer_users[:2]):  # 2 reviews per product
                ProductReview.objects.get_or_create(
                    product=product,
                    buyer=buyer,
                    defaults={
                        'rating': random.randint(3, 5),
                        'title': f'Great {product.crop.name}!',
                        'comment': f'Excellent quality {product.crop.name} from {product.farmer.user.first_name}. Will definitely order again.',
                        'is_verified_purchase': True,
                        'helpful_votes': random.randint(0, 5),
                    }
                )
        
        self.stdout.write('Seeded product reviews')

    def seed_wishlists(self):
        """Seed buyer wishlists"""
        buyer_users = CustomUser.objects.filter(user_type='buyer')
        products = Product.objects.all()
        
        for buyer in buyer_users:
            # Each buyer wishlists 2-3 random products
            wishlist_products = random.sample(list(products), min(3, len(products)))
            for product in wishlist_products:
                Wishlist.objects.get_or_create(
                    buyer=buyer,
                    product=product
                )
        
        self.stdout.write('Seeded wishlists')

    def seed_carts(self):
        """Seed shopping carts"""
        buyer_users = CustomUser.objects.filter(user_type='buyer')
        
        for buyer in buyer_users:
            Cart.objects.get_or_create(buyer=buyer)
        
        self.stdout.write('Seeded carts')

    def seed_cart_items(self):
        """Seed cart items"""
        carts = Cart.objects.all()
        products = Product.objects.all()
        
        for cart in carts:
            # Add 1-2 items to each cart
            cart_products = random.sample(list(products), min(2, len(products)))
            for product in cart_products:
                quantity = Decimal(str(random.uniform(1, 10)))
                unit_price = product.price_per_unit
                
                CartItem.objects.get_or_create(
                    cart=cart,
                    product=product,
                    defaults={
                        'quantity': quantity,
                        'unit_price': unit_price,
                        'total_price': quantity * unit_price,
                        'notes': 'Please pack carefully',
                    }
                )
        
        self.stdout.write('Seeded cart items')

    def seed_orders(self):
        """Seed orders"""
        buyer_users = CustomUser.objects.filter(user_type='buyer')
        farmer_profiles = FarmerProfile.objects.all()
        
        for i, buyer in enumerate(buyer_users):
            buyer_location = buyer.locations.first()
            farmer = farmer_profiles[i % len(farmer_profiles)]
            
            if buyer_location:
                order_date = timezone.now() - timedelta(days=random.randint(1, 30))
                subtotal = Decimal(str(random.uniform(1000, 10000)))
                delivery_fee = Decimal('200.00')
                tax_amount = subtotal * Decimal('0.16')  # 16% VAT
                total_amount = subtotal + delivery_fee + tax_amount
                
                Order.objects.get_or_create(
                    order_number=f'ORD{random.randint(10000, 99999)}',
                    defaults={
                        'buyer': buyer,
                        'farmer': farmer,
                        'delivery_location': buyer_location,
                        'order_date': order_date,
                        'expected_delivery_date': order_date + timedelta(days=random.randint(1, 7)),
                        'status': random.choice(['pending', 'confirmed', 'processing', 'delivered']),
                        'payment_status': random.choice(['pending', 'paid']),
                        'subtotal': subtotal,
                        'delivery_fee': delivery_fee,
                        'tax_amount': tax_amount,
                        'total_amount': total_amount,
                        'special_instructions': 'Handle with care',
                    }
                )
        
        self.stdout.write('Seeded orders')

    def seed_order_items(self):
        """Seed order items"""
        orders = Order.objects.all()
        products = Product.objects.all()
        
        for order in orders:
            # Add 1-3 items per order
            order_products = random.sample(list(products), min(3, len(products)))
            for product in order_products:
                quantity = Decimal(str(random.uniform(1, 20)))
                unit_price = product.price_per_unit
                
                OrderItem.objects.get_or_create(
                    order=order,
                    product=product,
                    defaults={
                        'quantity': quantity,
                        'unit_price': unit_price,
                        'total_price': quantity * unit_price,
                        'product_snapshot': {
                            'name': product.name,
                            'crop': product.crop.name,
                            'quality_grade': product.quality_grade,
                        }
                    }
                )
        
        self.stdout.write('Seeded order items')

    def seed_order_status_history(self):
        """Seed order status history"""
        orders = Order.objects.all()
        admin_user = CustomUser.objects.filter(user_type='admin').first()
        
        if admin_user:
            for order in orders:
                OrderStatusHistory.objects.get_or_create(
                    order=order,
                    new_status=order.status,
                    defaults={
                        'previous_status': 'pending',
                        'changed_by': admin_user,
                        'notes': f'Order status updated to {order.status}',
                    }
                )
        
        self.stdout.write('Seeded order status history')

    def seed_payment_methods(self):
        """Seed payment methods"""
        methods_data = [
            {
                'name': 'M-Pesa',
                'code': 'MPESA',
                'description': 'Mobile money payment via Safaricom M-Pesa',
                'processing_fee_percentage': Decimal('0.02'),
                'minimum_amount': Decimal('10.00'),
                'maximum_amount': Decimal('300000.00'),
            },
            {
                'name': 'Airtel Money',
                'code': 'AIRTEL',
                'description': 'Mobile money payment via Airtel Money',
                'processing_fee_percentage': Decimal('0.02'),
                'minimum_amount': Decimal('10.00'),
                'maximum_amount': Decimal('200000.00'),
            },
            {
                'name': 'Bank Transfer',
                'code': 'BANK',
                'description': 'Direct bank transfer',
                'processing_fee_percentage': Decimal('0.01'),
                'minimum_amount': Decimal('100.00'),
                'maximum_amount': Decimal('1000000.00'),
            },
            {
                'name': 'Cash on Delivery',
                'code': 'COD',
                'description': 'Pay cash upon delivery',
                'processing_fee_percentage': Decimal('0.00'),
                'minimum_amount': Decimal('50.00'),
                'maximum_amount': Decimal('50000.00'),
            },
        ]
        
        for method_data in methods_data:
            PaymentMethod.objects.get_or_create(
                code=method_data['code'],
                defaults=method_data
            )
        
        self.stdout.write('Seeded payment methods')

    def seed_payments(self):
        """Seed payments"""
        orders = Order.objects.all()
        payment_methods = PaymentMethod.objects.all()
        
        for order in orders:
            if order.payment_status == 'paid':
                payment_method = random.choice(payment_methods)
                processing_fee = order.total_amount * payment_method.processing_fee_percentage
                
                Payment.objects.get_or_create(
                    transaction_id=f'TXN{random.randint(100000, 999999)}',
                    defaults={
                        'order': order,
                        'payment_method': payment_method,
                        'amount': order.total_amount,
                        'processing_fee': processing_fee,
                        'net_amount': order.total_amount - processing_fee,
                        'status': 'completed',
                        'gateway_reference': f'MPX{random.randint(1000000, 9999999)}',
                        'gateway_response': {'status': 'success', 'message': 'Payment completed'},
                        'paid_at': order.order_date + timedelta(minutes=random.randint(1, 60)),
                    }
                )
        
        self.stdout.write('Seeded payments')

    def seed_delivery_zones(self):
        """Seed delivery zones"""
        counties = County.objects.filter(code__in=['001', '022', '023', '033'])
        
        zones_data = [
            {
                'name': 'Nairobi Metro',
                'description': 'Nairobi and surrounding areas',
                'base_delivery_fee': Decimal('200.00'),
                'free_delivery_threshold': Decimal('5000.00'),
                'estimated_delivery_days': 1,
            },
            {
                'name': 'Central Kenya',
                'description': 'Murang\'a, Kiambu, Nyeri regions',
                'base_delivery_fee': Decimal('300.00'),
                'free_delivery_threshold': Decimal('7000.00'),
                'estimated_delivery_days': 2,
            },
            {
                'name': 'Rift Valley',
                'description': 'Nakuru and surrounding areas',
                'base_delivery_fee': Decimal('400.00'),
                'free_delivery_threshold': Decimal('10000.00'),
                'estimated_delivery_days': 3,
            },
        ]
        
        for i, zone_data in enumerate(zones_data):
            zone, created = DeliveryZone.objects.get_or_create(
                name=zone_data['name'],
                defaults=zone_data
            )
            if created and i < len(counties):
                zone.counties.add(counties[i])
        
        self.stdout.write('Seeded delivery zones')

    def seed_delivery_partners(self):
        """Seed delivery partners"""
        counties = County.objects.all()[:5]
        
        partners_data = [
            {
                'name': 'Swift Delivery Services',
                'contact_person': 'John Mwangi',
                'phone_number': '+254700123456',
                'email': 'info@swiftdelivery.ke',
                'pricing_model': 'Per km + base fee',
                'rating': Decimal('4.5'),
            },
            {
                'name': 'Green Mile Logistics',
                'contact_person': 'Mary Wanjiku',
                'phone_number': '+254700234567',
                'email': 'info@greenmile.ke',
                'pricing_model': 'Flat rate per zone',
                'rating': Decimal('4.2'),
            },
            {
                'name': 'FarmLink Express',
                'contact_person': 'Peter Kamau',
                'phone_number': '+254700345678',
                'email': 'info@farmlink.ke',
                'pricing_model': 'Weight-based pricing',
                'rating': Decimal('4.7'),
            },
        ]
        
        for partner_data in partners_data:
            partner, created = DeliveryPartner.objects.get_or_create(
                name=partner_data['name'],
                defaults=partner_data
            )
            if created:
                partner.service_areas.set(counties)
        
        self.stdout.write('Seeded delivery partners')

    def seed_deliveries(self):
        """Seed deliveries"""
        orders = Order.objects.filter(status__in=['shipped', 'delivered'])
        delivery_partners = DeliveryPartner.objects.all()
        
        for order in orders:
            if not hasattr(order, 'delivery'):
                partner = random.choice(delivery_partners)
                
                pickup_time = order.order_date + timedelta(hours=random.randint(1, 24))
                delivery_time = pickup_time + timedelta(hours=random.randint(2, 48)) if order.status == 'delivered' else None
                
                Delivery.objects.get_or_create(
                    order=order,
                    defaults={
                        'delivery_partner': partner,
                        'driver_name': f'Driver {random.randint(1, 10)}',
                        'driver_phone': f'+25470012345{random.randint(0, 9)}',
                        'vehicle_details': f'KCA {random.randint(100, 999)}X',
                        'pickup_address': f'{order.farmer.user.first_name}\'s Farm',
                        'delivery_address': order.delivery_location.detailed_address,
                        'status': 'delivered' if order.status == 'delivered' else 'in_transit',
                        'estimated_delivery_time': pickup_time + timedelta(hours=24),
                        'actual_pickup_time': pickup_time,
                        'actual_delivery_time': delivery_time,
                        'delivery_fee': order.delivery_fee,
                        'tracking_updates': [
                            {'time': pickup_time.isoformat(), 'status': 'picked_up', 'message': 'Package picked up'},
                            {'time': (pickup_time + timedelta(hours=12)).isoformat(), 'status': 'in_transit', 'message': 'In transit'},
                        ] + ([{'time': delivery_time.isoformat(), 'status': 'delivered', 'message': 'Package delivered'}] if delivery_time else []),
                    }
                )
        
        self.stdout.write('Seeded deliveries')

    def seed_market_prices(self):
        """Seed market prices"""
        crops = Crop.objects.all()
        counties = County.objects.all()[:5]
        units = ProductUnit.objects.all()
        
        markets = ['Marikiti Market', 'Kangemi Market', 'Thika Market', 'Nakuru Market', 'Meru Market']
        
        for crop in crops:
            for county in counties:
                unit = random.choice(units)
                price_date = timezone.now().date() - timedelta(days=random.randint(0, 30))
                
                MarketPrice.objects.get_or_create(
                    crop=crop,
                    location=county,
                    date_recorded=price_date,
                    defaults={
                        'market_name': random.choice(markets),
                        'price_per_unit': Decimal(str(random.uniform(30, 200))),
                        'unit': unit,
                        'quality_grade': random.choice(['Premium', 'Grade A', 'Standard']),
                        'supply_level': random.choice(['High', 'Medium', 'Low']),
                        'demand_level': random.choice(['High', 'Medium', 'Low']),
                        'price_trend': random.choice(['Rising', 'Stable', 'Falling']),
                        'source': 'Ministry of Agriculture',
                        'notes': f'{crop.name} prices in {county.name}',
                    }
                )
        
        self.stdout.write('Seeded market prices')

    def seed_crop_calendar(self):
        """Seed crop calendar"""
        crops = Crop.objects.all()
        counties = County.objects.all()[:3]
        
        calendar_data = {
            'maize': {
                'planting_season_start': 'March',
                'planting_season_end': 'April',
                'harvesting_season_start': 'July',
                'harvesting_season_end': 'August',
                'recommended_varieties': 'H614, H629, DH04',
            },
            'beans': {
                'planting_season_start': 'March',
                'planting_season_end': 'May',
                'harvesting_season_start': 'June',
                'harvesting_season_end': 'July',
                'recommended_varieties': 'Rosecoco, Canadian Wonder, Mwitemania',
            },
            'coffee': {
                'planting_season_start': 'October',
                'planting_season_end': 'December',
                'harvesting_season_start': 'October',
                'harvesting_season_end': 'February',
                'recommended_varieties': 'SL28, SL34, K7',
            },
        }
        
        for crop in crops:
            if crop.name in calendar_data:
                for county in counties:
                    data = calendar_data[crop.name]
                    CropCalendar.objects.get_or_create(
                        crop=crop,
                        county=county,
                        defaults={
                            **data,
                            'special_notes': f'Best practices for {crop.name} in {county.name}',
                        }
                    )
        
        self.stdout.write('Seeded crop calendar')

    def seed_market_demand_forecasts(self):
        """Seed market demand forecasts"""
        crops = Crop.objects.all()[:3]
        counties = County.objects.all()[:3]
        
        forecast_periods = ['Q1 2025', 'Q2 2025', 'Q3 2025']
        demand_levels = ['high', 'medium', 'low']
        price_predictions = ['rising', 'stable', 'falling']
        
        for crop in crops:
            for county in counties:
                for period in forecast_periods:
                    MarketDemandForecast.objects.get_or_create(
                        crop=crop,
                        location=county,
                        forecast_period=period,
                        defaults={
                            'expected_demand': random.choice(demand_levels),
                            'price_prediction': random.choice(price_predictions),
                            'confidence_level': random.randint(70, 95),
                            'factors': ['Weather patterns', 'Market trends', 'Export demand'],
                            'recommendations': f'Consider increasing {crop.name} production in {county.name}',
                        }
                    )
        
        self.stdout.write('Seeded market demand forecasts')

    def seed_input_categories(self):
        """Seed input categories"""
        categories_data = [
            {'name': 'Seeds', 'description': 'Certified seeds for various crops'},
            {'name': 'Fertilizers', 'description': 'Chemical and organic fertilizers'},
            {'name': 'Pesticides', 'description': 'Crop protection chemicals'},
            {'name': 'Farm Tools', 'description': 'Hand tools and implements'},
            {'name': 'Irrigation', 'description': 'Irrigation equipment and supplies'},
        ]
        
        for category_data in categories_data:
            InputCategory.objects.get_or_create(
                name=category_data['name'],
                defaults=category_data
            )
        
        self.stdout.write('Seeded input categories')

    def seed_input_suppliers(self):
        """Seed input suppliers"""
        supplier_users = CustomUser.objects.filter(user_type='supplier')
        counties = County.objects.all()[:5]
        categories = InputCategory.objects.all()
        
        for supplier_user in supplier_users:
            supplier, created = InputSupplier.objects.get_or_create(
                user=supplier_user,
                defaults={
                    'business_name': f'{supplier_user.first_name}\'s Agro Supplies',
                    'license_number': f'LIC{random.randint(1000, 9999)}',
                    'business_registration': f'REG{random.randint(10000, 99999)}',
                    'delivery_available': True,
                    'credit_terms_available': random.choice([True, False]),
                    'minimum_order_amount': Decimal(str(random.uniform(500, 2000))),
                    'rating': Decimal(str(random.uniform(3.5, 5.0))),
                    'is_verified': True,
                }
            )
            
            if created:
                supplier.specialization.set(categories[:3])
                supplier.service_areas.set(counties)
        
        self.stdout.write('Seeded input suppliers')

    def seed_inputs(self):
        """Seed agricultural inputs"""
        suppliers = InputSupplier.objects.all()
        categories = InputCategory.objects.all()
        units = ProductUnit.objects.all()
        
        inputs_data = [ 
            {
                'name': 'Maize Seeds',
                'category': 'Seeds',
                'description': 'Certified hybrid maize seeds for high yield',
                'brand': 'Pannar',
                'model': 'PAN 53',
                'specifications': 'Drought tolerant, suitable for Kenyan climate',
                'usage_instructions': 'Plant at 90cm spacing, 2-3 seeds per hole',
                'safety_instructions': 'Store in a cool, dry place',
            },
            {
                'name': 'DAP Fertilizer',
                'category': 'Fertilizers',
                'description': 'Diammonium phosphate fertilizer for balanced nutrition',
                'brand': 'Yara',
                'model': 'Yara DAP',
                'specifications': '18-46-0 NPK formulation',
                'usage_instructions': 'Apply at planting time, 200kg/ha',
                'safety_instructions': 'Avoid inhalation, use protective gear',
            },
            {
                'name': 'Glyphosate Herbicide',
                'category': 'Pesticides',
                'description': 'Non-selective herbicide for weed control',
                'brand': 'Roundup',
                'model': 'Roundup UltraMax',
                'specifications': '41% glyphosate concentration',
                'usage_instructions': 'Dilute 1:10 with water, spray on weeds',
                'safety_instructions': 'Wear gloves and mask, avoid contact with skin',
            },
            {
                'name': 'Hand Hoe',
                'category': 'Farm Tools',
                'description': 'Durable hand hoe for weeding and soil preparation',
                'brand': 'Bahco',
                'model': 'Bahco Hoe 3000',
                'specifications': 'Steel blade with wooden handle, 1.2m length',
                'usage_instructions': 'Use for manual weeding and soil aeration',
                'safety_instructions': 'Handle with care to avoid injury',
            },
            {
                'name': 'Drip Irrigation Kit',
                'category': 'Irrigation',
                'description': 'Complete drip irrigation kit for small farms',
                'brand': 'Netafim',
                'model': 'Netafim Drip Kit 100m',
                'specifications': 'Includes tubing, emitters, and connectors',
                'usage_instructions': 'Install tubing along crop rows, connect to water source',
                'safety_instructions': 'Ensure water source is clean to avoid clogging',
            },
        ]

        