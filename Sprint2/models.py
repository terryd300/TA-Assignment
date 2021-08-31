from django.core.exceptions import FieldError, ObjectDoesNotExist
from django.core.validators import EmailValidator
from django.db import models, IntegrityError
from datetime import time


# User privilege level is constrained to the following options.
privilege_choices = [
    ("ADMIN", "Admin"),
    ("INSTRUCTOR", "Instructor"),
    ("TA", "TA"),
]

# Section type is constrained to the following options
type_choices = [
    ("LEC", "LEC"),
    ("DIS", "DIS"),
    ("LAB", "LAB"),
    ("ONL", "ONL"),
]

# Section days can be any combination of the following
days_choices = [
    'M',
    'T',
    'W',
    'R',
    'F',
    'O',
]


#  This comment is here to change this file, so I can test whether git is set up properly.
class User(models.Model):
    user_name = models.CharField(max_length=25, blank=False, default="", unique=True, primary_key=True)
    password = models.CharField(max_length=512, blank=False, default="")
    privilege_level = models.CharField(max_length=10, choices=privilege_choices, blank=False, default="")
    first_name = models.CharField(max_length=25, blank=True, default="")
    last_name = models.CharField(max_length=25, blank=True, default="")
    email = models.EmailField(max_length=25, blank=True, default="")
    phone = models.CharField(max_length=12, blank=True, default="")
    address = models.CharField(max_length=25, blank=True, default="")
    qualifications = models.CharField(max_length=500, blank=True, default="No qualification entered by this TA yet!")

    class Meta:
        app_label='Sprint2'

    def __str__(self):
        return self.user_name

    def save(self, *args, **kwargs):
        # user_name constraints
        # is string
        if type(self.user_name) is not str:
            raise TypeError("user.user_name only accepts strings")
        # is not blank
        if self.user_name == "":
            raise IntegrityError("user.user_name blank")

        # password constraints
        # is string
        if type(self.password) is not str:
            raise TypeError("user.password only accepts strings")
        # is not blank
        if self.password == "":
            raise IntegrityError("user.password blank")

        # privilege_level constraints
        # is string
        if type(self.privilege_level) is not str:
            raise TypeError("user.privilege_level only accepts strings")
        # is not blank
        if self.privilege_level == "":
            raise IntegrityError("user.privilege_level blank")
        # can't be changed
        try:
            user = User.objects.get(user_name=self.user_name)
            if self.privilege_level != user.privilege_level:
                raise FieldError("can't change privileges for existing account")
        except ObjectDoesNotExist:
            pass
        # can't give away admin privileges
        if self.privilege_level == "ADMIN" and self.user_name != "Admin":
            raise FieldError("only Admin account may have admin privileges")

        # first_name constraints
        # is string
        if type(self.first_name) is not str:
            raise TypeError("user.first_name only accepts strings")

        # last_name constraints
        # is string
        if type(self.last_name) is not str:
            raise TypeError("user.last_name only accepts strings")

        # email constraints
        # is string
        if type(self.email) is not str:
            raise TypeError("user.email only accepts strings")
        # is correct format
        if self.email != "":
            validator = EmailValidator()
            validator(self.email)

        # phone constraints
        # is string
        if type(self.phone) is not str:
            raise TypeError("user.phone only accepts strings")

        # address constraints
        # is string
        if type(self.address) is not str:
            raise TypeError("user.address only accepts strings")

        super().save(*args, **kwargs)


class Course(models.Model):
    name = models.CharField(max_length=25, default="")
    lecture_num = models.CharField(max_length=3, default="")
    description = models.CharField(max_length=50, blank=True, default="")
    instructor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        app_label = 'Sprint2'
        constraints = [models.UniqueConstraint(fields=["name", "lecture_num"], name="course_id")]

    def __str__(self):
        return self.name+", "+self.lecture_num

    def save(self, *args, **kwargs):
        # name constraints
        # is string
        if type(self.name) is not str:
            raise TypeError("course.name only accepts strings")
        # is not blank
        if self.name == "":
            raise IntegrityError("course.name is blank")

        # lecture_num constraints
        # is string
        if type(self.lecture_num) is not str:
            raise TypeError("course.lecture_num only accepts strings")
        # is not blank
        if self.lecture_num == "":
            raise IntegrityError("course.lecture_num is blank")
        # is correct format
        if len(self.lecture_num) != 3:
            raise FieldError("course.lecture_num must have length 3")
        if not self.lecture_num.isnumeric():
            raise FieldError("non-numeric course.lecture_number")

        # description constraints
        # is string
        if type(self.description) is not str:
            raise TypeError("course.description only accepts strings")

        # instructor constraints
        if self.instructor is not None:
            # is not a TA
            if self.instructor.privilege_level == "TA":
                raise FieldError("TA assigned as instructor")
            # is in DB
            user = User.objects.get(user_name=self.instructor.user_name)

        super().save(*args, **kwargs)


