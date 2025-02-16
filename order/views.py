import json
from django.shortcuts import get_object_or_404
from order.serializers import OrderItemSerializer, OrderSerializer, SavedOrderSerializer
import logging
import requests
logger = logging.getLogger(__name__)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from order.models import Order, OrderItem, SavedOrder  # Order, OrderItem და SavedOrder მოდელებიდან
from product.models import Product  # Product მოდელიდან'
from django.conf import settings
import base64
from django.core.cache import cache
from django.http import HttpResponse

class BOGPaymentAPI:
    BASE_URL = 'https://api.bog.ge/payments/v1'

    @staticmethod
    def get_access_token():
        """ იღებს ახალ ACCESS_TOKEN-ს, თუ ძველი ვადაგასულია. """
        access_token = cache.get('bog_access_token')
        
        if access_token:
            return access_token
        
        url = 'https://oauth2.bog.ge/auth/realms/bog/protocol/openid-connect/token'
        print("info from settings file" , settings.BOG_CLIENT_ID, settings.BOG_CLIENT_SECRET)
        auth_str = f"{settings.BOG_CLIENT_ID}:{settings.BOG_CLIENT_SECRET}"
        b64_auth_str = base64.b64encode(auth_str.encode()).decode()

        headers = {
            'Authorization': f'Basic {b64_auth_str}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        payload = {
            "grant_type": "client_credentials"
        }
        print("Payload",payload)

        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            expires_in = response.json().get("expires_in", 3600)

            cache.set('bog_access_token', access_token, expires_in - 60)

            return access_token
        else:
            logger.error("❌ ვერ მივიღეთ ACCESS_TOKEN: %s", response.json())
            return None

    @staticmethod
    def create_order(order_id, amount, currency='GEL'):
        """ ქმნის შეკვეთას და აბრუნებს გადახდის ბმულს. """
        access_token = BOGPaymentAPI.get_access_token()
        if not access_token:
            return None

        url = 'https://api.bog.ge/payments/v1/ecommerce/orders'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        API_BASE_URL=settings.API_BASE_URL
        payload = {
            'order_id': str(order_id),
            'amount': float(amount),
            'currency': currency,
            'callback_url': f"{API_BASE_URL}",
            'return_url': f"{API_BASE_URL}",
        }
        basket_items = []
        order_items = OrderItem.objects.filter(order_id=order_id)

        for item in order_items:
            basket_items.append({
                'quantity': item.quantity,
                "unit_price": float(item.product.price),
                "product_id": str(item.product.id),
            })
        total_amount = sum(item["quantity"] * item["unit_price"] for item in basket_items)
        API_BASE_URL=settings.API_BASE_URL
        redirect_url = f"{API_BASE_URL}order/redirect/{order_id}"
        payload = {
            "callback_url": f"{API_BASE_URL}order/callback/",
            "external_order_id": str(order_id),
            "purchase_units": {
                "currency": currency,
                "total_amount": float(total_amount),
                "basket": basket_items  # ✅ კალათაში ვამატებთ პროდუქტებს
            },
             "redirect_urls": {
                "fail": redirect_url,  # ❌ გადახდის ჩავარდნის შემთხვევაში
                "success": redirect_url  # ✅ გადახდის წარმატების შემთხვევაში
        }
        }
        print("Sending order request with payload:", json.dumps(payload, indent=2))

        response = requests.post(url, json=payload, headers=headers)
        print("BOG API Response:", response.status_code, response.text)  # ✅ Debugging

        if response.status_code == 201:
            return response.json().get('_links', {}).get('redirect')
        else:
            logger.error("❌ ვერ შევქმენით შეკვეთა: %s", response.json())
            return None
   



