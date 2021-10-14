from django.core.mail import send_mail


def send (user_email, url):
    send_mail(
        subject='qsar-me result',
        message=f'''Thank u for using qsar-me, a pharmacophore building tool 
        your model is availible at {url}''',
        from_email='h4rvydent@yandex.by',
        recipient_list=[user_email],
        fail_silently=False,  
    )