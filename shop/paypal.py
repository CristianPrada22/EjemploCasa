import sys
from django.conf import settings
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "ARZk3IYo3IZ4VLsf6tKoFxLkJzxV6_Ywg8-8SeLq19C67NsvAuTIeDtILVJ0gUgnXoPuEFqOxJSyW5Re"
        self.client_secret = "EML_y6k45KF_db79kiksQLzhl8nJez-XW-rhpym080yUn1rG1YpykrUy2xcdnhk6w1W7gtxLnSQNBLG0"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
