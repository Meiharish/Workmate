from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
from datetime import datetime
from .db import employee_logs, projects
from bson.errors import InvalidDocument

# Render the home page
def home(request):
    return render(request, 'index.html')

# Employee login
@csrf_exempt
def employee_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            if not name:
                return JsonResponse({'error': 'Name is required'}, status=400)
            timestamp = datetime.now()
            employee_logs.insert_one({
                'name': name,
                'action': 'login',
                'timestamp': timestamp
            })
            return JsonResponse({'message': 'Login recorded', 'timestamp': str(timestamp)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)

# Employee logout
@csrf_exempt
def employee_logout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            if not name:
                return JsonResponse({'error': 'Name is required'}, status=400)
            timestamp = datetime.now()
            employee_logs.insert_one({
                'name': name,
                'action': 'logout',
                'timestamp': timestamp
            })
            return JsonResponse({'message': 'Logout recorded', 'timestamp': str(timestamp)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)

# Get or update pending projects
@csrf_exempt
def manage_projects(request):
    try:
        if request.method == 'GET':
            project_list = list(projects.find({}, {"_id": 0}))
            return JsonResponse({'projects': project_list})
        elif request.method == 'POST':
            data = json.loads(request.body)
            if 'projects' not in data:
                return JsonResponse({'error': 'Projects data is required'}, status=400)
            
            for project in data['projects']:
                if not project.get('name') or not project.get('deadline'):
                    return JsonResponse({'error': 'Each project must have a name and deadline'}, status=400)
            
            try:
                result = projects.insert_many(data['projects'])
                return JsonResponse({
                    'message': 'Projects added successfully',
                    'count': len(result.inserted_ids)
                })
            except InvalidDocument:
                return JsonResponse({'error': 'Invalid project data format'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)

# Remove one project by name
@csrf_exempt
def remove_project(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            if not name:
                return JsonResponse({'error': 'Project name is required'}, status=400)
            
            result = projects.delete_one({'name': name})
            if result.deleted_count == 0:
                return JsonResponse({'error': 'Project not found'}, status=404)
                
            return JsonResponse({'message': 'Project removed successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)

# Get login/logout logs for a user
def get_logs(request):
    if request.method == 'GET':
        try:
            name = request.GET.get('name')
            if not name:
                return JsonResponse({'error': 'Name parameter is required'}, status=400)
                
            logs = list(employee_logs.find({'name': name}, {'_id': 0}))
            return JsonResponse({'logs': logs})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)

# ✅ Set reminder for a project
@csrf_exempt
def set_reminder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            reminder = data.get('reminder')  # Expecting True or False

            if name is None or reminder is None:
                return JsonResponse({'error': 'Name and reminder fields are required'}, status=400)

            project = projects.find_one({'name': name})
            if not project:
                return JsonResponse({'error': 'Project not found'}, status=404)

            projects.update_one({'name': name}, {'$set': {'reminder': reminder}})
            return JsonResponse({'message': 'Reminder preference saved successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)
def reminder_page(request):
    return render(request, 'reminder.html')
