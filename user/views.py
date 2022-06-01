# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView

# Models
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from shop.models import Order, OrderItem
from user.models import Person

# Forms
from user.forms import SignupForm
# Create your views here.


class LoginView(auth_views.LoginView):
    """Login view."""

    template_name = 'login.html'


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""

    template_name = 'logged_out.html'

class UserDetailView(LoginRequiredMixin, UpdateView):
    """User detail view."""

    template_name = 'detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    

    model = Person
    fields = ['name', 'lastName', 'cc', 'email', 'cellphone',  'home_address', 'Age']

    def get_object(self):
        """Return user's profile."""
        return self.request.user.person

    def get_success_url(self):
        """Return to user's profile."""
        username = self.object.user.username
        return reverse('user:detail', kwargs={'username': username})
    
    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context.update({
            "orders": Order.objects.filter(user=self.request.user, ordered=True)
        })
        return context


class SignupView(FormView):
    """Users sign up view."""

    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        """Save form data."""
        form.save()        
        return super().form_valid(form)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update profile view."""

    template_name = 'update_profile.html'
    model = Person
    fields = ['name', 'lastName', 'cc', 'email', 'cellphone',  'home_address', 'Age']

    def get_object(self):
        """Return user's profile."""
        return self.request.user.person

    def get_success_url(self):
        """Return to user's profile."""
        username = self.object.user.username
        return reverse('user:detail', kwargs={'username': username})

