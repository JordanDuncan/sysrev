from __future__ import unicode_literals

from django.db import models

class Researcher(models.Model):
    username = models.CharField(max_length=128, unique=True, primary_key=True) #Unique token used to login
    password = models.CharField(max_length=128) #The length of an MD5 hash digest
    email = models.CharField(max_length=128, unique=True) #To give notifications and check identity
    forename = models.CharField(max_length=128)
    surname = models.CharField(max_length=128)
    institution = (
        (UOG, 'University of Glasgow'),
        (GCU, 'Glasgow Caledonian University'),
        (GSU, 'Glasgow Strathclyde University'),
        (EDI, 'Edinburgh University'),
        (UWS, 'University of Western Scotland'),
        (STU, 'St.Andrews University'),
        (OXF, 'Oxford University'),
        (CAM, 'Cambridge University'),
        (OTH, 'Other'),
    )

    def __unicode__(self):
        return self.username

class Query(models.Model):
    queryID = models.AutoField(primary_key=True)
    researcher = models.ForeignKey(Researcher) #The user that made the request
    queryString = models.CharField(max_length=512)
    title = models.CharField(max_length=128) #Optionally specified by the user
    description = models.CharField(max_length=1024) #Optionally specified by the user
    poolSize = models.IntegerField() #Optionally specified by the user
    startDate = models.DateField.auto_now_add() #Timestamp
    resolved = models.BooleanField(default=False)
    result = models.CharField() #an array containing documents IDs

    def __unicode__(self):
        return self.queryString

class Paper(models.Model):
    paperID = models.AutoField(primary_key=True) #Could change this to the API's document id, I do not know the format and/or constraint of that
    title = models.CharField()
    authors = models.CharField()
    abstract = models.CharField()
    publishDate = models.DateField()
    paperUrl = models.URLField()
        #Did not implement the the relevance fields as they are referred in the review
        #In fact the same document could be relevant or not relevant for different reviews
    
    def __unicode__(self):
        return self.title

class Review(models.Model):
    reviewID = models.AutoField(primary_key=True)
    researcher = models.ForeignKey(Researcher) #The user reviewing
    query = models.ForeignKey(Query) #The query we are resolving
    paperID = models.ForeignKey(Paper) #This refers tothe paper table
    poolNumber = (
        (1,'API Level'),
        (2,'Abstract-Title level'),
        (3,'Document level'),
        (4,'Result level'),
    )
    relevant = models.BooleanField()
    notes = models.CharField()