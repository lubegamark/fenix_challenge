from django.db import models


class MomoRequest(models.Model):
    PENDING = 'PENDING'
    SUCCESSFUL = 'SUCCESSFUL'
    FAILED = 'FAILED'
    STATUS_CHOICES = (
        (PENDING, PENDING),
        (SUCCESSFUL, SUCCESSFUL),
        (FAILED, FAILED),
    )
    customer = models.CharField(max_length=250,)
    amount = models.DecimalField(decimal_places=4, max_digits=20)
    status = models.CharField(
        max_length=250,
        choices=STATUS_CHOICES,
        default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    last_edit_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Initialize a momo payment after saving
        """
        super().save(*args, **kwargs)
        make_momo_collection_request()


def make_momo_collection_request():
    pass


def get_access_token():

    api_base_url = os.environ.get('MOMOPAY_BASE_URL')
    api_user_id = os.environ.get('MOMOPAY_USER_ID')
    subscription_key = os.environ.get('MOMOPAY_SUBSCRIPTION_PRIMARY_KEY')
    api_secret_key = os.environ.get('MOMOPAY_API_SECRET')

    auth=HTTPBasicAuth(
        api_user_id,
        api_secret_key)

    headers = {
        'X-Reference-Id': api_user_id,
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
        }

    token_url = "{}{}".format(api_base_url,'collection/token/')

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
