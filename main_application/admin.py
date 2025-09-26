from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Sum
from django.contrib.admin import SimpleListFilter
import json

# Import all models
from .models import *


# ============== CUSTOM FILTERS ==============

class LocationFilter(SimpleListFilter):
    title = 'Location'
    parameter_name = 'location'

    def lookups(self, request, model_admin):
        counties = County.objects.all()
        return [(county.id, county.name) for county in counties]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(county_id=self.value())
        return queryset


class UserTypeFilter(SimpleListFilter):
    title = 'User Type'
    parameter_name = 'user_type'

    def lookups(self, request, model_admin):
        return CustomUser.USER_TYPE_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_type=self.value())
        return queryset


# ============== USER MANAGEMENT ==============

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'phone_number', 'is_verified', 'created_at', 'last_seen']
    list_filter = [UserTypeFilter, 'is_verified', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'phone_number', 'first_name', 'last_name']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_seen']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('id', 'user_type', 'phone_number', 'profile_picture', 
                      'date_of_birth', 'national_id', 'is_verified', 
                      'verification_document', 'created_at', 'updated_at', 'last_seen')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'preferred_language', 'website']
    search_fields = ['user__username', 'bio']
    list_filter = ['preferred_language']


# ============== LOCATION MODELS ==============

@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'population', 'area_sq_km', 'subcounty_count']
    search_fields = ['name', 'code']
    ordering = ['name']
    
    def subcounty_count(self, obj):
        return obj.subcounties.count()
    subcounty_count.short_description = 'Sub-Counties'


@admin.register(SubCounty)
class SubCountyAdmin(admin.ModelAdmin):
    list_display = ['name', 'county', 'code', 'ward_count']
    search_fields = ['name', 'code', 'county__name']
    list_filter = ['county']
    
    def ward_count(self, obj):
        return obj.wards.count()
    ward_count.short_description = 'Wards'


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ['name', 'subcounty', 'county', 'code']
    search_fields = ['name', 'code', 'subcounty__name']
    list_filter = ['subcounty__county']
    
    def county(self, obj):
        return obj.subcounty.county.name
    county.short_description = 'County'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'county', 'subcounty', 'ward', 'is_default']
    search_fields = ['name', 'user__username', 'village']
    list_filter = ['county', 'is_default']
    readonly_fields = ['created_at']


# ============== FARMER MODELS ==============

@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'farm_name', 'farming_type', 'years_of_experience', 
                   'total_farm_size', 'is_cooperative_member', 'created_at']
    search_fields = ['user__username', 'farm_name', 'cooperative_name']
    list_filter = ['farming_type', 'years_of_experience', 'is_cooperative_member']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'farm_name', 'farming_type', 'years_of_experience', 'total_farm_size')
        }),
        ('Methods & Certifications', {
            'fields': ('farming_methods', 'certifications')
        }),
        ('Financial Information', {
            'fields': ('bank_account_number', 'bank_name', 'mpesa_number')
        }),
        ('Cooperative Information', {
            'fields': ('is_cooperative_member', 'cooperative_name')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ['name', 'farmer', 'size', 'location', 'soil_type', 'is_active', 'created_at']
    search_fields = ['name', 'farmer__user__username', 'description']
    list_filter = ['is_active', 'soil_type', 'water_source']
    readonly_fields = ['created_at']


# ============== CROP MODELS ==============

@admin.register(CropCategory)
class CropCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'crop_count', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['is_active', 'parent']
    readonly_fields = ['created_at']
    
    def crop_count(self, obj):
        return obj.crops.count()
    crop_count.short_description = 'Crops'


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'scientific_name', 'category', 'variety', 'maturity_period_days', 'is_active']
    search_fields = ['name', 'scientific_name', 'variety']
    list_filter = ['category', 'is_active', 'growing_season']
    readonly_fields = ['created_at']


@admin.register(ProductUnit)
class ProductUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation', 'base_unit', 'conversion_factor']
    search_fields = ['name', 'abbreviation']


# ============== PRODUCT MODELS ==============

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'farmer', 'crop', 'price_per_unit', 'quantity_available', 
                   'quality_grade', 'status', 'featured', 'views_count', 'created_at']
    search_fields = ['name', 'farmer__user__username', 'crop__name', 'description']
    list_filter = ['status', 'quality_grade', 'featured', 'organic_certified', 'crop__category']
    readonly_fields = ['slug', 'views_count', 'likes_count', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('farmer', 'crop', 'farm', 'name', 'slug', 'description')
        }),
        ('Quantity & Pricing', {
            'fields': ('quantity_available', 'unit', 'price_per_unit', 'minimum_order')
        }),
        ('Quality & Certification', {
            'fields': ('quality_grade', 'organic_certified', 'certification_body', 
                      'storage_condition', 'packaging_options')
        }),
        ('Dates & Status', {
            'fields': ('harvest_date', 'expiry_date', 'status', 'featured')
        }),
        ('Media & Statistics', {
            'fields': ('images', 'videos', 'views_count', 'likes_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'caption', 'is_primary', 'order', 'image_preview']
    search_fields = ['product__name', 'caption']
    list_filter = ['is_primary']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'buyer', 'rating', 'title', 'is_verified_purchase', 
                   'helpful_votes', 'created_at']
    search_fields = ['product__name', 'buyer__username', 'title', 'comment']
    list_filter = ['rating', 'is_verified_purchase']
    readonly_fields = ['created_at', 'updated_at']


# ============== BUYER MODELS ==============

@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'buyer_type', 'business_name', 'credit_limit', 'created_at']
    search_fields = ['user__username', 'business_name', 'business_registration']
    list_filter = ['buyer_type']
    readonly_fields = ['created_at']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'product', 'created_at']
    search_fields = ['buyer__username', 'product__name']
    list_filter = ['created_at']


# ============== ORDER MODELS ==============

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'item_count', 'total_value', 'updated_at']
    search_fields = ['buyer__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'
    
    def total_value(self, obj):
        total = obj.items.aggregate(total=Sum('total_price'))['total']
        return f"KES {total:.2f}" if total else "KES 0.00"
    total_value.short_description = 'Total Value'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_snapshot']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'buyer', 'farmer', 'status', 'payment_status', 
                   'total_amount', 'order_date', 'expected_delivery_date']
    search_fields = ['order_number', 'buyer__username', 'farmer__user__username']
    list_filter = ['status', 'payment_status', 'order_date']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'buyer', 'farmer', 'delivery_location')
        }),
        ('Status & Dates', {
            'fields': ('status', 'payment_status', 'order_date', 'expected_delivery_date',
                      'delivered_at', 'cancelled_at')
        }),
        ('Financial Details', {
            'fields': ('subtotal', 'delivery_fee', 'tax_amount', 'discount_amount', 'total_amount')
        }),
        ('Additional Information', {
            'fields': ('special_instructions', 'tracking_number', 'cancellation_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['order', 'previous_status', 'new_status', 'changed_by', 'timestamp']
    search_fields = ['order__order_number', 'changed_by__username']
    list_filter = ['new_status', 'timestamp']
    readonly_fields = ['timestamp']


# ============== PAYMENT MODELS ==============

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'processing_fee_percentage', 'minimum_amount']
    search_fields = ['name', 'code']
    list_filter = ['is_active']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'order', 'payment_method', 'amount', 
                   'status', 'payment_type', 'paid_at', 'created_at']
    search_fields = ['transaction_id', 'order__order_number', 'gateway_reference']
    list_filter = ['status', 'payment_type', 'payment_method']
    readonly_fields = ['created_at']


# ============== DELIVERY MODELS ==============

@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_delivery_fee', 'free_delivery_threshold', 
                   'estimated_delivery_days', 'is_active']
    search_fields = ['name', 'description']
    list_filter = ['is_active', 'estimated_delivery_days']
    filter_horizontal = ['counties']


