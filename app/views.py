from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from app.forms import CustomUserCreationForm, ProductCreateForm, OrderCreateForm, RefundCreateForm
from app.models import Product, CustomUser, Order, Refund


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'index.html'
    login_url = 'login/'
    extra_context = {'order_form': OrderCreateForm(), 'create_form': ProductCreateForm()}
    paginate_by = 5


class Login(LoginView):
    success_url = '/'
    template_name = 'login.html'


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


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = '/'


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

            # user = CustomUser.objects.get(id=self.user_id)  # .update(money=money)
            product = Product.objects.get(id=self.object.product_id)
            self.request.user.money = money
            product.stock = in_stock

            with transaction.atomic():
                product.save()
                self.request.user.save()
                self.object.save()
            return super().form_valid(form=form)
        # else:
        #     return super().form_invalid(form=form)
        elif money < 0:
            return render(self.request, 'app/order_form.html', {'text': 'Не хватает денег'})
        else:
            return render(self.request, 'app/order_form.html', {'text': 'Не хватает товара на складе'})
        # return HttpResponseRedirect(self.get_success_url())


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order_list.html'
    login_url = 'login/'
    extra_context = {'refund_form': RefundCreateForm()}
    # paginate_by = 5


class RefundView(LoginRequiredMixin, CreateView):

    """
        Добавить проверку на повтор
    """

    login_url = 'login/'
    http_method_names = ['post']
    form_class = RefundCreateForm
    success_url = '/'

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.ref_id = self.kwargs['pk']

        return super().form_valid(form=form)


class RefundListView(LoginRequiredMixin, ListView):
    model = Refund
    template_name = 'refund_list.html'
    login_url = 'login/'
    # extra_context = {'refund_form': RefundCreateForm()}
    paginate_by = 5