from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime
from Thankyousys.models import Employee
from Thankyousys.models import Badges
from Thankyousys.models import RnR
from Thankyousys.models import Vendor
from Thankyousys.models import EmpUser
from Thankyousys.models import BadgesSentTable
from .serializers import EmployeeSerializer
from .serializers import BadgesSerializer
from .serializers import RnRSerializer
from .serializers import VendorSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.http import JsonResponse
from django.core.serializers import serialize
from django.core.mail import send_mail
from django.db.models import Count
from itertools import chain

#imports for html email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

#to show messages
from django.contrib import messages

from django.utils.datastructures import MultiValueDictKeyError

#for sign up
from django.contrib.auth.models import User,auth

# Create your views here.
def loggedin(request):
    if request.method=="POST":
        try:
            usernamelogin = request.POST['usernamelogin']
            passwordlogin=request.POST['passwordlogin']
        except MultiValueDictKeyError:
            passwordlogin= False
            usernamelogin = False
        #usernamelogin=request.POST['usernamelogin']
        #passwordlogin=request.POST['passwordlogin']
        if EmpUser.objects.filter(username=usernamelogin,password=passwordlogin).exists():
            loggedinemployee=EmpUser.objects.filter(username=usernamelogin)
            Emplist=EmpUser.objects.all()
                
            return render(request,'eng_emp_test.html',{'loggedinemployee':loggedinemployee,'Emplist':Emplist})
            #return redirect("/eng_emp_test",{'loggedinemployee':loggedinemployee})
        else:
            # return redirect("/make_badges_table")
            print("Cannot Login")

def register(request):
    if request.method=="POST":
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']
        if password1==password2:
            if EmpUser.objects.filter(username=username).exists():
                print("Username taken away!")
            else:
                registered_user= EmpUser(username=username,password=password1,email=email)
                registered_user.save()
                
                
                return redirect("/eng_emp_test")
            
    else:
        return render(request,"login.html")
    



def test(request):
    return render(request,'index.html',context)

def testkor(request):
    return render(request,'kortest.html')

def login(request):
    return render(request,'login.html')

def EngEmpTest(request):
    username="Farida Pithawala1" #SSO username will come here
    thanksent = RnR.objects.filter(empsent=username,badgetype="Thank You").count()
    kudossent = RnR.objects.filter(empsent=username,badgetype="Kudos").count()
    congratsent = RnR.objects.filter(empsent=username,badgetype="Congratulations").count()
    customsent = RnR.objects.filter(empsent=username,badgetype="Custom Badge").count()
    greatsent = RnR.objects.filter(empsent=username,badgetype="Great Job").count()
    bravosent = RnR.objects.filter(empsent=username,badgetype="Bravo").count()
    thankrecvd = RnR.objects.filter(emprecvd=username,badgetype="Thank You").count()
    kudosrecvd = RnR.objects.filter(emprecvd=username,badgetype="Kudos").count()
    congratrecvd = RnR.objects.filter(emprecvd=username,badgetype="Congratulations").count()
    customrecvd = RnR.objects.filter(emprecvd=username,badgetype="Custom Badge").count()
    greatrecvd = RnR.objects.filter(emprecvd=username,badgetype="Great Job").count()
    bravorecvd = RnR.objects.filter(emprecvd=username,badgetype="Bravo").count()
    employeelist = Employee.objects.all()
    context = {'username1':username,'bravorecvd':bravorecvd,'greatrecvd':greatrecvd,'customrecvd':customrecvd,'congratrecvd':congratrecvd,'kudosrecvd':kudosrecvd,'thankrecvd':thankrecvd,
                'bravosent':bravosent,'greatsent':greatsent,'customsent':customsent,'congratsent':congratsent,'kudossent':kudossent,'thanksent':thanksent,'employeelist': employeelist}
    return render(request,'eng_emp_test.html',context)

def EngVenTest(request):
    return render(request,'eng_ven_test.html')

