from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *



def is_wrong_input(value):
	allowed_words = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','1','2','3','4','5','6','7','8','9','0','_']
	wrong_input = False
	for i in value:
		if i not in allowed_words:
			wrong_input = True

	return wrong_input

def is_wrong_input_name(value):
	allowed_words = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','1','2','3','4','5','6','7','8','9','0',' ']
	wrong_input = False
	for i in value:
		if i not in allowed_words:
			wrong_input = True

	return wrong_input


class Login_Serializer(serializers.Serializer):
	username = serializers.CharField(max_length=300, required=True)
	password = serializers.CharField(required=True, write_only=True)


class Register_Serializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=True, style={
		"input_type":   "password"})
	password2 = serializers.CharField(
		style={"input_type": "password"}, write_only=True, label="Confirm password")

	class Meta:
		model = User
		fields = [
			"username",
			"email",
			"password",
			"password2",
		]
		extra_kwargs = {"password": {"write_only": True}}

	def create(self, validated_data):
		username = validated_data["username"]
		email = validated_data["email"]
		password = validated_data["password"]
		password2 = validated_data["password2"]
		if (email and User.objects.filter(email=email).exclude(username=username).exists()):
			raise serializers.ValidationError(
				{"email": "Email addresses must be unique."})
		if password != password2:
			raise serializers.ValidationError(
				{"password": "The two passwords differ."})
		user = User(username=username, email=email)
		user.set_password(password)
		user.save()
		return user


class Group_User_Serializer(serializers.Serializer):
	name = serializers.CharField(max_length=300, read_only=True)


class MainUser_Serializer(serializers.ModelSerializer):
	# recent_password = serializers.CharField(write_only=True,required=False)
	# new_password1 = serializers.CharField(write_only=True,required=False)
	# new_password2 = serializers.CharField(write_only=True,required=False)
	
	class Meta:
		model = User
		fields = ['username','email','date_joined','groups']
		read_only_fields = ['username','date_joined','groups']

	def validate_email(self, value):
		if User.objects.all().get(email=value).exists():
			raise serializers.ValidationError("cant be set, email already exists !")
		return value

	# def validate_recent_password(self, value):
	# 	if value != self.context['request'].user.password:
	# 		return serializers.ValidationError("password is incorrect")
	# 	return value

	# def update(self, instance, validated_data):
	# 	recent_password = validated_data["recent_password"]
	# 	new_password1 = validated_data["new_password1"]
	# 	new_password2 = validated_data["new_password2"]
	# 	if new_password1 != new_password2:
	# 		raise serializers.ValidationError({"password": "The two passwords differ."})

	# 	instance.set_password(password1)
	# 	instance.email = validated_data.get('email', instance.email)
	# 	instance.save()
	# 	return instance


class ChangePassword_Serializer(serializers.ModelSerializer):


	class Meta:
		model = User
		fields = ['recent_password','new_password1','new_password2']

	def validate_recent_password(self, value):
		if value != self.context['request'].user.password:
			return serializers.ValidationError("password is incorrect")
		return value

	def update(self, instance, validated_data):
		recent_password = validated_data["recent_password"]
		new_password1 = validated_data["new_password1"]
		new_password2 = validated_data["new_password2"]
		if new_password1 != new_password2:
			raise serializers.ValidationError({"password": "The two passwords differ."})

		instance.set_password(password1)
		instance.save()
		return instance
		



class MainAccount_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ['name','public_username','id_url']
		read_only_fields = ['id_url']

	def validate_public_username(self, value):
		if Account.objects.all().get(public_username = value).exists():
			raise serializers.ValidationError("can't be set . public_username already exists !")
		
		wrong_input = is_wrong_input(value)
		if wrong_input == True:
			raise serializers.ValidationError("can't be set, containts wrong input ! letters,numbers,and underscore are only allowed")

		return value

	def validate_name(self, value):

		wrong_input = is_wrong_input_name(value)
		if wrong_input == True:
			raise serializers.ValidationError("can't be set, containts wrong input ! letters,numbers,and spaces are only allowed")

		return value






class Hobby_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Hobby
		fields = '__all__'



