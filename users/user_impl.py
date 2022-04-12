import email
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from users.models import Users

from service.utils import http_constances
from service.utils.http_response import duplicate_content_response,service_unavailable,not_accepted_response
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from twilio.rest import Client
    



def user_registation(request):
    try:
        if request.data:
            _first_name=request.data['firstName']
            _last_name =request.data['lastName']
            _email =request.data['email']
            _password =request.data['password']
            _phone=request.data['phoneNumber']

            _user=Users.objects.filter(email=_email)
            if _user:
                response= duplicate_content_response(http_constances.email_exists)
                return JsonResponse(response,status=409)
            u=Users(first_name=_first_name,last_name=_last_name, email=_email,
                    password=make_password(_password), phone_number=_phone, user_name=_email,
                    address_id=1)
            u.save()
            return JsonResponse({'message':f'User: {_first_name} Registerd Successfully'},status=201)
        else:
            response=not_accepted_response(http_constances.bad_request)
            return JsonResponse(response,status=406)
    except Exception as e:
        response(service_unavailable(e))
        return JsonResponse(response,status=500)

def user_login(request):
    if request.data:
        _email=request.data.get('email')
        _Phone= request.data.get('phoneNumber')
        if _email:
            _user=Users.objects.values('first_name').filter(email=_email)
            if _user:
                for row in _user:
                    name=row['first_name']
                email_status=send_otp_to_email(_email,name)
                if email_status==1:
                    return JsonResponse({'message':f'OTP has been sent to {_email}'},status=200)
                else:
                    return JsonResponse({'message':f'unable to send otp to {_email}'},status=500)
            else:
                return JsonResponse({'message':http_constances.email_not_found},status=404)
        if _Phone:
            _user=_user=Users.objects.values('first_name').filter(phone_number=_Phone)
            if _user:
                for row in _user:
                        name=row['first_name']
                msg_status=send_otp_to_phone(_Phone,name)
                if msg_status:
                    return JsonResponse({'message':f'OTP has been sent to {_Phone}'},status=200)
                else:
                    return JsonResponse({'message':f'unable to send otp to {_Phone}'},status=500)
            else:
                return JsonResponse({'message':http_constances.phonenumber_not_found},status=404)

    else:
        response=not_accepted_response(http_constances.bad_request)
        return JsonResponse(response,status=406)


def send_otp_to_email(user_email,name):
    try:
        template= render_to_string('email_template.html',{'name':name,'OTP':2232})

        email=EmailMessage(
            'Invites: OTP for login',
            template,
            settings.EMAIL_HOST_USER,
            [user_email]
            )
        email.fail_silently = False
        email.send()
        return 1
    except:
        return 0


def send_otp_to_phone(phone_number,name):
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWIIO_AUTH_TOKEN)
    # print(settings.FROM_NUMBER,phone_number)
    account_sid = 'ACc605989a40e9ff241f3505e888ef86ef'
    auth_token = '41de380aeeb090c2a50bb30873fd0e3e'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                     body=f"Hi {name}, your one time password is: 2232",
                     from_=settings.FROM_NUMBER,
                     to=phone_number
                 )
    return message.sid