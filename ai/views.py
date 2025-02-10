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
import math

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
                # **OpenAI API გამოძახება**
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
                                - რაოდენობა (ლიტრებში) 
                                - ცხენის ძალა (HP)
                                - ნიუტონმეტრი (Nm)
                                - საწვავის ხარჯი: შერეული (ლ/100კმ), ქალაქი (ლ/100კმ), ავტობანი (ლ/100კმ)
                                გთხოვთ, დაალაგეთ ინფორმაცია ისე, რომ იყოს მარტივად წაკითხვადი და ვიზუალურად ლამაზი.
                                მაგალითი პასუხი:
                                📌 რეკომენდირებული ზეთი: 5W30
                                📌 რაოდენობა: 4 ლიტრი
                                📌 ძრავის მახასიათებლები:
                                🚗 ცხენის ძალა: 120 HP
                                ⚙️ ბრუნვის მომენტი: 200 Nm
                                📌 საწვავის მოხმარება:
                                🏙 ქალაქში: 8.5 ლ/100კმ
                                🛣 ტრასაზე: 6.2 ლ/100კმ
                            🔄 შერეული: 7.5 ლ/100კმ
                            📌 საწვავის ხარჯი: 0.5 ლ/100კმ
                                """
                                
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
                    products = list(Product.objects.filter(viscosity__in=viscosities).order_by('-liter'))  # ჯერ ყველაზე დიდი ბოთლები

                    selected_products = []
                    remaining_liters = required_liters

                    # **შევარჩიოთ რაც შეიძლება დიდი ბოთლები**
                    for product in products:
                        if remaining_liters <= 0:
                            break

                        bottle_count = int(remaining_liters // product.liter)  # რამდენი ცალია საჭირო ამ ბოთლიდან
                        if bottle_count > 0:
                            selected_products.append({
                                "product": product,
                                "recommended_quantity": bottle_count
                            })
                            remaining_liters -= bottle_count * product.liter

                    # **თუ მაინც დარჩა მოცულობა, ავავსოთ პატარა ბოთლებით**
                    if remaining_liters > 0:
                        smallest_bottle = min(products, key=lambda p: p.liter)  # ბაზაში არსებული ყველაზე პატარა ბოთლი
                        additional_bottles = math.ceil(remaining_liters / smallest_bottle.liter)  # ➜ დარჩენილი მოცულობის შევსება
                        selected_products.append({
                            "product": smallest_bottle,
                            "recommended_quantity": additional_bottles
                        })

                    # **პროდუქტების სერიალიზაცია**
                    product_list = ProductSerializer(
                        [item["product"] for item in selected_products], many=True,
                        context={'required_liters': required_liters, 'all_products': list(products)}
                    ).data

                    # **დავამატოთ "recommended_quantity" თითოეულ პროდუქტს**
                    for i, item in enumerate(selected_products):
                        product_list[i]["recommended_quantity"] = item["recommended_quantity"]

                    return Response({
                        "message": ai_response,
                        "products": product_list
                    }, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
