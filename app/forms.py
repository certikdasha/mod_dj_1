from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from app.models import CustomUser, Product, Order, Refund


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('money',)


class ProductCreateForm(ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'text', 'price', 'stock',)


class OrderCreateForm(ModelForm):

    class Meta:
        model = Order
        fields = ('num',)


class RefundCreateForm(ModelForm):

    class Meta:
        model = Refund
        exclude = ('ref', )
