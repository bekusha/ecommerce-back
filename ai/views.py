from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openai
from django.conf import settings
from .serializers import CarQuerySerializer
from product.models import Product

class OilRecommendationAPIView(APIView):
    def post(self, request):
        serializer = CarQuerySerializer(data=request.data)
        if serializer.is_valid():
            car_model_year = serializer.validated_data['car_model_year']

            try:
                openai.api_key = settings.OPENAI_API_KEY
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "შენ ხარ ძრავების ექსპერტი, მიღებულ მონაცემებზე დაყრდნობით უნდა დააბრუნო ერთი კონკრეტული შესაბამისი ზეთის სიბლანტე და რაოდენობა. დააბრუნე მოკლე პასუხები "},
                        {"role": "user", "content": car_model_year}
                    ]
                )

                if 'choices' in response and len(response['choices']) > 0:
                    message = response['choices'][0]['message']['content'].strip()
                    response_data = {"recommendation": message}

                    # Directly use the expected format (e.g., "5w30") from the message
                    # Assuming the message format directly matches the database format
                    product = Product.objects.filter(viscosity__iexact="5w30").first()  # example static viscosity
                    if product:
                        product_data = {
                            "id":product.id,
                            "name": product.name,
                            "description": product.description,
                            "price": product.price,
                            "volume":product.liter,
                            "viscosity":product.viscosity,
                            "vendor_name": product.get_vendor_name(),
                            "product_url": request.build_absolute_uri(product.get_absolute_url()),
                        }
                        response_data['product'] = product_data
                    else:
                        response_data['message'] = "No exact match found. Please browse our products for similar items."
                        response_data['browse_url'] = request.build_absolute_uri(reverse('product-list'))

                    return Response(response_data)
                else:
                    return Response({"error": "No recommendation found in API response"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
