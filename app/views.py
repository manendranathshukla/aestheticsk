

from django.shortcuts import render, get_object_or_404,redirect,reverse
from django.db.models import Count,Q
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from app.models import *

from django.http import JsonResponse
# Create your views here.
from django.template.loader import render_to_string



from django.template import RequestContext


def custom_page_not_found_view(request, exception):
    return render(request, "pageNotFound.html", {})
def custom_internal_server_error_view(request, *args, **argv):
    return render(request, "500.html", status=500)

def home(request):
    if 'term' in request.GET:
        qs=Room.objects.filter(name__icontains=request.GET.get('term'))
        svc=Service.objects.filter(name__icontains=request.GET.get('term'))
        names=[]
        for n in qs:
            names.append(n.name)
        if(len(svc)>0):
            for n in svc:
                names.append(n.name)
        return  JsonResponse(names,safe=False)
    whyAsth=WhyAesthetics.objects.all()
    aboutContent=About.objects.first()
    specialization=Specialized.objects.all()
    services=Service.objects.all()
    contact=Contact.objects.first()
    designer=Designer.objects.first()
    rooms=Room.objects.all()
    featuredRooms=Room.objects.filter(showFeatured=True)
    trendingRooms=Room.objects.filter(showTrending=True)
    featuredList=[]
    trendingList=[]
    for o in featuredRooms:
        images= Images.objects.filter(room=o,isFeatured=True)
        featuredList.append([o,images])
    for t in trendingRooms:
        images= Images.objects.filter(room=t,isTrending=True)
        trendingList.append([t,images])
    context={'whyAsth':whyAsth,'about':aboutContent,'specialization':specialization,'services':services,'contact':contact,"rooms":rooms,'designer':designer,"featuredRoom":featuredList,"trendingRoom":trendingList}
    return render(request,'index.html',context=context)




def room(request,pk):
    if 'term' in request.GET:
        qs=Room.objects.filter(name__icontains=request.GET.get('term'))
        svc=Service.objects.filter(name__icontains=request.GET.get('term'))
        names=[]
        for n in qs:
            names.append(n.name)
        if(len(svc)>0):
            for n in svc:
                names.append(n.name)
        return  JsonResponse(names,safe=False)
    myroom=Room.objects.get(pk=pk)
    images=Images.objects.filter(room=myroom)
    designer=Designer.objects.first()
    contact=Contact.objects.first()
    aboutContent=About.objects.first()
    rooms=Room.objects.all()
    return render(request, "room.html",context={"myroom":myroom,"images":images,'designer':designer,'contact':contact,'about':aboutContent,"rooms":rooms})

def service(request,pk):
    if 'term' in request.GET:
        qs=Room.objects.filter(name__icontains=request.GET.get('term'))
        svc=Service.objects.filter(name__icontains=request.GET.get('term'))
        names=[]
        for n in qs:
            names.append(n.name)
        if(len(svc)>0):
            for n in svc:
                names.append(n.name)
        return  JsonResponse(names,safe=False)
    mysvc=Service.objects.get(pk=pk)
    svcimages=ServiceImage.objects.filter(service=mysvc)
    designer=Designer.objects.first()
    contact=Contact.objects.first()
    aboutContent=About.objects.first()
    rooms=Room.objects.all()
    return render(request, "service.html",context={"mysvc":mysvc,"images":svcimages,'designer':designer,'contact':contact,'about':aboutContent,"rooms":rooms})




