import re
from django.urls import reverse
from product.serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from django.conf import settings
from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from .serializers import CarQuerySerializer
from product.models import Product

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class OilRecommendationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CarQuerySerializer(data=request.data)
        if serializer.is_valid():
            car_model_year = serializer.validated_data['car_model_year']
            country = "საქართველო"
            current_month = datetime.now().month
            season = "ზამთარი" if current_month in [12, 1, 2] else "ზაფხული" if current_month in [6, 7, 8] else "შუალედური სეზონი"
            try:
                # OpenAI API გამოძახება
                
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": f"""თქვენ ხართ მანქანის ზეთების ექსპერტი საქართველოში.
                                - **მდებარეობა:** {country}
                                - **ამჟამინდელი სეზონი:** {season}
                                - გაითვალისწინეთ, რომ საქართველოს კლიმატი ზამთარში შეიძლება იყოს -5°C-დან 5°C-მდე, ხოლო ზაფხულში 30°C-მდე.
                                - უნდა დააბრუნოთ მხოლოდ **ერთი** რეკომენდებული ზეთის სიბლანტე, შესაბამისი სეზონის მიხედვით.
                                მიიღებთ მანქანის მონაცემებს და უნდა დააბრუნოთ შემდეგი ინფორმაცია ლამაზად და გასაგებად ჩამოწერილი ტექსტური ფორმატით: 
                            - ზეთის სიბლანტე 
                            - ძრავის ზეთის რაოდენობა ლიტრებში 
                            - ცხენის ძალა (HP)
                            - ნიუტონმეტრი (Nm)
                            - საწვავის ხარჯი: შერეული (ლ/100კმ), ქალაქი (ლ/100კმ), ავტობანი (ლ/100კმ)
                            გთხოვთ, დაალაგეთ ინფორმაცია ისე, რომ იყოს მარტივად წაკითხვადი და ვიზუალურად ლამაზი."""
                            
                        },
                        {"role": "user", "content": car_model_year}
                    ]
                )

                ai_response = response.choices[0].message.content if response.choices else "AI პასუხი ვერ მოიძებნა"

                # **სიბლანტის ამოღება**
                viscosity_matches = re.findall(r'\b\d{1,2}W[-]?\d{1,2}\b', ai_response, re.IGNORECASE)
                viscosities = [v.replace('-', '').upper() for v in viscosity_matches]

                # **ლიტრაჟის ამოღება**
                liters_match = re.search(r'(\d{1,2}\.?\d?)\s?ლიტრი', ai_response)
                required_liters = float(liters_match.group(1)) if liters_match else 4  # Default 4 ლიტრი

                # **პროდუქტების მოძებნა**
                if viscosities:
                    products = Product.objects.filter(viscosity__in=viscosities)

                    if products.exists():
                        product_list = ProductSerializer(
                            products, many=True, 
                            context={'required_liters': required_liters, 'all_products': list(products)}
                        ).data

                        return Response({
                            "message": ai_response,
                            "products": product_list
                        }, status=status.HTTP_200_OK)
                    
                    else:
                        return Response({
                            "message": ai_response,
                            "warning": f"ვერ ვიპოვე პროდუქტები ამ სიბლანტეებით: {', '.join(viscosities)}"
                        }, status=status.HTTP_200_OK)

                return Response({
                    "message": ai_response,
                    "warning": "სიბლანტე ვერ გამოვლინდა AI პასუხიდან"
                }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# from datetime import datetime
# import re
# from rest_framework import viewsets, permissions
# from rest_framework.response import Response
# from rest_framework import status
# from openai import OpenAI
# from django.conf import settings
# from .serializers import CarQuerySerializer
# from product.models import Product
# from product.serializers import ProductSerializer

# client = OpenAI(api_key=settings.OPENAI_API_KEY)

# class OilRecommendationAPIView(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticated]

#     def create(self, request):
#         serializer = CarQuerySerializer(data=request.data)
#         if serializer.is_valid():
#             car_model_year = serializer.validated_data['car_model_year']

            # 🛠️ **ქვეყანა და პერიოდი ვამატებთ AI-დაკითხვაში**  
            # country = "საქართველო"
            # current_month = datetime.now().month
            # season = "ზამთარი" if current_month in [12, 1, 2] else "ზაფხული" if current_month in [6, 7, 8] else "შუალედური სეზონი"

#             try:
#                 response = client.chat.completions.create(
#                     model="gpt-4o",
#                     messages=[
#                         {
#                             "role": "system",
#                             "content": f"""თქვენ ხართ მანქანის ზეთების ექსპერტი საქართველოში.
#                                 - **მდებარეობა:** {country}
#                                 - **ამჟამინდელი სეზონი:** {season}
#                                 - გაითვალისწინეთ, რომ საქართველოს კლიმატი ზამთარში შეიძლება იყოს -5°C-დან 5°C-მდე, ხოლო ზაფხულში 30°C-მდე.
#                                 - უნდა დააბრუნოთ მხოლოდ **ერთი** რეკომენდებული ზეთის სიბლანტე, შესაბამისი სეზონის მიხედვით.
#                                 მიიღებთ მანქანის მონაცემებს და უნდა დააბრუნოთ შემდეგი ინფორმაცია ლამაზად და გასაგებად ჩამოწერილი ტექსტური ფორმატით: 
#                             - ზეთის სიბლანტე 
#                             - ძრავის ზეთის რაოდენობა ლიტრებში 
#                             - ცხენის ძალა (HP)
#                             - ნიუტონმეტრი (Nm)
#                             - საწვავის ხარჯი: შერეული (ლ/100კმ), ქალაქი (ლ/100კმ), ავტობანი (ლ/100კმ)
#                             გთხოვთ, დაალაგეთ ინფორმაცია ისე, რომ იყოს მარტივად წაკითხვადი და ვიზუალურად ლამაზი."""
                            
