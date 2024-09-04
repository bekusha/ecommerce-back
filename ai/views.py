from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from django.conf import settings
client = OpenAI(api_key=settings.OPENAI_API_KEY)

from .serializers import CarQuerySerializer
from product.models import Product

class OilRecommendationAPIView(APIView):
    def post(self, request):
        serializer = CarQuerySerializer(data=request.data)
        if serializer.is_valid():
            car_model_year = serializer.validated_data['car_model_year']

            try:
                response = client.chat.completions.create(model="gpt-4o",
                messages=[
                    {"role": "system", "content": "you are the best professional of engine oils, you should response viscosity and oil capacity based on the requested car data return short answers oil viscosity and capacity in litters"},
                    {"role": "user", "content": car_model_year}
                ])
                print("API Response:", response)

                return Response({"message": response.choices[0].message.content}, status=status.HTTP_200_OK)
                

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
