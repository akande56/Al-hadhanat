import random

from django.core.management import BaseCommand

from Students.models import Subject


class Command(BaseCommand):
    help = "update third term total scores"

    def handle(self, *args, **options):
        all = Subject.objects.all()
        ref = ""
        self.stdout.write(
            self.style.SUCCESS("Running dear abdulsalam... updating third term totalls.. :)")
        )
        for i in all:
            total = (
            i.test1_term3
            + i.test2_term3
            + i.assignment1_term3
            + i.assignment2_term3
            + i.Exam_term3
           )
            i.total_term3 = total
            if total >= 70 and total <= 100:
                i.grade_term3 = "A"
            elif total >= 60 and total <= 70:
                i.grade_term3 = "B"
            elif total >= 50 and total <= 59:
                i.grade_term3 = "C"
            elif total >= 40 and total <= 49:
                i.grade_term3 = "D"
            else:
                i.grade_term3 = "E"
            i.save()
        self.stdout.write(self.style.SUCCESS("done!"))