#                         },
#                         {"role": "user", "content": car_model_year}
#                     ]
#                 )

#                 ai_response = response.choices[0].message.content if response.choices else "AI პასუხი ვერ მოიძებნა"

#                 # **სიბლანტის ამოღება**
#                 viscosity_matches = re.findall(r'\b\d{1,2}W[-]?\d{1,2}\b', ai_response, re.IGNORECASE)
#                 viscosities = [v.replace('-', '').upper() for v in viscosity_matches]

#                 # **ლიტრაჟის ამოღება**
#                 liters_match = re.search(r'(\d{1,2}\.?\d?)\s?ლიტრი', ai_response)
#                 required_liters = float(liters_match.group(1)) if liters_match else 4  # Default 4 ლიტრი

#                 # **თუ რამდენიმე სიბლანტე არსებობს, სეზონის მიხედვით ვირჩევთ სწორ ვარიანტს**
#                 recommended_viscosity = viscosities[0] if viscosities else None
#                 if len(viscosities) > 1:
#                     recommended_viscosity = viscosities[0] if season == "ზამთარი" else viscosities[-1]  # ზამთარში თხელი ზეთი, ზაფხულში სქელი

#                 # **პროდუქტების მოძებნა**
#                 if recommended_viscosity:
#                     products = Product.objects.filter(viscosity=recommended_viscosity)

#                     if products.exists():
#                         product_list = ProductSerializer(products, many=True).data

#                         return Response({
#                             "message": ai_response,
#                             "season": season,
#                             "recommended_viscosity": recommended_viscosity,
#                             "products": product_list
#                         }, status=status.HTTP_200_OK)

#                 return Response({
#                     "message": ai_response,
#                     "season": season,
#                     "recommended_viscosity": recommended_viscosity,
#                     "warning": "სიბლანტე ვერ გამოვლინდა AI პასუხიდან"
#                 }, status=status.HTTP_200_OK)

#             except Exception as e:
#                 return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
