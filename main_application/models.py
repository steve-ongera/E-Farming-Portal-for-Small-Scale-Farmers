from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
import uuid


from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
import uuid


# ============== USER MANAGEMENT MODELS ==============

class CustomUser(AbstractUser):
    """Extended user model with additional fields"""
    USER_TYPE_CHOICES = [
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
        ('admin', 'Administrator'),
        ('agent', 'Agricultural Agent'),
        ('supplier', 'Input Supplier'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='buyer')
    phone_number = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    national_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_document = models.FileField(upload_to='verification/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_seen = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'


class UserProfile(models.Model):
    """Additional profile information for users"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    preferred_language = models.CharField(max_length=10, default='en')
    notification_preferences = models.JSONField(default=dict)
    privacy_settings = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'user_profiles'


# ============== LOCATION MODELS ==============

class County(models.Model):
    """Kenyan counties"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    population = models.IntegerField(blank=True, null=True)
    area_sq_km = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

        
    
    def __str__(self):
        return self.name


class SubCounty(models.Model):
    """Sub-counties within counties"""
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name='subcounties')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=15)
    
    class Meta:
        db_table = 'subcounties'
        unique_together = ['county', 'name']
        verbose_name_plural = 'Sub-counties'
    
    def __str__(self):
        return f"{self.name}, {self.county.name}"


class Ward(models.Model):
    """Wards within sub-counties"""
    subcounty = models.ForeignKey(SubCounty, on_delete=models.CASCADE, related_name='wards')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'wards'
        unique_together = ['subcounty', 'name']
    
    def __str__(self):
        return f"{self.name}, {self.subcounty.name}"


class Location(models.Model):
    """Specific location/address"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=100, help_text="e.g., Home, Farm, Office")
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    subcounty = models.ForeignKey(SubCounty, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    village = models.CharField(max_length=100)
    detailed_address = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'locations'


# ============== FARMER-SPECIFIC MODELS ==============

class FarmerProfile(models.Model):
    """Extended profile for farmers"""
    FARMING_TYPE_CHOICES = [
        ('crop', 'Crop Farming'),
        ('livestock', 'Livestock Farming'),
        ('mixed', 'Mixed Farming'),
        ('poultry', 'Poultry Farming'),
        ('fish', 'Fish Farming'),
        ('horticulture', 'Horticulture'),
    ]
    
    EXPERIENCE_CHOICES = [
        ('beginner', '0-2 years'),
        ('intermediate', '3-5 years'),
        ('experienced', '6-10 years'),
        ('expert', '10+ years'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='farmer_profile')
    farm_name = models.CharField(max_length=200)
    farming_type = models.CharField(max_length=20, choices=FARMING_TYPE_CHOICES)
    years_of_experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    total_farm_size = models.DecimalField(max_digits=10, decimal_places=2, help_text="In acres")
    farming_methods = models.JSONField(default=list, help_text="e.g., organic, conventional, etc.")
    certifications = models.JSONField(default=list)
    bank_account_number = models.CharField(max_length=50, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    mpesa_number = models.CharField(max_length=15, blank=True)
    is_cooperative_member = models.BooleanField(default=False)
    cooperative_name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    


from django.db import models
from django.utils.text import slugify


class Farm(models.Model):
    """Individual farms owned by farmers"""
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=200, unique=True)  # enforce uniqueness
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    size = models.DecimalField(max_digits=10, decimal_places=2, help_text="In acres")
    soil_type = models.CharField(max_length=100, blank=True)
    water_source = models.CharField(max_length=100, blank=True)
    irrigation_method = models.CharField(max_length=100, blank=True)
    elevation = models.IntegerField(blank=True, null=True, help_text="In meters above sea level")
    photos = models.JSONField(default=list)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'farms'
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Always slugify the name
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1

        # Ensure uniqueness by checking existing records
        while Farm.objects.filter(name=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        self.name = slug
        super().save(*args, **kwargs)



# ============== CROP AND PRODUCT MODELS ==============
from django.db import models
from django.utils.text import slugify


class CropCategory(models.Model):
    """Categories for different types of crops"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
   
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # slugify the name before saving
        self.name = slugify(self.name)
        super().save(*args, **kwargs)


class Crop(models.Model):
    """Types of crops that can be grown"""
    name = models.CharField(max_length=100, unique=True)
    scientific_name = models.CharField(max_length=150, blank=True)
    category = models.ForeignKey(CropCategory, on_delete=models.CASCADE, related_name='crops')
    variety = models.CharField(max_length=100, blank=True)
    growing_season = models.CharField(max_length=100, blank=True)
    maturity_period_days = models.IntegerField(blank=True, null=True)
    ideal_temperature_min = models.FloatField(blank=True, null=True)
    ideal_temperature_max = models.FloatField(blank=True, null=True)
    ideal_rainfall = models.FloatField(blank=True, null=True)
    storage_requirements = models.TextField(blank=True)
    nutritional_info = models.JSONField(default=dict)
    image = models.ImageField(upload_to='crops/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # slugify the name before saving
        self.name = slugify(self.name)
        super().save(*args, **kwargs)



class ProductUnit(models.Model):
    """Units of measurement for products"""
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)
    base_unit = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    conversion_factor = models.DecimalField(max_digits=10, decimal_places=4, default=1)
    
    class Meta:
        db_table = 'product_units'
    
    def __str__(self):
        return f"{self.name} ({self.abbreviation})"


