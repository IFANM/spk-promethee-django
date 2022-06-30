from django.core.exceptions import ValidationError

def validate_email(value):
	email_pass = ['@gmail.com', '@yahoo.com', '@outlook.com', '@unej.ac.id']
	for x in email_pass:
		if x in value:
			break
	else:
		raise ValidationError("Domain Email Tidak Valid!")