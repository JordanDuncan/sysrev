from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class Researcher(models.Model):
    user = models.OneToOneField(User) #extending the user model used for authentication
    #this already contains Username, Password and Email
    lastViewed = models.DateTimeField(auto_now_add=True)
    #forename = models.CharField(max_length=128)
    #surname = models.CharField(max_length=128)
    insSelection = (
        ('UOG', 'University of Glasgow'),
        ('GCU', 'Glasgow Caledonian University'),
        ('GSU', 'Glasgow Strathclyde University'),
        ('EDI', 'Edinburgh University'),
        ('UWS', 'University of Western Scotland'),
        ('STU', 'St.Andrews University'),
        ('OXF', 'Oxford University'),
        ('CAM', 'Cambridge University'),
        ('OTH', 'Other'),
    )

    institution = models.CharField(max_length=3, choices=insSelection)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username

class Paper(models.Model):
    paperID = models.CharField(max_length=12,unique=True,primary_key=True) #Could change this to the API's document id, I do not know the format and/or constraint of that
    queryID = models.ForeignKey(Query) #Query foreign key
    title = models.CharField(max_length=512)
    authors = models.CharField(max_length=512)
    abstract = models.CharField(max_length=4096)
    publishDate = models.DateField()
    paperUrl = models.URLField()
    documentApproved = models.BooleanField(default = None)
    abstractApproved = models.BooleanField(default = None)
        #Did not implement the the relevance fields as they are referred in the review
        #In fact the same document could be relevant or not relevant for different reviews

    def __unicode__(self):
        return self.title

class Query(models.Model):
    queryID = models.AutoField(primary_key=True)
    researcher = models.ForeignKey(Researcher) #The user that made the request
    queryString = models.CharField(max_length=512)
    title = models.CharField(max_length=128) #Optionally specified by the user
    description = models.CharField(max_length=1024) #Optionally specified by the user
    poolSize = models.IntegerField() #Optionally specified by the user
    startDate = models.DateTimeField(auto_now_add=True) #Timestamp
    resolved = models.BooleanField(default=False)
    result = models.CharField(max_length=2048) #an array containing documents IDs

    def __unicode__(self):
        return self.queryString

class Review(models.Model):
    reviewID = models.AutoField(primary_key=True)
    paperID = models.ForeignKey(Paper) #This refers tothe paper table
    researcher = models.ForeignKey(Researcher) #The user reviewing
    query = models.ForeignKey(Query) #The query we are resolving
    poolNumber = (
        (1,'API Level'),
        (2,'Abstract-Title level'),
        (3,'Document level'),
        (4,'Result level'),
    )
    relevant = models.BooleanField(default = None)
    notes = models.CharField(max_length=4096)