from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    """Products listed by farmers"""
    QUALITY_CHOICES = [
        ('premium', 'Premium'),
        ('grade_a', 'Grade A'),
        ('grade_b', 'Grade B'),
        ('standard', 'Standard'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('sold_out', 'Sold Out'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='products')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='products')
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)  # 👈 slug field
    description = models.TextField()
    quantity_available = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    quality_grade = models.CharField(max_length=20, choices=QUALITY_CHOICES, default='standard')
    harvest_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    organic_certified = models.BooleanField(default=False)
    certification_body = models.CharField(max_length=100, blank=True)
    storage_condition = models.CharField(max_length=200, blank=True)
    packaging_options = models.JSONField(default=list)
    images = models.JSONField(default=list)
    videos = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
 
    def __str__(self):
        return f"{self.name} - {self.farmer.user.username}"

    def save(self, *args, **kwargs):
        # Generate slug if empty
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)



class ProductImage(models.Model):
    """Multiple images for products"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='products/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    


class ProductReview(models.Model):
    """Reviews for products by buyers"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='product_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    images = models.JSONField(default=list, blank=True)
    is_verified_purchase = models.BooleanField(default=False)
    helpful_votes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'product_reviews'
        unique_together = ['product', 'buyer']


# ============== BUYER MODELS ==============