def redirect_after_payment(request, order_id):
    """ გადახდის დასრულების შემდეგ გადამისამართება აპლიკაციაში """
    try:
        order = Order.objects.get(id=order_id)
        payment_status = order.payment_status  # მიიღე გადახდის სტატუსი

        if payment_status == "paid":
            redirect_url = f"krossGeorgia://payment-success/{order_id}"
        else:
            redirect_url = "krossGeorgia://payment-failed"

        html_response = f"""
        <html>
        <head>
            <script type="text/javascript">
                window.location.href = "{redirect_url}";
            </script>
            <meta http-equiv="refresh" content="0; url={redirect_url}" />
        </head>
        <body>
            <p>Redirecting... If nothing happens, <a href="{redirect_url}">click here</a>.</p>
        </body>
        </html>
        """
        return HttpResponse(html_response)

    except Order.DoesNotExist:
        return HttpResponse("❌ Order not found", status=404)


class PaymentCallbackApiView(APIView):    
    permission_classes = [AllowAny]  
    def post(self, request):
        payment_data = request.data
        order_id = payment_data.get('order_id')
        status = payment_data.get('status')

        if not order_id or not status:
            return Response({"error": "Invalid payment data"}, status=status.HTTP_400_BAD_REQUEST)

        try: 
            order = Order.objects.get(id=order_id)
            
            if status == "paid":
                order.payment_status = "paid"
            elif status == "pending":
                order.payment_status = "pending"
            elif status == "failed":
                order.payment_status = "failed"
            
            order.save()

            return Response({"message": "Payment status updated successfully"}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

            

class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


# get order details
class OrderDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        order_serializer = OrderSerializer(order)
        order_items = OrderItem.objects.filter(order=order)
        order_items_serializer = OrderItemSerializer(order_items, many=True)

        return Response({
            'order': order_serializer.data,
            'order_items': order_items_serializer.data,
            'payment_status': order.payment_status
        }, status=status.HTTP_200_OK)


# Create your views here.
# @transaction.atomic
class PurchaseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        order_items = request.data.get('order_items', [])
        order_type = request.data.get('order_type', 'product_delivery')  
        phone = request.data.get('phone')
        address = request.data.get('address')
        email = request.data.get('email')
        logger.error(f"Received request data: {request.data}") 
        print("order items" , order_items)
        
        if not order_items:
            logger.error("❌ order_items ცარიელია")
            return Response({"error": "order_items ცარიელია"}, status=status.HTTP_400_BAD_REQUEST)


        # გადაამოწმე სწორი ტიპი
        if order_type not in dict(Order.ORDER_TYPE_CHOICES):
            return Response({"detail": "Invalid order type."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new order
        order = Order.objects.create(user=user,
                                    order_type=order_type,
                                    phone=phone,
                                    address=address,
                                    email=email
                                     )
                                     

        total_amount = 0  # მთლიანი თანხა
        
        for item in order_items:
            product_id = item.get("product_id") or item.get("id")
            quantity = item.get("quantity")
            
            if not product_id:
                return Response({"error": "პროდუქტის ID არ არის მითითებული"}, status=status.HTTP_400_BAD_REQUEST)
            
            product = get_object_or_404(Product, id=product_id)
            
            if quantity > product.quantity:
                return Response({"detail": f"{product.name} მარაგში არ არის საკმარისი."}, status=status.HTTP_400_BAD_REQUEST)

            OrderItem.objects.create(order=order, product=product, quantity=quantity)
            
            product.quantity -= quantity
            product.save()

            total_amount += product.price * quantity  # შეკვეთის საერთო თანხა

        # **გადახდის ბმულის გენერირება**
        payment_url = BOGPaymentAPI.create_order(order.id, total_amount)

        if not payment_url:
            return Response({"error": "გადახდის ბმულის გენერირება ვერ მოხერხდა"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "message": "შეკვეთა წარმატებით გაფორმდა!",
            "order_id": order.id,
            "payment_url": payment_url
        }, status=status.HTTP_201_CREATED)


class SavedOrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        saved_orders = SavedOrder.objects.filter(user=request.user)
        serializer = SavedOrderSerializer(saved_orders, many=True)
        return Response(serializer.data) 