def RecognitionTest(request):
    sendsent = []
    sendrec = []
    recsent = []
    recrec = []
    lastsendsend = []
    lastsendrec = []
    lastrecsend = []
    lastrecrec = []
    topsend = RnR.objects.all().values('empsent').annotate(total=Count('empsent')).order_by('-total')[:5]
    toprec = RnR.objects.all().values('emprecvd').annotate(total=Count('emprecvd')).order_by('-total')[:5]
    last5 = RnR.objects.all().order_by('-id').values('empsent','emprecvd')[:5]
    
    last5pic0 = Employee.objects.filter(name=last5[0]['empsent']).values('picture')
    last5pic1 = Employee.objects.filter(name=last5[1]['empsent']).values('picture')
    last5pic2 = Employee.objects.filter(name=last5[2]['empsent']).values('picture')
    last5pic3 = Employee.objects.filter(name=last5[3]['empsent']).values('picture')
    last5pic4 = Employee.objects.filter(name=last5[4]['empsent']).values('picture')

    last5picR0 = Employee.objects.filter(name=last5[0]['emprecvd']).values('picture')
    last5picR1 = Employee.objects.filter(name=last5[1]['emprecvd']).values('picture')
    last5picR2 = Employee.objects.filter(name=last5[2]['emprecvd']).values('picture')
    last5picR3 = Employee.objects.filter(name=last5[3]['emprecvd']).values('picture')
    last5picR4 = Employee.objects.filter(name=last5[4]['emprecvd']).values('picture')

    last5pic = list(chain(last5pic0,last5pic1,last5pic2,last5pic3,last5pic4))
    last5picR = list(chain(last5picR0,last5picR1,last5picR2,last5picR3,last5picR4))

    sendpic0=Employee.objects.filter(name=topsend[0]['empsent']).values('picture')
    sendpic1=Employee.objects.filter(name=topsend[1]['empsent']).values('picture')
    sendpic2=Employee.objects.filter(name=topsend[2]['empsent']).values('picture')
    sendpic3=Employee.objects.filter(name=topsend[3]['empsent']).values('picture')
    sendpic4=Employee.objects.filter(name=topsend[4]['empsent']).values('picture')
    
    for i in range(5):
        sendsent.append(RnR.objects.filter(empsent=topsend[i]['empsent']).count())
        sendrec.append(RnR.objects.filter(emprecvd=topsend[i]['empsent']).count())
        recsent.append(RnR.objects.filter(empsent=toprec[i]['emprecvd']).count())
        recrec.append(RnR.objects.filter(emprecvd=toprec[i]['emprecvd']).count())
        lastsendsend.append(RnR.objects.filter(empsent=last5[i]['empsent']).count())
        lastsendrec.append(RnR.objects.filter(emprecvd=last5[i]['empsent']).count())
        lastrecsend.append(RnR.objects.filter(empsent=last5[i]['emprecvd']).count())
        lastrecrec.append(RnR.objects.filter(emprecvd=last5[i]['emprecvd']).count())

    recpic0=Employee.objects.filter(name=toprec[0]['emprecvd']).values('picture')
    recpic1=Employee.objects.filter(name=toprec[1]['emprecvd']).values('picture')
    recpic2=Employee.objects.filter(name=toprec[2]['emprecvd']).values('picture')
    recpic3=Employee.objects.filter(name=toprec[3]['emprecvd']).values('picture')
    recpic4=Employee.objects.filter(name=toprec[4]['emprecvd']).values('picture')

    sendpics = list(chain(sendpic0,sendpic1,sendpic2,sendpic3,sendpic4))
    recpics = list(chain(recpic0,recpic1,recpic2,recpic3,recpic4))

    username="Harsh Shinde" #SSO username will come here
    thanksent = RnR.objects.filter(empsent=username,badgetype="Thank You").count()
    kudossent = RnR.objects.filter(empsent=username,badgetype="Kudos").count()
    congratsent = RnR.objects.filter(empsent=username,badgetype="Congratulations").count()
    customsent = RnR.objects.filter(empsent=username,badgetype="Custom Badge").count()
    greatsent = RnR.objects.filter(empsent=username,badgetype="Great Job").count()
    bravosent = RnR.objects.filter(empsent=username,badgetype="Bravo").count()
    thankrecvd = RnR.objects.filter(emprecvd=username,badgetype="Thank You").count()
    kudosrecvd = RnR.objects.filter(emprecvd=username,badgetype="Kudos").count()
    congratrecvd = RnR.objects.filter(emprecvd=username,badgetype="Congratulations").count()
    customrecvd = RnR.objects.filter(emprecvd=username,badgetype="Custom Badge").count()
    greatrecvd = RnR.objects.filter(emprecvd=username,badgetype="Great Job").count()
    bravorecvd = RnR.objects.filter(emprecvd=username,badgetype="Bravo").count()

    context =   {
                'bravorecvd':bravorecvd,'greatrecvd':greatrecvd,'customrecvd':customrecvd,'congratrecvd':congratrecvd,'kudosrecvd':kudosrecvd,'thankrecvd':thankrecvd,
                'bravosent':bravosent,'greatsent':greatsent,'customsent':customsent,'congratsent':congratsent,'kudossent':kudossent,'thanksent':thanksent,
                'lastsendsend':lastsendsend,'lastsendrec':lastsendrec,'lastrecsend':lastrecsend,'lastrecrec':lastrecrec,
                'topsend': topsend,'toprec':toprec,'sendpics':sendpics,'recpics':recpics,'last5':last5,'last5pic':last5pic,'last5picR':last5picR,
                'sendsent':sendsent,'sendrec':sendrec,'recsent':recsent,'recrec':recrec
                }
    return render(request,'recognitiontest.html',context)