@admin.register(DeliveryPartner)
class DeliveryPartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone_number', 'rating', 'is_active']
    search_fields = ['name', 'contact_person', 'phone_number', 'email']
    list_filter = ['is_active', 'rating']
    filter_horizontal = ['service_areas']


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['order', 'delivery_partner', 'driver_name', 'status', 
                   'estimated_delivery_time', 'actual_delivery_time']
    search_fields = ['order__order_number', 'driver_name', 'driver_phone']
    list_filter = ['status', 'delivery_partner']
    readonly_fields = ['created_at']


# ============== MARKET INTELLIGENCE ==============

@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ['crop', 'location', 'price_per_unit', 'unit', 'quality_grade', 
                   'price_trend', 'date_recorded']
    search_fields = ['crop__name', 'location__name', 'market_name']
    list_filter = ['price_trend', 'quality_grade', 'date_recorded', 'location']
    date_hierarchy = 'date_recorded'


@admin.register(CropCalendar)
class CropCalendarAdmin(admin.ModelAdmin):
    list_display = ['crop', 'county', 'planting_season_start', 'planting_season_end',
                   'harvesting_season_start', 'harvesting_season_end']
    search_fields = ['crop__name', 'county__name']
    list_filter = ['county', 'crop__category']


@admin.register(MarketDemandForecast)
class MarketDemandForecastAdmin(admin.ModelAdmin):
    list_display = ['crop', 'location', 'forecast_period', 'expected_demand', 
                   'price_prediction', 'confidence_level']
    search_fields = ['crop__name', 'location__name', 'forecast_period']
    list_filter = ['expected_demand', 'price_prediction', 'location']


# ============== INPUT SUPPLIERS ==============

@admin.register(InputCategory)
class InputCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active']
    search_fields = ['name', 'description']
    list_filter = ['is_active', 'parent']


@admin.register(InputSupplier)
class InputSupplierAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'user', 'is_verified', 'rating', 'total_sales']
    search_fields = ['business_name', 'user__username', 'license_number']
    list_filter = ['is_verified', 'delivery_available', 'credit_terms_available']
    filter_horizontal = ['specialization', 'service_areas']


@admin.register(AgriculturalInput)
class AgriculturalInputAdmin(admin.ModelAdmin):
    list_display = ['name', 'supplier', 'input_type', 'brand', 'price_per_unit', 
                   'stock_quantity', 'is_active']
    search_fields = ['name', 'brand', 'supplier__business_name', 'manufacturer']
    list_filter = ['input_type', 'is_active', 'category']
    filter_horizontal = ['compatible_crops']


# ============== EXTENSION SERVICES ==============

@admin.register(ExtensionAgent)
class ExtensionAgentAdmin(admin.ModelAdmin):
    list_display = ['user', 'employee_id', 'years_of_experience', 'rating', 'is_available']
    search_fields = ['user__username', 'employee_id', 'qualifications']
    list_filter = ['is_available', 'years_of_experience']
    filter_horizontal = ['service_areas']


@admin.register(Advisory)
class AdvisoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'agent', 'advisory_type', 'priority', 'is_published', 
                   'valid_from', 'views_count']
    search_fields = ['title', 'content', 'agent__user__username']
    list_filter = ['advisory_type', 'priority', 'is_published']
    filter_horizontal = ['target_crops', 'target_areas']
    date_hierarchy = 'valid_from'


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'agent', 'subject', 'consultation_type', 'status', 
                   'preferred_date', 'consultation_fee']
    search_fields = ['farmer__user__username', 'agent__user__username', 'subject']
    list_filter = ['consultation_type', 'status']


# ============== COOPERATIVE MODELS ==============

@admin.register(Cooperative)
class CooperativeAdmin(admin.ModelAdmin):
    list_display = ['name', 'cooperative_type', 'chairman', 'member_count', 
                   'registration_date', 'is_active']
    search_fields = ['name', 'registration_number', 'description']
    list_filter = ['cooperative_type', 'is_active']


