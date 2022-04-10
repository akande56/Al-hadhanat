# from django.db.models.signals import pre_save
# from django.dispatch import receiver

# from .models import Session,Class,Student


# @receiver(pre_save, sender=Session)
# def create_add_class_student(sender, instance, **kwargs):
#     session = instance.session
#     instance.save()
#     Class.objects.create(name="pp1({})".format(session),session=instance)
