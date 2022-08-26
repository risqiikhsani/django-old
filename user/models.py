from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
User = get_user_model()
from .middlewares import RequestMiddleware

# https://stackoverflow.com/questions/17328910/django-what-is-reverse-relationship
# https://stackoverflow.com/questions/17328910/django-what-is-reverse-relationship

# https://stackoverflow.com/questions/17328910/django-what-is-reverse-relationship
# https://stackoverflow.com/questions/17328910/django-what-is-reverse-relationship
# https://stackoverflow.com/questions/17328910/django-what-is-reverse-relationship

# https://stackoverflow.com/questions/17328910/django-what-is-reverse-relationship
# https://stackoverflow.com/questions/17328910/django-what-is-reverse-relationship


class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=100, blank=True, null=True)
	public_username = models.CharField(max_length=200, null=True, blank=True, unique=True)
	id_url = models.CharField(max_length=200, null=True, blank=True , unique=True)

	def __str__(self):
		return "username={}-name={}".format(self.user.username,self.name)

#new
class Hobby(models.Model):
	name = models.CharField(max_length=200, blank=True, null=True)
	description = models.TextField(blank=True, null=True)

	def __str__(self):
		return str(self.name)

import random
import string


#https://pynative.com/python-generate-random-string/
def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str

def namefile_profile_picture(instance, filename):
	ext = filename.split('.')[-1]
	get_random_1 = get_random_alphanumeric_string(10)
	get_random_2 = get_random_alphanumeric_string(10)
	name_of_file = "{}{}{}".format(get_random_1,str(instance.id),get_random_2)
	filename = "%s.%s" % (name_of_file, ext)
	return 'user_{}/{}/{}'.format(instance.user.username,'profile_picture',filename)


def namefile_poster_picture(instance, filename):
	ext = filename.split('.')[-1]
	get_random_1 = get_random_alphanumeric_string(10)
	get_random_2 = get_random_alphanumeric_string(10)
	name_of_file = "{}{}{}".format(get_random_1,str(instance.id),get_random_2)
	filename = "%s.%s" % (name_of_file, ext)
	return 'user_{}/{}/{}'.format(instance.user.username,'poster_picture',filename)
	
def namefile_photo(instance, filename):
	ext = filename.split('.')[-1]
	get_random_1 = get_random_alphanumeric_string(10)
	get_random_2 = get_random_alphanumeric_string(10)
	name_of_file = "{}{}{}".format(get_random_1,str(instance.id),get_random_2)
	filename = "%s.%s" % (name_of_file, ext)
	return 'user_{}/{}/{}'.format(instance.user.username,'photo',filename)
	

def namefile_post_photo(instance, filename):
	ext = filename.split('.')[-1]
	get_random_1 = get_random_alphanumeric_string(10)
	get_random_2 = get_random_alphanumeric_string(10)
	name_of_file = "{}{}{}".format(get_random_1,str(instance.id),get_random_2)
	filename = "%s.%s" % (name_of_file, ext)
	return 'user_{}/post_{}/{}'.format(instance.poster.username,instance.id,filename)
	
def namefile(instance, filename):
	def fixednamefile(person,name):
		ext = filename.split('.')[-1]
		get_random_1 = get_random_alphanumeric_string(10)
		get_random_2 = get_random_alphanumeric_string(10)
		name_of_file = "{}{}{}".format(get_random_1,str(instance.id),get_random_2)
		filename = "%s.%s" % (name_of_file, ext)
		return 'user_{}/{}/{}'.format(person,name,filename)
	return fixednamefile

# obj1 = namefile()
# obj1(instance.user.username , "post")