@admin.register(CooperativeMembership)
class CooperativeMembershipAdmin(admin.ModelAdmin):
    list_display = ['cooperative', 'member', 'membership_number', 'status', 
                   'shares_owned', 'join_date']
    search_fields = ['cooperative__name', 'member__username', 'membership_number']
    list_filter = ['status', 'join_date']


# ============== FINANCIAL SERVICES ==============

@admin.register(FinancialInstitution)
class FinancialInstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'institution_type', 'contact_person', 'phone_number', 'is_active']
    search_fields = ['name', 'contact_person', 'phone_number', 'email']
    list_filter = ['institution_type', 'is_active']
    filter_horizontal = ['service_areas']


@admin.register(LoanProduct)
class LoanProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'institution', 'minimum_amount', 'maximum_amount', 
                   'interest_rate', 'repayment_period_months', 'is_active']
    search_fields = ['name', 'institution__name', 'loan_type']
    list_filter = ['institution', 'is_active', 'collateral_required']


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['application_number', 'farmer', 'loan_product', 'requested_amount', 
                   'status', 'submitted_date']
    search_fields = ['application_number', 'farmer__user__username', 'loan_product__name']
    list_filter = ['status', 'submitted_date', 'loan_product__institution']
    readonly_fields = ['application_number', 'created_at', 'updated_at']


# ============== INSURANCE MODELS ==============

@admin.register(InsuranceProvider)
class InsuranceProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'license_number', 'contact_person', 'phone_number', 'is_active']
    search_fields = ['name', 'license_number', 'contact_person']
    list_filter = ['is_active']
    filter_horizontal = ['service_areas']


@admin.register(InsuranceProduct)
class InsuranceProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider', 'coverage_type', 'coverage_percentage', 
                   'premium_rate', 'is_active']
    search_fields = ['name', 'provider__name', 'description']
    list_filter = ['coverage_type', 'is_active', 'provider']
    filter_horizontal = ['covered_crops']


@admin.register(InsurancePolicy)
class InsurancePolicyAdmin(admin.ModelAdmin):
    list_display = ['policy_number', 'farmer', 'product', 'coverage_amount', 
                   'status', 'policy_start_date', 'policy_end_date']
    search_fields = ['policy_number', 'farmer__user__username', 'product__name']
    list_filter = ['status', 'policy_start_date', 'product__provider']
    filter_horizontal = ['covered_farms']


@admin.register(InsuranceClaim)
class InsuranceClaimAdmin(admin.ModelAdmin):
    list_display = ['claim_number', 'policy', 'incident_date', 'claimed_amount', 
                   'status', 'approved_amount']
    search_fields = ['claim_number', 'policy__policy_number', 'incident_description']
    list_filter = ['status', 'incident_date']
    readonly_fields = ['created_at', 'updated_at']


# ============== COMMUNICATION MODELS ==============

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'title', 'notification_type', 'is_read', 'is_sent', 'created_at']
    search_fields = ['recipient__username', 'title', 'message']
    list_filter = ['notification_type', 'is_read', 'is_sent', 'send_email', 'send_sms']
    readonly_fields = ['sent_at', 'read_at', 'created_at']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'subject', 'is_read', 'created_at']
    search_fields = ['sender__username', 'recipient__username', 'subject', 'content']
    list_filter = ['is_read', 'created_at']
    readonly_fields = ['read_at', 'created_at']


# ============== ANALYTICS MODELS ==============

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'description', 'timestamp']
    search_fields = ['user__username', 'activity_type', 'description']
    list_filter = ['activity_type', 'timestamp']
    readonly_fields = ['timestamp']


@admin.register(SystemMetrics)
class SystemMetricsAdmin(admin.ModelAdmin):
    list_display = ['metric_name', 'metric_value', 'metric_type', 'period', 'date_recorded']
    search_fields = ['metric_name', 'metric_type']
    list_filter = ['metric_type', 'period', 'date_recorded']
    readonly_fields = ['created_at']


