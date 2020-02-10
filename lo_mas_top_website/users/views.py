# Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.views.generic import DetailView, FormView, UpdateView

# Models
from django.contrib.auth.models import User
from posts.models import Post
from users.models import Profile

# Forms
from users.forms import SignupForm


class UserDetailView(LoginRequiredMixin, DetailView):

    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context

class SignupView(FormView):
    """Users sign up view."""

    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('posts:feed')
        return super(FormView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update profile view."""

    template_name = 'users/update_profile.html'
    model = Profile
    fields = ['website', 'biography', 'phone_number', 'picture']

    def get_object(self):
        """Return user's profile."""
        return self.request.user.profile

    def get_success_url(self):
        """Return to user's profile."""
        username = self.object.user.username
        return reverse('users:detail', kwargs={'username': username})

class LoginView(auth_views.LoginView):
    """Login view."""

    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('posts:feed')
        return super(LoginView, self).get(request, *args, **kwargs)
        

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""

    template_name = 'users/logged_out.html'

#######   Deprecated Methods #########
# Create your views here.
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user =authenticate(request, username=username,password=password)
#         if user:
#             login(request,user)
#             return redirect('posts:feed')
#         else:
#             return render(
#                 request, 
#                 'users/login.html', 
#                 {
#                     'error': 'Invalid username and password!'
#                 })
#     else:
#         if request.user.is_authenticated:
#             return redirect('posts:feed')


#     return render(request, 'users/login.html')

# @login_required
# def logout_view(request):
#     logout(request)
#     return redirect('users:login')

# def signup(request):
#     """Sign up view."""
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('users:login')
#     else:
#         if request.user.is_authenticated:
#             return redirect('posts:feed')

#         form = SignupForm()

#     return render(
#         request=request,
#         template_name='users/signup.html',
#         context={'form': form}
#     )

# def signup(request):

#     if request.method == 'POST':
#         username = request.POST['username']
#         passwd = request.POST['passwd']
#         passwd_confirmation = request.POST['passwd_confirmation']

#         if passwd != passwd_confirmation:
#             return render(
#                 request, 
#                 'users/signup.html',
#                 {
#                     'error': 'Password confirmation does not match!'
#                 })
#         else:
#             try:
#                 user = User.objects.create_user(username=username, password=passwd)
#             except IntegrityError as ie:
#                 print(ie)
#                 return render(request, 'users/signup.html', { 'error': 'Username is already in user!'})
            
#             user.first_name = request.POST['first_name']
#             user.last_name = request.POST['last_name']
#             user.email = request.POST['email']
#             user.save()

#             profile = Profile(user=user)
#             profile.save()

#             return redirect('users:login')
#     else:
#         if request.user.is_authenticated:
#             return redirect('posts:feed')

#     return render(request, 'users/signup.html')

# @login_required
# def update_profile(request):

#     try:
#         profile = request.user.profile
#     except ObjectDoesNotExist:
#         profile = dict()

#     if  request.method == 'POST':
#         form = ProfileForm(request.POST,request.FILES)
#         if form.is_valid():
#             data = form.cleaned_data

#             profile.website = data['website']
#             profile.phone_number = data['phone_number']
#             profile.biography = data['biography']
#             profile.picture = data['picture']
#             profile.save()

#             url = reverse('users:detail',kwargs={'username' : request.user.username})
#             return redirect(url)
#     else:
#         form = ProfileForm()

#     return render(
#         request=request,
#         template_name='users/update_profile.html',
#         context={
#             'profile': profile,
#             'user': request.user,
#             'form': form
#         }
#     )