import requests
from django.conf import settings
#? Class for processing all Xpress requests from their api
class XpressPay:
    XPRESS_PAY_PUBLIC_KEY = settings.XPRESS_PAY_PUBLIC_KEY
    base_url = "https://myxpresspay.com:6004/api/Payments/VerifyPayment"

    def verify_payment (self, ref, *args, **kwargs):

        data = {
            "transactionId": ref,
        }

        #todo replace here with xpress pay secret key
        headers = {
            "Authorization": f"Bearer {self.XPRESS_PAY_PUBLIC_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(self.base_url, headers=headers, json=data)

        print(response.json())

        #check response status code