# ============== CONTENT MODELS ==============

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'content_type', 'is_published', 'is_featured', 
                   'views_count', 'published_at']
    search_fields = ['title', 'content', 'author__username']
    list_filter = ['content_type', 'is_published', 'is_featured', 'published_at']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['related_crops']
    readonly_fields = ['views_count', 'likes_count', 'created_at', 'updated_at']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_active', 'views_count', 'helpful_votes']
    search_fields = ['question', 'answer']
    list_filter = ['category', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'user', 'subject', 'category', 'priority', 
                   'status', 'assigned_to', 'created_at']
    search_fields = ['ticket_number', 'user__username', 'subject', 'description']
    list_filter = ['category', 'priority', 'status', 'assigned_to']
    readonly_fields = ['ticket_number', 'created_at', 'updated_at']


# ============== SUBSCRIPTION MODELS ==============

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'price', 'billing_cycle', 'commission_rate', 'is_active']
    search_fields = ['name', 'description']
    list_filter = ['plan_type', 'billing_cycle', 'is_active']


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'start_date', 'end_date', 'auto_renew']
    search_fields = ['user__username', 'plan__name']
    list_filter = ['status', 'auto_renew', 'start_date']


# ============== WAREHOUSE MODELS ==============

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager', 'capacity', 'monthly_rate', 'is_active']
    search_fields = ['name', 'manager__username']
    list_filter = ['is_active']


@admin.register(StorageBooking)
class StorageBookingAdmin(admin.ModelAdmin):
    list_display = ['booking_number', 'farmer', 'warehouse', 'product', 
                   'status', 'start_date', 'end_date', 'total_cost']
    search_fields = ['booking_number', 'farmer__user__username', 'warehouse__name']
    list_filter = ['status', 'start_date']


# ============== QUALITY ASSURANCE ==============

@admin.register(QualityStandard)
class QualityStandardAdmin(admin.ModelAdmin):
    list_display = ['crop', 'standard_name', 'certifying_body', 'validity_period_months', 'is_active']
    search_fields = ['crop__name', 'standard_name', 'certifying_body']
    list_filter = ['certifying_body', 'is_active']


@admin.register(QualityInspector)
class QualityInspectorAdmin(admin.ModelAdmin):
    list_display = ['user', 'license_number', 'inspection_fee', 'rating', 'is_available']
    search_fields = ['user__username', 'license_number']
    list_filter = ['is_available', 'rating']
    filter_horizontal = ['specialization', 'service_areas']


@admin.register(QualityInspection)
class QualityInspectionAdmin(admin.ModelAdmin):
    list_display = ['inspection_number', 'product', 'inspector', 'inspection_type', 
                   'status', 'overall_grade', 'certificate_issued']
    search_fields = ['inspection_number', 'product__name', 'inspector__user__username']
    list_filter = ['inspection_type', 'status', 'certificate_issued']


# ============== TRAINING MODELS ==============

@admin.register(TrainingProvider)
class TrainingProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone_number', 'is_verified', 'rating']
    search_fields = ['name', 'contact_person', 'phone_number', 'email']
    list_filter = ['is_verified', 'rating']
    filter_horizontal = ['service_areas']


@admin.register(TrainingCourse)
class TrainingCourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'provider', 'course_type', 'difficulty_level', 
                   'duration_hours', 'course_fee', 'is_active']
    search_fields = ['title', 'provider__name', 'description']
    list_filter = ['course_type', 'difficulty_level', 'is_active']
    filter_horizontal = ['target_crops']


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ['session_name', 'course', 'instructor', 'start_date', 
                   'status', 'enrolled_count', 'completion_rate']
    search_fields = ['session_name', 'course__title', 'instructor']
    list_filter = ['status', 'start_date']


@admin.register(TrainingEnrollment)
class TrainingEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'session', 'status', 'progress_percentage', 
                   'completion_date', 'certificate_issued']
    search_fields = ['farmer__user__username', 'session__session_name']
    list_filter = ['status', 'certificate_issued', 'enrollment_date']


# ============== GOVERNMENT SCHEMES ==============

