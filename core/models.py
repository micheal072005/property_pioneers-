# models.py
from django.db import models
from django.core.validators import RegexValidator
from django.utils.text import slugify
from django.urls import reverse
import random
import string

def generate_unique_slug(instance, base_slug=None):
    """
    Generate unique slug like: mike-ben-45631
    """
    if not base_slug:
        # Use name as base
        base = instance.name.lower()
        base = ''.join(c if c.isalnum() else '-' for c in base)
        base = base.strip('-')
        base_slug = base[:50]  # Limit length
    
    slug = f"{base_slug}-{''.join(random.choices(string.digits, k=5))}"
    
    # Ensure uniqueness
    ModelClass = instance.__class__
    while ModelClass.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{''.join(random.choices(string.digits, k=5))}"
    
    return slug


# CONTACT MODEL
class Contact(models.Model):
    name = models.CharField(max_length=150, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in format: '+2348012345678'. Up to 15 digits."
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        verbose_name="Phone Number"
    )
    
    subject = models.CharField(max_length=200, blank=True, null=True, verbose_name="Subject")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Submitted On")
    
    # Status
    is_read = models.BooleanField(default=False, verbose_name="Read by Admin")
    is_replied = models.BooleanField(default=False, verbose_name="Replied")
    
    # AUTO SLUG (e.g. john-doe-49281)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.email}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = generate_unique_slug(self, base_slug)
        super().save(*args, **kwargs)

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])

    def mark_as_replied(self):
        if not self.is_replied:
            self.is_replied = True
            self.save(update_fields=['is_replied'])


# REPLY MODEL
class MessageReply(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='replies')
    reply_text = models.TextField(verbose_name="Reply Message")
    replied_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    replied_at = models.DateTimeField(auto_now_add=True)
    sent_via_email = models.BooleanField(default=False, verbose_name="Email Sent")

    class Meta:
        ordering = ['-replied_at']

    def __str__(self):
        return f"Reply to {self.contact.name}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Only mark as replied when first reply is saved
        if is_new:
            self.contact.mark_as_replied()


# PROPERTY MODEL
class Property(models.Model):
    name = models.CharField(max_length=200, help_text="e.g. 5 Bedroom Duplex in GRA Phase 2")
    slug = models.SlugField(unique=True, blank=True, max_length=250)
    price = models.CharField(max_length=50, help_text="e.g. ₦350 Million or ₦2.5M per plot")
    location = models.CharField(max_length=200, help_text="e.g. GRA Phase 2, Port Harcourt")
    details = models.TextField(help_text="Short description of the property")
    image = models.ImageField(upload_to='properties/', help_text="Main photo")
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_added']
        verbose_name_plural = "Properties"

    def __str__(self):
        return f"{self.name} - {self.location}"

    def get_absolute_url(self):
        return reverse('property_detail', args=[self.slug])

    # Auto-generate slug from name
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Property.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)






