from django.db import models
from django.utils import timezone


class VerificationCode(models.Model):
    mobile_phone = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    valid = models.BooleanField(default=True)
    created_datetime = models.DateTimeField(auto_now_add=True, editable=False)

    def is_valid(self, expiry_seconds=600):
        return self.valid and (timezone.now() - self.created_datetime).total_seconds() < expiry_seconds
    
    def invalidate(self):
        if self.valid:
            self.valid = False
            self.save()

    @classmethod
    def get_latest(cls, mobile_phone, code=None):
        try:
            if code is not None:
                return cls.objects.filter(mobile_phone=mobile_phone, code=code).order_by('-created_datetime')[:1].get()
            else:
                return cls.objects.filter(mobile_phone=mobile_phone).order_by('-created_datetime')[:1].get()
        except cls.DoesNotExist:
            return None
