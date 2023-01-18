from urllib import response
from django.conf import settings
import requests


class PayStack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    base_url = "https://api.paystack.co"

    def verify_payment(self, ref, *args, **kwargs):
        reff = ref
        print("passssssssssssssss")
        print(reff)

        path = f'/transaction/verify/{reff}'
        print('debug')

        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            "Content-Type": 'application/json',
        }
        print('debug22')
        url = self.base_url + path
        response = requests.get(url, headers=headers)

        print('debug27')
        if response.status_code == 200:
            print('debug2000')
            response_data = response.json()
            return response_data['status'], response_data['data']

        response_data = response.json()
        print(response_data)
        return response_data["status"], response_data["message"]
