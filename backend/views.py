from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group, User
from .serializer import *
from rest_framework.response import Response
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json
from datetime import datetime


# Create your views here.
@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')


            messages.success(request, username + ' account created')
            return redirect('/login')

    context = {'form':form}
    return render(request, 'backend/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password incorrect')
        
    context={}
    return render(request, 'backend/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    tutor_subject = TutorSubject.objects.all()
    tutee = Tutee.objects.all()
    tutee_hours = TuteeHours.objects.all()
    context = {'tutor_subject': tutor_subject, 'tutee': tutee, 'tutee_hours': tutee_hours}
    return render(request, 'backend/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor'])
def userPage(request):
    TS = request.user.tutor.tutorsubject_set.all()
    context = {'tutor_subject':TS}
    return render(request, 'backend/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['tutor'])
def profile(request):
    tutor = request.user.tutor
    form = TutorForm(instance=tutor) 

    if request.method == 'POST':
        form = TutorForm(request.POST, request.FILES, instance=tutor)
        if form.is_valid():
            form.save()

    context={'form': form}
    return render(request, 'backend/profile.html', context)

def subjects(request):
    subjects = Subject.objects.all()

    return render(request, 'backend/subjects.html', {'subjects': subjects})

@login_required(login_url='login')
@admin_only
def tutors(request):
    tutor_subject = TutorSubject.objects.all()

    context = {'tutor_subject': tutor_subject}
    return render(request, 'backend/tutors.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def tutor(request, pk):
    tutor_id = Tutor.objects.get(id=pk)
    tutorsubject = tutor_id.tutorsubject_set.all()

    context = {'tutor': tutor_id, 'tutorsubject': tutorsubject}
    return render(request, 'backend/tutor.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createTS(request):
    form = TutorSubjectForm()
    if request.method == 'POST':
        form = TutorSubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/tutors')

    context = {'form':form}
    return render(request, 'backend/TS_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateTS(request, pk):
    TS = TutorSubject.objects.get(id=pk)
    form = TutorSubjectForm(instance=TS)

    if request.method =='POST':
        form = TutorSubjectForm(request.POST, instance=TS)
        if form.is_valid():
            form.save()
            return redirect('/tutors')

    context = {"form":form}
    return render(request, 'backend/TS_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteTS(request, pk):
    TS = TutorSubject.objects.get(id=pk)
    if request.method =="POST":
        TS.delete()
        return redirect('/tutors')
    context = {'TS':TS}
    return render(request, 'backend/delete.html', context)


# ------------------------ DRFW views ------------------------


@api_view(['GET'])
def getRoutes(request):
    routes=[
        {
            'Endpoint': '/tutors_s/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of tutors'
        },
        {
            'Endpoint': '/tutors/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single tutor object'
        },
        {
            'Endpoint': '/tutors/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new tutor with data sent in post request'
        },
        {
            'Endpoint': '/tutors/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Creates an existing tutor with data sent in post request'
        },
        {
            'Endpoint': '/tutors_s/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting tutor'
        },
    ]
    return Response(routes)

@api_view(['GET'])
def getTutors(request):
    tutors = Tutor.objects.all()
    serializer = TutorSerializer(tutors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTutor(request, pk):
    tutors = Tutor.objects.get(id=pk)
    serializer = TutorSerializer(tutors, many=False)
    return Response(serializer.data)    


@api_view(['PUT'])
def updateTutor(request, pk):
    data = request.data
    tutor = Tutor.object.get(id=pk)
    serializer = TutorSerializer(instance=tutor, data=data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


# ------------------- Front End Authentication Login/Register --------------------
def api_register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email', '')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User.objects.create_user(username=username, password=password, email=email)
        return JsonResponse({'message': f'User {username} created successfully'}, status=201)
        

@ensure_csrf_cookie
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})

def api_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({
                'message': 'Login successful',
                'is_superuser': user.is_superuser
                })
        
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def api_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_get_user(request):
    return JsonResponse({'username': request.user.username})


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([AllowAny])
def api_delete_tutor(request,pk):
    try:
        tutor = Tutor.objects.get(id=pk)
        user = tutor.user

        tutor.delete()

        if user is not None:
            user.delete()

        return Response('Tutor was deleted')
    except Tutor.DoesNotExist:
        return Response({'error': 'Tutor not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    

@api_view(['GET'])
def getTutorSubject(request):
    tutor_subject = TutorSubject.objects.all()
    serializer = TutorSubjectSerializer(tutor_subject, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getTutees(request):
    tutees = Tutee.objects.all()
    serializer = TuteesSerializer(tutees, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTuteeHours(request):
    tutee_hours = TuteeHours.objects.all()
    serializer = TuteeHoursSerializer(tutee_hours, many=True)
    return Response(serializer.data)

# Invoice status
@api_view(['GET'])
def getPaymentStatuses(request):
    payment_statuses = PaymentStatus.objects.all()
    serializer = PaymentStatusSerializer(payment_statuses, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def updatePaymentStatus(request):
    data = request.data
    tutor_subject_id = data.get('tutor_subject_id')
    status = data.get('status')
    month_year = data.get('month_year')  # Format: "YYYY-MM"
    
    # Convert month_year string to date (set to first day of month)
    month_date = datetime.strptime(month_year, "%Y-%m").date()
    
    # Try to find existing payment status for this tutor_subject and month
    try:
        payment_status = PaymentStatus.objects.get(
            tutor_subject_id=tutor_subject_id,
            month__year=month_date.year,
            month__month=month_date.month
        )
        payment_status.status = status
        payment_status.save()
    except PaymentStatus.DoesNotExist:
        # Create new payment status record
        tutor_subject = TutorSubject.objects.get(id=tutor_subject_id)
        payment_status = PaymentStatus.objects.create(
            tutor_subject=tutor_subject,
            status=status,
            month=month_date
        )
    
    serializer = PaymentStatusSerializer(payment_status)
    return Response(serializer.data)


@api_view(['POST'])
def addTuteeHours(request):
    data = request.data
    tutee_id = data.get('tutee_id')
    subject_id = data.get('subject_id')
    hours = data.get('hours')
    date = data.get('date')
    
    try:
        tutee = Tutee.objects.get(id=tutee_id)
        subject = Subject.objects.get(id=subject_id)
        
        tutee_hours = TuteeHours.objects.create(
            name=tutee,
            subject=subject,
            hours=hours,
            date=date
        )
        
        serializer = TuteeHoursSerializer(tutee_hours)
        return Response(serializer.data, status=201)
    except Exception as e:
        return Response({'detail': str(e)}, status=400)


@api_view(['GET'])
def getSubjects(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createTutorSubject(request):
    tutor_id = request.data.get('tutor_id')
    subject_id = request.data.get('subject_id')
    desc = request.data.get('desc', '')

    try:
        tutor = Tutor.objects.get(id=tutor_id)
        subject = Subject.objects.get(id=subject_id)
        
        tutor_subject = TutorSubject.objects.create(
            tutor=tutor,
            subject=subject,
            desc=desc
        )
        
        serializer = TutorSubjectSerializer(tutor_subject)
        return Response(serializer.data, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=400)
    


@api_view(['POST'])
def addTuteeHours(request):
    data = request.data
    tutee_id = data.get('tutee_id')
    subject_id = data.get('subject_id')
    hours = data.get('hours')
    date = data.get('date')
    
    try:
        tutee = Tutee.objects.get(id=tutee_id)
        subject = Subject.objects.get(id=subject_id)
        
        tutee_hours = TuteeHours.objects.create(
            name=tutee,
            subject=subject,
            hours=hours,
            date=date
        )
        
        serializer = TuteeHoursSerializer(tutee_hours)
        return Response(serializer.data, status=201)
    except Exception as e:
        return Response({'detail': str(e)}, status=400)

@api_view(['POST'])
def createTutee(request):
    try:
        print("Received data:", request.data)  # Debug: log the incoming data
        
        name = request.data.get('name')
        level_id = request.data.get('level_id')
        phone = request.data.get('phone')
        tutor_subject_ids = request.data.get('tutor_subject_ids', [])
        
        if not name or not level_id:
            return Response({'error': 'Name and level are required'}, status=400)
        
        try:
            level = Level.objects.get(id=level_id)
        except Level.DoesNotExist:
            return Response({'error': f'Level with id {level_id} does not exist'}, status=400)
        
        # Create tutee with properly handled phone field
        tutee = Tutee.objects.create(
            name=name,
            level=level,
            phone=str(phone) if phone is not None else None
        )
        
        # Save the tutee first to ensure it exists before adding many-to-many relationships
        tutee.save()
        
        # Add tutor subjects if provided
        if tutor_subject_ids:
            try:
                tutor_subjects = TutorSubject.objects.filter(id__in=tutor_subject_ids)
                if tutor_subjects.exists():
                    tutee.tutor_subject.add(*tutor_subjects)
                else:
                    print(f"No tutor subjects found with ids {tutor_subject_ids}")
            except Exception as e:
                print(f"Error adding tutor subjects: {str(e)}")
        
        # Refresh tutee from DB to ensure we have the latest data including M2M relations
        tutee.refresh_from_db()
        
        serializer = TuteesSerializer(tutee)
        print("Created tutee:", serializer.data)  # Debug: log the created tutee
        return Response(serializer.data, status=201)
        
    except Exception as e:
        import traceback
        print("Error creating tutee:", str(e))
        print(traceback.format_exc())  # Print the full traceback for debugging
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
def getLevels(request):
    level = Level.objects.all()
    serializer = LevelSerializer(level, many=True)
    return Response(serializer.data)



