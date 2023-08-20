from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .models import UserProfile, PaymentAccounts
from .serializer import UserProfileSerializer, UserNotificationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import requests
import json

class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request):
        print(request.user)
        serializer = UserProfileSerializer(request.user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = UserProfile.objects.get(email=request.user.email)
        user.avatar = request.data['avatar']
        user.save()
        return Response({'message': 'Image updated'}, status=status.HTTP_200_OK)


class RegisterUserView(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        # if email is already in use
        if UserProfile.objects.filter(email=request.data['email']).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllUsersView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        if request.user.is_staff:
            users = UserProfile.objects.all()
            serializer = UserProfileSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AllCourses(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            data = requests.get('http://api')
            return data.json()
        except Exception as e:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class AllTutors(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            data = request.get('http://api')
            return data.json()
        except Exception as e:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



class TutorRequest(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:

            requests.post('http://api', {'tutor_id': request.data["tutor_id"],
                                         'client_id': request.user.id,
                                         'date_time': request.data["date_time"],
                                         'text': request.data["text"],
                                         'course_id': request.data["course_id"]
                                         })
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserNotification(APIView):

    def post(self, request):
        # tutor_id = request.data["tutor_id"]
        # user_id = request.data["user_id"]
        # status = request.data["status"]
        # text = request.data["text"]
        # price = request.data["price"]

        serializer = UserNotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        usernotifications = UserNotification.objects.all()
        serializer = UserNotificationSerializer(usernotifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Payment(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tutor_id = request.data["tutor_id"]
        usernotifications = UserNotification.objects.get(id = request.data["usernotifications_id"])


        ####GET ACCESS TOKEN#####
        url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
        payload = 'grant_type=client_credentials'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic QWNXbEJQQWxhUGFXUTlqWkx0b1kyTFVQdGptZU5rd2RfdTFBZEJSbUxNOWlOUTRnVHllYTVUMGZkMzF6a0RWNEhQaG5zT2VVdU8wUkRrTTU6RU52OG1SN284TjFxNHhFeHNib2c4UnhyRFBzM2c4cGdUU1hOSGZyWGEtdHhjcG9ZcXNVOHN2VXd2MHViT01SVTdtOWNQa1VRd0xLczdGV3k=',
            'Cookie': 'cookie_prefs=T%3D0%2CP%3D0%2CF%3D0%2Ctype%3Dinitial; ts=vreXpYrS%3D1785426761%26vteXpYrS%3D1690734161%26vr%3Da780720a1890a1d678deb0c4fee59964%26vt%3Da780720a1890a1d678deb0c4fee59963%26vtyp%3Dnew; ts_c=vr%3Da780720a1890a1d678deb0c4fee59964%26vt%3Da780720a1890a1d678deb0c4fee59963; tsrce=devdiscoverynodeweb'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        token = response.json()['access_token']

        #########
        price = 30
        tax = price * 0.1
        total = price + tax

        url = "https://api-m.sandbox.paypal.com/v1/payments/payment"

        payload = json.dumps({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [
                {
                    "amount": {
                        "total": total,
                        "currency": "USD",
                        "details": {
                            "subtotal": price,
                            "tax": tax,
                            "shipping": "0.00",
                            "handling_fee": "0.00",
                            "shipping_discount": "0.00",
                            "insurance": "0.00"
                        }
                    },
                    "description": "The payment transaction description.",
                    "custom": "EBAY_EMS_90048630024435",
                    "invoice_number": "48787589673",
                    "payment_options": {
                        "allowed_payment_method": "INSTANT_FUNDING_SOURCE"
                    },
                    "soft_descriptor": "ECHI5786786",
                    "item_list": {
                        "items": [
                            {
                                "name": "education",
                                "description": "education service",
                                "quantity": "1",
                                "price": price,
                                "tax": tax,
                                "sku": "1",
                                "currency": "USD"
                            },
                            {
                                "name": "handbag",
                                "description": "Black handbag.",
                                "quantity": "1",
                                "price": "15",
                                "tax": "0.02",
                                "sku": "product34",
                                "currency": "USD"
                            }
                        ],
                        "shipping_address": {
                            "recipient_name": "",
                            "line1": "",
                            "line2": "",
                            "city": "",
                            "country_code": "",
                            "postal_code": "",
                            "phone": "",
                            "state": ""
                        }
                    }
                }
            ],
            "note_to_payer": "Contact us for any questions on your order.",
            "redirect_urls": {
                "return_url": "http://127.0.0.1:8000/payment_return/pid/",
                "cancel_url": "http://127.0.0.1:8000/payment_cancel/pid/"
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token,
            'Cookie': 'cookie_prefs=T%3D0%2CP%3D0%2CF%3D0%2Ctype%3Dinitial; ts=vreXpYrS%3D1785426761%26vteXpYrS%3D1690734161%26vr%3Da780720a1890a1d678deb0c4fee59964%26vt%3Da780720a1890a1d678deb0c4fee59963%26vtyp%3Dnew; ts_c=vr%3Da780720a1890a1d678deb0c4fee59964%26vt%3Da780720a1890a1d678deb0c4fee59963; tsrce=devdiscoverynodeweb'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        link = response.json()['links'][1]



        #### Save payment account in DB ######

        paymentAccount = PaymentAccounts()
        paymentAccount.payment_id = response.json()['id']
        paymentAccount.user_id = usernotifications.user_id
        paymentAccount.tutor_id = usernotifications.tutor_id
        paymentAccount.status = 'false'

        ##########

        return Response({'link': link}, status=status.HTTP_200_OK)




class PaymentReturn(APIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.method == 'GET':
            payer_id = self.request.GET.get('PayerID', None)
            payment_id = self.request.GET.get('paymentID', None)
            if payer_id is not None:

                ####GET ACCESS TOKEN#####
                url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
                payload = 'grant_type=client_credentials'
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Basic QWNXbEJQQWxhUGFXUTlqWkx0b1kyTFVQdGptZU5rd2RfdTFBZEJSbUxNOWlOUTRnVHllYTVUMGZkMzF6a0RWNEhQaG5zT2VVdU8wUkRrTTU6RU52OG1SN284TjFxNHhFeHNib2c4UnhyRFBzM2c4cGdUU1hOSGZyWGEtdHhjcG9ZcXNVOHN2VXd2MHViT01SVTdtOWNQa1VRd0xLczdGV3k=',
                    'Cookie': 'cookie_prefs=T%3D0%2CP%3D0%2CF%3D0%2Ctype%3Dinitial; ts=vreXpYrS%3D1785426761%26vteXpYrS%3D1690734161%26vr%3Da780720a1890a1d678deb0c4fee59964%26vt%3Da780720a1890a1d678deb0c4fee59963%26vtyp%3Dnew; ts_c=vr%3Da780720a1890a1d678deb0c4fee59964%26vt%3Da780720a1890a1d678deb0c4fee59963; tsrce=devdiscoverynodeweb'
                }
                response = requests.request("POST", url, headers=headers, data=payload)
                token = response.json()['access_token']
                #########


                ####Access Payment#####
                url = "https://api.sandbox.paypal.com/v1/payments/payment/" + payment_id + "/execute"

                payload = json.dumps({
                    "payer_id": payer_id
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token,
                    'Cookie': 'cookie_prefs=T%3D0%2CP%3D0%2CF%3D0%2Ctype%3Dinitial; ts=vreXpYrS%3D1785426761%26vteXpYrS%3D1690734161%26vr%3Da780720a1890a1d678deb0c4fee59964%26vt%3Da780720a1890a1d678deb0c4fee59963%26vtyp%3Dnew; ts_c=vr%3Da780720a1890a1d678deb0c4fee59964%26vt%3Da780720a1890a1d678deb0c4fee59963'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                return Response(response, status=status.HTTP_200_OK)

            else:
                return Response(status.HTTP_405_METHOD_NOT_ALLOWED)




