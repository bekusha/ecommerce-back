

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AboutPage, ContactPage
from .serializers import AboutPageSerializer, ContactPageSerializer

class AboutPageView(APIView):
    def get(self, request, *args, **kwargs):
        instance = AboutPage.objects.last()  # Assuming you want the last created/updated entry
        serializer = AboutPageSerializer(instance)
        return Response(serializer.data)


class ContactPageView(APIView):
    def get(self, request, *args, **kwargs):
        instance = ContactPage.objects.last()  # Assuming you want the last created/updated entry
        serializer = ContactPageSerializer(instance)
        return Response(serializer.data)
