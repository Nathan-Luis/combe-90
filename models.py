from django.utils import timezone
from django.db import models


# Carousel Image Model
class CarouselImage(models.Model):
    image = models.ImageField(upload_to='carousel/')
    alt_text = models.CharField(max_length=255, help_text="Alternative text for the image")

    def __str__(self):
        return self.alt_text


class Quotation(models.Model):
    reference = models.CharField(max_length=255, unique=True)
    date_created = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=255)  # New field for user's name
    email = models.EmailField()  # New field for user's email
    phone = models.CharField(max_length=20)  # New field for user's contact number
    settled = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.reference


class StockQuantity(models.Model):
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product_name


class MailingList(models.Model):
    email = models.EmailField(unique=True)
    date_subscribed = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email


class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    date_submitted = models.DateTimeField(default=timezone.now)
    contacted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} - {self.email}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    stock_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock_quantity > 0


class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        # Automatically calculate total price based on quantity and unit price
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} ({self.quantity} units)"


# Service Model
class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def short_description(self):
        return self.description[:100] + '...' if len(self.description) > 100 else self.description


# Survey Request Model
class SurveyRequest(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField()
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    survey_address = models.CharField(max_length=255, verbose_name="Survey Address")
    survey_type = models.CharField(max_length=255, verbose_name="Type of Survey")
    location = models.CharField(max_length=255, verbose_name="Manual Location")
    geo_location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Geo-Location")
    additional_info = models.TextField(blank=True, null=True, verbose_name="Additional Information")
    requested_at = models.DateTimeField(default=timezone.now, verbose_name="Requested At")

    def __str__(self):
        return f"{self.name} - {self.survey_type} ({self.requested_at})"


class SurveyImage(models.Model):
    survey_request = models.ForeignKey(SurveyRequest, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='survey_images/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Image for {self.survey_request}"