def bookSession(request):
    name=request.POST['name']
    email=request.POST['email']
    number=request.POST['number']
    pincode=request.POST['pincode']
    address=request.POST['address']

    BookSession(name=name,email=email,number=number,pincode=pincode,address=address,designer=Designer.objects.first()).save()
    messages.success(request, 'Session Booked Successfully!')
    sess=BookSession.objects.latest('id')
    html_content = render_to_string('emailTemplates/sessionBookedEmail.html', {'name': name,'sessionId':sess.id,'bookeddate':sess.created_at})
    text_content = "..."                      
    msg = EmailMultiAlternatives("Your Session Booked With Us", text_content, settings.EMAIL_HOST_USER, [email])                                      
    msg.attach_alternative(html_content, "text/html")   
    issessemailSentUser=msg.send(fail_silently=False)
    html_contentadmin = render_to_string('emailTemplates/sessionBookedEmailAdmin.html', {'designer':Designer.objects.first(),'name': name,'email':email,'contact':number,'address':address,'pincode':pincode,  'sessionId':sess.id,'bookeddate':sess.created_at})                      
    msgAdmin = EmailMultiAlternatives("Alert : User Booked a Session", text_content, settings.EMAIL_HOST_USER, [Contact.objects.first().office_email])                                      
    msgAdmin.attach_alternative(html_contentadmin, "text/html")                                                                                                                                                                            
    issessemailSentAdmin=msgAdmin.send(fail_silently=False)
    if(issessemailSentUser != 1 and issessemailSentAdmin !=1):
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
    prevUrl=request.META.get('HTTP_REFERER')
    if('services' in prevUrl):
        BookDesign(name=name,email=email,number=number,pincode=pincode,address=address,message=message,interestedServiceDesign=ServiceImage.objects.filter(id=pk)[0],designer=Designer.objects.first()).save()
    if('rooms' in prevUrl):
        BookDesign(name=name,email=email,number=number,pincode=pincode,address=address,message=message,interestedDesign=Images.objects.filter(id=pk)[0],designer=Designer.objects.first()).save()
    messages.success(request, 'Selected Design Booked Successfully!')
    design=BookDesign.objects.latest('id')
    html_content = render_to_string('emailTemplates/designBookedEmail.html', {'name': name,'design':design})
    text_content = "..."                      
    msg = EmailMultiAlternatives("Your Interested Design Booked With Us", text_content, settings.EMAIL_HOST_USER, [email])                                      
    msg.attach_alternative(html_content, "text/html")   
    isdesignemailSentUser=msg.send(fail_silently=False)
    html_contentadmin = render_to_string('emailTemplates/designBookedEmailAdmin.html', {'bookedDesign':design})                      
    msgAdmin = EmailMultiAlternatives("Alert : User Booked Interested Design", text_content, settings.EMAIL_HOST_USER, [Contact.objects.first().office_email])                                      
    msgAdmin.attach_alternative(html_contentadmin, "text/html")                                                                                                                                                                            
    isdesignemailSentAdmin=msgAdmin.send(fail_silently=False)
    if(isdesignemailSentUser != 1 and isdesignemailSentAdmin !=1):
        messages.error(request, 'Email Not Sent!')

    return redirect(request.META.get('HTTP_REFERER'))
    




@login_required(login_url='/aesthetic/login')
def adminPage(request):
    if request.user.is_staff :
        sessionBookedCount=len(BookSession.objects.all())
        bookedDesignCount=len(BookDesign.objects.all())
        rooms=len(Room.objects.all())
        designers=len(Designer.objects.all())
        context={"sessionCount":sessionBookedCount,"designBookedCount":bookedDesignCount,"roomCount":rooms,"designersCount":designers}
        return render(request,"adminArea/index.html",context)
    else:
        return redirect('error')

@login_required(login_url='/aesthetic/login')
def updateAbout(request):
    if request.user.is_staff :
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
    else:
        return redirect('error')

@login_required(login_url='/aesthetic/login')
def viewWhyAestheticsk(request):
    if request.user.is_staff :
        whyAesth=WhyAesthetics.objects.all()
        # if(request.method == "POST"):
        #     name=request.POST['name']
        #     iconUrl=request.POST['iconUrl']
        #     WhyAesthetics(name=name,iconUrl=iconUrl).save()
        #     messages.success(request, 'Saved')
        #     return redirect("adminArea")
        return render(request,"adminArea/whyaestheticsk.html",{"whyAesth":whyAesth})
    else:
        return redirect('error')

