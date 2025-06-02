from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.employee_login, name='employee_login'),
    path('logout/', views.employee_logout, name='employee_logout'),
    path('projects/', views.manage_projects, name='manage_projects'),       # GET + POST
    path('remove_project/', views.remove_project, name='remove_project'),  # POST only
    path('logs/', views.get_logs, name='get_logs'),  
    path('reminder/', views.reminder_page, name='reminder_page'),          # Renders reminder.html page
    path('set-reminder/', views.set_reminder, name='set_reminder'),        # POST to set reminder
]
