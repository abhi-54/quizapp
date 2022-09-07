from django.db import models
from .utils import stdchoice, generate_ref_code
from django.contrib.auth.models import User

class profile1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    std = models.CharField(max_length=20, choices=stdchoice, default='')
    ref_code = models.CharField(max_length=12, blank=True, unique=True)
    reward_points = models.IntegerField(default=0)
    referred_by = models.CharField(max_length=120, blank=True)

    def save(self, *args, **kwargs):
       if self.ref_code == '':
           ref_code = generate_ref_code()
           self.ref_code = ref_code
       super().save(*args, **kwargs) # Call the real save() method

    def get_username(self):
        return str(self.user)

    def get_std(self):
        return str(self.std)

    def get_ref_code(self):
        return str(self.ref_code)

    def get_reward_points(self):
        return str(self.reward_points)

    def __str__(self):
        return f"{self.user}-{self.std}"