def RecognitionKorean(request):
    sendsent = []
    sendrec = []
    recsent = []
    recrec = []
    lastsendsend = []
    lastsendrec = []
    lastrecsend = []
    lastrecrec = []
    topsend = RnR.objects.all().values('empsent').annotate(total=Count('empsent')).order_by('-total')[:5]
    toprec = RnR.objects.all().values('emprecvd').annotate(total=Count('emprecvd')).order_by('-total')[:5]
    last5 = RnR.objects.all().order_by('-id').values('empsent','emprecvd')[:5]
    
    last5pic0 = Employee.objects.filter(name=last5[0]['empsent']).values('picture')
    last5pic1 = Employee.objects.filter(name=last5[1]['empsent']).values('picture')
    last5pic2 = Employee.objects.filter(name=last5[2]['empsent']).values('picture')
    last5pic3 = Employee.objects.filter(name=last5[3]['empsent']).values('picture')
    last5pic4 = Employee.objects.filter(name=last5[4]['empsent']).values('picture')

    last5picR0 = Employee.objects.filter(name=last5[0]['emprecvd']).values('picture')
    last5picR1 = Employee.objects.filter(name=last5[1]['emprecvd']).values('picture')
    last5picR2 = Employee.objects.filter(name=last5[2]['emprecvd']).values('picture')
    last5picR3 = Employee.objects.filter(name=last5[3]['emprecvd']).values('picture')
    last5picR4 = Employee.objects.filter(name=last5[4]['emprecvd']).values('picture')

    last5pic = list(chain(last5pic0,last5pic1,last5pic2,last5pic3,last5pic4))
    last5picR = list(chain(last5picR0,last5picR1,last5picR2,last5picR3,last5picR4))

    sendpic0=Employee.objects.filter(name=topsend[0]['empsent']).values('picture')
    sendpic1=Employee.objects.filter(name=topsend[1]['empsent']).values('picture')
    sendpic2=Employee.objects.filter(name=topsend[2]['empsent']).values('picture')
    sendpic3=Employee.objects.filter(name=topsend[3]['empsent']).values('picture')
    sendpic4=Employee.objects.filter(name=topsend[4]['empsent']).values('picture')
    
    for i in range(5):
        sendsent.append(RnR.objects.filter(empsent=topsend[i]['empsent']).count())
        sendrec.append(RnR.objects.filter(emprecvd=topsend[i]['empsent']).count())
        recsent.append(RnR.objects.filter(empsent=toprec[i]['emprecvd']).count())
        recrec.append(RnR.objects.filter(emprecvd=toprec[i]['emprecvd']).count())
        lastsendsend.append(RnR.objects.filter(empsent=last5[i]['empsent']).count())
        lastsendrec.append(RnR.objects.filter(emprecvd=last5[i]['empsent']).count())
        lastrecsend.append(RnR.objects.filter(empsent=last5[i]['emprecvd']).count())
        lastrecrec.append(RnR.objects.filter(emprecvd=last5[i]['emprecvd']).count())

    recpic0=Employee.objects.filter(name=toprec[0]['emprecvd']).values('picture')
    recpic1=Employee.objects.filter(name=toprec[1]['emprecvd']).values('picture')
    recpic2=Employee.objects.filter(name=toprec[2]['emprecvd']).values('picture')
    recpic3=Employee.objects.filter(name=toprec[3]['emprecvd']).values('picture')
    recpic4=Employee.objects.filter(name=toprec[4]['emprecvd']).values('picture')

    sendpics = list(chain(sendpic0,sendpic1,sendpic2,sendpic3,sendpic4))
    recpics = list(chain(recpic0,recpic1,recpic2,recpic3,recpic4))

    username="Harsh Shinde" #SSO username will come here
    thanksent = RnR.objects.filter(empsent=username,badgetype="Thank You").count()
    kudossent = RnR.objects.filter(empsent=username,badgetype="Kudos").count()
    congratsent = RnR.objects.filter(empsent=username,badgetype="Congratulations").count()
    customsent = RnR.objects.filter(empsent=username,badgetype="Custom Badge").count()
    greatsent = RnR.objects.filter(empsent=username,badgetype="Great Job").count()
    bravosent = RnR.objects.filter(empsent=username,badgetype="Bravo").count()
    thankrecvd = RnR.objects.filter(emprecvd=username,badgetype="Thank You").count()
    kudosrecvd = RnR.objects.filter(emprecvd=username,badgetype="Kudos").count()
    congratrecvd = RnR.objects.filter(emprecvd=username,badgetype="Congratulations").count()
    customrecvd = RnR.objects.filter(emprecvd=username,badgetype="Custom Badge").count()
    greatrecvd = RnR.objects.filter(emprecvd=username,badgetype="Great Job").count()
    bravorecvd = RnR.objects.filter(emprecvd=username,badgetype="Bravo").count()

    context =   {
                'bravorecvd':bravorecvd,'greatrecvd':greatrecvd,'customrecvd':customrecvd,'congratrecvd':congratrecvd,'kudosrecvd':kudosrecvd,'thankrecvd':thankrecvd,
                'bravosent':bravosent,'greatsent':greatsent,'customsent':customsent,'congratsent':congratsent,'kudossent':kudossent,'thanksent':thanksent,
                'lastsendsend':lastsendsend,'lastsendrec':lastsendrec,'lastrecsend':lastrecsend,'lastrecrec':lastrecrec,
                'topsend': topsend,'toprec':toprec,'sendpics':sendpics,'recpics':recpics,'last5':last5,'last5pic':last5pic,'last5picR':last5picR,
                'sendsent':sendsent,'sendrec':sendrec,'recsent':recsent,'recrec':recrec
                }

    return render(request,'recognitionkor.html',context)

