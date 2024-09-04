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
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system", 
                            "content": """თქვენ ხართ მანქანის ზეთების ექსპერტი. მიიღებთ მანქანის მონაცემებს და უნდა დააბრუნოთ შემდეგი ინფორმაცია ლამაზად და გასაგებად ჩამოწერილი ტექსტური ფორმატით: 
- ზეთის სიბლანტე (მაგ. 5W-30)
- ზეთის რაოდენობა ლიტრებში (ფილტრის შეცვლიანად)
- ცხენის ძალა (HP)
- ნიუტონმეტრი (Nm)
- საწვავის ხარჯი: შერეული (ლ/100კმ), ქალაქი (ლ/100კმ), ავტობანი (ლ/100კმ)

გთხოვთ, დაალაგეთ ინფორმაცია ისე, რომ იყოს მარტივად წაკითხვადი და ვიზუალურად ლამაზი, მაგალითად, თითოეული პარამეტრი ახალ ხაზზე გამოყოფილი და დასათაურებული, რათა მომხმარებელი ადვილად გაერკვეს და სწორად გამოიყენოს."""
                        },
                        {
                            "role": "user", 
                            "content": car_model_year
                        }
                    ]
                )
                print("API Response:", response)

                return Response({"message": response.choices[0].message.content}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
