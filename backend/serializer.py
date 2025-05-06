from .models import *
from rest_framework.serializers import ModelSerializer


class ReactSerializer(ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['name', 'email', 'joined']


class TutorSerializer(ModelSerializer):
    class Meta:
        model = Tutor
        fields = '__all__'


class LevelSerializer(ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'level_name', 'level_class']


class SubjectSerializer(ModelSerializer):
    level = LevelSerializer(read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'subject_name', 'level', 'price', 'exam_prep']


class TuteesSerializer(ModelSerializer):
    class Meta:
        model = Tutee
        fields = '__all__'
        depth = 2


class TutorSubjectSerializer(ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    tutor = TutorSerializer(read_only=True)
    
    class Meta:
        model = TutorSubject
        fields = ['id', 'tutor', 'subject', 'desc']


class TuteeHoursSerializer(ModelSerializer):
    class Meta:
        model = TuteeHours
        fields = '__all__'
        depth = 3


class PaymentStatusSerializer(ModelSerializer):
    class Meta:
        model = PaymentStatus
        fields = '__all__'
        depth = 1