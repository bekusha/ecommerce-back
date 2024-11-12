from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

from .serializers import CarQuerySerializer
from product.models import Product
import re
class OilRecommendationAPIView(APIView):
    def post(self, request):
        serializer = CarQuerySerializer(data=request.data)
        if serializer.is_valid():
            car_model_year = serializer.validated_data['car_model_year']

            try:
                # Call OpenAI API to get oil recommendation based on car data
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system", 
                            "content": """თქვენ ხართ მანქანის ზეთების ექსპერტი. მიიღებთ მანქანის მონაცემებს და უნდა დააბრუნოთ შემდეგი ინფორმაცია ლამაზად და გასაგებად ჩამოწერილი ტექსტური ფორმატით: 
                            - ზეთის სიბლანტე 
                            - შესაფერისი ზეთის ფილტრი
                            - ძრავის ზეთის რაოდენობა ლიტრებში 
                            - ცხენის ძალა (HP)
                            - ნიუტონმეტრი (Nm)
                            - საწვავის ხარჯი: შერეული (ლ/100კმ), ქალაქი (ლ/100კმ), ავტობანი (ლ/100კმ)

                            გთხოვთ, დაალაგეთ ინფორმაცია ისე, რომ იყოს მარტივად წაკითხვადი და ვიზუალურად ლამაზი."""
                        },
                        {
                            "role": "user", 
                            "content": car_model_year
                        }
                    ]
                )

                # Get the response text
                ai_response = response.choices[0].message.content
                
                # Normalize viscosities (e.g., 5W-30, 5w30 -> 5W30)
                viscosity_matches = re.findall(r'\b\d{1,2}w[-]?\d{1,2}\b', ai_response.lower())
                
                if viscosity_matches:
                    viscosities = [v.replace('-', '').upper() for v in viscosity_matches]  # Normalize to uppercase and remove hyphen
                    
                    # Find products matching these viscosities
                    products = Product.objects.filter(viscosity__in=viscosities)

                    if products.exists():
                        product_list = []
                        for product in products:
                            product_data = {
                                "id": product.id,
                                "name": product.name,
                                "price": product.price,
                                "description": product.description,
                                "image_url": product.image1.url if product.image1 else None
                            }
                            print(product_data)
                            product_list.append(product_data)
                        
                        return Response({
                            "message": ai_response,
                            "products": product_list
                        }, status=status.HTTP_200_OK)
                    else:
                        return Response({
                            "message": ai_response,
                            "warning": f"ვერ ვიპოვე პროდუქტები ამ სიბლანტეებით: {', '.join(viscosities)}"
                        }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": ai_response,
                        "warning": "სიბლანტე ვერ გამოვლინდა AI პასუხიდან"
                    }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)