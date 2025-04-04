from djongo import models  # Use this for MongoDB integration

class DataEntry(models.Model):
    end_year = models.IntegerField(null=True, blank=True)
    topic = models.CharField(max_length=255, null=True, blank=True)
    sector = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    pestle = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    swot = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    intensity = models.IntegerField(null=True, blank=True)
    likelihood = models.IntegerField(null=True, blank=True)
    relevance = models.IntegerField(null=True, blank=True)

    objects = models.DjongoManager()  

    def __str__(self):
        return f"{self.topic} - {self.region}"


class DataPoint(models.Model):
    name = models.CharField(max_length=255)
    value = models.FloatField()
    
    objects = models.DjongoManager()  

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    
    def __str__(self):
        return self.username