@admin.register(GovernmentScheme)
class GovernmentSchemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'scheme_type', 'implementing_agency', 'benefit_amount', 
                   'application_deadline', 'is_active']
    search_fields = ['name', 'implementing_agency', 'description']
    list_filter = ['scheme_type', 'is_active', 'application_deadline']
    filter_horizontal = ['coverage_areas', 'target_crops']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SchemeApplication)
class SchemeApplicationAdmin(admin.ModelAdmin):
    list_display = ['application_number', 'scheme', 'farmer', 'status', 
                   'submitted_date', 'approved_amount']
    search_fields = ['application_number', 'scheme__name', 'farmer__user__username']
    list_filter = ['status', 'submitted_date', 'scheme']
    readonly_fields = ['application_number', 'created_at', 'updated_at']


# ============== MOBILE APP MODELS ==============

@admin.register(MobileDevice)
class MobileDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_type', 'app_version', 'os_version', 'is_active', 'last_seen']
    search_fields = ['user__username', 'device_id', 'device_token']
    list_filter = ['device_type', 'is_active', 'app_version']
    readonly_fields = ['last_seen', 'created_at']


@admin.register(AppVersion)
class AppVersionAdmin(admin.ModelAdmin):
    list_display = ['platform', 'version_number', 'build_number', 'force_update', 
                   'is_active', 'release_date']
    search_fields = ['version_number', 'build_number', 'release_notes']
    list_filter = ['platform', 'force_update', 'is_active', 'release_date']
    readonly_fields = ['created_at']


# ============== AUDIT TRAIL ==============

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'object_type', 'object_repr', 'timestamp']
    search_fields = ['user__username', 'object_type', 'object_repr']
    list_filter = ['action', 'object_type', 'timestamp']
    readonly_fields = ['timestamp']
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


# ============== SYSTEM CONFIGURATION ==============

@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    list_display = ['key', 'config_type', 'value_preview', 'is_active', 'updated_at']
    search_fields = ['key', 'description']
    list_filter = ['config_type', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    def value_preview(self, obj):
        return obj.value[:50] + "..." if len(obj.value) > 50 else obj.value
    value_preview.short_description = 'Value'


# ============== ADDITIONAL NEWS MODEL ==============

@admin.register(AgriculturalNews)
class AgriculturalNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'published_date', 'is_featured', 'created_at']
    search_fields = ['title', 'summary', 'content', 'source']
    list_filter = ['is_featured', 'published_date', 'source']
    readonly_fields = ['created_at']
    date_hierarchy = 'published_date'


# ============== CUSTOM ADMIN SITE CONFIGURATION ==============

# Customize the admin site header and title
admin.site.site_header = "Agricultural Marketplace Admin"
admin.site.site_title = "AgriMarket Admin"
admin.site.index_title = "Welcome to Agricultural Marketplace Administration"


# ============== ADMIN ACTIONS ==============

def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)
make_active.short_description = "Mark selected items as active"

def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)
make_inactive.short_description = "Mark selected items as inactive"

def mark_as_featured(modeladmin, request, queryset):
    queryset.update(featured=True)
mark_as_featured.short_description = "Mark selected products as featured"

def remove_featured(modeladmin, request, queryset):
    queryset.update(featured=False)
remove_featured.short_description = "Remove featured status"

def approve_items(modeladmin, request, queryset):
    queryset.update(status='approved')
approve_items.short_description = "Approve selected items"

def verify_users(modeladmin, request, queryset):
    queryset.update(is_verified=True)
verify_users.short_description = "Verify selected users"


# Add actions to relevant admin classes
ProductAdmin.actions = [make_active, make_inactive, mark_as_featured, remove_featured]
CustomUserAdmin.actions = [verify_users, make_active, make_inactive]
FarmerProfileAdmin.actions = [make_active, make_inactive]
InputSupplierAdmin.actions = [verify_users, make_active, make_inactive]


# ============== INLINE ADMIN CLASSES ==============

class FarmInline(admin.TabularInline):
    model = Farm
    extra = 1
    fields = ['name', 'size', 'location', 'is_active']


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ['name', 'crop', 'price_per_unit', 'quantity_available', 'status']
    readonly_fields = ['views_count', 'likes_count']


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['total_price']


