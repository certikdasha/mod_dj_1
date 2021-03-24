import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from app.forms import CustomUserCreationForm, ProductCreateForm, OrderCreateForm, RefundCreateForm
from app.models import Product, CustomUser, Order, Refund


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'index.html'
    login_url = 'login/'
    extra_context = {'order_form': OrderCreateForm(), 'create_form': ProductCreateForm()}
    paginate_by = 5


class Login(LoginView, ListView):
    success_url = '/'
    template_name = 'login.html'
    model = Product
    paginate_by = 5


class Register(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = '/'


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'


class ProductCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    http_method_names = ['post']
    form_class = ProductCreateForm
    success_url = '/'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return super().form_valid(form=form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ('name', 'text', 'price', 'stock',)
    template_name_suffix = '_update_form'
    success_url = '/'


class ProductBuyView(LoginRequiredMixin, CreateView):
    login_url = 'login/'
    http_method_names = ['post']
    form_class = OrderCreateForm
    success_url = '/'

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.product_id = self.kwargs['pk']
        self.object.user_id = self.request.user.id

        in_stock = Product.objects.get(id=self.object.product_id).stock - int(self.request.POST['num'])

        all_price = Product.objects.get(id=self.kwargs['pk']).price * int(self.request.POST['num'])
        money = self.request.user.money - all_price

        if in_stock >= 0 and money >= 0:

            product = Product.objects.get(id=self.object.product_id)
            self.request.user.money = money
            product.stock = in_stock

            with transaction.atomic():
                product.save()
                self.request.user.save()
                self.object.save()
            return super().form_valid(form=form)
        elif money < 0:
            return render(self.request, 'app/order_form.html', {'text': 'Не хватает денег'})
        else:
            return render(self.request, 'app/order_form.html', {'text': 'Не хватает товара на складе'})


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order_list.html'
    login_url = 'login/'
    extra_context = {'refund_form': RefundCreateForm()}
    # paginate_by = 5


class RefundView(LoginRequiredMixin, CreateView):

    login_url = 'login/'
    http_method_names = ['post']
    form_class = RefundCreateForm
    success_url = '/'

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.ref_id = self.kwargs['pk']
        refund = Refund.objects.filter(ref=self.kwargs['pk'])

        order_time = Order.objects.get(id=self.kwargs['pk']).created_at
        refund_time = datetime.timedelta(0, 3 * 60)
        time = order_time + refund_time
        now = datetime.datetime.now(tz=datetime.timezone.utc)

        if len(refund) == 0:
            if now > time:
                return render(self.request, 'app/order_form.html', {'text': 'время на возврат истекло'})
            else:
                return super().form_valid(form=form)
        else:
            return render(self.request, 'app/order_form.html', {'text': 'Запрос уже был отправлен'})


class RefundListView(LoginRequiredMixin, ListView):
    model = Refund
    template_name = 'refund_list.html'
    login_url = 'login/'
    paginate_by = 5


class RefundAcceptView(LoginRequiredMixin, DeleteView):
    model = Refund
    success_url = reverse_lazy('refund')


class RefundRejectView(LoginRequiredMixin, DeleteView):
    model = Refund
    success_url = reverse_lazy('refund')

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        success_url = self.get_success_url()
        order_id = self.object.ref_id
        if self.request.POST['a'] == 'reject':
            Order.objects.get(id=order_id).delete()
        else:
            with transaction.atomic():

                product_id = Order.objects.get(id=order_id).product_id
                product_price = Product.objects.get(id=product_id).price
                order_price = product_price * Order.objects.get(id=order_id).num
                user_id = Order.objects.get(id=order_id).user_id
                money = CustomUser.objects.get(id=user_id).money + order_price
                user = CustomUser.objects.get(id=user_id)
                user.money = money

                sum_product = Order.objects.get(id=order_id).num + Product.objects.get(id=product_id).stock
                product = Product.objects.get(id=product_id)
                product.stock = sum_product

                user.save()
                product.save()
            Order.objects.get(id=order_id).delete()

        self.object.delete()
        return HttpResponseRedirect(success_url)
