from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import re
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from django.shortcuts import get_object_or_404
from datetime import timedelta
import random
from django.contrib import messages as django_messages
from .models import *

# Create your views here.


# Home page view
def home(request):
    latest_properties = Property.objects.filter(is_active=True).order_by('-date_added')[:2]
    context = { 'latest_properties': latest_properties }

    return render(request, 'core/home.html', context)


# About page view
def about(request):
    return render(request, 'core/about.html')



def services(request):
    return render(request, 'core/services.html')



# Simple but powerful email regex (blocks 99.9% of fake emails)
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# Contact page view
def contact(request):
    # === AUTO-CHECK & CLEAN EXPIRED SESSION DATA ===
    expiry_timestamp = request.session.get('otp_expiry')
    if expiry_timestamp:
        if int(datetime.now().timestamp()) > expiry_timestamp:
            keys_to_clear = [
                'contact_name', 'contact_email', 'otp_code',
                'otp_expiry', 'otp_sent', 'otp_verified'
            ]
            for key in keys_to_clear:
                request.session.pop(key, None)
            request.session.modified = True

    context = {
        'name': request.session.get('contact_name', ''),
        'email': request.session.get('contact_email', ''),
    }

    if request.method == "POST":
        action = request.POST.get("action")

        # === SEND OTP ===
        if action == "send_otp":
            name = request.POST.get("name", "").strip()
            email = request.POST.get("email", "").strip().lower()

            if not name or not email:
                messages.error(request, "Please fill in your name and email.")
            else:
                otp = random.randint(10000, 99999)
                expiry = datetime.now() + timedelta(minutes=5)

                request.session['contact_name'] = name
                request.session['contact_email'] = email
                request.session['otp_code'] = otp
                request.session['otp_expiry'] = int(expiry.timestamp())
                request.session['otp_sent'] = True
                request.session['otp_verified'] = False

                try:
                    html_message = render_to_string('emails/otp_verification.html', {
                        'name': name.split()[0],
                        'otp': otp,
                        'year': datetime.now().year,
                    })
                    plain_message = strip_tags(html_message)

                    send_mail(
                        subject="Your Verification Code – Property Pioneers",
                        message=plain_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        html_message=html_message,
                        fail_silently=False,
                    )

                    messages.success(request, f"Verification code sent to {email}")
                except Exception as e:
                    messages.error(request, "Failed to send code. Please try again.")
                    print(f"OTP Email failed: {e}")

            return render(request, 'core/contact.html', context)

        # === VERIFY OTP ===
        elif action == "verify_otp":
            if int(datetime.now().timestamp()) > request.session.get('otp_expiry', 0):
                messages.error(request, "Session expired. Please start again.")
                for key in ['contact_name', 'contact_email', 'otp_code', 'otp_expiry', 'otp_sent', 'otp_verified']:
                    request.session.pop(key, None)
                return render(request, 'core/contact.html', {})

            code = "".join(request.POST.get(f"digit{i}", "") for i in range(1, 6))
            saved_code = request.session.get('otp_code')

            if str(code) == str(saved_code):
                request.session['otp_verified'] = True
                request.session['otp_sent'] = False
                messages.success(request, "Email verified! Now complete your message.")
            else:
                messages.error(request, "Invalid code. Please try again.")

            return render(request, 'core/contact.html', context)

        # === CANCEL OTP ===
        elif action == "cancel_otp":
            for key in ['contact_name', 'contact_email', 'otp_code', 'otp_expiry', 'otp_sent', 'otp_verified']:
                request.session.pop(key, None)
            return render(request, 'core/contact.html', {})

        # === SEND FINAL MESSAGE ===
        elif action == "send_message" and request.session.get('otp_verified'):

            if int(datetime.now().timestamp()) > request.session.get('otp_expiry', 0):
                messages.error(request, "Session expired. Please start over.")
                for key in ['contact_name', 'contact_email', 'otp_code', 'otp_expiry', 'otp_sent', 'otp_verified']:
                    request.session.pop(key, None)
                return render(request, 'core/contact.html', {})

            # Process final message form
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip().lower()
            phone = request.POST.get('phone', '').strip()
            subject = request.POST.get('subject', '').strip()
            message = request.POST.get('message', '').strip()

            errors = []

            if not name or len(name) < 2:
                errors.append("Please enter a valid name.")

            if not email:
                errors.append("Email address is required.")
            elif not is_valid_email(email):
                errors.append("Please enter a valid email address.")

            if not message or len(message) < 10:
                errors.append("Message is too short. Please tell us more.")

            if errors:
                for error in errors:
                    messages.error(request, error)
                return render(request, 'core/contact.html', context)

            try:
                contact_entry = Contact.objects.create(
                    name=name,
                    email=email,
                    phone=phone or None,
                    subject=subject or None,
                    message=message
                )

                ctx = {
                    'name': name,
                    'email': email,
                    'phone': phone or 'Not provided',
                    'subject': subject or 'General Inquiry',
                    'message': message,
                    'submitted_at': contact_entry.created_at
                }

                html_message = render_to_string('emails/new_contact.html', ctx)
                plain_message = strip_tags(html_message)

                send_mail(
                    subject=f"NEW LEAD: {name} - {subject or 'Contact Form'}",
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['contact@propertypioneersltd.com'],
                    html_message=html_message,
                    fail_silently=False,
                )

                messages.success(request, "Thank you! Your message has been sent successfully.")
            except Exception as e:
                messages.error(request, "Message sent, but admin notification failed.")
                print(f"Admin email failed: {e}")

            # Clear session after success
            for key in ['contact_name', 'contact_email', 'otp_code', 'otp_expiry', 'otp_sent', 'otp_verified']:
                request.session.pop(key, None)

            return redirect('contact')

    # GET request
    return render(request, 'core/contact.html', context)


