from django.db import models


# Create your models here.

class CategoryModel(models.Model):
    category_name = models.CharField(max_length=250, blank=False)

    class Meta:
        db_table = "db_category"

