from main import models

#checks if account is verified
def checkVerified(key=None, user_id=None):
    if key:
        company = models.Company.objects.filter(key=key).first()
        return company.verified
    elif user_id:
        client = models.Client.objects.filter(user_id=user_id).first()
        return client.verified

#methods to perform validation in views
#gets the company_id related to the user_id
def getCompanyId(user_id=None):
    admin = models.Company.objects.filter(user_id=user_id).first()
    if admin:
        company_id = admin.company_id
    else:
        company_id = 0
    return company_id

#gets check_number from SaveViewed with user_id
def getCheckNumber(user_id=None):
    save = models.SaveViewed.objects.filter(user_id=user_id).first()
    if save:
        check_number = save.check_number
    else:
        check_number = 0
    return check_number

#checks if the Client object related to the 
#user_id from a request is an admin
def isAdmin(user_id=None):
    valid = False
    admin = models.Company.objects.filter(user_id=user_id).first()
    if admin and admin.verified:
        valid = True
    return valid

#filters searched checks
#cast with datetime.date
def filterChecks(user_id, search):
    company_id = getCompanyId(user_id=user_id)
    checks = models.Check.objects.filter(company_id=company_id).order_by('-completed_time')
    use_date = False
    status = search.status
    start_date = search.start_date
    end_date = search.end_date

    if status == 'safe':
        filtered = checks.filter(passed=True)
    elif status == 'unsafe':
        filtered = checks.filter(passed=False)
    elif status == 'all':
        filtered = checks

    if start_date and end_date:
        use_date = True
        date_filtered = filtered.filter(completed_time__range=[start_date, end_date])

    if use_date:
        return date_filtered
    else:
        return filtered



def validateCheck(company_id, check_number):
    valid = False
    entries = models.Entry.objects.filter(company_id=company_id, check_number=check_number)
    questions = models.Question.objects.filter(company_id=company_id)
    if entries.count() == questions.count():
        valid = True
    return valid