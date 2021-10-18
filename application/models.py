from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, auth
from django.db.models.base import ModelState
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.deletion import CASCADE
from django.utils import timezone
# Create your models here.

# CATEGORY MODEL 
class Category(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to='category_icon/')

    def __str__(self):
        return f"{self.name}"




#REVIEW MODEL
class Review(models.Model):
    text = models.TextField()
    star_num = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    posted_at = models.DateTimeField(auto_now=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
            return f"{self.text}"
# PRODUCT MODEL 
class Product(models.Model):
    name = models.CharField(max_length=50)
    tag_line = models.CharField(max_length=20, default=None)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=CASCADE)
    # features = models.ManyToManyField(Feature) 
    reviews = models.ManyToManyField(Review)
    aff_link = models.URLField(max_length=255)
    added_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
            return f"{self.name}"

    def get_primary_picture(self):
        selected_picture = Picture.objects.filter(product = self, is_primary=True)
        if selected_picture.exists():
            selected_picture = selected_picture[0]
            return selected_picture
        return None


    def get_all_pictures(self):
            selected_picture = Picture.objects.filter(product = self, is_primary=False)
            if selected_picture.exists():
                return selected_picture
            return None

# FEATURE MODEL 
class Feature(models.Model):
    text = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
            return f"{self.text}"
        

# PICTURE MODEL 
class Picture(models.Model):
    image = models.ImageField(upload_to='product_pictures/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, default=None)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.image}"


            
# FAVOURITE MODEL 
class Favourite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now=True)

