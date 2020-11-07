from django.contrib.gis.db import models 

class PAU(models.Model):
    objectid_1 = models.BigIntegerField(null=True)
    objectid = models.BigIntegerField(null=True)
    pau_name = models.CharField(max_length=254,null=True)
    village = models.CharField(max_length=254,null=True)
    pau_code = models.CharField(max_length=254,null=True)
    vill_code = models.CharField(max_length=254,null=True)
    st_name = models.CharField(max_length=254,null=True)
    st_code = models.FloatField(null=True)
    loc_name = models.CharField(max_length=254,null=True)
    loc_code = models.CharField(max_length=254,null=True)
    au_name = models.CharField(max_length=254,null=True)
    au_code = models.CharField(max_length=254,null=True)
    elec = models.FloatField(null=True)
    phone = models.FloatField(null=True)
    wc = models.FloatField(null=True)
    oid_join = models.CharField(max_length=254,null=True)
    state = models.CharField(max_length=254,null=True)
    county = models.CharField(max_length=254,null=True)
    au = models.CharField(max_length=254,null=True)
    pau = models.CharField(max_length=254,null=True)
    m_0_4 = models.BigIntegerField(null=True)
    f_0_4 = models.BigIntegerField(null=True)
    m_5_14 = models.BigIntegerField(null=True)
    f_5_14 = models.BigIntegerField(null=True)
    m_15_24 = models.BigIntegerField(null=True)
    f_15_24 = models.BigIntegerField(null=True)
    m_25_44 = models.BigIntegerField(null=True)
    f_25_44 = models.BigIntegerField(null=True)
    m_45_plus = models.BigIntegerField(null=True)
    f_45_plus = models.BigIntegerField(null=True)
    tot_pop = models.BigIntegerField(null=True)
    tot_hhs = models.BigIntegerField(null=True)
    shape_leng = models.FloatField(null=True)
    shape_le_1 = models.FloatField(null=True)
    shape_area = models.FloatField(null=True)
    fam = models.CharField(max_length=254,null=True)
    census = models.BigIntegerField(null=True)
    es1 = models.BigIntegerField(null=True)
    es2 = models.BigIntegerField(null=True)
    geom = models.MultiPolygonField(srid=4326,null=True)

    def __str__(self) -> str:
        return self.pau_name
    class meta:
        ordering=["-objectid_1"]

class ShortestPath(models.Model):
    pathid = models.IntegerField()
    geom = models.MultiLineStringField(srid=4326)

    def __str__(self) -> str:
        return str(self.id)
    class meta:
        ordering=['id'] 
