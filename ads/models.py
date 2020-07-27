from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings

# Create your models here.
class Ad(models.Model):
	title = models.CharField(
							max_length=200, 
							validators=[MinLengthValidator(2, "This must be greater than 2 characters")])
	text = models.TextField()
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	picture = models.BinaryField(null=True, blank=True, editable=True)
	content_type = models.CharField(max_length=256, null=True, blank=True, help_text="The MIMEtype of the file")

	comments = models.ManyToManyField(settings.AUTH_USER_MODEL,
        through='Comment', related_name='comments_owned')

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title	

class Comment(models.Model):
	text = models.TextField(validators=[MinLengthValidator(3,"Comment must be greater than 3 characters!")])

	ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		if len(text) < 15: return self.text
		return self.text[:11] + '...'