class Ta(User):
    pref_1 = models.ForeignKey(Course, related_name="preference_1", null=True, blank=True, on_delete=models.SET_NULL)
    pref_2 = models.ForeignKey(Course, related_name="preference_2", null=True, blank=True, on_delete=models.SET_NULL)
    pref_3 = models.ForeignKey(Course, related_name="preference_3", null=True, blank=True, on_delete=models.SET_NULL)
    quals = models.ForeignKey(User, related_name="qual", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        app_label='Sprint2'

    def save(self, *args, **kwargs):
        # pref_1 constraints
        if self.pref_1 is not None:
            # is in DB
            pref = Course.objects.get(name=self.pref_1.name, lecture_num=self.pref_1.lecture_num)

        # pref_2 constraints
        if self.pref_2 is not None:
            # is in DB
            pref = Course.objects.get(name=self.pref_2.name, lecture_num=self.pref_2.lecture_num)

        # pref_3 constraints
        if self.pref_3 is not None:
            # is in DB
            pref = Course.objects.get(name=self.pref_3.name, lecture_num=self.pref_3.lecture_num)

        # qualifications constraints
        # is string
        if type(self.qualifications) is not str:
            raise TypeError("Ta.qualifications only accepts string")

        # privilege_level is "TA"
        if not self.privilege_level == "TA":
            raise FieldError("TA object must have matching privilege level")
        super().save(*args, **kwargs)


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    number = models.CharField(max_length=3, default="")
    type = models.CharField(max_length=3, default="", choices=type_choices)
    days = models.CharField(max_length=5, default="")
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    ta = models.ForeignKey(Ta, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        app_label = 'Sprint2'
        constraints = [models.UniqueConstraint(fields=["course", "number"], name="section_id")]

    def __str__(self):
        return self.course.name+", "+self.number

    def save(self, *args, **kwargs):
        # course constraints
        if self.course is not None:
            # is in DB
            course = Course.objects.get(name=self.course.name, lecture_num=self.course.lecture_num)

        # number constraints
        # is string
        if type(self.number) is not str:
            raise TypeError("section.number only accepts strings")
        # is not blank
        if self.number == "":
            raise IntegrityError("section.number is blank")
        # is correct format
        if len(self.number) != 3:
            raise FieldError("section.number must have length 3")
        if not self.number.isnumeric():
            raise FieldError("non-numeric section.number")

        # type constraints
        # is string
        if type(self.type) is not str:
            raise TypeError("section.type only accepts strings")
        # is not blank
        if self.type == "":
            raise IntegrityError("section.type is blank")
        # can't be changed
        try:
            section = Section.objects.get(course=self.course, number=self.number)
            if self.type != section.type:
                raise FieldError("can't change type for existing section")
        except ObjectDoesNotExist:
            pass

        # days constraints
        # is string
        if type(self.days) is not str:
            raise TypeError("section.days only accepts strings")
        # is not blank
        if self.days == "":
            raise IntegrityError("section.days is blank")
        # is correct format
        if len(self.days) > 5:
            raise FieldError("section.days must have length <= 5")
        found = [False, False, False, False, False, False]
        for i in range(len(self.days)):
            if self.days[i] not in days_choices:
                raise FieldError("Invalid section.days")
            if found[days_choices.index(self.days[i])]:
                raise FieldError("Duplicate days in section.days")
            found[days_choices.index(self.days[i])] = True

        # start_time constraints
        # is time
        if type(self.start_time) is not time:
            raise TypeError("section.start_time only accepts times")
        # not null
        if self.start_time is None:
            raise IntegrityError("section.start_time is blank")

        # end_time constraints
        # is time
        if type(self.end_time) is not time:
            raise TypeError("section.end_time only accepts times")
        # not null
        if self.end_time is None:
            raise IntegrityError("section.end_time is blank")
        # is after start_time
        if self.end_time < self.start_time:
            raise FieldError("section.end_time before start_time")

        # ta constraints
        if self.ta is not None:
            # is TA
            if self.ta.privilege_level != "TA":
                raise FieldError("section.ta must be TA")
            # is in DB
            ta = Ta.objects.get(user_name=self.ta.user_name)

        super().save(*args, **kwargs)


class Enroll(models.Model):
    ta = models.ForeignKey(Ta, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    class Meta:
        app_label = 'Sprint2'
        constraints = [models.UniqueConstraint(fields=["ta", "section"], name="enroll_identifier")]

    def __str__(self):
        return self.section.__str__()

    def save(self, *args, **kwargs):
        # ta constraints
        if self.ta is not None:
            # is in DB
            ta = Ta.objects.get(user_name=self.ta.user_name)

        # section constraints
        if self.section is not None:
            # is in DB
            section = Section.objects.get(course=self.section.course, number=self.section.number)

        super().save(*args, **kwargs)


class CourseAssignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    ta = models.ForeignKey(Ta, on_delete=models.CASCADE)

    class Meta:
        app_label = 'Sprint2'
        constraints = [models.UniqueConstraint(fields=["course", "ta"], name="course_assignment_identifier")]

    def __str__(self):
        return self.ta.__str__()

    def save(self, *args, **kwargs):
        # course constraints
        if self.course is not None:
            # is in DB
            course = Course.objects.get(name=self.course.name, lecture_num=self.course.lecture_num)

        # ta constraints
        if self.ta is not None:
            # is in DB
            ta = Ta.objects.get(user_name=self.ta.user_name)

        super().save(*args, **kwargs)
