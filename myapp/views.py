from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.db.models import Q
from .forms import SearchForm, MessageForm,  UsernameChangingForm, EmailChangingForm, IconChangingForm, CustomPasswordChangeForm
from .models import CustomUser, Message

def superuser_detector(view_func):
    def internal_func(request, *args, **kwargs):
        if request.user.is_superuser:
            logout(request)
            return redirect("account_login")
        return view_func(request, *args, **kwargs)
    return internal_func

def index(request):
    return render(request, "myapp/index.html")

""""
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("login_view")
    else:
        form = CustomUserCreationForm()
    return render(request, "myapp/signup.html", {"form": form})
"""

""" 
class CustomLoginView(LoginView):
    template_name = 'myapp/login.html'
"""
    
@login_required
@superuser_detector
def friends(request):
    users_precursor = CustomUser.objects.exclude(is_superuser=True).exclude(id=request.user.id)

    if request.method == "POST":
        form = SearchForm(request.POST)
        str = request.POST.get('entered_text')

        users = []

        if form.is_valid():
            if users_precursor:
                for friend_user in users_precursor:
                    if str in friend_user.username:
                        users.append(friend_user)
            else:
                users = users_precursor
    else:
        form = SearchForm()
        users = users_precursor

    information_list = []

    for friend_user in users:
        q_obj = Q(sender=request.user, recipient=friend_user) | Q(sender=friend_user, recipient=request.user)
        base = Message.objects.filter(q_obj).order_by('-created_at').first()
        if base:
            latest_message = base.text
            latest_message_time = base.created_at
        else:
            latest_message = ''
            latest_message_time = ''
        information_list.append((friend_user, latest_message, latest_message_time))

    return render(request, "myapp/friends.html", {"information_list": information_list, "form": form})

@login_required
@superuser_detector
def talk_room(request, param):
    talk_user = get_object_or_404(CustomUser, id=param)
    
    q_obj = Q(is_superuser=True) | Q(username=request.user.username)
    id_list = CustomUser.objects.filter(q_obj).values_list('id', flat=True)
    for x in id_list:
        if param == x:
            return redirect("friends")

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = talk_user
            message.save()
            return redirect('talk_room', param=talk_user.id)
    else:
        form = MessageForm()

    q_obj = Q(sender=request.user, recipient=talk_user) | Q(sender=talk_user, recipient=request.user)

    messages = Message.objects.filter(q_obj).order_by('created_at')

    return render(request, "myapp/talk_room.html", {
        'talk_user': talk_user,
        'form': form,
        'messages': messages,
    })

@login_required
@superuser_detector
def setting(request):
    return render(request, "myapp/setting.html")

@login_required
@superuser_detector
def suc(request):
    if request.method == "POST":
        form = UsernameChangingForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("scc")
    else:
        form = UsernameChangingForm(instance=request.user)
    return render(request, "myapp/s_username_change.html", {"form": form})

@login_required
@superuser_detector
def sec(request):
    if request.method == "POST":
        form = EmailChangingForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("scc")
    else:
        form = EmailChangingForm(instance=request.user)
    return render(request, "myapp/s_email_change.html", {"form": form})

@login_required
@superuser_detector
def sic(request):
    if request.method == "POST":
        form = IconChangingForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("scc")
    else:
        form = IconChangingForm(instance=request.user)
    return render(request, "myapp/s_icon_change.html", {"form": form})

@method_decorator(login_required, name='dispatch')
@method_decorator(superuser_detector, name='dispatch')
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'myapp/s_password_change.html'
    success_url = '/s_change_completed'
    form_class = CustomPasswordChangeForm

@method_decorator(login_required, name='dispatch')
@method_decorator(superuser_detector, name='dispatch')
class CustomLogoutView(LogoutView):
    next_page = 'account_login'

@login_required
@superuser_detector
def scc(request):
    return render(request, "myapp/s_change_completed.html")