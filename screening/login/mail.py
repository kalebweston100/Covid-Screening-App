from django.core.mail import send_mail

#checks that email exists
def checkEmail(email):
    subject = 'Coronavirus Screening Account Created'

    message = (
        'This email was used to create an account '
        'on Coronavirus screening website'
    )

    from_email = 'noreply@test.com'
    recipient_list = [email]
    success = send_mail(subject, message, from_email, recipient_list)
    return success

#confirms that email created company
#########################explain how to use company key
def verifyCompanyEmail(email, verify, company):
    subject = 'Validate Coronavirus Screening Account'

    url_string = verify.url_string

    message = (
        'An account for ' + company.name + ' was created with this email \n'
        'Your company key is: ' + company.key + '\n'
        'If you created an account on Coronavirus screening website '
        'then in order to validate it click on '
        'http://localhost:8000/verify/company/' + url_string
    )

    from_email = 'noreply@test.com'
    recipient_list = [email]
    success = send_mail(subject, message, from_email, recipient_list)
    return success


#validates that email created account
def verifyAccountEmail(email, verify):
    subject = 'Validate Coronavirus Screening Account'

    url_string = verify.url_string

    message = (
        'If you created an account on Coronavirus screening website '
        'then in order to validate it click on '
        'http://localhost:8000/verify/account/' + url_string
    )

    from_email = 'noreply@test.com'
    recipient_list = [email]
    success = send_mail(subject, message, from_email, recipient_list)
    return success