class BuyerProfile(models.Model):
    """Profile for buyers (consumers, restaurants, etc.)"""
    BUYER_TYPE_CHOICES = [
        ('individual', 'Individual Consumer'),
        ('restaurant', 'Restaurant'),
        ('hotel', 'Hotel'),
        ('retailer', 'Retailer'),
        ('wholesaler', 'Wholesaler'),
        ('processor', 'Food Processor'),
        ('exporter', 'Exporter'),
        ('institution', 'Institution'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='buyer_profile')
    buyer_type = models.CharField(max_length=20, choices=BUYER_TYPE_CHOICES)
    business_name = models.CharField(max_length=200, blank=True)
    business_registration = models.CharField(max_length=100, blank=True)
    tax_pin = models.CharField(max_length=20, blank=True)
    annual_purchase_volume = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    preferred_payment_method = models.CharField(max_length=50, blank=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_instructions = models.TextField(blank=True)
    special_requirements = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

class Wishlist(models.Model):
    """Buyer's wishlist of products"""
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'wishlists'
        unique_together = ['buyer', 'product']


# ============== ORDER MANAGEMENT MODELS ==============

class Cart(models.Model):
    """Shopping cart for buyers"""
    buyer = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
   
class CartItem(models.Model):
    """Items in shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cart_items'
        unique_together = ['cart', 'product']


class Order(models.Model):
    """Customer orders"""
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('ready', 'Ready for Delivery'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid'),
        ('refunded', 'Refunded'),
        ('failed', 'Failed'),
    ]
    
    order_number = models.CharField(max_length=50, unique=True)
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='received_orders')
    delivery_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    special_instructions = models.TextField(blank=True)
    tracking_number = models.CharField(max_length=100, blank=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    cancelled_at = models.DateTimeField(blank=True, null=True)
    cancellation_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
   
    
    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):
    """Individual items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_snapshot = models.JSONField(default=dict, help_text="Product details at time of order")
    
    class Meta:
        db_table = 'order_items'


class OrderStatusHistory(models.Model):
    """Track order status changes"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    previous_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    changed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
   

# ============== PAYMENT MODELS ==============

class PaymentMethod(models.Model):
    """Available payment methods"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    processing_fee_percentage = models.DecimalField(max_digits=5, decimal_places=4, default=0)
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maximum_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    
    
    def __str__(self):
        return self.name


class Payment(models.Model):
    """Payment transactions"""
    PAYMENT_TYPE_CHOICES = [
        ('order', 'Order Payment'),
        ('refund', 'Refund'),
        ('partial', 'Partial Payment'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    transaction_id = models.CharField(max_length=100, unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES, default='order')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    processing_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    gateway_reference = models.CharField(max_length=200, blank=True)
    gateway_response = models.JSONField(default=dict)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
  

# ============== DELIVERY MODELS ==============

class DeliveryZone(models.Model):
    """Delivery zones with different rates"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    counties = models.ManyToManyField(County, related_name='delivery_zones')
    base_delivery_fee = models.DecimalField(max_digits=8, decimal_places=2)
    free_delivery_threshold = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estimated_delivery_days = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    
 
    def __str__(self):
        return self.name


class DeliveryPartner(models.Model):
    """Third-party delivery partners"""
    name = models.CharField(max_length=200, unique=True)
    contact_person = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    service_areas = models.ManyToManyField(County, related_name='delivery_partners')
    pricing_model = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
   
    
    def __str__(self):
        return self.name


class Delivery(models.Model):
    """Delivery tracking"""
    DELIVERY_STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('returned', 'Returned'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    delivery_partner = models.ForeignKey(DeliveryPartner, on_delete=models.CASCADE, related_name='deliveries')
    driver_name = models.CharField(max_length=200, blank=True)
    driver_phone = models.CharField(max_length=15, blank=True)
    vehicle_details = models.CharField(max_length=200, blank=True)
    pickup_address = models.TextField()
    delivery_address = models.TextField()
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='assigned')
    estimated_delivery_time = models.DateTimeField()
    actual_pickup_time = models.DateTimeField(blank=True, null=True)
    actual_delivery_time = models.DateTimeField(blank=True, null=True)
    delivery_notes = models.TextField(blank=True)
    recipient_name = models.CharField(max_length=200, blank=True)
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2)
    tracking_updates = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
   

# ============== MARKET INTELLIGENCE MODELS ==============

class MarketPrice(models.Model):
    """Historical and current market prices"""
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='market_prices')
    location = models.ForeignKey(County, on_delete=models.CASCADE)
    market_name = models.CharField(max_length=200, blank=True)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE)
    quality_grade = models.CharField(max_length=50, blank=True)
    supply_level = models.CharField(max_length=50, blank=True, help_text="e.g., High, Medium, Low")
    demand_level = models.CharField(max_length=50, blank=True)
    price_trend = models.CharField(max_length=20, blank=True, help_text="e.g., Rising, Falling, Stable")
    source = models.CharField(max_length=100, blank=True)
    date_recorded = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'market_prices'
        indexes = [
            models.Index(fields=['crop', 'location', 'date_recorded']),
            models.Index(fields=['date_recorded']),
        ]



# ============== USER MANAGEMENT MODELS ==============

class CropCalendar(models.Model):
    """Seasonal planting and harvesting calendar"""
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='calendar_entries')
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    planting_season_start = models.CharField(max_length=20)  # e.g., "March"
    planting_season_end = models.CharField(max_length=20)
    harvesting_season_start = models.CharField(max_length=20)
    harvesting_season_end = models.CharField(max_length=20)
    recommended_varieties = models.TextField(blank=True)
    special_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'crop_calendar'
        unique_together = ['crop', 'county']


class MarketDemandForecast(models.Model):
    """Demand forecasting for different crops"""
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='demand_forecasts')
    location = models.ForeignKey(County, on_delete=models.CASCADE)
    forecast_period = models.CharField(max_length=50)  # e.g., "Q1 2025", "March 2025"
    expected_demand = models.CharField(max_length=20, choices=[
        ('very_high', 'Very High'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ('very_low', 'Very Low'),
    ])
    price_prediction = models.CharField(max_length=20, choices=[
        ('rising', 'Rising'),
        ('stable', 'Stable'),
        ('falling', 'Falling'),
    ])
    confidence_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    factors = models.JSONField(default=list, help_text="Factors affecting demand")
    recommendations = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'market_demand_forecasts'


# ============== AGRICULTURAL INPUT MODELS ==============

class InputCategory(models.Model):
    """Categories for agricultural inputs"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='input_categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'input_categories'
        verbose_name_plural = 'Input Categories'
    
    def __str__(self):
        return self.name


class InputSupplier(models.Model):
    """Suppliers of agricultural inputs"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='supplier_profile')
    business_name = models.CharField(max_length=200)
    license_number = models.CharField(max_length=100, blank=True)
    business_registration = models.CharField(max_length=100, blank=True)
    specialization = models.ManyToManyField(InputCategory, related_name='suppliers')
    service_areas = models.ManyToManyField(County, related_name='input_suppliers')
    delivery_available = models.BooleanField(default=False)
    credit_terms_available = models.BooleanField(default=False)
    minimum_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'input_suppliers'
    
    def __str__(self):
        return self.business_name


class AgriculturalInput(models.Model):
    """Agricultural inputs (seeds, fertilizers, etc.)"""
    INPUT_TYPE_CHOICES = [
        ('seeds', 'Seeds'),
        ('fertilizer', 'Fertilizer'),
        ('pesticide', 'Pesticide'),
        ('herbicide', 'Herbicide'),
        ('fungicide', 'Fungicide'),
        ('equipment', 'Equipment'),
        ('tools', 'Tools'),
        ('irrigation', 'Irrigation'),
        ('other', 'Other'),
    ]
    
    supplier = models.ForeignKey(InputSupplier, on_delete=models.CASCADE, related_name='inputs')
    category = models.ForeignKey(InputCategory, on_delete=models.CASCADE, related_name='inputs')
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True)
    input_type = models.CharField(max_length=20, choices=INPUT_TYPE_CHOICES)
    description = models.TextField()
    specifications = models.JSONField(default=dict)
    unit = models.ForeignKey(ProductUnit, on_delete=models.CASCADE)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    stock_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expiry_date = models.DateField(blank=True, null=True)
    manufacturer = models.CharField(max_length=200, blank=True)
    registration_number = models.CharField(max_length=100, blank=True)
    safety_instructions = models.TextField(blank=True)
    application_instructions = models.TextField(blank=True)
    compatible_crops = models.ManyToManyField(Crop, related_name='compatible_inputs', blank=True)
    images = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'agricultural_inputs'
        indexes = [
            models.Index(fields=['input_type', 'is_active']),
            models.Index(fields=['supplier', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.supplier.business_name}"


# ============== EXTENSION SERVICES MODELS ==============

class ExtensionAgent(models.Model):
    """Agricultural extension agents"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='agent_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    specialization = models.JSONField(default=list)
    qualifications = models.TextField()
    years_of_experience = models.PositiveIntegerField()
    service_areas = models.ManyToManyField(County, related_name='extension_agents')
    contact_hours = models.CharField(max_length=100, blank=True)
    languages_spoken = models.JSONField(default=list)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'extension_agents'
    
    def __str__(self):
        return f"Agent {self.user.get_full_name()}"


class Advisory(models.Model):
    """Agricultural advisories and recommendations"""
    ADVISORY_TYPE_CHOICES = [
        ('weather', 'Weather Advisory'),
        ('pest', 'Pest Control'),
        ('disease', 'Disease Management'),
        ('planting', 'Planting Advisory'),
        ('harvesting', 'Harvesting Advisory'),
        ('market', 'Market Advisory'),
        ('general', 'General Advisory'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    agent = models.ForeignKey(ExtensionAgent, on_delete=models.CASCADE, related_name='advisories')
    title = models.CharField(max_length=200)
    advisory_type = models.CharField(max_length=20, choices=ADVISORY_TYPE_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    content = models.TextField()
    target_crops = models.ManyToManyField(Crop, related_name='advisories', blank=True)
    target_areas = models.ManyToManyField(County, related_name='advisories', blank=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField(blank=True, null=True)
    attachments = models.JSONField(default=list)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'advisories'
        indexes = [
            models.Index(fields=['advisory_type', 'is_published']),
            models.Index(fields=['valid_from', 'valid_until']),
        ]


class ConsultationRequest(models.Model):
    """Consultation requests from farmers to extension agents"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='consultation_requests')
    agent = models.ForeignKey(ExtensionAgent, on_delete=models.CASCADE, related_name='consultation_requests')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    preferred_date = models.DateTimeField()
    consultation_type = models.CharField(max_length=20, choices=[
        ('phone', 'Phone Call'),
        ('video', 'Video Call'),
        ('visit', 'Farm Visit'),
        ('online', 'Online Chat'),
    ])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    scheduled_date = models.DateTimeField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(default=60)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'consultation_requests'


# ============== COOPERATIVE MODELS ==============

class Cooperative(models.Model):
    """Farmer cooperatives and groups"""
    COOPERATIVE_TYPE_CHOICES = [
        ('primary', 'Primary Cooperative'),
        ('secondary', 'Secondary Cooperative'),
        ('union', 'Cooperative Union'),
        ('sacco', 'SACCO'),
        ('group', 'Farmer Group'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    registration_number = models.CharField(max_length=100, unique=True)
    cooperative_type = models.CharField(max_length=20, choices=COOPERATIVE_TYPE_CHOICES)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    chairman = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chaired_cooperatives')
    secretary = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='secretary_cooperatives')
    treasurer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='treasurer_cooperatives')
    registration_date = models.DateField()
    member_count = models.PositiveIntegerField(default=0)
    share_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    services_offered = models.JSONField(default=list)
    contact_phone = models.CharField(max_length=15)
    contact_email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'cooperatives'
    
    def __str__(self):
        return self.name


class CooperativeMembership(models.Model):
    """Membership in cooperatives"""
    MEMBERSHIP_STATUS_CHOICES = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('terminated', 'Terminated'),
        ('pending', 'Pending Approval'),
    ]
    
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE, related_name='memberships')
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cooperative_memberships')
    membership_number = models.CharField(max_length=50)
    join_date = models.DateField()
    status = models.CharField(max_length=20, choices=MEMBERSHIP_STATUS_CHOICES, default='pending')
    shares_owned = models.PositiveIntegerField(default=0)
    total_contribution = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    position = models.CharField(max_length=100, blank=True)
    monthly_contribution = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    last_contribution_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'cooperative_memberships'
        unique_together = ['cooperative', 'member']


# ============== FINANCING MODELS ==============

class FinancialInstitution(models.Model):
    """Banks and financial institutions offering agricultural loans"""
    INSTITUTION_TYPE_CHOICES = [
        ('bank', 'Commercial Bank'),
        ('microfinance', 'Microfinance Institution'),
        ('sacco', 'SACCO'),
        ('government', 'Government Agency'),
        ('ngo', 'NGO'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    institution_type = models.CharField(max_length=20, choices=INSTITUTION_TYPE_CHOICES)
    description = models.TextField(blank=True)
    contact_person = models.CharField(max_length=200, blank=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(blank=True)
    service_areas = models.ManyToManyField(County, related_name='financial_institutions')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'financial_institutions'
    
    def __str__(self):
        return self.name


class LoanProduct(models.Model):
    """Loan products offered by financial institutions"""
    institution = models.ForeignKey(FinancialInstitution, on_delete=models.CASCADE, related_name='loan_products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    loan_type = models.CharField(max_length=100)
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    repayment_period_months = models.PositiveIntegerField()
    processing_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    collateral_required = models.BooleanField(default=True)
    collateral_types = models.JSONField(default=list)
    eligibility_criteria = models.TextField()
    required_documents = models.JSONField(default=list)
    application_process = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'loan_products'


class LoanApplication(models.Model):
    """Loan applications by farmers"""
    APPLICATION_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
        ('cancelled', 'Cancelled'),
    ]
    
    application_number = models.CharField(max_length=50, unique=True)
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='loan_applications')
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.CASCADE, related_name='applications')
    requested_amount = models.DecimalField(max_digits=10, decimal_places=2)
    loan_purpose = models.TextField()
    business_plan = models.TextField(blank=True)
    collateral_offered = models.TextField(blank=True)
    guarantors = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default='draft')
    submitted_date = models.DateTimeField(blank=True, null=True)
    review_date = models.DateTimeField(blank=True, null=True)
    decision_date = models.DateTimeField(blank=True, null=True)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rejection_reason = models.TextField(blank=True)
    disbursement_date = models.DateTimeField(blank=True, null=True)
    documents_uploaded = models.JSONField(default=list)
    officer_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'loan_applications'


# ============== INSURANCE MODELS ==============

class InsuranceProvider(models.Model):
    """Insurance companies offering agricultural insurance"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    license_number = models.CharField(max_length=100, unique=True)
    contact_person = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(blank=True)
    service_areas = models.ManyToManyField(County, related_name='insurance_providers')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'insurance_providers'
    
    def __str__(self):
        return self.name


class InsuranceProduct(models.Model):
    """Insurance products for farmers"""
    COVERAGE_TYPE_CHOICES = [
        ('crop', 'Crop Insurance'),
        ('livestock', 'Livestock Insurance'),
        ('weather', 'Weather Index Insurance'),
        ('area_yield', 'Area Yield Insurance'),
        ('multi_peril', 'Multi-Peril Crop Insurance'),
    ]
    
    provider = models.ForeignKey(InsuranceProvider, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    coverage_type = models.CharField(max_length=20, choices=COVERAGE_TYPE_CHOICES)
    description = models.TextField()
    covered_crops = models.ManyToManyField(Crop, related_name='insurance_products', blank=True)
    coverage_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=80)
    premium_rate = models.DecimalField(max_digits=5, decimal_places=4)
    minimum_coverage = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_coverage = models.DecimalField(max_digits=10, decimal_places=2)
    covered_perils = models.JSONField(default=list)
    exclusions = models.TextField(blank=True)
    eligibility_criteria = models.TextField()
    claim_process = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class InsurancePolicy(models.Model):
    """Insurance policies purchased by farmers"""
    POLICY_STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('suspended', 'Suspended'),
        ('claimed', 'Claimed'),
    ]
    
    policy_number = models.CharField(max_length=50, unique=True)
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='insurance_policies')
    product = models.ForeignKey(InsuranceProduct, on_delete=models.CASCADE, related_name='policies')
    coverage_amount = models.DecimalField(max_digits=10, decimal_places=2)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    policy_start_date = models.DateField()
    policy_end_date = models.DateField()
    status = models.CharField(max_length=20, choices=POLICY_STATUS_CHOICES, default='active')
    covered_farms = models.ManyToManyField(Farm, related_name='insurance_policies')
    beneficiaries = models.JSONField(default=list)
    payment_schedule = models.CharField(max_length=50, blank=True)
    last_premium_payment = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    


class InsuranceClaim(models.Model):
    """Insurance claims made by farmers"""
    CLAIM_STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_investigation', 'Under Investigation'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
        ('closed', 'Closed'),
    ]
    
    claim_number = models.CharField(max_length=50, unique=True)
    policy = models.ForeignKey(InsurancePolicy, on_delete=models.CASCADE, related_name='claims')
    incident_date = models.DateField()
    incident_description = models.TextField()
    claimed_amount = models.DecimalField(max_digits=10, decimal_places=2)
    supporting_documents = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=CLAIM_STATUS_CHOICES, default='submitted')
    assessor_assigned = models.CharField(max_length=200, blank=True)
    assessment_date = models.DateField(blank=True, null=True)
    assessment_report = models.TextField(blank=True)
    approved_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    rejection_reason = models.TextField(blank=True)
    payment_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'insurance_claims'


# ============== COMMUNICATION MODELS ==============

class Notification(models.Model):
    """System notifications for users"""
    NOTIFICATION_TYPE_CHOICES = [
        ('order', 'Order Update'),
        ('payment', 'Payment'),
        ('delivery', 'Delivery'),
        ('weather', 'Weather Alert'),
        ('market', 'Market Update'),
        ('advisory', 'Agricultural Advisory'),
        ('system', 'System Notification'),
        ('promotion', 'Promotion'),
    ]
    
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    send_email = models.BooleanField(default=False)
    send_sms = models.BooleanField(default=False)
    send_push = models.BooleanField(default=True)
    related_object_id = models.CharField(max_length=100, blank=True)
    action_url = models.URLField(blank=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    read_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    



class Message(models.Model):
    """Direct messages between users"""
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    attachments = models.JSONField(default=list)
    read_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'messages'
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['sender', 'created_at']),
        ]


# ============== ANALYTICS AND REPORTING MODELS ==============

class UserActivity(models.Model):
    """Track user activities for analytics"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    metadata = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_activities'
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['activity_type', 'timestamp']),
        ]


class SystemMetrics(models.Model):
    """System-wide metrics and statistics"""
    metric_name = models.CharField(max_length=100)
    metric_value = models.DecimalField(max_digits=15, decimal_places=2)
    metric_type = models.CharField(max_length=50)
    period = models.CharField(max_length=20)  # daily, weekly, monthly
    date_recorded = models.DateField()
    additional_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'system_metrics'
        unique_together = ['metric_name', 'period', 'date_recorded']


# ============== CONTENT MANAGEMENT MODELS ==============

class BlogPost(models.Model):
    """Educational blog posts and articles"""
    CONTENT_TYPE_CHOICES = [
        ('article', 'Article'),
        ('guide', 'How-to Guide'),
        ('news', 'News'),
        ('case_study', 'Case Study'),
        ('research', 'Research'),
    ]
    
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    content = models.TextField()
    summary = models.TextField(blank=True)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default='article')
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    tags = models.JSONField(default=list)
    related_crops = models.ManyToManyField(Crop, related_name='blog_posts', blank=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'blog_posts'
        indexes = [
            models.Index(fields=['is_published', 'published_at']),
            models.Index(fields=['content_type', 'is_published']),
        ]
    
    def __str__(self):
        return self.title


class FAQ(models.Model):
    """Frequently asked questions"""
    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('farming', 'Farming'),
        ('marketplace', 'Marketplace'),
        ('payments', 'Payments'),
        ('delivery', 'Delivery'),
        ('insurance', 'Insurance'),
        ('loans', 'Loans'),
        ('technical', 'Technical Support'),
    ]
    
    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    helpful_votes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'faqs'
        ordering = ['category', 'order', 'created_at']


class SupportTicket(models.Model):
    """Customer support tickets"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('waiting_response', 'Waiting for Response'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    CATEGORY_CHOICES = [
        ('technical', 'Technical Issue'),
        ('account', 'Account Issue'),
        ('payment', 'Payment Issue'),
        ('order', 'Order Issue'),
        ('delivery', 'Delivery Issue'),
        ('general', 'General Inquiry'),
        ('complaint', 'Complaint'),
        ('suggestion', 'Suggestion'),
    ]
    
    ticket_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='support_tickets')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_tickets')
    attachments = models.JSONField(default=list)
    resolution = models.TextField(blank=True)
    satisfaction_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'support_tickets'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'priority']),
        ]