@login_required(login_url='/aesthetic/login')
def updateWhyAestheticsk(request,pk):
    if request.user.is_staff :
        singleWhyAesth=WhyAesthetics.objects.filter(id=pk)[0]
        if(request.method == "POST"):
            name=request.POST['name']
            iconUrl=request.POST['iconUrl']
            singleWhyAesth.name=name
            singleWhyAesth.iconUrl=iconUrl
            singleWhyAesth.save()
            messages.success(request, 'Updated')
            return redirect('viewWhyAestheticsk')
        return render(request,"adminArea/updateWhyAesth.html",{"singleWhyAesth":singleWhyAesth})
    else:
        return redirect('error')

@login_required(login_url='/aesthetic/login')
def addWhyAestheticsk(request):
    if request.user.is_staff :
        if(request.method == "POST"):
            name=request.POST['name']
            iconUrl=request.POST['iconUrl']
            WhyAesthetics(name=name,iconUrl=iconUrl).save()
            messages.success(request, 'Added!!')
            return redirect('viewWhyAestheticsk')
        return render(request,"adminArea/updateWhyAesth.html")
    else:
        return redirect('error')

@login_required(login_url='/aesthetic/login')
def delWhyAestheticsk(request,pk):
    if request.user.is_staff :
            singleWhyAesth=WhyAesthetics.objects.filter(id=pk)[0]
            singleWhyAesth.delete()
            messages.success(request,"Deleted!!")
            return redirect('viewWhyAestheticsk')
            
    else:
        return redirect('error')

@login_required(login_url='/aesthetic/login')
def addSpecialized(request):
    if request.user.is_staff :
        if(request.method == "POST"):
            name=request.POST['name']
            imgUrl=request.POST['imgUrl']
            Specialized(name=name,imgUrl=imgUrl).save()
            print("saved")
            messages.success(request, 'Saved')
            return redirect("viewSpecialized")
        return render(request,"adminArea/updateSpecialized.html")
    else:
        return redirect('error')

@login_required(login_url='/aesthetic/login')
def viewSpecialized(request):
    if request.user.is_staff :
        spclz=Specialized.objects.all()
        return render(request,"adminArea/viewSpecialized.html",{"spclz":spclz})
    else:
        return redirect('error')

@login_required(login_url='/aesthetic/login')
def updateSpecialized(request,pk):
    if request.user.is_staff :
        spclz=Specialized.objects.filter(id=pk)[0]
        if(request.method == "POST"):
            name=request.POST['name']
            imgUrl=request.POST['imgUrl']
            spclz.name=name
            spclz.imgUrl=imgUrl
            spclz.save()
            messages.success(request, 'Update!!')
            return redirect("viewSpecialized")
        return render(request,"adminArea/updateSpecialized.html",{"spclz":spclz})
    else:
        return redirect('error')

@login_required(login_url='/aesthetic/login')
def delSpecialized(request,pk):
    if request.user.is_staff :
        spclz=Specialized.objects.filter(id=pk)[0]
        spclz.delete()
        messages.success(request, 'Deleted!!')
        return redirect("viewSpecialized")
    else:
        return redirect('error')


@login_required(login_url='/aesthetic/login')
def viewService(request):
    if request.user.is_staff :
        svc=Service.objects.all()
        return render(request,"adminArea/viewServices.html",{"svc":svc})
    else:
        return redirect('error')

@login_required(login_url='/aesthetic/login')
def addService(request):
    if request.user.is_staff :
        if(request.method == "POST"):
            name=request.POST['name']
            iconUrl=request.POST['iconUrl']
            mainDivBackImageUrl=request.POST['mainDivBackImageUrl']
            
            Service(name=name,iconUrl=iconUrl,mainDivBackImageUrl=mainDivBackImageUrl).save()
            messages.success(request, 'Added!!')
            return redirect("viewService")
        return render(request,"adminArea/updateService.html")
    else:
        return redirect('error')


