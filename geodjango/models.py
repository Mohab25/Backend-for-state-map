from django.contrib.gis.db import models 

class SimpleLocation(models.Model):
    name = models.CharField(max_length=100)
    point = models.PointField(srid=3426)

    class Meta:
        ordering=['name']
        verbose_name_plural = 'SimpleLocaitons'
    def __str__(self):
        return self.name

class roads(models.Model):
    med_descri = models.CharField(max_length=254)
    rtt_descri = models.CharField(max_length=254)
    f_code_des = models.CharField(max_length=10)
    iso = models.CharField(max_length=7)
    isocountry = models.CharField(max_length=54)
    geom = models.MultiLineStringField(srid=4326)

    class Meta:
        verbose_name_plural = 'roads'
    def __str__(self):
        return self.med_descri