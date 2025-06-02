from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('rights/', views.rights_view, name='rights'),

    path('lawyers/', views.lawyers, name='lawyers'),

    path('forum/', views.forum, name='forum'),

    path('documents/', views.documents_view, name='documents'),
    path('documents/<int:doc_id>/', views.document_detail, name='document_detail'),
    path('documents/<int:doc_id>/generate/', views.generate_document, name='generate_document'),
    
    path('emergency/', views.emergency, name='emergency'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Password reset paths
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
