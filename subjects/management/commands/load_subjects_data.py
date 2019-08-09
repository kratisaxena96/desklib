from django.core.management.base import BaseCommand, CommandError
from subjects.models import Subject
import json

class Command(BaseCommand):
    help = 'Loads subjects data'

    def handle(self, *args, **options):
        filename = 'subjects/data/subjects.json'  # https://github.com/classcentral/online-course-taxonomy
        try:
            with open(filename, 'r') as f:
                subjects_data = json.load(f)
        except Exception as e:
            raise CommandError('Cannot read subject.json')

        for subject, data in subjects_data.items():
            try:
                slug = data.get("slug")
                keywords = data.get("keywords")
                parent_subject = data.get("parent_slug")
                subject_obj = Subject()
                subject_obj.name = subject
                subject_obj.slug = slug
                subject_obj.save()
                parent_obj = Subject.objects.filter(slug=parent_subject)
                if parent_obj:
                    subject_obj.parent_subject = parent_obj[0]
                    subject_obj.save()
                # subject_obj.keywords.add(keywords)
                for keyword in keywords:
                    subject_obj.keywords.add(keyword)

                self.stdout.write('Successfully added subject: ' + subject)

            except Exception as e:
                self.stdout.write(self.style.ERROR(e))

        self.stdout.write(self.style.SUCCESS('Successfully added subject data'))