from .helpers import calculateAge
import datetime
class Profile(models.Model):
	GENDER_CHOICES = [
		('male','male'),
		('female','female'),
	]

	user = models.OneToOneField(User,on_delete=models.CASCADE, null=True)
	about = models.TextField(blank=True, null=True)
	gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
	live_in = models.CharField(max_length=200, blank=True, null=True)
	born_time = models.DateTimeField(blank=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	# new
	hobby = models.ManyToManyField(Hobby, null=True, blank=True)
	profile_picture = models.ImageField(null=True, blank=True, default="profile_default.jpg")
	poster_picture = models.ImageField(null=True, blank=True, default="poster_default.jpg")

	# hoby
	# #picture profile
	# profile_picture = models.OneToOneField(Photo, blank=True, null=True)
	# #picture sample
	# sample_picture = models.OneToOneField(Photo, blank=True, null=True)

	def __str__(self):
		return "{}".format(self.user.username)

	@property
	def get_age(self):
		if self.born_time is None:
			return ""
		else:
			# return (datetime.datetime.today() - self.born_time)
			a = str(self.born_time)
			x = a.split()

			#['2000-10-27', '07:34:53+00:00']
			z = x[0].split("-")
			#['2000', '10', '27']

			result = calculateAge(datetime.date(int(z[0]), int(z[1]), int(z[2])))
			return result




class Relationship(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	users = models.ManyToManyField('self', related_name="connected_users", blank=True, null=True)

	def __str__(self):
		return "{}".format(self.user.username)

	@property
	def connected_users_amount(self):
		return self.connected_users.count()

class Request(models.Model):
	STATUS_CHOICES = [
		('pending','pending'),
		('accepted','accepted'),
		('cancelled','cancelled'),
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	from_user = models.ForeignKey(User, related_name="requested_by",on_delete=models.CASCADE, null=True)
	status = models.CharField(max_length=100,choices=STATUS_CHOICES, blank=True, null=True)

class Follow(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	to_user = models.ManyToManyField(User,related_name="follows", null=True)

	@property
	def follow_amount(self):
		return self.count()

class Follower(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
	from_user = models.ManyToManyField(User, related_name="followers", null=True)

	@property
	def follower_amount(self):
		return self.count()



#new
class Photo(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	image = models.ImageField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	likes = models.ManyToManyField(User, related_name="photolikes", null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

	def __str__(self):
		return str(self.user.username)

	@property
	def does_authenticated_user_like(self):
		request = RequestMiddleware(get_response=None)
		request = request.thread_local.current_request
		user = request.user
		if user in self.likes.all():
			return True
		else:
			return False

	@property
	def like_amount(self):
		return self.likes.count()

	@property
	def comment_amount(self):
		return self.photocomment_set.all().count()

class PhotoComment(models.Model):
	photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)
	commentator = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField(blank=True, null=True)
	likes = models.ManyToManyField(User, related_name="photocommentlikes", null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	

	def __str__(self):
		return "photo={} - commented by={} - comment={}".format(self.photo.id,self.commentator.username,self.text)

	@property
	def does_authenticated_user_like(self):
		request = RequestMiddleware(get_response=None)
		request = request.thread_local.current_request
		user = request.user
		if user in self.likes.all():
			return True
		else:
			return False

	@property
	def like_amount(self):
		return self.likes.count()

def convertDatetimeToString(o):
	DATE_FORMAT = "%Y-%m-%d" 
	TIME_FORMAT = "%H:%M:%S"

	if isinstance(o, datetime.datetime):
	    return o.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT))
	else:
		return null


class Post(models.Model):
	poster = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=200, null=True, blank=True)
	text = models.TextField(blank=True, null=True)
	likes = models.ManyToManyField(User, related_name="postlikes", null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True,null=True)

	def __str__(self):
		return "by:{}--title:{}".format(self.poster.username,self.title)

	@property
	def does_authenticated_user_like(self):
		request = RequestMiddleware(get_response=None)
		request = request.thread_local.current_request
		user = request.user
		if user in self.likes.all():
			return True
		else:
			return False

	@property
	def like_amount(self):
		return self.likes.count()

	@property
	def comment_amount(self):
		return self.comment_set.all().count()

	@property
	def created_at_string(self):
		if self.created_at is None:
			return null
		else:
			return convertDatetimeToString(self.created_at) 

	class Meta:
		ordering = ['-created_at']

#new
class PostPhoto(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
	image = models.ImageField(blank=True,null=True)
	description = models.TextField(blank=True, null=True)

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	commentator = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.TextField(blank=True, null=True)
	likes = models.ManyToManyField(User, related_name="commentlikes", null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, null=True)

	

	def __str__(self):
		return "post={} - commented by={} - comment={}".format(self.post.id,self.commentator.username,self.text)

	@property
	def does_authenticated_user_like(self):
		request = RequestMiddleware(get_response=None)
		request = request.thread_local.current_request
		user = request.user
		if user in self.likes.all():
			return True
		else:
			return False

	@property
	def like_amount(self):
		return self.likes.count()
#new
# class CommentPhoto(models.Model):
# 	comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
# 	image = models.ImageField(blank=True, null=True)
