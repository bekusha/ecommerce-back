import re
from django.urls import reverse
from product.serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from django.conf import settings
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

            try:
                # OpenAI API გამოძახება
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": """თქვენ ხართ მანქანის ზეთების ექსპერტი. 
                                უნდა დააბრუნოთ:
                                - **ზეთის სიბლანტე:** (მაგ. 5W-30)
                                - **ძრავის ზეთის რაოდენობა:** (ლიტრებში)
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