class MainProfile_Serializer(serializers.ModelSerializer):
	# hobby = Hobby_Serializer(many=True)
	# hobby = serializers.ListSerializer(many=True)
	hobby_update = serializers.ListField(write_only=True, required=False)
	hobby = Hobby_Serializer(many=True,read_only=True)
	class Meta:
		model = Profile
		fields = ['about','gender','live_in','born_time','updated_at','hobby','hobby_update','profile_picture','poster_picture']
		read_only_fields =  ['updated_at','hobby']

	def update(self, instance, validated_data):
		if "hobby_update" in validated_data:
			hobby_data = validated_data['hobby_update']
			del validated_data['hobby_update']
			instance.hobby.all().delete()
			print(hobby_data)
			# for i in hobby_data:
			# 	hobby_chosen = Hobby.objects.get(id=i)
			# 	profile = instance.hobby.add(hobby_chosen)
			for i in hobby_data:
				print(i)
				try:
				    hobby = Hobby.objects.get(pk=i)
				except Hobby.DoesNotExist:
				    hobby = None
				instance.hobby.add(hobby)
			
			
			

		instance.about = validated_data.get('about', instance.about)
		instance.gender = validated_data.get('gender', instance.gender)
		instance.live_in = validated_data.get('live_in', instance.live_in)
		instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
		instance.poster_picture = validated_data.get('poster_picture', instance.poster_picture)
		instance.save()

		

		return instance





class MainRequest_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Request
		fields = '__all__'
		read_only_fields = ['status']


class MainFollow_Serializer(serializers.ModelSerializer):
	class Meta:
		model = Follow
		fields = '__all__'




class Account_Serializer(serializers.ModelSerializer):
	profile_picture = serializers.ImageField(source="user.profile.profile_picture")
	class Meta:
		model = Account
		fields = ['name', 'public_username', 'id_url','profile_picture']


#hanya untuk MainRelationship_Serializer
class User_Serializer(serializers.ModelSerializer):
	account = Account_Serializer()

	class Meta:
		model = User
		fields = ['id', 'account', 'is_active']

class MainRelationship_Serializer(serializers.ModelSerializer):
	user = User_Serializer()
	class Meta:
		model = Relationship
		fields = ['user']

class UserList_Serializer(serializers.ModelSerializer):
	account = Account_Serializer()
	profile_picture = serializers.ImageField(source="profile.profile_picture")

	class Meta:
		model = User
		fields = ['id', 'account', 'is_active','profile_picture']

	# def get_profile_picture(self, obj):
	# 	return obj.profile.profile_picture

class Profile_Serializer(serializers.ModelSerializer):
	born_time = serializers.CharField(read_only=True)
	age = serializers.CharField(max_length=None, min_length=None, allow_blank=True,source="get_age",read_only=True)
	class Meta:
		model = Profile
		
		exclude = ['id','user']

class UserDetail_Serializer(serializers.ModelSerializer):
		account = Account_Serializer(read_only=True)
		profile = Profile_Serializer(read_only=True)
		# post_set = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='post-detail', lookup_url_kwarg='pk')
		posts = serializers.HyperlinkedIdentityField(view_name="post-list", read_only=True,lookup_url_kwarg='user_id')

		i_requested = serializers.SerializerMethodField()
		i_relationshiped = serializers.SerializerMethodField()
		i_followed = serializers.SerializerMethodField()



		class Meta:
				model = User
				fields = ['id','account','profile','posts','is_active','i_requested','i_relationshiped','i_followed']

		def get_i_requested(self, obj):

			#testing kenapa obj.relationship.connected_users.all() ga bisa
			#testing kenapa obj.relationship.users_set.all() ga bisa

			print("TESTING")
			logged_in_user = self.context['request'].user
			# a = Relationship.objects.get(user=logged_in_user)

			# print(a.users.all())

			#ternyata harus pake obj.users.all()


			
			if logged_in_user.id is None:
				return ""
			if obj.relationship == logged_in_user.relationship:
				return ""
			r = obj.relationship
			if logged_in_user.relationship in r.users.all():
				return "Accepted"
			else:
				if obj.request_set.all().filter(from_user=logged_in_user).exists():
					return True
				else:
					return False


		def get_i_relationshiped(self, obj):
			logged_in_user = self.context['request'].user
			if logged_in_user.id is None:
				return ""
			if obj.relationship == logged_in_user.relationship:
				return ""
			r = obj.relationship
			if logged_in_user.relationship in r.users.all():
				return True
			else:
				return False

		def get_i_followed(self, obj):
			logged_in_user = self.context['request'].user
			if logged_in_user.id is None:
				return ""
			if obj == logged_in_user:
				return ""
			if obj in logged_in_user.follow.to_user.all():
				return True
			else:
				return False
















# post list
#   -id
#   -poster
#   -title
#   -text
#   -likes_amount
#   -comments_amount
#   -created_at

