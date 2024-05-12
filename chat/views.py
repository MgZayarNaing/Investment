
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from account.models import User

from .models import Room


@require_POST
def create_room(request, uuid):
    name = request.POST.get('name', '')
    url = request.POST.get('url', '')

    Room.objects.create(uuid=uuid, client=name, url=url)

    return JsonResponse({'message': 'room created'})

def chat_room_list(request):
    rooms = Room.objects.all()
    users = User.objects.filter(is_staff=True)

    return render(request, 'chat_room_list.html', {
        'rooms': rooms,
        'users': users
    })

@login_required(login_url='/account/login/')
def room(request, uuid):
    room = Room.objects.get(uuid=uuid)

    if room.status == Room.WAITING:
        room.status = Room.ACTIVE
        room.agent = request.user
        room.save()

    return render(request, 'chat/room.html', {
        'room': room
    })

@login_required(login_url='/account/login/')
def delete_room(request, uuid):
    if request.user.has_perm('room.delete_room'):
        room = Room.objects.get(uuid=uuid)
        room.delete()
                
        messages.success(request, 'The room was deleted!')

        return redirect('/chat/chat-room-list/')
    else:
        messages.error(request, 'You don\'t have access to delete rooms!')

        return redirect('/chat/chat-room-list/')
