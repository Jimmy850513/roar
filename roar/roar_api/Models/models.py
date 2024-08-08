from django.db import models

# Create your models here.
class Active_Show_Information(models.Model):
    id = models.ForeignKey()
    show_start_time = models.DateTimeField(null=False)
    show_location = models.CharField(max_length=200,null=False)
    show_location_addr = models.CharField(max_length=200,null=False)
    on_sale = models.BooleanField(default=False)
    price = models.CharField(max_length=200)

class Active_Information(models.Model):
    id = models.CharField(primary_key=True,max_length=200,null=False)
    title = models.CharField(max_length=300,null=False)
    discount_info = models.CharField(max_length=200)
    active_description = models.TextField()
    active_promo_image = models.CharField(max_length=500)
    source_web_name = models.CharField(max_length=200)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)