# post detail
#   -id
#   -poster
#   -title
#   -text
#   -likes
#   -likebutton
#   -likes_amount
#   -comments_amount
#   -comment_set
#   -created_at


class PostPhoto_S(serializers.ModelSerializer):
		class Meta:
				model = PostPhoto
				fields = '__all__'

class PostPhotoList_S(serializers.ModelSerializer):
		class Meta:
				model = PostPhoto
				fields = ['image','description']

class PostPhotoDetail_S(serializers.ModelSerializer):
		class Meta:
				model = PostPhoto
				fields = ['image','description']

class PostList_returnDetailLink_S(serializers.HyperlinkedModelSerializer):

		class Meta:
				model = Post
				fields = ['id','url']

# POST, modifable field = title,text 
class PostList_S(serializers.ModelSerializer):
		likes_amount = serializers.IntegerField(
		source='like_amount', read_only=True)
		comments_amount = serializers.IntegerField(
				source='comment_amount', read_only=True
		)
		poster = Account_Serializer(source='poster.account', read_only=True)

		postphoto_set = PostPhoto_S(many=True, read_only=True)

		descriptions = serializers.ListField(write_only=True)


		likebutton = serializers.BooleanField(source='does_authenticated_user_like', required=False)

		class Meta:
				model = Post
				fields = ['id','poster','title','text','likes_amount','likebutton','comments_amount','created_at','postphoto_set','descriptions']
		
		def create(self, validated_data):
			post = Post.objects.create(
				poster = self.context['request'].user,
				title = validated_data['title'],
				text = validated_data['text']
			)


			for i in validated_data:
				print(i)

			for i in self.context['request'].FILES:
				print(i)
			
			if self.context['request'].FILES is not None:
				if 'descriptions' in validated_data:
					for (i) , (a, b) in zip(self.context['request'].FILES.values(), validated_data['descriptions']):
						PostPhoto.objects.create(
							post = post,
							image = i,
							description = b
						)
						print("IM RUNNING")
						# postphoto.save()
					
					del validated_data['descriptions']
			
			return post



# UPDATE, modifable field = title,text,likebutton 
class PostDetail_S(serializers.ModelSerializer):
		likes_amount = serializers.IntegerField(
		source='like_amount', read_only=True)
		comments_amount = serializers.IntegerField(
				source='comment_amount', read_only=True
		)
		poster = Account_Serializer(source='poster.account', read_only=True)
		postphoto_set = PostPhoto_S(many=True, read_only=True)
		likebutton = serializers.BooleanField(source='does_authenticated_user_like', required=False)
		#comment_set = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name="comment-detail",lookup_url_kwarg="comment_id")
		comments = serializers.HyperlinkedIdentityField(view_name="comment-list", read_only=True,lookup_url_kwarg='post_id')
		likes = serializers.HyperlinkedIdentityField(view_name="post-likes", read_only=True)
		time_creation = serializers.CharField(source="created_at_string")
		class Meta:
				model = Post
				fields = ['id','poster','title','text','likes','likebutton','likes_amount','comments','comments_amount','time_creation','postphoto_set']
				read_only_fields = ['likes','time_creation']

# UPDATE , modifable field = likebutton 
class PostDetail_notOwner_S(serializers.ModelSerializer):
		likes_amount = serializers.IntegerField(
		source='like_amount', read_only=True)
		comments_amount = serializers.IntegerField(
				source='comment_amount', read_only=True
		)
		poster = Account_Serializer(source='poster.account', read_only=True)
		postphoto_set = PostPhoto_S(many=True, read_only=True)
		likebutton = serializers.BooleanField(source='does_authenticated_user_like', required=False)
		#comment_set = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name="comment-detail",lookup_url_kwarg="comment_id")
		comments = serializers.HyperlinkedIdentityField(view_name="comment-list", read_only=True,lookup_url_kwarg='post_id')
		likes = serializers.HyperlinkedIdentityField(view_name="post-likes", read_only=True)
		time_creation = serializers.CharField(source="created_at_string")
		class Meta:
				model = Post
				fields = ['id','poster','title','text','likes','likebutton','likes_amount','comments_amount','comments','time_creation','postphoto_set']
				read_only_fields = ['title','text','likes','time_creation']