class TicketMessage(models.Model):
    """Messages/replies in support tickets"""
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    attachments = models.JSONField(default=list)
    is_internal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ticket_messages'
        ordering = ['created_at']


# ============== SUBSCRIPTION AND PREMIUM SERVICES MODELS ==============

class SubscriptionPlan(models.Model):
    """Premium subscription plans for users"""
    PLAN_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('professional', 'Professional'),
        ('enterprise', 'Enterprise'),
    ]
    
    BILLING_CYCLE_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annual'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLE_CHOICES)
    features = models.JSONField(default=list)
    max_products = models.PositiveIntegerField(blank=True, null=True)
    max_orders_per_month = models.PositiveIntegerField(blank=True, null=True)
    premium_support = models.BooleanField(default=False)
    market_insights = models.BooleanField(default=False)
    priority_listing = models.BooleanField(default=False)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'subscription_plans'
    
    def __str__(self):
        return f"{self.name} - {self.billing_cycle}"


class UserSubscription(models.Model):
    """User subscriptions to premium plans"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('suspended', 'Suspended'),
        ('pending', 'Pending Payment'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='subscriptions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    auto_renew = models.BooleanField(default=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    last_payment_date = models.DateTimeField(blank=True, null=True)
    next_payment_date = models.DateTimeField(blank=True, null=True)
    cancellation_date = models.DateTimeField(blank=True, null=True)
    cancellation_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_subscriptions'
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['end_date', 'status']),
        ]


# ============== LOGISTICS AND WAREHOUSE MODELS ==============

class Warehouse(models.Model):
    """Storage warehouses for agricultural products"""
    name = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='managed_warehouses')
    capacity = models.DecimalField(max_digits=10, decimal_places=2, help_text="In metric tons")
    storage_types = models.JSONField(default=list, help_text="e.g., cold storage, dry storage")
    facilities = models.JSONField(default=list)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    monthly_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    security_features = models.JSONField(default=list)
    certifications = models.JSONField(default=list)
    operating_hours = models.CharField(max_length=200, blank=True)
    contact_phone = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'warehouses'


class StorageBooking(models.Model):
    """Bookings for warehouse storage"""
    BOOKING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    booking_number = models.CharField(max_length=50, unique=True)
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='storage_bookings')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='bookings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='storage_bookings')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    storage_type = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='pending')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    special_requirements = models.TextField(blank=True)
    check_in_date = models.DateTimeField(blank=True, null=True)
    check_out_date = models.DateTimeField(blank=True, null=True)
    condition_report = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'storage_bookings'


# ============== QUALITY ASSURANCE MODELS ==============

class QualityStandard(models.Model):
    """Quality standards for different crops"""
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='quality_standards')
    standard_name = models.CharField(max_length=100)
    certifying_body = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.JSONField(default=dict)
    testing_parameters = models.JSONField(default=list)
    validity_period_months = models.PositiveIntegerField(default=12)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'quality_standards'
        unique_together = ['crop', 'standard_name']


class QualityInspector(models.Model):
    """Certified quality inspectors"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='inspector_profile')
    license_number = models.CharField(max_length=100, unique=True)
    specialization = models.ManyToManyField(Crop, related_name='quality_inspectors')
    certifications = models.JSONField(default=list)
    service_areas = models.ManyToManyField(County, related_name='quality_inspectors')
    inspection_fee = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'quality_inspectors'