def KorEmp(request):
    employeelist = Employee.objects.all()
    username="Harsh Shinde" #SSO username will come here
    thanksent = RnR.objects.filter(empsent=username,badgetype="Thank You").count()
    kudossent = RnR.objects.filter(empsent=username,badgetype="Kudos").count()
    congratsent = RnR.objects.filter(empsent=username,badgetype="Congratulations").count()
    customsent = RnR.objects.filter(empsent=username,badgetype="Custom Badge").count()
    greatsent = RnR.objects.filter(empsent=username,badgetype="Great Job").count()
    bravosent = RnR.objects.filter(empsent=username,badgetype="Bravo").count()
    thankrecvd = RnR.objects.filter(emprecvd=username,badgetype="Thank You").count()
    kudosrecvd = RnR.objects.filter(emprecvd=username,badgetype="Kudos").count()
    congratrecvd = RnR.objects.filter(emprecvd=username,badgetype="Congratulations").count()
    customrecvd = RnR.objects.filter(emprecvd=username,badgetype="Custom Badge").count()
    greatrecvd = RnR.objects.filter(emprecvd=username,badgetype="Great Job").count()
    bravorecvd = RnR.objects.filter(emprecvd=username,badgetype="Bravo").count()
    employeelist = Employee.objects.all()
    context = {'bravorecvd':bravorecvd,'greatrecvd':greatrecvd,'customrecvd':customrecvd,'congratrecvd':congratrecvd,'kudosrecvd':kudosrecvd,'thankrecvd':thankrecvd,
                'bravosent':bravosent,'greatsent':greatsent,'customsent':customsent,'congratsent':congratsent,'kudossent':kudossent,'thanksent':thanksent,'employeelist': employeelist}
    return render(request,'kor_emp.html',context)

