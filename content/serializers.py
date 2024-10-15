from rest_framework import serializers
from .models import AboutPage, ContactPage, MainPage

class AboutPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutPage
        fields = '__all__'

class ContactPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPage
        fields = '__all__'

class MainPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPage
        fields = ['title', 'image', 'action']