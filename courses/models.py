from __future__ import unicode_literals

#from django.conf import settings    ###############################
from django.core.validators import MinValueValidator, MaxValueValidator ###############################
from django.db import models
from django.contrib.auth import get_user_model  ############################### TEST!


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_picture = models.URLField(max_length=300)
    course_about = models.TextField(null=True, blank=True)   ###############################
    pub_date = models.DateTimeField('date published')
#    course_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    ###############################
    course_owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)    ############################### TEST!

    def __str__(self):
        return self.course_name


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.lesson_name


class Text(models.Model):
    content = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_video = models.BooleanField(default=False)
    priority = models.PositiveSmallIntegerField(default=0)
    
    def __str__(self):
        return self.content


class Exam(models.Model):                                         ###############################
    question = models.TextField()                                 ###############################
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  ###############################
    first_answer = models.TextField()                             ###############################
    second_answer = models.TextField()                            ###############################
    third_answer = models.TextField()                             ###############################
    fourth_answer = models.TextField()                            ###############################
    correct_answer = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])  ###############################
                                                                  ###############################
    def __str__(self):                                            ###############################
        return self.question                                      ###############################


class Submission(models.Model):                                                      ###############################
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)                         ###############################
#    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  ###############################
    student = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  ############################### TEST!
    answer = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])                    ###############################
                                                                                     ###############################
    def __str__(self):                                                               ###############################
        return '%s %s %s' % (self.exam, self.student, self.answer)                   ###############################