class QualityInspection(models.Model):
    """Quality inspection reports"""
    INSPECTION_TYPE_CHOICES = [
        ('pre_harvest', 'Pre-Harvest'),
        ('post_harvest', 'Post-Harvest'),
        ('storage', 'Storage Inspection'),
        ('export', 'Export Inspection'),
        ('certification', 'Certification Inspection'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    inspection_number = models.CharField(max_length=50, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='quality_inspections')
    inspector = models.ForeignKey(QualityInspector, on_delete=models.CASCADE, related_name='inspections')
    inspection_type = models.CharField(max_length=20, choices=INSPECTION_TYPE_CHOICES)
    scheduled_date = models.DateTimeField()
    actual_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    inspection_parameters = models.JSONField(default=dict)
    test_results = models.JSONField(default=dict)
    overall_grade = models.CharField(max_length=20, blank=True)
    pass_fail_status = models.CharField(max_length=10, blank=True)
    recommendations = models.TextField(blank=True)
    certificate_issued = models.BooleanField(default=False)
    certificate_number = models.CharField(max_length=100, blank=True)
    validity_date = models.DateField(blank=True, null=True)
    inspection_fee = models.DecimalField(max_digits=8, decimal_places=2)
    report_document = models.FileField(upload_to='inspection_reports/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'quality_inspections'


# ============== TRAINING AND EDUCATION MODELS ==============

class TrainingProvider(models.Model):
    """Organizations providing agricultural training"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    contact_person = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(blank=True)
    specializations = models.JSONField(default=list)
    accreditation = models.CharField(max_length=200, blank=True)
    service_areas = models.ManyToManyField(County, related_name='training_providers')
    is_verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'training_providers'
    
    def __str__(self):
        return self.name


class TrainingCourse(models.Model):
    """Training courses offered to farmers"""
    COURSE_TYPE_CHOICES = [
        ('online', 'Online Course'),
        ('physical', 'Physical Training'),
        ('hybrid', 'Hybrid'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    provider = models.ForeignKey(TrainingProvider, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=200)
    description = models.TextField()
    course_type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    duration_hours = models.PositiveIntegerField()
    course_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    max_participants = models.PositiveIntegerField(default=50)
    prerequisites = models.TextField(blank=True)
    learning_objectives = models.JSONField(default=list)
    curriculum = models.JSONField(default=list)
    certification_offered = models.BooleanField(default=False)
    certificate_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    target_crops = models.ManyToManyField(Crop, related_name='training_courses', blank=True)
    materials_provided = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'training_courses'


class TrainingSession(models.Model):
    """Individual training sessions/batches"""
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    course = models.ForeignKey(TrainingCourse, on_delete=models.CASCADE, related_name='sessions')
    session_name = models.CharField(max_length=200)
    instructor = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    online_meeting_link = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    enrolled_count = models.PositiveIntegerField(default=0)
    completion_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    materials = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'training_sessions'


class TrainingEnrollment(models.Model):
    """Farmer enrollments in training courses"""
    ENROLLMENT_STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('failed', 'Failed'),
    ]
    
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='training_enrollments')
    session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ENROLLMENT_STATUS_CHOICES, default='enrolled')
    progress_percentage = models.PositiveIntegerField(default=0)
    completion_date = models.DateTimeField(blank=True, null=True)
    certificate_issued = models.BooleanField(default=False)
    certificate_number = models.CharField(max_length=100, blank=True)
    final_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    feedback_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)
    feedback_comment = models.TextField(blank=True)
    
    class Meta:
        db_table = 'training_enrollments'
        unique_together = ['farmer', 'session']


# ============== GOVERNMENT INTEGRATION MODELS ==============

class GovernmentScheme(models.Model):
    """Government agricultural schemes and subsidies"""
    SCHEME_TYPE_CHOICES = [
        ('subsidy', 'Subsidy'),
        ('loan', 'Loan Scheme'),
        ('insurance', 'Insurance Scheme'),
        ('training', 'Training Program'),
        ('equipment', 'Equipment Support'),
        ('input', 'Input Support'),
        ('market', 'Market Support'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    scheme_type = models.CharField(max_length=20, choices=SCHEME_TYPE_CHOICES)
    description = models.TextField()
    implementing_agency = models.CharField(max_length=200)
    eligibility_criteria = models.TextField()
    application_process = models.TextField()
    required_documents = models.JSONField(default=list)
    benefit_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    coverage_areas = models.ManyToManyField(County, related_name='government_schemes')
    target_crops = models.ManyToManyField(Crop, related_name='government_schemes', blank=True)
    application_deadline = models.DateField(blank=True, null=True)
    scheme_validity = models.DateField(blank=True, null=True)
    contact_information = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'government_schemes'


class SchemeApplication(models.Model):
    """Applications for government schemes"""
    APPLICATION_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
    ]
    
    application_number = models.CharField(max_length=50, unique=True)
    scheme = models.ForeignKey(GovernmentScheme, on_delete=models.CASCADE, related_name='applications')
    farmer = models.ForeignKey(FarmerProfile, on_delete=models.CASCADE, related_name='scheme_applications')
    application_data = models.JSONField(default=dict)
    supporting_documents = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS_CHOICES, default='draft')
    submitted_date = models.DateTimeField(blank=True, null=True)
    review_date = models.DateTimeField(blank=True, null=True)
    decision_date = models.DateTimeField(blank=True, null=True)
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    disbursement_date = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True)
    officer_comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'scheme_applications'


# ============== MOBILE APP SPECIFIC MODELS ==============

class MobileDevice(models.Model):
    """Registered mobile devices for push notifications"""
    DEVICE_TYPE_CHOICES = [
        ('android', 'Android'),
        ('ios', 'iOS'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='mobile_devices')
    device_id = models.CharField(max_length=200, unique=True)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPE_CHOICES)
    device_token = models.TextField()
    app_version = models.CharField(max_length=20, blank=True)
    os_version = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'mobile_devices'


class AppVersion(models.Model):
    """Mobile app version control"""
    PLATFORM_CHOICES = [
        ('android', 'Android'),
        ('ios', 'iOS'),
    ]
    
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    version_number = models.CharField(max_length=20)
    build_number = models.CharField(max_length=20)
    release_notes = models.TextField(blank=True)
    minimum_supported_version = models.CharField(max_length=20, blank=True)
    force_update = models.BooleanField(default=False)
    download_url = models.URLField()
    is_active = models.BooleanField(default=True)
    release_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'app_versions'
        unique_together = ['platform', 'version_number']


# ============== AUDIT TRAIL MODELS ==============

class AuditLog(models.Model):
    """Audit trail for important system actions"""
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('export', 'Export'),
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    object_type = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, blank=True)
    object_repr = models.CharField(max_length=200, blank=True)
    changes = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'audit_logs'
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['object_type', 'object_id']),
            models.Index(fields=['timestamp']),
        ]


# ============== SYSTEM CONFIGURATION MODELS ==============

class SystemConfiguration(models.Model):
    """System-wide configuration settings"""
    CONFIG_TYPE_CHOICES = [
        ('general', 'General Settings'),
        ('payment', 'Payment Settings'),
        ('notification', 'Notification Settings'),
        ('security', 'Security Settings'),
        ('integration', 'Integration Settings'),
    ]
    
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    config_type = models.CharField(max_length=20, choices=CONFIG_TYPE_CHOICES)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.key}: {self.value[:50]}"


# Add any additional custom model methods, properties, and manager classes as neededustomUser(AbstractUser):
    """Extended user model with additional fields"""
    USER_TYPE_CHOICES = [
        ('farmer', 'Farmer'),
        ('buyer', 'Buyer'),
        ('admin', 'Administrator'),
        ('agent', 'Agricultural Agent'),
        ('supplier', 'Input Supplier'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='buyer')
    phone_number = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    national_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    verification_document = models.FileField(upload_to='verification/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_seen = models.DateTimeField(auto_now=True)
    
 


# ============== LOCATION MODELS ==============

class AgriculturalNews(models.Model):
    """Agricultural news articles"""
    title = models.CharField(max_length=300)
    summary = models.TextField()
    content = models.TextField()
    source = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True)
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    published_date = models.DateTimeField()
    tags = models.JSONField(default=list, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
 
    def __str__(self):
        return self.title