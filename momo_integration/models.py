from django.db import models
import os
import requests
import json
from requests.auth import HTTPBasicAuth


class MomoRequest(models.Model):
    PENDING = 'PENDING'
    SUCCESSFUL = 'SUCCESSFUL'
    FAILED = 'FAILED'
    STATUS_CHOICES = (
        (PENDING, PENDING),
        (SUCCESSFUL, SUCCESSFUL),
        (FAILED, FAILED),
    )
    customer = models.CharField(max_length=250)
    msisdn = models.CharField(max_length=250)
    x_reference_id = models.UUIDField()
    amount = models.DecimalField(decimal_places=4, max_digits=20)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edit_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Initialize a momo payment after saving
        """
        super().save(*args, **kwargs)
        make_momo_collection_request(self.id, self.msisdn, self.amount)


def get_access_token():

    api_base_url = os.environ.get('MOMOPAY_BASE_URL')
    api_user_id = os.environ.get('MOMOPAY_USER_ID')
    subscription_key = os.environ.get('MOMOPAY_SUBSCRIPTION_PRIMARY_KEY')
    api_secret_key = os.environ.get('MOMOPAY_API_SECRET')

    auth = HTTPBasicAuth(
        api_user_id,
        api_secret_key)

    headers = {
        'X-Reference-Id': api_user_id,
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
        }

    token_url = "{}{}".format(api_base_url, 'collection/token/')

    r = requests.post(
        url=token_url,
        headers=headers,
        data=json.dumps({}),
        auth=auth,
        verify=True)

    print(r.status_code)
    response_data = json.loads(r.text)
    print(response_data)

    return response_data["access_token"]


def make_momo_collection_request(momorequest_id, msisdn, amount):
    callback_url = os.environ.get('MOMOPAY_CALLBACK_URL')
    target_environment = os.environ.get('MOMOPAY_TARGET_ENVIRONMENT')
    api_base_url = os.environ.get('MOMOPAY_BASE_URL')
    subscription_key = os.environ.get('MOMOPAY_SUBSCRIPTION_PRIMARY_KEY')

    access_token = get_access_token()

    momo_request = MomoRequest.objects.get(id=momorequest_id)

    headers = {
        'Authorization': access_token,
        'X-Callback-Url': callback_url,
        'X-Reference-Id': str(momo_request.x_reference_id),
        'X-Target-Environment': target_environment,
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    payer_message = "Payment to Fenix"
    payee_message = "Payment from {}".format(msisdn)

    request_data = {
        "amount": amount,
        "currency": "EUR",
        "externalId": str(momorequest_id),
        "payer": {
            "partyIdType": "MSISDN",
            "partyId": msisdn
        },
        "payerMessage": payer_message,
        "payeeNote": payee_message,
    }
    request_json = json.dumps(request_data, separators=(',', ':'))

    payment_url = api_base_url + "/requesttopay"

    r = requests.post(
        url=payment_url,
        data=request_json,
        headers=headers,
    )

    if r.status_code != 202:
        momo_request.status = MomoRequest.FAILED
    else:
        print("Request Received")
    momo_request.save()
    return momorequest_id


def poll_transaction(momorequest_id):
    target_environment = os.environ.get('MOMOPAY_TARGET_ENVIRONMENT')
    api_base_url = os.environ.get('MOMOPAY_BASE_URL')
    subscription_key = os.environ.get('MOMOPAY_SUBSCRIPTION_PRIMARY_KEY')

    access_token = get_access_token()
    momo_request = MomoRequest.objects.get(id=momorequest_id)

    headers = {
        'Authorization': access_token,
        'X-Reference-Id': str(momo_request.x_reference_id),
        'X-Target-Environment': target_environment,
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    status_url = api_base_url + "/collection/v1_0/requesttopay/{}".format(
        momo_request.x_reference_id)

    r = requests.get(
        url=status_url,
        headers=headers,
    )

    print(r.status_code)
    response_data = json.loads(r.text)
    response_data["status"]

    if r.status_code == 200:
        if response_data["status"] == 'SUCCESSFUL':
            momo_request.status = MomoRequest.SUCCESSFUL
        elif response_data["status"] == 'PENDING':
            # transaction is still pending
            pass
        else:
            # Any other situation means it failed
            momo_request.status = MomoRequest.FAILED
    momo_request.save()
    return momorequest_id
