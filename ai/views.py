from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openai
from django.conf import settings
from .serializers import CarQuerySerializer

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
                        {"role": "system", "content": "you are engine oils expert assistant, return the best analyzed info in Georgian native language, focuse on oils consistency and litters and focuse on good translate into georgian, return short answers"},
                        {"role": "user", "content": car_model_year}
                    ]
                )

                if 'choices' in response and len(response['choices']) > 0:
                    message = response['choices'][0]
                    if 'message' in message and 'content' in message['message']:
                        recommendation = message['message']['content'].strip()
                    else:
                        return Response({"error": "Malformed response from API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"error": "No recommendation found in API response"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response({"recommendation": recommendation})
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
