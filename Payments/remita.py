from django.conf import settings
import requests
from .help import hash_keys

class Remita:
    REMITA_PUBLIC_KEY = settings.REMITA_PUBLIC_KEY
    base_url = "https://remitademo.net/payment/v1/payment/query"

    def verify_payment (self, ref, *args, **kwargs):
        payload = {}
        hash_value = hash_keys(ref)
        path = f'/{ref}'
        url = self.base_url + path

        headers = {
            'publicKey': self.REMITA_PUBLIC_KEY,
            'Content-Type': 'application/json',
            'TXN_HASH': str(hash_value)
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            response_data = response.json()
            return (response_data['responseData']), (response_data['responseCode'])
        else:
            response_data = response.json()
            return (response_data['responseData']), (response_data['responseCode'])
            
            
# qapusfsviv
