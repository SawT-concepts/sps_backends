x = [
    'amount',
    'callbackUrl',
    'country',
    'currency',
    'email',
    'firstName',
    'lastName',
    'phoneNumber',
    'transactionId'
]

body = {
    "publicKey": "XPPUBK-fba882fb30efff88ca35a1c86553fd78-X",
    "transactionId": "ref",
    "amount": 100,
    "currency": "NGN",
    "country": "NG",
    "email": "aminu.kabunu@xpresspayments.com",
    "phoneNumber": "xxx",
    "firstName": "Aminu",
    "lastName": "Cincin",
    "callbackUrl": "https://www.sample.xpresspayments.com/resp"
}

hashed_value = ""
for index in x:
    new = body.get(index)
    print (new)
    