@login_required(login_url='/aesthetic/login')
def updateService(request,pk):
    if request.user.is_staff :
        svc=Service.objects.filter(id=pk)[0]
        if(request.method == "POST"):
            name=request.POST['name']
            iconUrl=request.POST['iconUrl']
            mainDivBackImageUrl=request.POST['mainDivBackImageUrl']
            svc.name=name
            svc.iconUrl=iconUrl
            svc.mainDivBackImageUrl=mainDivBackImageUrl
            svc.save()
            messages.success(request, 'Updated!!')
            return redirect("viewService")
        return render(request,"adminArea/updateService.html",{"svc":svc})
    else:
        return redirect('error')

@login_required(login_url='/aesthetic/login')
def delService(request,pk):
    if request.user.is_staff :
        svc=Service.objects.filter(id=pk)[0]
        svc.delete()
        messages.success(request, 'Deleted!!')
        return redirect("viewService")
    else:
        return redirect('error')



@login_required(login_url='/aesthetic/login')
def updateContact(request):
    if request.user.is_staff :
        contactDetails= Contact.objects.first()
        if(request.method == "POST"):
            address=request.POST['address']
            email=request.POST['email']
            contact=request.POST['contact']
            facebook=request.POST['facebook']
            linkedin=request.POST['linkedin']
            twitter=request.POST['twitter']
            instagram=request.POST['instagram']
            youtube=request.POST['youtube']
            
            contactDetails.office_address=address
            contactDetails.office_email=email
            contactDetails.office_contact=contact
            contactDetails.facebook=facebook
            contactDetails.linkedin=linkedin
            contactDetails.twitter=twitter
            contactDetails.instagram=instagram
            contactDetails.youtube=youtube
            
            contactDetails.save()
        
            messages.success(request, 'Contact Details Updated Successfully!')
            return redirect("adminArea")
        return render(request,"adminArea/updateContact.html",context={"contactDetails":contactDetails})
    else:
        return redirect('error')

@login_required(login_url='/aesthetic/login')
def updateDesigner(request):
    if request.user.is_staff :
        designer= Designer.objects.first()
        if(request.method == "POST"):
            name=request.POST['name']
            bio=request.POST['bio']
            profile=request.POST['profile']
            linkedin=request.POST['linkedin']
            facebook=request.POST['facebook']
            twitter=request.POST['twitter']
            instagram=request.POST['instagram']
            youtube=request.POST['youtube']
            designer.name=name
            designer.bio=bio
            designer.profilePic=profile
            designer.linkedin=linkedin
            designer.facebook=facebook
            designer.instagram=instagram
            designer.twitter=twitter
            designer.youtube=youtube
            designer.save()
            messages.success(request, 'Updated')
            return redirect("adminArea")
        return render(request,"adminArea/updateDesigner.html",context={"designer":designer})
    else:
        return redirect('error')


# @login_required(login_url='/aesthetic/login')
# def addDesigner(request):
#     if request.user.is_staff :
#         if(request.method == "POST"):
#             name=request.POST['name']
#             bio=request.POST['bio']
#             profile=request.POST['profile']
#             linkedin=request.POST['linkedin']
#             facebook=request.POST['facebook']
#             twitter=request.POST['twitter']
#             instagram=request.POST['instagram']
#             youtube=request.POST['youtube']
#             designer.name=name
#             designer.bio=bio
#             designer.profilePic=profile
#             designer.linkedin=linkedin
#             designer.facebook=facebook
#             designer.instagram=instagram
#             designer.twitter=twitter
#             designer.youtube=youtube
#             Designer(name=name,bio=bio,profilePic=profile,linkedin=linkedin,facebook=facebook,instagram=instagram,twitter=twitter,youtube=youtube).save()
#             messages.success(request, 'New Designer Added Succesfully!')
#             return redirect("adminArea")
#         return render(request,"adminArea/addDesigner.html")
#     else:
#         return redirect('error')



# @login_required(login_url='/aesthetic/login')
# def viewDesigners(request):
#     if request.user.is_staff :
#         designers=Designer.objects.all()
#         return render(request,"adminArea/designers.html",{"designers":designers})
#     else:
#         return redirect('error')




