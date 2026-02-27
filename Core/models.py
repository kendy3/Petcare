from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class RescueRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    ANIMAL_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rescue_requests')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    animal_type = models.CharField(max_length=20, choices=ANIMAL_TYPES)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='rescue_requests/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Rescue Request by {self.name} - {self.animal_type}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.send_confirmation_email()
    
    def send_confirmation_email(self):
        try:
            subject = 'Rescue Request Confirmation - Pet Care'
            message = f"""
Dear {self.name},

Thank you for submitting a rescue request to Pet Care!

Your rescue request details:
- Animal Type: {self.get_animal_type_display()}
- Date: {self.date}
- Time: {self.time}
- Location: {self.location}
- Status: {self.get_status_display()}

We have received your request and our team will review it shortly. We will contact you at {self.phone_number} with updates.

Together, we're making a difference in the lives of animals in need.

Best regards,
Pet Care Team
            """
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [self.user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email sending failed: {e}")

class AdoptableAnimal(models.Model):
    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('adopted', 'Adopted'),
        ('pending', 'Pending'),
    ]
    
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100, blank=True)
    age = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    description = models.TextField()
    image = models.ImageField(upload_to='animals/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    adoption_fee = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.species}"

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('toys', 'Toys'),
        ('clothes', 'Clothes'),
        ('accessories', 'Accessories'),
        ('shelter', 'Shelter Items'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class ServicePlan(models.Model):
    PLAN_TYPES = [
        ('low', 'Low Hour Plan'),
        ('medium', 'Medium Hour Plan'),
        ('high', 'High Hour Plan'),
    ]
    
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    duration_hours = models.IntegerField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.TextField(help_text="Comma-separated features")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - ${self.price}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    ANIMAL_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service_plan = models.ForeignKey(ServicePlan, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=20, choices=ANIMAL_TYPES)
    booking_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Booking by {self.user.username} - {self.service_plan.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class AdoptionRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_requests')
    animal = models.ForeignKey(AdoptableAnimal, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Adoption Request for {self.animal.name} by {self.user.username}"
