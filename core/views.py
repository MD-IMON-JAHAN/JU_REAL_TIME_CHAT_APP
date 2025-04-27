from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, ChatRoomForm, MessageForm, UserProfileForm
from .models import User, ChatRoom, Message
import uuid
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

def user_login(request):
    next_url = request.GET.get('next', '')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    rooms = ChatRoom.objects.filter(members=request.user)
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'core/index.html', {
        'rooms': rooms,
        'users': users,
    })

@login_required
def create_room(request):
    if request.method == 'POST':
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.admin = request.user
            room.save()
            room.members.add(request.user)
            return redirect('room', room_id=room.id)
    else:
        form = ChatRoomForm()
    return render(request, 'core/create_room.html', {'form': form})

@login_required
def room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in room.members.all():
        return redirect('index')
    
    messages = Message.objects.filter(room=room).order_by('timestamp')
    all_users = User.objects.exclude(id=request.user.id)  # Include all users except the current user

    return render(request, 'core/room.html', {
        'room': room,
        'messages': messages,
        'all_users': all_users,  # Pass all users here
    })

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'core/profile.html', {'user_profile': user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'core/edit_profile.html', {'form': form})

@login_required
def admin_panel(request):
    if not request.user.is_superuser:
        return redirect('index')
    
    users = User.objects.all()
    rooms = ChatRoom.objects.all()
    messages = Message.objects.all()
    
    return render(request, 'core/admin_panel.html', {
        'users': users,
        'rooms': rooms,
        'messages': messages,
    })

@login_required
def invite_to_room(request, room_id):
    room = ChatRoom.objects.get(id=room_id)  # Changed Room to ChatRoom
    if request.method == 'POST':
        user_id = request.POST.get('user')
        user_to_add = User.objects.get(id=user_id)
        
        if user_to_add not in room.members.all():
            room.members.add(user_to_add)
            messages.success(request, f'{user_to_add.username} has been added to the room!')
        else:
            messages.error(request, f'{user_to_add.username} is already in the room.')

    return redirect('room', room_id=room.id)  # Updated redirect to 'room'
