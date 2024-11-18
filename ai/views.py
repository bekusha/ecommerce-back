# import math
# from openai import OpenAI
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.conf import settings

# from .serializers import CarQuerySerializer
# from product.models import Product
# import re

# # OpenAI API Key
# client = OpenAI(api_key=settings.OPENAI_API_KEY)

# class OilRecommendationAPIView(APIView):
#     def post(self, request):
#         serializer = CarQuerySerializer(data=request.data)
#         if serializer.is_valid():
#             car_model_year = serializer.validated_data['car_model_year']

#             try:
#                 # Call OpenAI API to get oil recommendation based on car data
#                 response = client.chat.completions.create(
#                     model="gpt-4-turbo",
#                    messages=[
#                         {
#                             "role": "system",
#                             "content": """თქვენ ხართ მანქანის ზეთების ექსპერტი. მიიღებთ მანქანის მონაცემებს და უნდა დააბრუნოთ შემდეგი ინფორმაცია ლამაზად და გასაგებად ჩამოწერილი ტექსტური ფორმატით:
#                             - ზეთის სიბლანტე 
#                             - შესაფერისი ზეთის ფილტრი
#                             - ძრავის ზეთის რაოდენობა ლიტრებში 
#                             - ცხენის ძალა (HP)
#                             - ნიუტონმეტრი (Nm)
#                             - საწვავის ხარჯი: შერეული (ლ/100კმ), ქალაქი (ლ/100კმ), ავტობანი (ლ/100კმ)

#                             გთხოვთ, დაალაგეთ ინფორმაცია ისე, რომ იყოს მარტივად წაკითხვადი და ვიზუალურად ლამაზი. არ დაამატო არანაირი ზედმეტი ტექსტი"""
#                         },
#                         {
#                             "role": "user",
#                             "content": car_model_year
#                         }
#                     ]
#                 )

#                 # Get the response text from AI
#                 ai_response = response.choices[0].message.content
#                 print(ai_response)
#                 # Extract the required viscosity and oil volume from AI response
#                 viscosity_matches = re.findall(r'\b\d{1,2}W[-]?\d{1,2}\b', ai_response.upper())
#                 volume_match = re.search(r'დაახლოებით\s*(\d+(?:\.\d+)?)\s*ლიტრ\b', ai_response.lower())
#                 print("Volume Match:", volume_match.group() if volume_match else "No match found for volume")

#                 print(viscosity_matches, volume_match)
#                 if viscosity_matches and volume_match:
#                     viscosities = [v.replace('-', '').upper() for v in viscosity_matches]
#                     required_liters = float(re.findall(r'\d+(?:\.\d+)?', volume_match.group())[0])

#                     # Find available products with specified viscosities
#                     products = Product.objects.filter(viscosity__in=viscosities).order_by('-liter')

#                     selected_products = []
#                     remaining_volume = required_liters

#                     for product in products:
#                         if remaining_volume <= 0:
#                             break
#                         if product.liter and product.liter > 0:
#                             count = math.floor(remaining_volume / product.liter)
#                             if count > 0:
#                                 selected_products.append({
#                                     'product': product,
#                                     'count': count
#                                 })
#                                 remaining_volume -= count * product.liter

#                     # If there's still remaining volume, add the smallest available product
#                     if remaining_volume > 0:
#                         smallest_product = products.filter(liter__gte=remaining_volume).order_by('liter').first()
#                         if smallest_product:
#                             selected_products.append({
#                                 'product': smallest_product,
#                                 'count': 1
#                             })
#                             remaining_volume -= smallest_product.liter

#                     # Prepare the product list with total price calculation
#                     product_list = []
#                     total_price = 0
#                     for item in selected_products:
#                         product = item['product']
#                         count = item['count']
#                         product_data = {
#                             "id": product.id,
#                             "name": product.name,
#                             "volume": product.liter,
#                             "price_per_unit": product.price,
#                             "count": count,
#                             "total_price": product.price * count,
#                             "image_url": product.image1.url if product.image1 else None
#                         }
#                         product_list.append(product_data)
#                         total_price += product_data["total_price"]

#                     return Response({
#                         "message": ai_response,
#                         "products": product_list,
#                         "total_price": total_price
#                     }, status=status.HTTP_200_OK)

#                 else:
#                     return Response({
#                         "message": ai_response,
#                         "warning": "სიბლანტე ან ლიტრაჟი ვერ გამოვლინდა AI პასუხიდან"
#                     }, status=status.HTTP_200_OK)

#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
                                "viscosity": product.viscosity,
                                "liter": product.liter,
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