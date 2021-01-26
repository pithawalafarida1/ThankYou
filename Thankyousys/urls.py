from django.contrib import admin
from django.urls import path
from Thankyousys import views

urlpatterns = [
    path("", views.login, name='home1'),
    path("register",views.register,name="register"),
    
    path("make_badges_table",views.make_badges_table,name="make_badges_table"),
    path("loggedin",views.loggedin,name="loggedin"),
    path("test", views.test,name = 'home'),
    path("testkor", views.testkor, name="homekor"),
    path("login", views.login,name = 'login'),
    path("eng_emp_test", views.EngEmpTest,name = 'English_Employee_Test'),
    path("eng_ven_test", views.EngVenTest,name = 'English_Vendor_Test'),
    path("recognition_test", views.RecognitionTest,name = 'English_Recognition_Test'),
    path("recognition_kor", views.RecognitionKorean,name = 'English_Recognition_Kor'),
    path("kor_emp", views.KorEmp,name = 'Korean_Employee'),
    path("kor_ven", views.KorVen,name = 'Korean_Vendor'),
    path("add_rnr/", views.RnRAdd,name = 'Add_Rnr'),
    path("vendor_rnr/", views.VendorAdd,name = 'Vendor_Rnr'),
]