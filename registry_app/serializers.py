'''
Created on Jul 14, 2014

@author: tiendung
'''
from django.forms import widgets
from rest_framework import serializers
# from registry_app.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from registry_app.models import User_ssh

class UserSshRegisSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_ssh
        fields = ('pool','nat_type','ipaddr','port_ex')