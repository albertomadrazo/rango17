# -*- coding: utf-8 -*-
from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		if self.views < 1:
			self.views = 0

		if self.likes < 1:
			self.likes = 0

		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.name

class Page(models.Model):

	now = timezone.now()

	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default=0)
	first_visit = models.DateTimeField('first visit', default=now)
	last_visit = models.DateTimeField('last visit', default=now)

	def last_visit_is_after_first(self):
		return self.first_visit <= self.last_visit or self.first_visit == self.last_visit

	def visits_not_in_future(self):
		now = timezone.now()
		print "In visits_not_in_future()"
		print "first", self.first_visit
		print "last ", self.last_visit
		print "now  ", self.now
		return self.first_visit <= self.now and self.last_visit <= self.now

	def __unicode__(self):
		return self.title

class UserProfile(models.Model):
	# This line is required. Links UserProfile to a User model instance.
	user = models.OneToOneField(User)

	# The additional attributes we wish to include.
	website = models.URLField(blank=True) # Aqui blank=True para que sea opcional
	picture = models.ImageField(upload_to='profile_images', blank=True)

	# Override the __unicode__() method to return out something meaningful!
	def __unicode__(self):
		return self.user.username
