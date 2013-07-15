#-*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from heimdall.models import Server,Permission, Demands,SshKeys
from heimdall.objects import Statistics
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User, Group
from datetime import date
from form import UploadSshKeyForm
from django.core.urlresolvers import reverse

def redirect_home(request,notification):
	user_count = Group.objects.get(name="heimdall").user_set.all().count()
	server_count = Server.objects.all().count()
	keys_count = SshKeys.objects.all().count()
	demands_count = Demands.objects.filter(close_date__isnull=True).all().count()
	
	permissions_count = Permission.objects.all().count()
	stats = Statistics(user_count,server_count,permissions_count,demands_count,keys_count)
	
	demands = Demands.objects.filter(close_date__isnull=True).all()
	if notification:
		return render_to_response('index.html', {'stats': stats, 'demands':demands, 'PAGE_TITLE': 'Accueil', 'APP_TITLE' : "Heimdall", 'NOTIFICATION': notification }, context_instance=RequestContext(request))
	else:
		return render_to_response('index.html', {'stats': stats, 'demands':demands, 'PAGE_TITLE': 'Accueil', 'APP_TITLE' : "Heimdall" }, context_instance=RequestContext(request))
		
def index(request):
	user_count = Group.objects.get(name="heimdall").user_set.all().count()
	server_count = Server.objects.all().count()
	keys_count = SshKeys.objects.all().count()
	demands_count = Demands.objects.filter(close_date__isnull=True).all().count()
	
	permissions_count = Permission.objects.all().count()
	stats = Statistics(user_count,server_count,permissions_count,demands_count,keys_count)
	
	demands = Demands.objects.filter(close_date__isnull=True).all()
	return render_to_response('index.html', {'stats': stats, 'demands':demands, 'PAGE_TITLE': 'Accueil', 'APP_TITLE' : "Heimdall" }, context_instance=RequestContext(request))
		
	
def users(request):
	list_users = User.objects.all()
	return render_to_response('users.html', { 'list_users': list_users , 'PAGE_TITLE': 'Utilisateurs', 'APP_TITLE' : "Heimdall"}, context_instance=RequestContext(request))
	
def servers(request):
	list_servers = Server.objects.all()
	return render_to_response('servers.html', { 'list_servers': list_servers , 'PAGE_TITLE': 'Serveurs', 'APP_TITLE' : "Heimdall" }, context_instance=RequestContext(request))
	
def permissions(request):
	all_permissions = Permission.objects.all()
	users_in_group = Group.objects.get(name="heimdall").user_set.all()
	users_in_group_admin = Group.objects.get(name="heimdall-admin").user_set.all()
	
	userConnected = request.user
	if userConnected.is_authenticated:
		if userConnected.groups.filter(name="heimdall-admin"):
			return render_to_response('permissions.html', { 'permissions': convertToIterable(all_permissions) , 'PAGE_TITLE': 'Permissions', 'APP_TITLE' : "Heimdall" }, context_instance=RequestContext(request))
		elif userConnected.groups.filter(name="heimdall"):
			permissions_visible = Permission.objects.get(user=userConnected)
			return render_to_response('permissions.html', { 'permissions': convertToIterable(permissions_visible) , 'PAGE_TITLE': 'Permissions', 'APP_TITLE' : "Heimdall" }, context_instance=RequestContext(request))
		else:
			return render_to_response('permissions.html', {'PAGE_TITLE': 'Permissions', 'APP_TITLE' : "Heimdall" }, context_instance=RequestContext(request))

def convertToIterable(permissions_visible):
	try:
		some_object_iterator = iter(permissions_visible)
		permissions_visible_to_return = permissions_visible
	except TypeError, te:
		permissions_visible_to_return = [1]
		permissions_visible_to_return[0] = permissions_visible
	
	return permissions_visible_to_return

def deposite(request):
	userConnected = request.user
	# Handle file upload
	docfile = []
	if request.method == 'POST':
		form = UploadSshKeyForm(request.POST, request.FILES)
		if form.is_valid():
		    docfile = request.FILES['docfile']
		    for line in docfile:
		    	    if SshKeys.objects.filter(user=userConnected).count()>0:
		    	    	oldkey = SshKeys.objects.get(user=userConnected)
		    	    	oldkey.key = line
		    	    else:
				sshkey = SshKeys(user=userConnected,key=line, host="userHost")
		    	    	sshkey.save()
		    
		    # Redirect to the document list after POST
		    return HttpResponseRedirect(reverse('deposite'))
	else:
		if SshKeys.objects.filter(user=userConnected).count()>0:
			key = None
		else:
			key = SshKeys.objects.get(user=userConnected).key
			form = UploadSshKeyForm()
	return render_to_response(
		'deposite.html',
		{'documents': docfile, 'form': form, 'key':key,'PAGE_TITLE': 'Depot', 'APP_TITLE' : "Heimdall" },
		context_instance=RequestContext(request)
	)
	
def connect(request):
	return render_to_response('connect.html', {'PAGE_TITLE': 'Connect', 'APP_TITLE' : "Heimdall" }, context_instance=RequestContext(request))
	

def auth():
	if user is not None:
	    # the password verified for the user
	    if user.is_active:
		print("User is valid, active and authenticated")
	    else:
		print("The password is valid, but the account has been disabled!")
	else:
	    # the authentication system was unable to verify the username and password
	    print("The username and password were incorrect.")
	    
	 
	 
def mylogin(request):
	if request.method == 'POST':
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		if user is not None:
			if user.is_active:
				login(request, user)
				# success
				return HttpResponseRedirect('home')
			else:
				#disabled account
				return direct_to_template(request, 'inactive_account.html')
		else:
			# invalid login
			return HttpResponseRedirect('home')
	else:
		return HttpResponseRedirect('home')
      

def mylogout(request):
	logout(request)
	return HttpResponseRedirect('home')
	
def register(request):
	return render_to_response('register.html', {'PAGE_TITLE': 'Register', 'APP_TITLE' : "Heimdall" }, context_instance=RequestContext(request))

def register_action(request):
	if request.method == 'POST':
		notification="User registered ! "
		return redirect_home(request,notification)
		
	else:
		return HttpResponseRedirect('home')
	
def require_access(request):
	if request.method == 'POST':
		userConnected = request.user
		if userConnected.is_authenticated:
			if userConnected.groups.filter(name="heimdall"):
				serverHost = Server.objects.get(hostname=request.POST['server'])
				userHost = request.POST['user']
				priority = request.POST['priority']
				comments = request.POST['comments']
				cdate = date.today()
				demand = Demands(user=userConnected,server=serverHost,hostuser=userHost,priority=priority,comments=comments,cdate=cdate)
				demand.save()
				
				list_servers = Server.objects.all()
				return render_to_response('servers.html', { 'list_servers': list_servers , 'PAGE_TITLE': 'Serveurs', 'APP_TITLE' : "Heimdall", 'ACTION':'DONE' }, context_instance=RequestContext(request))
				
		else:
			return HttpResponseRedirect('home')
	else:
		return HttpResponseRedirect('home')
		