class NotificationInline(admin.TabularInline):
    model = Notification
    extra = 0
    fields = ['title', 'notification_type', 'is_read', 'created_at']
    readonly_fields = ['created_at']


class MessageInline(admin.TabularInline):
    model = Message
    fk_name = 'recipient'
    extra = 0
    fields = ['sender', 'subject', 'is_read', 'created_at']
    readonly_fields = ['created_at']


class TicketMessageInline(admin.TabularInline):
    model = TicketMessage
    extra = 1
    readonly_fields = ['created_at']


# Add inlines to relevant admin classes
FarmerProfileAdmin.inlines = [FarmInline, ProductInline]
CartAdmin.inlines = [CartItemInline]
CustomUserAdmin.inlines = [NotificationInline, MessageInline]
SupportTicketAdmin.inlines = [TicketMessageInline]


# ============== DASHBOARD CUSTOMIZATION ==============

class DashboardAdmin(admin.ModelAdmin):
    """Custom dashboard functionality"""
    
    def changelist_view(self, request, extra_context=None):
        # Add custom statistics to the changelist view
        extra_context = extra_context or {}
        
        # Get statistics
        extra_context['total_users'] = CustomUser.objects.count()
        extra_context['total_farmers'] = CustomUser.objects.filter(user_type='farmer').count()
        extra_context['total_buyers'] = CustomUser.objects.filter(user_type='buyer').count()
        extra_context['active_products'] = Product.objects.filter(status='active').count()
        extra_context['pending_orders'] = Order.objects.filter(status='pending').count()
        
        return super().changelist_view(request, extra_context=extra_context)

# ============== EXPORT FUNCTIONALITY ==============

def export_as_csv(modeladmin, request, queryset):
    """Export selected objects as CSV"""
    import csv
    from django.http import HttpResponse
    
    meta = modeladmin.model._meta
    field_names = [field.name for field in meta.fields]
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={meta}.csv'
    writer = csv.writer(response)
    
    writer.writerow(field_names)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    
    return response

export_as_csv.short_description = "Export selected as CSV"

# Add export action to relevant admin classes
# ProductAdmin.actions = ProductAdmin.actions + (export_as_csv,)
# OrderAdmin.actions = OrderAdmin.actions + (export_as_csv,)
# CustomUserAdmin.actions = CustomUserAdmin.actions + (export_as_csv,)


# ============== ADVANCED FILTERS ==============

class DateRangeFilter(admin.SimpleListFilter):
    title = 'Date Range'
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Today'),
            ('week', 'This week'),
            ('month', 'This month'),
            ('year', 'This year'),
        )

    def queryset(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        
        if self.value() == 'today':
            return queryset.filter(created_at__date=timezone.now().date())
        elif self.value() == 'week':
            return queryset.filter(created_at__gte=timezone.now() - timedelta(days=7))
        elif self.value() == 'month':
            return queryset.filter(created_at__gte=timezone.now() - timedelta(days=30))
        elif self.value() == 'year':
            return queryset.filter(created_at__gte=timezone.now() - timedelta(days=365))
        return queryset


class PriceRangeFilter(admin.SimpleListFilter):
    title = 'Price Range'
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return (
            ('0-100', '0 - 100'),
            ('100-500', '100 - 500'),
            ('500-1000', '500 - 1000'),
            ('1000+', '1000+'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0-100':
            return queryset.filter(price_per_unit__lt=100)
        elif self.value() == '100-500':
            return queryset.filter(price_per_unit__gte=100, price_per_unit__lt=500)
        elif self.value() == '500-1000':
            return queryset.filter(price_per_unit__gte=500, price_per_unit__lt=1000)
        elif self.value() == '1000+':
            return queryset.filter(price_per_unit__gte=1000)
        return queryset


# Add advanced filters to ProductAdmin
ProductAdmin.list_filter += [DateRangeFilter, PriceRangeFilter]