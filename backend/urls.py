from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('', views.getRoutes, name="routes"),

    path('register/', views.registerPage, name= "register"),
    path('login/', views.loginPage, name= "login"),
    path('logout/', views.logoutUser, name= "logout"),
    
    path('', views.home, name= "home"),
    path('user/', views.userPage, name= "user_page"),
    # path('subjects/', views.subjects, name= "subjects"),
    path('tutors/', views.tutors, name= "tutors"),

    path('tutors_s/', views.getTutors, name= "tutors_s"),
    path('tutors/<str:pk>/', views.tutor, name= "tutor"),
    path('tutors_s/<str:pk>/', views.getTutor, name= "tutor_s"),
    path('tutors_s/<str:pk>/delete/', views.api_delete_tutor, name= "delete-tutor_s"),
    path('tutorSubject_s/', views.getTutorSubject, name= "tutorSubject_s"),
    path('tutorSubject_s_G/', views.getTutorSubject_G, name= "tutorSubject_s_G"),
    path('tutees_s/', views.getTutees, name= "tutees_s"),
    path('tuteeHours_s/', views.getTuteeHours, name="tuteeHours_s"),
    path('levels_s/', views.getLevels, name= "level_s"),
    path('profile/', views.profile, name='profile'),

    path('create_TS/', views.createTS, name="create_TS"),
    path('update_TS/<str:pk>/', views.updateTS, name="update_TS"),
    path('delete_TS/<str:pk>/', views.deleteTS, name="delete_TS"),


    # ---------- Frontend Authentication ----------
    path('register_s/', views.api_register),
    path('login_s/', views.api_login),
    path('logout_s/', views.api_logout),
    path('user_s/', views.api_get_user),
    path('get-csrf-token/', views.get_csrf_token),
    path('api/user_s/<str:username>/', views.get_user_by_username, name='get_user_by_username'),


    # ---------- Invoice ----------
    path('payment-statuses/', views.getPaymentStatuses, name="payment-statuses"),
    path('update-payment-status/', views.updatePaymentStatus, name="update-payment-status"),
    path('tutee-hours/add/', views.addTuteeHours, name="add-tutee-hours"),
    path('subjects/', views.getSubjects, name="subjects"),


    # ---------------- CRUD operatoins ------------
    path('create-tutee/', views.createTutee, name='create-tutee'),
    path('create-tutor-subject/', views.createTutorSubject, name='create-tutor-subject'),
    path('create-tutee-hours/', views.createTuteeHours, name='create-tutee-hours'),
    path('tutors_update/<str:pk>/', views.updateTutor, name= "update-tutor_s"),

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])




