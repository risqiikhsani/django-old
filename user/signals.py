from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import *

import random
import string

#https://pynative.com/python-generate-random-string/
def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def set_user(sender, instance, created, **kwargs):
    if created:

        # add user to a group of "member"
        # group = Group.objects.get(name='member')
        # instance.groups.add(group)

        # create Account
        id_user = str(instance.id)
        randomwords = get_random_alphanumeric_string(20)
        id_url = "{}{}"
        id_url_fixed = id_url.format(id_user,randomwords)

        account = Account.objects.create(
            user = instance,
            name = "anonymous user",
            public_username = "anonymous_" + str(get_random_alphanumeric_string(10)) + str(instance.id),
            id_url = id_url_fixed
        )

        # create profile
        profile = Profile.objects.create(
            user = instance,
        )
        
        # create Relationship
        relationship = Relationship.objects.create(
            user=instance
        )

        # #create Follow

        # follow = Follow.objects.create(user=instance)

        # #create Follower

        # follower = Follower.objects.create(user=instance)

        print("signals for user creation is made , models associated with the user have been created !")
post_save.connect(set_user, sender=User, dispatch_uid="unique")


def if_accepted_then_relationship_will_be_added(sender, instance, created, **kwargs):
    if instance.status == "accepted":

        request_to = instance.user
        request_by = instance.from_user

        relationship = Relationship.objects.get(user=request_to)
        if relationship.users.all().filter(user=request_by.relationship).exists():
            pass
        else:
            relationship.users.add(Relationship.objects.get(user=request_by))

            #follows automatically
            # Follow.objects.create(user=request_by,to_user=request_to)
            # Follow.objects.create(user=request_to,to_user=request_by)

            request_to.follow.to_user.all().add(request_by)
            request_by.follow.to_user.all().add(request_to)


            #Follower automatically
            # Follower.objects.create(user=request_to,from_user=request_by)
            # Follower.objects.create(user=request_by,from_user=request_to)

            request_to.follower.from_user.all().add(request_by)
            request_by.follower.from_user.all().add(request_to)

            # request_by.follow_set.create(to_user=request_to)

        instance.delete()

post_save.connect(if_accepted_then_relationship_will_be_added, sender=Request, dispatch_uid="unique")
            
def if_cancelled_then_nothing(sender, instance, created, **kwargs):
    if instance.status == 'cancelled':
        instance.delete()

post_save.connect(if_cancelled_then_nothing, sender=Request, dispatch_uid='unique')



