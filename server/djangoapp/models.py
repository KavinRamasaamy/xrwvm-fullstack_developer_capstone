# Uncomment the following imports before adding the Model code

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# Car Make model
class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Optional extra fields
    country = models.CharField(max_length=100, blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


# Car Model model
class CarModel(models.Model):
    # Many-To-One relationship to Car Make model
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)

    # Dealer ID refers to a dealer created in Cloudant database
    dealer_id = models.IntegerField(blank=True, null=True)

    name = models.CharField(max_length=100)

    # Type choices
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON'),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=SEDAN)

    # Year with min 2015 and max 2023
    year = models.IntegerField(
        default=2023,
        validators=[MinValueValidator(2015), MaxValueValidator(2023)],
    )

    def __str__(self):
        return f"{self.car_make.name} {self.name} ({self.year})"
    