class PostLikes_Serializer(serializers.ModelSerializer):
		account = Account_Serializer(read_only=True)
		profile_picture = serializers.ImageField(source="profile.profile_picture",read_only=True)
		i_relationshiped = serializers.SerializerMethodField()
		i_followed = serializers.SerializerMethodField()
		class Meta:
			model = User
			fields = ['id','account','profile_picture']

		def get_i_relationshiped(self, obj):
			logged_in_user = self.context['request'].user
			if logged_in_user.id is None:
				return ""
			if obj.relationship == logged_in_user.relationship:
				return ""
			r = obj.relationship
			if logged_in_user.relationship in r.users.all():
				return True
			else:
				return False

		def get_i_followed(self, obj):
			logged_in_user = self.context['request'].user
			if logged_in_user.id is None:
				return ""
			if obj == logged_in_user:
				return ""
			if obj in logged_in_user.follow.to_user.all():
				return True
			else:
				return False

#comment list
	# -id
	# -Post
	# -commentator
	# -text
	# -likes_amount
	# -created_at

#comment detail
	# -id
	# -Post
	# -commentator
	# -text
	# -likes_amount
	# -created_at
	# -likes
	# -likebutton
	
class CommentList_returnDetailLink_S(serializers.HyperlinkedModelSerializer):
		url = serializers.HyperlinkedIdentityField(view_name="comment-detail", read_only=True, lookup_url_kwarg="comment_id")
		#url kwargs = comment_id , liat url bagian comment-detail
		class Meta:
				model = Comment
				fields = ['id','url']


# POST , modifable field = text
class CommentList_S(serializers.ModelSerializer):
		likes_amount = serializers.IntegerField(
		source='like_amount', read_only=True)
		commentator = Account_Serializer(source='commentator.account', read_only=True)
		class Meta:
				model = Comment
				fields = ['id','post','commentator','text','likes_amount','created_at','image']

# UPDATE , modifable field = text,likebutton
class CommentDetail_S(serializers.ModelSerializer):
		likes_amount = serializers.IntegerField(
		source='like_amount', read_only=True)
		commentator = Account_Serializer(source='commentator.account', read_only=True)
		likebutton = serializers.BooleanField(source='does_authenticated_user_like', required=False)
		
		class Meta:
				model = Comment
				fields = ['id','post','commentator','text','likes_amount','created_at','likes','likebutton','image']
				read_only_fields = ['post','likes','created_at']

# UPDATE , modifable field = likebutton
class CommentDetail_notOwner_S(serializers.ModelSerializer):
		likes_amount = serializers.IntegerField(
		source='like_amount', read_only=True)
		commentator = Account_Serializer(source='commentator.account', read_only=True)
		likebutton = serializers.BooleanField(source='does_authenticated_user_like', required=False)
		
		class Meta:
				model = Comment
				fields = ['id','post','commentator','text','likes_amount','created_at','likes','likebutton','image']
				read_only_fields = ['post','text','likes','created_at']


#POST , modifable field = image,description
class PhotoList_S(serializers.ModelSerializer):
		user = Account_Serializer(source='user.account', read_only=True)
		likes_amount = serializers.IntegerField(
		source='like_amount', read_only=True)
		class Meta:
				model =Photo
				fields = ['id','user','image','description','likes','likes_amount','created_at']
				read_only_fields = ['user','likes','created_at']

#UPDATE , modifable field = image,description,likebutton
class PhotoDetail_S(serializers.ModelSerializer):
		user = Account_Serializer(source='user.account', read_only=True)
		likes_amount = serializers.IntegerField(
		source='like_amount', read_only=True)
		likebutton = serializers.BooleanField(source='does_authenticated_user_like', required=False)
		class Meta:
				model = Photo
				fields = ['id','user','image','description','likes','likes_amount','likebutton','created_at']
				read_only_fields = ['user','likes','created_at']

#UPDATE, modifable field = likebutton
class PhotoDetail_notOwner_S(serializers.ModelSerializer):
		user = Account_Serializer(source='user.account', read_only=True)
		likes_amount = serializers.IntegerField(
		source='like_amount', read_only=True)
		likebutton = serializers.BooleanField(source='does_authenticated_user_like', required=False)
		class Meta:
				model = Photo
				fields = ['id','user','image','description','likes','likes_amount','likebutton','created_at']
				read_only_fields = ['user','likes','image','description','created_at']


#POST , modifable field = text
class PhotoCommentList_S(serializers.ModelSerializer):
		likes_amount = serializers.IntegerField(
		source='like_amount', read_only=True)
		commentator = Account_Serializer(source='commentator.account', read_only=True)
		class Meta:
				model = PhotoComment
				fields = ['photo','commentator','text','likes','created_at','likes_amount','image']
				read_only_fields = ['photo','likes','created_at']

