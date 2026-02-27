from django.contrib import admin
from .models import UserProfile, RescueRequest, AdoptableAnimal, Product, ServicePlan, Booking, Order, AdoptionRequest

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'created_at']
    search_fields = ['user__username', 'phone_number']

@admin.register(RescueRequest)
class RescueRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'animal_type', 'status', 'date', 'time', 'created_at']
    list_filter = ['status', 'animal_type', 'date']
    search_fields = ['name', 'location', 'description']
    readonly_fields = ['created_at']

@admin.register(AdoptableAnimal)
class AdoptableAnimalAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'age', 'gender', 'status', 'adoption_fee', 'created_at']
    list_filter = ['species', 'status', 'gender']
    search_fields = ['name', 'breed', 'description']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'created_at']
    list_filter = ['category']
    search_fields = ['name', 'description']

@admin.register(ServicePlan)
class ServicePlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'duration_hours', 'price', 'created_at']
    list_filter = ['plan_type']
    search_fields = ['name', 'description']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'service_plan', 'animal_type', 'booking_date', 'status', 'payment_completed', 'created_at']
    list_filter = ['status', 'payment_completed', 'animal_type', 'booking_date']
    search_fields = ['user__username', 'pet_name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'product__name']

@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'animal', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'animal__name', 'message']
