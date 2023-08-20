import requests
import json

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

print(token)
        #########
price = 30
tax = price*0.1
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
            "name": "hat",
            "description": "Brown hat.",
            "quantity": "5",
            "price": "3",
            "tax": "0.01",
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
          "recipient_name": "Brian Robinson",
          "line1": "4th Floor",
          "line2": "Unit #34",
          "city": "San Jose",
          "country_code": "US",
          "postal_code": "95131",
          "phone": "011862212345678",
          "state": "CA"
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
  'Authorization': 'Bearer ' + token ,
  'Cookie': 'cookie_prefs=T%3D0%2CP%3D0%2CF%3D0%2Ctype%3Dinitial; ts=vreXpYrS%3D1785426761%26vteXpYrS%3D1690734161%26vr%3Da780720a1890a1d678deb0c4fee59964%26vt%3Da780720a1890a1d678deb0c4fee59963%26vtyp%3Dnew; ts_c=vr%3Da780720a1890a1d678deb0c4fee59964%26vt%3Da780720a1890a1d678deb0c4fee59963; tsrce=devdiscoverynodeweb'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.json()['links'][1])

