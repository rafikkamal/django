from django.db.models import Q
from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth import authenticate, login
from .models import Conversation
from django.views.generic import View
from .forms import UserForm
from django.contrib.auth.models import User
from .models import Conversation,Conversations


#from django.core.urlsolvers import reverse_lazy
# Create your views here.
def index(request):
    if request.user.is_authenticated():
        users = User.objects.all().exclude(pk=request.user.id)
        #return HttpResponse(users)
        return render(request, 'conversation/index.html', {'users': users})
    else:
        return render(request, 'conversation/login.html', {'message': 'HEllo !'})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'conversation/index.html', {'message': 'Logged in Successfully !'})
            else:
                return render(request, 'conversation/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'conversation/login.html', {'error_message': 'Invalid login'})
    return render(request, 'conversation/login.html')


class DetailView(generic.DetailView):
    model = Conversation
    template_name = 'conversation/detail.html'


class UserFormView(View):
    form_class = UserForm
    template_name = 'conversation/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('conversation:index')

        return render(request, self.template_name, {'form': form})


def VarifyUser(pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        users = User.objects.all().exclude(pk=request.user.id)
        return render(request, 'conversation/index.html', {'users': users, 'message': 'No Such User Found'})
    return user


class ConversationListView(View):

    def get(self, request, pk, *args, **kwargs):

        user = VarifyUser(pk)

        conversations = Conversations.objects.get(Q(created_by=request.user.id, created_for=pk) |
                                                  Q(created_by=pk, created_for=request.user.id))

        #return HttpResponse(conversations)
        if conversations:
            conversation = Conversation.objects.filter(conversation=conversations)
            return render(request, 'conversation/conversation_template.html',
                          {'user': user, 'conversation': conversation, 'id': conversations.id})
        return render(request, 'conversation/connect.html', {'user': user, 'conversations': conversations})


class ConversationProcessor(View):

    def post(self, request, pk, *args, **kwargs):

        user = VarifyUser(pk)

        if request.method == "POST":
            message = request.POST['message']
            conversations = Conversations.objects.get(Q(created_by=request.user.id, created_for=pk) |
                                                Q(created_by=pk, created_for=request.user.id))

            if str(conversations.id) == request.POST['conversation']:
                conversation = Conversation()
                conversation.message = message
                conversation.user = request.user
                conversation.conversation = conversations
                conversation.save()
                return redirect('conversation:conversation_connect', pk=int(pk))
            else:
                users = User.objects.all().exclude(pk=request.user.id)
                return render(request, 'conversation/index.html', {'users': users, 'message': 'You Dont have access!!!'})


class ConversationProcessorUpdate(View):

    def post(self, request, pk, *args, **kwargs):

        user = VarifyUser(pk)

        if request.method == "POST":
            message = request.POST['message']
            conversations = Conversations.objects.get(Q(created_by=request.user.id, created_for=pk) |
                                                      Q(created_by=pk, created_for=request.user.id))

            if str(conversations.id) == request.POST['conversation']:
                conversation = Conversation.objects.get(pk=request.POST['conversation_id'])
                conversation.message = message
                conversation.save()
                return redirect('conversation:conversation_connect', pk=int(pk))


class ConversationProcessorDelete(View):

    def post(self, request, pk, *args, **kwargs):

        user = VarifyUser(pk)

        if request.method == "POST":
            conversations = Conversations.objects.get(Q(created_by=request.user.id, created_for=pk) |
                                                      Q(created_by=pk, created_for=request.user.id))

            if str(conversations.id) == request.POST['conversation']:
                conversation = Conversation.objects.get(pk=request.POST['conversation_id'])
                conversation.delete()
                return redirect('conversation:conversation_connect', pk=int(pk))


class ConversationProcessorArchive(View):

    def post(self, request, pk, *args, **kwargs):

        user = VarifyUser(pk)

        if request.method == "POST":
            conversations = Conversations.objects.get(Q(created_by=request.user.id, created_for=pk) |
                                                      Q(created_by=pk, created_for=request.user.id))

            if str(conversations.id) == request.POST['conversation']:
                conversation = Conversation.objects.get(pk=request.POST['conversation_id'])
                conversation.archive = True
                conversation.save()
                return redirect('conversation:conversation_connect', pk=int(pk))