# @login_required(login_url='/aesthetic/login')
# def delDesigner(request,pk):
#     if request.user.is_staff :
#         Designer.objects.filter(id=pk)[0].delete()
#         messages.success(request,"Designer Deleted Succesfully!")
#         return redirect(request.META.get('HTTP_REFERER'))
#     else:
#         return redirect('error')



@login_required(login_url='/aesthetic/login')
def viewBookedSessions(request):
    if request.user.is_staff :
        sessions=BookSession.objects.all()
        context={"sessions":sessions}
        return render(request,"adminArea/bookedSession.html",context=context)
    else:
        return redirect('error')

@login_required(login_url='/aesthetic/login')
def viewBookedDesigns(request):
    if request.user.is_staff :
        designs=BookDesign.objects.all()
        context={"designs":designs}
        return render(request,"adminArea/bookedDesign.html",context=context)
    else:
        return redirect('error')
@login_required(login_url='/aesthetic/login')
def viewRooms(request):
    if request.user.is_staff :
        if request.method == 'POST':
            featured = request.POST.getlist('featured')
            trending = request.POST.getlist('trending')
            # print(trending)
            # if(len(featured) > 1 and len(trending) > 1):
            #     messages.error(request,"You are allowed to make only one room featured and trending")
            #     return redirect(request.META.get('HTTP_REFERER'))
            # else:
            for f in featured:
                fl=f.split(',')
                
                room=Room.objects.filter(id=int(fl[0]))[0]
                
                if(fl[1] == '1'):
                    room.showFeatured=True
                else: 
                    room.showFeatured=False 
                room.save()
            for t in trending:
                tl=t.split(',')
                room=Room.objects.filter(id=int(tl[0]))[0]
                if(tl[1] == '1'):
                    room.showTrending=True
                else: 
                    room.showTrending=False 
                room.save()
            messages.success(request,"Updated")
            return redirect(request.META.get('HTTP_REFERER'))
        rooms=Room.objects.all()
        context={"rooms":rooms}
        return render(request,"adminArea/rooms.html",context=context)
    else:
        return redirect('error')


@login_required(login_url='/aesthetic/login')
def addRoom(request):
    if request.user.is_staff :
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
    else:
        return redirect('error')


@login_required(login_url='/aesthetic/login')
def viewRoomImage(request,pk):
    if request.user.is_staff :
        room=Room.objects.filter(id=pk)[0]
        images=Images.objects.filter(room=room)
        context={"room":room,"images":images}
        if(request.method == "POST"):
            featured = request.POST.getlist('featured')
            trending = request.POST.getlist('trending')
        
            if( len([ o for o in trending if o[-1] == '1']) > 9):
                messages.error(request,"only 9 designs can be in trending")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                for f in featured:
                    fl=f.split(',')
                    
                    roomImage=Images.objects.filter(id=int(fl[0]))[0]
                    
                    if(fl[1] == '1'):
                        roomImage.isFeatured=True
                    else: 
                        roomImage.isFeatured=False 
                    roomImage.save()
                for t in trending:
                    tl=t.split(',')
                    roomImage=Images.objects.filter(id=int(tl[0]))[0]
                    if(tl[1] == '1'):
                        roomImage.isTrending=True
                    else: 
                        roomImage.isTrending=False 
                    roomImage.save()
                messages.success(request,"Updated")
                return redirect(request.META.get('HTTP_REFERER'))
        
        return render(request,"adminArea/roomImage.html",context)
    else:
        return redirect('error')



@login_required(login_url='/aesthetic/login')
def viewServiceImage(request,pk):
    if request.user.is_staff :
        service=Service.objects.filter(id=pk)[0]
        images=ServiceImage.objects.filter(service=service)
        context={"service":service,"images":images}
        return render(request,"adminArea/serviceImage.html",context)
    else:
        return redirect('error')



