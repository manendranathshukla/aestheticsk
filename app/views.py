
from django.shortcuts import render, get_object_or_404,redirect,reverse
from django.db.models import Count,Q
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages


from app.models import *

# Create your views here.


def home(request):
    whyAsth=WhyAesthetics.objects.all()
    aboutContent=About.objects.first()
    specialization=Specialized.objects.all()
    services=Service.objects.all()
    contact=Contact.objects.first()
    designer=Designer.objects.first()
    rooms=Room.objects.all()
    context={'whyAsth':whyAsth,'about':aboutContent,'specialization':specialization,'services':services,'contact':contact,"rooms":rooms,'designer':designer}
    return render(request,'index.html',context=context)




def room(request,pk):
    myroom=Room.objects.get(pk=pk)
    images=Images.objects.filter(room=myroom)
    designer=Designer.objects.first()
    contact=Contact.objects.first()
    aboutContent=About.objects.first()
    return render(request, "room.html",context={"myroom":myroom,"images":images,'designer':designer,'contact':contact,'about':aboutContent})





def bookSession(request):
    name=request.POST['name']
    email=request.POST['email']
    number=request.POST['number']
    pincode=request.POST['pincode']
    address=request.POST['address']

    BookSession(name=name,email=email,number=number,pincode=pincode,address=address,designer=Designer.objects.first()).save()
    print("Session Booked Successfully!")
    # id=BookSession.objects.latest('id').id
    # subject = 'Your Session Booked With Us !!!'
    # message = f'Hi {name}, thank you for booking session with us.\n Here is your booking id : {id} '
    # email_from = settings.EMAIL_HOST_USER
    # recipient_list = [email, ]
    # send_mail( subject, message, email_from, recipient_list )
    return redirect('homepage')
    


def bookDesign(request,pk):
    name=request.POST['name']
    email=request.POST['email']
    number=request.POST['number']
    pincode=request.POST['pincode']
    address=request.POST['address']
    message=request.POST['message']

    BookDesign(name=name,email=email,number=number,pincode=pincode,address=address,message=message,interestedDesign=Images.objects.filter(id=pk)[0],designer=Designer.objects.first()).save()
    messages.success(request, 'Selected Design Booked Successfully!')
   
    email = EmailMessage(
    subject='Your Design Booked With Us!!!',
    body='Hi '+name+' thank you for showing interest in our designs. \n Here is your booked design ID:'+str(BookDesign.objects.latest('id').id),
    from_email=settings.EMAIL_HOST_USER,
    to=[email],
    headers={'Content-Type': 'text/plain'},
    )
    email.send()
    print("Booking details email successfully!")

    return redirect(request.META.get('HTTP_REFERER'))
    





def adminPage(request):
    return render(request,"admin/index.html")


def updateAbout(request):
    abt = About.objects.first()
    if(request.method == "POST"):
        about=request.POST['about']
        footer_about=request.POST['footer_about']
        meta_about=request.POST['meta_about']
        abt.content=about
        abt.footer_content=footer_about
        abt.footer_meta_content=meta_about
        abt.save()
        return redirect("adminArea")
    return render(request,"admin/updateAbout.html",context={"abt":abt})




