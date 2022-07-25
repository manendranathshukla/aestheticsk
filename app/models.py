
from django.db import models
from django.db.models import Model


class WhyAesthetics(Model):
    name=models.CharField(max_length=50)
    iconUrl=models.URLField(max_length=200)

    def __str__(self):
        return self.name
    

class Specialized(Model):
    name=models.CharField(max_length=50)
    imgUrl=models.URLField(max_length=200)

    def __str__(self):
        return self.name

class Service(Model):
    name=models.CharField(max_length=50)
    iconUrl=models.URLField(max_length=200)
    mainDivBackImageUrl=models.URLField(max_length=200,blank=True,null=True)

    def __str__(self):
        return self.name

class ServiceImage(Model):
    service=models.ForeignKey(Service,on_delete=models.CASCADE)
    imgUrl=models.URLField(max_length=200)
    

class Contact(Model):
    office_address=models.TextField()
    office_email=models.CharField(max_length=50)
    office_contact=models.CharField(max_length=50)
    linkedin=models.URLField(max_length=200,null=True,blank=True)
    facebook=models.URLField(max_length=200,null=True,blank=True)
    instagram=models.URLField(max_length=200,null=True,blank=True)
    twitter=models.URLField(max_length=200,null=True,blank=True)
    youtube=models.URLField(max_length=200,null=True,blank=True)





class About(Model):
    content=models.TextField()
    footer_content=models.TextField(null=True, blank=True)
    footer_meta_content=models.CharField(max_length=100,blank=True,null=True)


class Designer(Model):
    name=models.CharField(max_length=50)
    bio=models.TextField(null=True, blank=True)
    profilePic=models.URLField(max_length=200,null=True,blank=True)
    linkedin=models.URLField(max_length=200,null=True,blank=True)
    facebook=models.URLField(max_length=200,null=True,blank=True)
    instagram=models.URLField(max_length=200,null=True,blank=True)
    twitter=models.URLField(max_length=200,null=True,blank=True)
    youtube=models.URLField(max_length=200,null=True,blank=True)
    def __str__(self):
        return self.name



class Room(Model):
    name=models.CharField(max_length=50)
    mainDivBackImageUrl=models.URLField(max_length=200)
    designedBy=models.ForeignKey(Designer,on_delete=models.CASCADE)
    thumbnailImgUrl=models.URLField(max_length=200,null=True,blank=True)
    showFeatured=models.BooleanField(default=False)
    showTrending=models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Images(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    isFeatured=models.BooleanField(default=False)
    isTrending=models.BooleanField(default=False)
    image = models.URLField(max_length=200)

    @property
    def custom_id(self):
        return str(self.room.name)+'sample'+str(self.id) ; 
    def __str__(self):
        return str(self.custom_id)


class BookSession(Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    number=models.IntegerField(max_length=10)
    pincode=models.IntegerField(max_length=6)
    address=models.TextField(null=True, blank=True)
    designer=models.ForeignKey(Designer,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.name)+str(self.number) + " -> " + str(self.designer.name) 



class BookDesign(Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    number=models.IntegerField(max_length=10)
    pincode=models.IntegerField(max_length=6)
    address=models.TextField(null=True, blank=True)
    message=models.TextField(null=True, blank=True)
    interestedDesign=models.ForeignKey(Images,on_delete=models.CASCADE,null=True)
    interestedServiceDesign=models.ForeignKey(ServiceImage,on_delete=models.CASCADE,null=True)
    designer=models.ForeignKey(Designer,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)