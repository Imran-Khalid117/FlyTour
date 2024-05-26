from django.db import models


# Create your models here.

class CategoryModel(models.Model):
    """
    This model class is inherited from models.Model class.

    This class is used to define the fields and name the database table for `Category`
    """
    category_name = models.CharField(max_length=250, blank=False)

    class Meta:
        db_table = "db_category"

