from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.contrib.auth import login 



# Create your views here.

class MyLoginView(LoginView):
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('task_list') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password login again')
        return self.render_to_response(self.get_context_data(form=form))

# this is registration form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name=forms.CharField(label="firstname")
    last_name=forms.CharField(label="lastname")

    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email', 'password1', 'password2', )


# this is view which renders the registration form
class RegisterView(FormView):
    redirect_authenticated_user = True
    success_url = reverse_lazy('task_list')
    template_name = 'registration/register.html'
    form_class = RegisterForm
    

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('task_list')
        return super(RegisterView,self).get(request,*args,**kwargs)

        
    
    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        
        return super(RegisterView, self).form_valid(form)