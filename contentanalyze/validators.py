from django.core.exceptions import ValidationError


def validate_file(value):
    value= str(value)
    if value.endswith(".txt") != True and value.endswith(".xlsx") != True: 
        raise ValidationError("Faqat TXT yoki Excel (.xlsx) formatdagi xujjat yuklashingiz mumkin")
    else:
        return value