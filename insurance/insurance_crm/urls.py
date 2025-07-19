"""
URL configuration for insurance_crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('login/',views.login_view,name="login"),
    path('admin_dashboard/',views.admin_dashboard,name="admin_dashboard"),
    path('add_agents/',views.add_agents,name="add_agents"),
    path('logout/', views.logout_view, name='logout'),
    path('edit-agent/<int:agent_id>/', views.edit_agent, name='edit_agent'),
    path('delete-agent/<int:agent_id>/', views.delete_agent, name='delete_agent'),
    path('campaigns/', views.manage_campaigns, name='manage_campaigns'),
    path('campaigns/delete/<int:campaign_id>/', views.delete_campaign, name='delete_campaign'),
    path('campaigns/edit/<int:campaign_id>/', views.edit_campaign, name='edit_campaign'),
    path('agent/dashboard/', views.agent_dashboard, name='agent_dashboard'),
    path('agent/reset_password/', views.reset_agent_password, name='reset_agent_password'),
    path('manage-clients/', views.manage_clients, name='manage_clients'),
    path('clients/', views.view_clients, name='view_clients'),
    path('edit-client/<int:pk>/', views.edit_client, name='edit_client'),
    path('delete-client/<int:pk>/', views.delete_client, name='delete_client'),
    path('agent/campaigns/', views.agent_campaigns, name='agent_campaigns'),
    path('agent/<int:agent_id>/clients/', views.agent_clients_detail, name='agent_clients_detail'),
    path('all_agents/', views.all_agents, name='all_agents'),
    path('all_campaigns/', views.all_campaigns, name='all_campaigns'),
    path('account/', views.agent_account, name='agent_account'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)