def KorVen(request):
    employeelist = Employee.objects.all()
    context = {'employeelist': employeelist}
    return render(request,'kor_ven.html',context)

@api_view(['GET','POST'])
def make_badges_table(request):
    badge_picture=request.POST.get("badge_picture")
    Received=request.POST.get("Received")
    newobject=BadgesSentTable(Sender="Farida",badge_title=badge_picture,Receiver=Received)
    newobject.save()
    return redirect("/eng_emp_test")
    #return Response()

@api_view(['GET','POST'])
def RnRAdd(request):
    print("Enter")
    serializer = RnRSerializer(data=request.data)
    badge_title = request.POST.get("badgename")
    recipientname = request.POST.get("emprecvd")
    sendername = request.POST.get("empsent")
    reason1 = request.POST.get("message")
    print(recipientname)
    employee1 = EmpUser.objects.get(username=recipientname)
    

    if badge_title=="Kudos":
        badge_link = "https://i.ibb.co/2dTxhv0/kudos.png"
    elif badge_title=="Bravo":
        badge_link = "https://i.ibb.co/nD0x454/Bravo.jpg"
    elif badge_title=="Congratulations":
        badge_link = "https://i.ibb.co/zhNVR2D/congratulations.png"
    elif badge_title=="Great Job":
        badge_link = "https://i.ibb.co/hdKbMP0/great-job.png"
    elif badge_title=="Thank You":
        badge_link = "https://i.ibb.co/Fgmhyfh/Thank-you.png"
    else:
        badge_link = ""

    if serializer.is_valid():
        serializer.save()
    
    html_content = render_to_string("email_template.html",{'Badge_Title':badge_title,'recipient_name':recipientname,'sender_name':sendername,'Badge_Reason':reason1,'Badge_Link':badge_link,'Custom_Text':badge_title})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        #subject
        "You have received a new badge!",
        #content
        text_content,
        #from email
        "donotreply.thankyousystem@gmail.com",
        #recipient user
        [employee1.email]
    )
    email.attach_alternative(html_content,"text/html") 
    email.send()
    return Response(serializer.data)

@api_view(['GET','POST'])
def VendorAdd(request):
    serializer = VendorSerializer(data=request.data)
    badge_title = request.POST.get("badgename")
    vendor_company = request.POST.get("vendorcompany")
    vendor_name = request.POST.get("vendorname")
    recipientname = request.POST.get("empsent")
    reason1 = request.POST.get("message")
    employee1 = Employee.objects.get(name=recipientname)

    if badge_title=="Kudos":
        badge_link = "https://i.ibb.co/2dTxhv0/kudos.png"
    elif badge_title=="Bravo":
        badge_link = "https://i.ibb.co/nD0x454/Bravo.jpg"
    elif badge_title=="Congratulations":
        badge_link = "https://i.ibb.co/zhNVR2D/congratulations.png"
    elif badge_title=="Great Job":
        badge_link = "https://i.ibb.co/hdKbMP0/great-job.png"
    elif badge_title=="Thank You":
        badge_link = "https://i.ibb.co/Fgmhyfh/Thank-you.png"
    else:
        badge_link = ""

    if serializer.is_valid():
        serializer.save()
    
    html_content = render_to_string("email_template1.html",{'Badge_Title':badge_title,'recipient_name':recipientname,'vendor_name':vendor_name,'vendor_company':vendor_company,'Badge_Reason':reason1,'Badge_Link':badge_link,'Custom_Text':badge_title})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        #subject
        "You have received a new badge!",
        #content
        text_content,
        #from email
        "donotreply.thankyousystem@gmail.com",
        #recipient user
        [employee1.email]
    )
    email.attach_alternative(html_content,"text/html")
    email.send()
    return Response(serializer.data)




