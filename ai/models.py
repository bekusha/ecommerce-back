from django.db import models

class CarQuery(models.Model):
    car_model_year = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class OilRecommendation(models.Model):
    query = models.ForeignKey(CarQuery, related_name='recommendations', on_delete=models.CASCADE)
    recommendation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
