#from django.db import models
from django.db import models
from django.db.models import *
from djangotoolbox.fields import ListField, EmbeddedModelField
import os
from django.contrib.auth.models import User

from django_facebook.models import BaseFacebookProfileModel


class TrocaUserProfile(BaseFacebookProfileModel):
    '''
    From django_facebook
    '''
    user = models.OneToOneField('auth.User')
    image = models.ImageField(blank=True, null=True, upload_to='newprofiles', max_length=255)

    class Meta:
        app_label = 'django_facebook'

#Make sure we create a MyCustomProfile when creating a User
from django.db.models.signals import post_save

def create_facebook_profile(sender, instance, created, **kwargs):
    if created:
        TrocaUserProfile.objects.create(user=instance)

post_save.connect(create_facebook_profile, sender=User)


class Category(models.Model):
    categoryTitle = CharField(max_length=100, )
    parentCategory = models.ForeignKey('self', null=True, blank=True, related_name='subs')

    def __unicode__(self):
        oneUp = self.parentCategory
        printable = self.categoryTitle
        while oneUp:    
            printable = oneUp.categoryTitle +'>' + printable
            oneUp = oneUp.parentCategory
        
        return printable

    def howToOrder(self):
        oneUp = self.parentCategory
        printable = self.categoryTitle
        while oneUp:    
            printable = oneUp.categoryTitle +'>'+ printable
            oneUp = oneUp.parentCategory
        
        return printable

    class Meta:
        verbose_name_plural = "Categories"
        #app_label = 'relational'


class GenericItem(models.Model):
    owner_id = IntegerField()
    title = CharField(max_length=70, )
    description = CharField(max_length=140, )
    value = IntegerField()
    location = CharField(max_length=70, blank=True, null=True)
    offers = ListField(EmbeddedModelField('Offer'), editable=False)

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = False
        app_label = 'nonrel_troca_app'
        db_table = 'generic_item'
        #allow_inheritance = True
        

class ItemInOffer(models.Model):
    itemTitle = CharField(max_length=70, )
    value = IntegerField()
    item = ForeignKey(GenericItem)

    def __unicode__(self):
        return self.itemTitle
    
    class Meta:
        app_label = 'nonrel_troca_app'

class Offer(models.Model):
    title = CharField(max_length=70, )
    author_id = IntegerField()
    author = CharField(max_length=70, )
    items = ListField(EmbeddedModelField('ItemInOffer'), editable=False)
    
    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'nonrel_troca_app'


class Car(GenericItem):
    kilometers = IntegerField()


