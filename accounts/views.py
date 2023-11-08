from .models import Account
from .serializers import AccountSerializer
from rest_framework.generics import CreateAPIView

class AccountView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer