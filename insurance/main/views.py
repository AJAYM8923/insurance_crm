from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import Agent 
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from .models import Campaign
from datetime import datetime
from .forms import ClientForm
from .models import Client, Campaign


def home(request):
    return render(request, "home.html")

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_dashboard')  
        else:
            return redirect('home')     

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('home')  
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    return render(request, "admin_dashboard.html", {
        'admin_user': request.user
    })
@user_passes_test(lambda u: u.is_superuser)
def add_agents(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        profile_pic = request.FILES.get('profile_picture')

        # Check for duplicates
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'add_agents.html')

        if Agent.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists.")
            return render(request, 'add_agents.html')

        # Create random credentials
        username = email.split('@')[0]
        password = get_random_string(length=6, allowed_chars='1234567890')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Create agent profile
        Agent.objects.create(
            user=user,
            phone=phone,
            address=address,
            gender=gender,
            dob=dob,
            profile_picture=profile_pic
        )

        # Send email
        send_mail(
            subject='Agent Account Created',
            message=f'Your Insurance CRM account has been created.\n\nUsername: {username}\nPassword: {password}',
            from_email='admin@insurancecrm.com',
            recipient_list=[email],
            fail_silently=False
        )

        messages.success(request, 'Agent added and credentials sent to their email.')
        return redirect('add_agents')
    agents = Agent.objects.all()

    return render(request, 'add_agents.html',{'agents': agents})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        
    return redirect('home')

from django.shortcuts import get_object_or_404

@user_passes_test(lambda u: u.is_superuser)
def edit_agent(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    user = agent.user

    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        profile_pic = request.FILES.get('profile_picture')

        # Check for duplicate email/phone excluding current agent
        if User.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif Agent.objects.exclude(id=agent.id).filter(phone=phone).exists():
            messages.error(request, "Phone number already exists.")
        else:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()

            agent.phone = phone
            agent.address = address
            agent.gender = gender
            agent.dob = dob
            if profile_pic:
                agent.profile_picture = profile_pic
            agent.save()

            messages.success(request, "Agent details updated successfully.")
            return redirect('all_agents')

    return render(request, 'edit_agent.html', {'agent': agent})
@user_passes_test(lambda u: u.is_superuser)
def delete_agent(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    agent.user.delete()  # This will also delete Agent due to OneToOne
    messages.success(request, "Agent deleted successfully.")
    return redirect('all_agents')

@user_passes_test(lambda u: u.is_superuser)
def manage_campaigns(request):
    agents = Agent.objects.all()
    campaigns = Campaign.objects.all().order_by('-date')

    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        location = request.POST.get('location')
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        agent_id = request.POST.get('agent')

        if Campaign.objects.filter(name=name).exists():
            messages.error(request, "Campaign name already exists.")
        else:
            Campaign.objects.create(
                name=name,
                date=date,
                location=location,
                latitude=lat,
                longitude=lon,
                agent=Agent.objects.get(id=agent_id)
            )
            messages.success(request, "Campaign added successfully.")
            return redirect('manage_campaigns')

    return render(request, 'manage_campaigns.html', {
        'agents': agents,
        'campaigns': campaigns
    })


@user_passes_test(lambda u: u.is_superuser)
def delete_campaign(request, campaign_id):
    Campaign.objects.get(id=campaign_id).delete()
    messages.success(request, "Campaign deleted.")
    return redirect('all_campaigns')


@user_passes_test(lambda u: u.is_superuser)
def edit_campaign(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    agents = Agent.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        date = request.POST.get('date')
        location = request.POST.get('location')
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')
        agent_id = request.POST.get('agent')  # Single agent, not a list

        if Campaign.objects.exclude(id=campaign.id).filter(name=name).exists():
            messages.error(request, "Campaign name already exists.")
        else:
            campaign.name = name
            campaign.date = date
            campaign.location = location
            campaign.latitude = lat
            campaign.longitude = lon
            campaign.agent = Agent.objects.get(id=agent_id)
            campaign.save()

            messages.success(request, "Campaign updated successfully.")
            return redirect('all_campaigns')

    return render(request, 'edit_campaign.html', {
        'campaign': campaign,
        'agents': agents
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Agent
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

@login_required
def agent_dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')

    agent = get_object_or_404(Agent, user=request.user)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        profile_pic = request.FILES.get('profile_picture')

        # Check for existing email/phone
        if User.objects.exclude(id=request.user.id).filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already exists.'})
        if Agent.objects.exclude(id=agent.id).filter(phone=phone).exists():
            return JsonResponse({'status': 'error', 'message': 'Phone number already exists.'})

        # Update User and Agent
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()

        agent.phone = phone
        agent.address = address
        agent.gender = gender
        agent.dob = dob
        if profile_pic:
            agent.profile_picture = profile_pic
        agent.save()

        return JsonResponse({'status': 'success', 'message': 'Profile updated successfully.'})

    return render(request, 'agent_dashboard.html', {'agent': agent})
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse

@login_required
def reset_agent_password(request):
    if request.method == 'POST':
        current_pwd = request.POST.get('current_password')
        new_pwd = request.POST.get('new_password')
        confirm_pwd = request.POST.get('confirm_password')

        if not check_password(current_pwd, request.user.password):
            return JsonResponse({'status': 'error', 'message': 'Current password is incorrect.'})

        if new_pwd != confirm_pwd:
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match.'})

        # Strong password check: 8+ chars, letter, number, special char
        if (
            len(new_pwd) < 8 or
            not any(c.isalpha() for c in new_pwd) or
            not any(c.isdigit() for c in new_pwd) or
            not any(c in "!@#$%^&*()-_=+[{]};:'\",<.>/?\\|`~" for c in new_pwd)
        ):
            return JsonResponse({
                'status': 'error',
                'message': 'Password must be at least 8 characters long and contain at least one letter, one number, and one special character.'
            })

        user = request.user
        user.set_password(new_pwd)
        user.save()

        logout(request)  # log the user out
        return JsonResponse({'status': 'success', 'message': 'Password reset successfully. Please log in again.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required
def manage_clients(request):
    # Get campaigns assigned to the current agent
    campaigns = Campaign.objects.filter(agent=request.user.agent)

    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.agent = request.user.agent  # Fix: assign Agent object, not User
            client.save()
            return redirect('view_clients')
    else:
        form = ClientForm()
        form.fields['campaign'].queryset = campaigns  # Set campaigns only for GET request

    return render(request, 'manage_clients.html', {'form': form})

@login_required
def view_clients(request):
    agent = Agent.objects.get(user=request.user)  
    clients = Client.objects.filter(agent=agent)  
    return render(request, 'view_clients.html', {'clients': clients})

# views.py (add to same file)

@login_required
def edit_client(request, pk):
    agent = get_object_or_404(Agent, user=request.user)
    client = get_object_or_404(Client, id=pk, agent=agent)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('view_clients')
    else:
        form = ClientForm(instance=client)

    return render(request, 'manage_clients.html', {'form': form})


@login_required
def delete_client(request, pk):
    agent = get_object_or_404(Agent, user=request.user)
    client = get_object_or_404(Client, id=pk, agent=agent)
    client.delete()
    return redirect('view_clients')

@login_required
def agent_campaigns(request):
    agent = get_object_or_404(Agent, user=request.user)
    campaigns = Campaign.objects.filter(agent=agent).order_by('-date')
    return render(request, 'agent_campaigns.html', {'campaigns': campaigns})

@user_passes_test(lambda u: u.is_superuser)
def agent_clients_detail(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    clients = Client.objects.filter(agent=agent).order_by('-created_at')
    return render(request, 'agent_clients_detail.html', {
        'agent': agent,
        'clients': clients
    })

@user_passes_test(lambda u: u.is_superuser)
def all_agents(request):
    agents = Agent.objects.all()
    return render(request, 'all_agents.html', {'agents': agents})

@user_passes_test(lambda u: u.is_superuser)
def all_campaigns(request):
    campaigns = Campaign.objects.all().order_by('-date')
    return render(request, 'all_campaigns.html', {'campaigns': campaigns})


@login_required
def agent_account(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')  # Optional: prevent superuser access

    agent = get_object_or_404(Agent, user=request.user)
    return render(request, 'agent_account.html', {'agent': agent})