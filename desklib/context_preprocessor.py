from subjects.models import Subject


def get_subjects(request):
    p_subjects = Subject.objects.filter(parent_subject__isnull=True).prefetch_related('subject_set')
    context = {'parent_subjects': p_subjects
               }
    return context
