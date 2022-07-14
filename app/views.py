
from django.shortcuts import render, get_object_or_404,redirect,reverse
from django.db.models import Count,Q
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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
    messages.success(request, 'Session Booked Successfully!')
    email = EmailMessage(
    subject='Your Session Booked With Us!!!',
    body='Hi '+name+'\nThank you for booking session with us. \n Here is your booked session ID:'+str(BookSession.objects.latest('id').id),
    from_email=settings.EMAIL_HOST_USER,
    to=[email],
    headers={'Content-Type': 'text/plain'},
    )
    isSent=email.send()
    if(isSent != 1):
        messages.error(request, 'Email Not Sent!')
    print("Booking details email successfully!")

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
    sessionBookedCount=len(BookSession.objects.all())
    bookedDesignCount=len(BookDesign.objects.all())
    rooms=len(Room.objects.all())
    designers=len(Designer.objects.all())
    context={"sessionCount":sessionBookedCount,"designBookedCount":bookedDesignCount,"roomCount":rooms,"designersCount":designers}
    return render(request,"adminArea/index.html",context)


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
        messages.success(request, 'Saved')
        return redirect("adminArea")
    return render(request,"adminArea/updateAbout.html",context={"abt":abt})

def updateWhyAestheticsk(request):
    if(request.method == "POST"):
        name=request.POST['name']
        iconUrl=request.POST['iconUrl']
        WhyAesthetics(name=name,iconUrl=iconUrl).save()
        messages.success(request, 'Saved')
        return redirect("adminArea")
    return render(request,"adminArea/updateWhyAesth.html")


def updateSpecialized(request):
    if(request.method == "POST"):
        name=request.POST['name']
        imgUrl=request.POST['imgUrl']
        Specialized(name=name,imgUrl=imgUrl).save()
        print("saved")
        messages.success(request, 'Saved')
        return redirect("adminArea")
    return render(request,"adminArea/updateSpecialized.html")

def updateService(request):
    if(request.method == "POST"):
        name=request.POST['name']
        iconUrl=request.POST['iconUrl']
        Service(name=name,iconUrl=iconUrl).save()
        messages.success(request, 'Saved')
        return redirect("adminArea")
    return render(request,"adminArea/updateService.html")
def updateContact(request):
    contactDetails= Contact.objects.first()
    if(request.method == "POST"):
        address=request.POST['address']
        email=request.POST['email']
        contact=request.POST['contact']
        contactDetails.office_address=address
        contactDetails.office_email=email
        contactDetails.office_contact=contact
        contactDetails.save()
      
        messages.success(request, 'Contact Details Updated Successfully!')
        return redirect("adminArea")
    return render(request,"adminArea/updateContact.html",context={"contactDetails":contactDetails})

def updateDesigner(request):
    designer= Designer.objects.first()
    if(request.method == "POST"):
        name=request.POST['name']
        bio=request.POST['bio']
        linkedin=request.POST['linkedin']
        facebook=request.POST['facebook']
        twitter=request.POST['twitter']
        instagram=request.POST['instagram']
        youtube=request.POST['youtube']
        designer.name=name
        designer.bio=bio
        designer.linkedin=linkedin
        designer.facebook=facebook
        designer.instagram=instagram
        designer.twitter=twitter
        designer.youtube=youtube
        designer.save()
        messages.success(request, 'Saved')
        return redirect("adminArea")
    return render(request,"adminArea/updateDesigner.html",context={"designer":designer})

def viewBookedSessions(request):
    sessions=BookSession.objects.all()
    context={"sessions":sessions}
    return render(request,"adminArea/bookedSession.html",context=context)


def viewBookedDesigns(request):
    designs=BookDesign.objects.all()
    context={"designs":designs}
    return render(request,"adminArea/bookedDesign.html",context=context)

def viewRooms(request):
    rooms=Room.objects.all()
    context={"rooms":rooms}
    return render(request,"adminArea/rooms.html",context=context)

def addRoom(request):
    designers=Designer.objects.all()
    context={"designers":designers}
    if(request.method == "POST"):
        name=request.POST['name']
        mainDivBackImageUrl=request.POST['maindivbg']
        designerid=request.POST['designer']
        thumbnailImgUrl=request.POST['thumbnail']
        Room(name=name,mainDivBackImageUrl=mainDivBackImageUrl,designedBy=Designer.objects.filter(id=designerid)[0],thumbnailImgUrl=thumbnailImgUrl).save()
      
        messages.success(request, 'New Room Added Successfully!')
        return redirect("adminArea")
    return render(request,"adminArea/addRoom.html",context)

def viewRoomImage(request,pk):
    room=Room.objects.filter(id=pk)[0]
    images=Images.objects.filter(room=room)
    context={"room":room,"images":images}
    if(request.method == "POST"):
        imgurl=request.POST['imgUrl']
        Images(room=room,image=imgurl).save()
        messages.success(request, 'Image Added Successfully!')
        return redirect(request.META.get('HTTP_REFERER'))

    
    return render(request,"adminArea/roomImage.html",context)

def delRoom(request,pk):
    pk=Room.objects.filter(id=pk)[0]
    pk.delete()
    messages.success(request, 'Room Deleted Successfully!')
    return redirect("adminArea")

def delBookedDesign(request,pk):
    BookDesign.objects.filter(id=pk).delete()
    messages.success(request,"Data deleted !!")
    return redirect("adminArea")

def delBookedSession(request,pk):
    BookSession.objects.filter(id=pk).delete()
    messages.success(request,"Data deleted !!")
    return redirect("adminArea")


def loginPage(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' Welcome {username} !!')
            return redirect('adminArea')
        else:
            messages.info(request, f'account done not exit plz sign in')
    return render(request,"adminArea/login.html")

def registerPage(request):
    form=CreateUserForm()
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,"Account created for "+user)
            return redirect('login')
    context={'form':form}
    return render(request,"adminArea/register.html",context)