# Custom login view for staff members
def admin_login(request):
    if request.user.is_authenticated:
        return redirect('messages_dashboard')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # Only staff/admin allowed
            login(request, user)
            return redirect('messages_dashboard')
        else:
            messages.error(request, "Invalid credentials or not authorized.")
    
    return render(request, 'core/login.html')


# Custom logout view
@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect('home')



# Messages dashboard view for staff members
@login_required(login_url='admin_login')  # Redirects to  admin login
def messages_dashboard(request):
    admin_messages = Contact.objects.all().order_by('-created_at')
    
    context = {
        'admin_messages': admin_messages,
        'total': admin_messages.count(),
        'unread': admin_messages.filter(is_read=False).count(),
        'today': admin_messages.filter(created_at__date=timezone.now().date()).count(),
    }
    return render(request, 'core/messages.html', context)



@login_required(login_url='admin_login')
def reply_message(request, slug):
    if not request.user.is_staff:
        return redirect('admin_login')
    
    contact = get_object_or_404(Contact, slug=slug)
    
    if request.method == "POST":
        reply_text = request.POST.get('reply_text', '').strip()
        
        if not reply_text:
            django_messages.error(request, "Reply cannot be empty.")
        else:
            # Save reply
            reply = MessageReply.objects.create(
                contact=contact,
                reply_text=reply_text,
                replied_by=request.user
            )

            contact.is_replied = True
            contact.is_read = True
            contact.save(update_fields=['is_replied'])
            contact.save(update_fields=['is_read'])


            # === SEND HTML EMAIL ===
            subject = f"Re: {contact.subject or 'Your Inquiry'} - Property Pioneers"
            
            html_content = render_to_string('emails/reply_email.html', {
                'name': contact.name.split()[0],
                'reply_text': reply_text,
                'year': datetime.now().year,
            })
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(
                subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [contact.email],
                reply_to=[settings.DEFAULT_FROM_EMAIL],
            )
            email.attach_alternative(html_content, "text/html")
            
            try:
                email.send()
                reply.sent_via_email = True
                reply.save(update_fields=['sent_via_email'])
                django_messages.success(request, f"Reply sent to {contact.name}!")
            except Exception as e:
                django_messages.warning(request, f"Reply saved but email failed to send.")

            return redirect('messages_dashboard')
    
    context = {'contact': contact}
    return render(request, 'core/reply.html', context)


# Anyone can view
def property_list(request):
    properties = Property.objects.filter(is_active=True)
    return render(request, 'core/property_list.html', {'properties': properties})


# Anyone can view
def property_detail(request, slug):
    property = get_object_or_404(Property, slug=slug, is_active=True)
    return render(request, 'core/property_detail.html', {'property': property})


# Only staff can add property
@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_staff)
def add_property(request, slug=None):
    property = None
    if slug:
        property = get_object_or_404(Property, slug=slug)

    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        location = request.POST.get('location')
        details = request.POST.get('details')
        image = request.FILES.get('image')

        if not all([name, price, location, details]):
            messages.error(request, "All fields are required!")
        else:
            if property:
                # EDIT EXISTING
                property.name = name
                property.price = price
                property.location = location
                property.details = details
                if image:
                    property.image = image  # Update image if new one uploaded
                property.save()
                messages.success(request, f"Property '{name}' updated successfully!")
            else:
                # ADD NEW
                Property.objects.create(
                    name=name, price=price, location=location,
                    details=details, image=image
                )
                messages.success(request, f"Property '{name}' added successfully!")
            return redirect('property_list')

    return render(request, 'core/add_property.html', {'property': property})


# DELETE PROPERTY
@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_staff)
def delete_property(request, slug):
    property = get_object_or_404(Property, slug=slug)
    if request.method == "POST":
        property_name = property.name
        property.delete()
        messages.success(request, f"Property '{property_name}' deleted successfully!")
        return redirect('property_list')
    return redirect('property_list')  # Safety







