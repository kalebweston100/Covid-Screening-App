from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

#company being registered
#creates admin account tied to company
class Company(models.Model):
    #got rid of max_accounts so a user can only create one account with an email

    #length of randomly generated company key
    length = 5

    #unique primary key for company
    company_id = models.AutoField(primary_key=True)
    #user_id of user who created company
    #unique for extra security (prevents false user_id request accessing data)
    user_id = models.IntegerField(blank=True, unique=True)
    #name of company
    name = models.TextField()
    #company key used to register users/employees
    key = models.TextField(blank=True)
    #email used to register company and send verification link
    email = models.TextField(blank=True)
    #admin user can deactivate company account
    #which prevents users from registering with its key
    active = models.BooleanField(default=True)
    #whether the user clicked on the email link sent to them
    #and entered their account information (username and password)
    verified = models.BooleanField(default=False)
    
    #if the reset_key keyword is passed then
    #the save method resets the key
    def save(self, *args, **kwargs):
        reset_key = kwargs.pop('reset_key', None)
        initial = kwargs.pop('initial', None)

        if reset_key:
            self.key = get_random_string(length=self.length)
        elif initial:
            self.email = make_password(self.email, salt='salt')
        super().save(*args, **kwargs)


#user who registers for a company
#and completes surveys
class Client(models.Model):
    #max number of accounts that can be created with the client's email
    max_accounts = 3

    #unique primary key for client
    client_id = models.AutoField(primary_key=True)
    #user_id of client who registers
    user_id = models.IntegerField()
    #company_id of company whose key the client registers with
    company_id = models.IntegerField()
    #number of the client in the company
    #so that raw ids are never sent or received with the frontend
    client_number = models.IntegerField(blank=True)
    #first and last name provided by the client when registered
    #displayed to the admin only on the users page 
    #so they can delete unwanted users
    first_name = models.TextField()
    last_name = models.TextField()
    #email provided by the client during registering
    #hashed and only used to control action on that email
    email = models.TextField(blank=True)
    #whether or not the client has clicked on the provided verification link
    #and inputted their username and password
    verified = models.BooleanField(default=False)
    #whether or not the admin has deleted the user from their company
    #kept so that the same email cannot register for that company
    #and other email validation using clients
    active = models.BooleanField(default=True)

    #modifies save behavior for the client model
    def save(self, *args, **kwargs):
        create_client = kwargs.pop('create_client', None)
        if create_client:
            #creats a ClientString row with the client's user_id 
            #used for cache behavior in the user app during Checks
            #also used as a salt for email hashing
            user_string = ClientString.objects.create(user_id=self.user_id)
            self.email = make_password(self.email, salt='salt')
            #creates client number that is used instead of direct client_id
            last_user = Client.objects.filter(company_id=self.company_id).last()
            if last_user:
                self.client_number = last_user.client_number + 1
            else:
                self.client_number = 1
        super().save(*args, **kwargs)


#generates a string when a client is created with their user_id
#to abstract for security
class ClientString(models.Model):
    #length of the generated string
    length = 12

    #user_id of the client that the row was generated with
    user_id = models.IntegerField(primary_key=True)
    #random string generated and used
    user_string = models.TextField(blank=True)

    #modifies save behavior to generate random user_string
    def save(self, *args, **kwargs):
        self.user_string = get_random_string(length=self.length)
        super().save(*args, **kwargs)


#question that is created by admin 
#and answered by user on the survey
class Question(models.Model):
    #unique primary key
    question_id = models.AutoField(primary_key=True)
    #company_id of the company that the question is created by
    company_id = models.IntegerField()
    #the number of the question in the company it belongs to
    question_number = models.IntegerField()
    #the text of the question
    content = models.TextField()
    #if the answer is yes or no
    #if it is then content is either 'yes' or 'no'
    bool_answer = models.BooleanField(default=True)
    #change the Check passed to False if the answer is 'yes'
    notify = models.BooleanField(default=True)
    #if a personal question the bool_answer must be True
    #they are calculated into the pass of a Check
    #but the question content is not saved in the Entry
    personal = models.BooleanField(default=False)
    ############################################################use active or just delete row??
    #active = models.BooleanField(default=True)

    #modifies save behavior to generate question_number
    def save(self, *args, **kwargs):
        last_question = Question.objects.filter(company_id=self.company_id).last()
        if last_question:
            self.question_number = last_question.question_number + 1
        else:
            self.question_number = 1
        super().save(*args, **kwargs)


#standard screening questions
class DefaultQuestions(models.Model):
    row_id = models.AutoField(primary_key=True)
    content = models.TextField()


#the results of a survey taken by the user
#many Entries correspond to one Check with check_number and company_id
class Check(models.Model):
    #unique primary_key for Check rows
    check_id = models.AutoField(primary_key=True)
    #company_id of the company the user who completes the check belongs to 
    company_id = models.IntegerField()
    #number of the check in the company that the user who completes the check belongs to 
    check_number = models.IntegerField()
    #completed is update to True once all the company's
    #questions are answered
    completed = models.BooleanField(default=False)
    #time that the check is completed
    #sent from client javascript to get local timezone
    completed_time = models.DateField(blank=True, null=True)
    #if there are a set of yes or no questions
    #they can be calculated to either pass or fail
    passed = models.BooleanField(default=False)

    #use to verify that number of Entries matches number of Questions
    #valid = models.BooleanField(default=False)

    #modifies save behavior of Checks
    def save(self, *args, **kwargs):
        #if keyword set_number then create check_number
        #save is used after initial save so it can't change 
        #its check_number after every save
        set_number = kwargs.pop('set_number', None)
        if set_number:
            last_check = Check.objects.filter(company_id=self.company_id).last()
            if last_check:
                self.check_number = last_check.check_number + 1
            else:
                self.check_number = 1
        super().save(*args, **kwargs)


#answer to question on user survey
#has a many to one relationship with Check
#using check_number and company_id
class Entry(models.Model):
    #unique primary key
    entry_id = models.AutoField(primary_key=True)
    #company_id of the user taking the survey
    company_id = models.IntegerField()
    #number of the user's current check in their company
    check_number = models.IntegerField()
    #number of the question being answered in the user's company
    #used on admin page to display all the answers to questions
    #if the question is personal then it is not saved
    question_number = models.IntegerField(blank=True, null=True)
    #saved from question being answered
    #if notify is True then the Check that check_number corresponds to 
    #will set pass to False if answered 'yes'
    notify = models.BooleanField(default=False)
    #content of the answer
    #if bool_answer is True on the question then
    #it will be either 'yes' or 'no'
    content = models.TextField()

    #modifies save behavior to not save question_number
    #if it is a personal question
    def save(self, *args, **kwargs):
        personal = kwargs.pop('personal')
        if personal:
            self.question_number = None
        super().save(*args, **kwargs)

    
#stores the urls for the links sent
#to users to verify their account
#used for both admin and user verification
class VerifyAccount(models.Model):
    #length of the random url_string
    length = 40

    #unique primary_key
    verify_id = models.AutoField(primary_key=True)
    #user_id of the user who the verification link belongs to 
    user_id = models.IntegerField()
    #string of the random url
    url_string = models.TextField(blank=True)
    #whether the link is active
    #changes to False after the related user activates their account
    active = models.BooleanField(default=True)

    #modifies save behavior to generate the random url_string
    def save(self, *args, **kwargs):
        self.url_string = get_random_string(length=self.length)
        super().save(*args, **kwargs)