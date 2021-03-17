from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView

from app.forms import CustomUserCreationForm, ProductCreateForm
from app.models import Product


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'index.html'
    login_url = 'login/'
    extra_context = {'create_form': ProductCreateForm()}
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