#UPDATE , modifable field = text,likebutton
class PhotoCommentDetaiL_S(serializers.ModelSerializer):
		likes_amount = serializers.IntegerField(
		source='like_amount', read_only=True)
		commentator = Account_Serializer(source='commentator.account', read_only=True)
		likebutton = serializers.BooleanField(source='does_authenticated_user_like', required=False)
		class Meta:
				model = PhotoComment
				fields = ['photo','commentator','text','likes','created_at','likes_amount','likebutton','image']
				read_only_fields = ['photo','likes','created_at']

#UPDATE , modifable field = likebutton
class PhotoCommentDetail_notOwner_S(serializers.ModelSerializer):
		likes_amount = serializers.IntegerField(
		source='like_amount', read_only=True)
		commentator = Account_Serializer(source='commentator.account', read_only=True)
		likebutton = serializers.BooleanField(source='does_authenticated_user_like', required=False)
		class Meta:
				model = PhotoComment
				fields = ['photo','commentator','text','likes','created_at','likes_amount','likebutton','image']
				read_only_fields = ['photo','likes','created_at','text']



















class PostPhoto_S(serializers.ModelSerializer):
		class Meta:
				model = PostPhoto
				fields = '__all__'

import itertools  
class T_PostList_S(serializers.ModelSerializer):
		likes_amount = serializers.IntegerField(
		source='like_amount', read_only=True)
		comments_amount = serializers.IntegerField(
				source='comment_amount', read_only=True
		)
		poster = Account_Serializer(source='poster.account', read_only=True)

		postphoto_set = PostPhoto_S(many=True, read_only=True)

		descriptions = serializers.ListField(write_only=True)

		class Meta:
				model = Post
				fields = ['id','poster','title','text','likes_amount','comments_amount','created_at','postphoto_set','descriptions']
		
		def create(self, validated_data):
			post = Post.objects.create(
				poster = self.context['request'].user,
				title = validated_data['title'],
				text = validated_data['text']
			)


			for i in validated_data:
				print(i)

			for i in self.context['request'].FILES:
				print(i)
			
			if self.context['request'].FILES is not None:
				if 'descriptions' in validated_data:
					for (i) , (b) in zip(self.context['request'].FILES.values(), validated_data['descriptions']):
						PostPhoto.objects.create(
							post = post,
							image = i,
							description = b
						)
						print("IM RUNNING")
						# postphoto.save()
					
					del validated_data['descriptions']
			
			return post


		# def create(self, validated_data):
				# images_data = self.context.get('view').request.FILES

				# post = Post.objects.create(
				# 	poster = self.context['request'].user,
				# 	title = validated_data['title'],
				# 	text = validated_data['text']
				# )

				# for i in images_data.values():
				# 	PostPhoto.objects.create(
				# 		post=post,
				# 		image = i,
				# 		description = i['description']
				# 	)
				# return post
				# data = validated_data.copy()
				# data.pop('images')

				# images_data = self.context['request'].data.images

				# post = Post.object.create(
				# 	poster = self.context['request'].user,
				# 	**data
				# )

				# for image_data in images_data:
				# 	PostPhoto.objects.create(
				# 		post = post,
				# 		image = image_data,
				# 		description = ""
				# 	)
				# return post

# class CommentPhoto_S(serializers.ModelSerializer):
# 		class Meta:
# 			model = CommentPhoto
# 			fields = ['id','image']


# POST , modifable field = text
# class T_CommentList_S(serializers.ModelSerializer):
# 		likes_amount = serializers.IntegerField(
# 		source='like_amount', read_only=True)
# 		commentator = Account_Serializer(source='commentator.account', read_only=True)
		
# 		commentphoto_set = CommentPhoto_S(many=True, read_only=True)
		
# 		class Meta:
# 				model = Comment
# 				fields = ['id','post','commentator','text','likes_amount','created_at','commentphoto_set']
# 				read_only_fields = ['post']

# 		def create(self, validated_data):
# 			post_id = self.context.get('view').kwargs.get('post_id')
# 			post = Post.objects.get(id=post_id)

# 			comment = Comment.objects.create(
# 				post = post,
# 				commentator = self.context['request'].user,
# 				text = validated_data['text']
# 			)


# 			for i in validated_data:
# 				print(i)

# 			for i in self.context['request'].FILES:
# 				print(i)
			
# 			if self.context['request'].FILES is not None:
# 				for i in self.context['request'].FILES.values():
# 					CommentPhoto.objects.create(
# 						comment = comment,
# 						image = i
# 					)
# 					print("IM RUNNING")
# 					# postphoto.save()
			
# 			return comment