@login_required(login_url='/aesthetic/login')
def addRoomImage(request):
    if request.user.is_staff :
        rooms=Room.objects.all()
        context={"rooms":rooms}
        if(request.method == "POST"):
            imgurl=request.POST['designUrl']
            checks=request.POST.getlist('checks')
            room=request.POST['rooms']
            roomObj=Room.objects.filter(id=int(room))[0]
            if("showFeatured" in checks):
                showFeatured=True
            else:
                showFeatured=False
            if("showTrending" in checks):
                if(len(Images.objects.filter(isTrending=True)) == 9):
                    messages.error(request,"only 9 designs can be in trending")
                    return redirect('viewRoomImage',pk=roomObj.id)
                showTrending=True
            else:
                showTrending=False
            Images(room=roomObj,isFeatured=showFeatured,isTrending=showTrending,image=imgurl).save()
            messages.success(request, 'Image Added Successfully!')
            return redirect('viewRoomImage',pk=roomObj.id)
        return render(request,"adminArea/addRoomImage.html",context=context)
    else:
        return redirect('error')

@login_required(login_url='/aesthetic/login')
def addServiceImage(request):
    if request.user.is_staff :
        rooms=Room.objects.all()
        svc=Service.objects.all()
        context={"rooms":rooms,"svc":svc}
        if(request.method == "POST"):
            imgurl=request.POST['designUrl']
            service=request.POST['svc']
            serviceObj=Service.objects.filter(id=int(service))[0]
            ServiceImage(service=serviceObj,imgUrl=imgurl).save()
            messages.success(request, 'Image Added Successfully!')
            return redirect('viewServiceImage',pk=serviceObj.id)
        return render(request,"adminArea/addRoomImage.html",context=context)
    else:
        return redirect('error')




@login_required(login_url='/aesthetic/login')
def delRoom(request,pk):
    if request.user.is_staff :
        pk=Room.objects.filter(id=pk)[0]
        pk.delete()
        messages.success(request, 'Room Deleted Successfully!')
        return redirect("adminArea")
    else:
        return redirect('error')




@login_required(login_url='/aesthetic/login')
def delBookedDesign(request,pk):
    if request.user.is_staff :
        BookDesign.objects.filter(id=pk).delete()
        messages.success(request,"Data deleted !!")
        return redirect("adminArea")
    else:
        return redirect('error')


@login_required(login_url='/aesthetic/login')
def delBookedSession(request,pk):
    if request.user.is_staff :
        BookSession.objects.filter(id=pk).delete()
        messages.success(request,"Data deleted !!")
        return redirect("adminArea")
    else:
        return redirect('error')
@login_required(login_url='/aesthetic/login')
def delRoomImage(request,pk):
    if request.user.is_staff :
        Images.objects.filter(id=pk).delete()
        messages.success(request,"Image deleted !!")
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('error')
@login_required(login_url='/aesthetic/login')
def delServiceImage(request,pk):
    if request.user.is_staff :
        ServiceImage.objects.filter(id=pk).delete()
        messages.success(request,"Image deleted !!")
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('error')
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
            messages.error(request, f'account done not exit plz sign in')
    return render(request,"adminArea/login.html")

def registerPage(request):
    form=CreateUserForm()
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            if(len(User.objects.filter(email=email))>0):
                messages.error(request,"Email already used!!")
                return redirect(request.META.get('HTTP_REFERER'))
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,"Account created for "+user)
            return redirect('login')
    context={'form':form}
    return render(request,"adminArea/register.html",context)


@login_required(login_url='/aesthetic/login')
def Logout(request):
    logout(request)
    return redirect('homepage')


def errorPage(request):
    return render(request,"pageNotFound.html")

def searchPage(request):
    if request.method == 'POST':
        q=request.POST['search']
        if(len(Room.objects.filter(name__icontains=q))>0):
            results=Room.objects.filter(name__icontains=q)
        else:
            results=Service.objects.filter(name__icontains=q)
        return render(request,"searchResults.html",{"searchResults":results,'q':q})

def commingSoonPage(request):
    return render(request,"commingSoon.html",{"contact":Contact.objects.first()})




