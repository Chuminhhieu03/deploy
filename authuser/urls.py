from django.urls import path
from authuser import views

urlpatterns = [
    path('', views.edit_profile, name='edit_profile_user'),
    path('feedback/', views.feedback_user, name='feedback_user'),
    path('login/', views.handleLogin, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('reset/<uidb64>/<token>',views.SetNewPasswordView.as_view(),name='reset'),
    path('change_password/', views.changepassword, name='changepassword'),
    path('upgrade/', views.upgrade, name='upgrade'),
    path('checkout/', views.upgrade_checkout, name='upgrade_checkout'),
    path('success/', views.upgrade_success, name='upgrade_success'),
]
