from django.core.exceptions import ValidationError
from django.forms import CharField, Form, ModelForm, HiddenInput, PasswordInput, ModelChoiceField, ChoiceField, Textarea
from Sprint2.models import *
from hashlib import sha512


class LoginForm(Form):
    username = CharField(max_length=25, label="Username")
    password = CharField(max_length=25, label="Password", widget=PasswordInput())

    def clean_username(self):
        data = self.data['username']
        if not User.objects.filter(user_name=data).exists():
            raise ValidationError("Invalid user name or password.")
        else:
            return data

    def clean_password(self):
        data = self.data['password']
        hashed_data = sha512(data.encode()).hexdigest()
        try:
            user = User.objects.get(user_name=self.data['username'])
        except ObjectDoesNotExist:
            raise ValidationError("Invalid user name or password.")

        if user.password != hashed_data:
            raise ValidationError("Invalid user name or password.")
        else:
            return hashed_data


class ChangePasswordForm(ModelForm):
    password_repeat = CharField(max_length=25, label="Repeat Password", widget=PasswordInput())

    class Meta:
        model = User
        fields = ['password', 'user_name']
        labels = {'password': "Password"}
        widgets = {'user_name': HiddenInput(), 'password': PasswordInput()}

    def clean_password(self):
        data = self.data['password']

        if type(data) is not str:
            raise ValidationError("Password must be string.")

        if self.data['password_repeat'] != data:
            raise ValidationError("Password fields don't match.")

        if len(data) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        foundletter = False
        foundnumber = False
        for c in data:
            if c.isalpha():
                foundletter = True
            if c.isdigit():
                foundnumber = True
        if not foundletter or not foundnumber:
            raise ValidationError("Password must contain at least one letter and at least one number.")

        hashed_data = sha512(data.encode()).hexdigest()
        return hashed_data


class CreateUserForm(ModelForm):

    class Meta:
        model = User
        fields = ['user_name', 'password', 'privilege_level']
        labels = {'user_name': 'User name', 'password': 'Default Password', 'privilege_level': 'Account Type'}

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        limited_choices=[(choice[0], choice[1]) for choice in privilege_choices if choice[0] != "ADMIN"]
        self.fields['privilege_level'] = ChoiceField(choices=limited_choices)

    def save(self, commit=True):
        # If the user being created is a TA, use that model instead
        if self.cleaned_data['privilege_level'] == "TA":
            ta = Ta(user_name=self.cleaned_data['user_name'],
                    password=self.cleaned_data['password'],
                    privilege_level=self.cleaned_data['privilege_level'])
            ta.save()
        else:
            super().save(commit)

    def clean_user_name(self):
        data = self.cleaned_data['user_name']
        try:
            user = User.objects.get(user_name=data)
            raise ValidationError("User already exists.")
        except ObjectDoesNotExist:
            pass
        return data

    def clean_privilege_level(self):
        data = self.data['privilege_level']
        if data == "ADMIN":
            raise ValidationError("Cannot create another admin account.")
        return data

    def clean_password(self):
        data=self.data['password']
        hashed_data=sha512(data.encode()).hexdigest()
        return hashed_data


class CreateCourseForm(ModelForm):

    class Meta:
        model = Course
        fields = ['name', 'description', 'lecture_num']
        labels = {'name': 'Subject & Number', 'description': 'Title', 'lecture_num': 'Lecture Number'}

    def clean_lecture_num(self):
        data = self.data['lecture_num']
        if not data.isnumeric():
            raise ValidationError("Lecture number must be numeric.")
        if len(data) != 3:
            raise ValidationError("Lecture number must have length 3.")
        return data


class CreateSectionForm(ModelForm):

    class Meta:
        model = Section
        fields = ['course', 'number', 'type', 'days', 'start_time', 'end_time']
        labels = {'course': 'Associated Lecture', 'number': 'Section Number', 'type': 'Section Type',
                  'days': 'Meeting Days', 'start_time': 'Start Time', 'end_time': 'End Time'}

    def clean_number(self):
        data = self.data['number']
        if not data.isnumeric():
            raise ValidationError("Section number must be numeric.")
        if len(data) != 3:
            raise ValidationError("Section number must have length 3.")
        return data

    def clean_days(self):
        data = self.data['days']
        if len(data) > 5:
            raise ValidationError("Sections must meet five or fewer days per week.")
        found = [False, False, False, False, False, False]
        for i in range(len(data)):
            if data[i] not in days_choices:
                raise ValidationError("Days must be M, T, W, R, F or O for Online.")
            if found[days_choices.index(data[i])]:
                raise ValidationError("Duplicate days.")
            found[days_choices.index(data[i])] = True
        return data

    def clean_end_time(self):
        data = self.data['end_time']
        if data < self.data['start_time']:
            raise ValidationError("End time must be later than start time.")
        return data


class ContactInfoForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'email': 'Email',
                  'phone': 'Phone Number', 'address': 'Mailing Address'}

    # TODO implement phone number validation


class TaPrefForm(ModelForm):

    class Meta:
        model = Ta
        fields = ['qualifications', 'pref_1', 'pref_2', 'pref_3']
        labels = {'qualifications': 'Qualifications', 'pref_1': 'First Assignment Choice',
                  'pref_2': 'Second Assignment Choice', 'pref_3': 'Third Assignment Choice'}
        widgets = {'qualifications': Textarea}


class TaEntersSchedule(ModelForm):

    class Meta:
        model = Enroll
        fields = ['ta', 'section']
        labels = {'section': 'Course Section to add'}
        widgets = {'ta': HiddenInput()}


class InstructorAssignmentForm(Form):
    course = ModelChoiceField(queryset=Course.objects.all(), label="Course")
    instructor = ModelChoiceField(queryset=User.objects.filter(privilege_level="INSTRUCTOR"), label="Instructor")

    class Meta:
        model = Course

    def save(self):
        if not self.is_valid():
            raise ValueError("Form is not valid.")
        course_data = self.cleaned_data['course']
        course_to_mod = Course.objects.get(name=course_data.name, lecture_num=course_data.lecture_num)
        course_to_mod.instructor = self.cleaned_data['instructor']
        course_to_mod.save()


class CourseAssignmentForm(ModelForm):

    class Meta:
        model = CourseAssignment
        fields = ['course', 'ta']
        labels = {'course': "Course", 'ta': "TA"}


class SelectionForm(Form):

    def __init__(self, queryset, *args, **kwargs):
        super(SelectionForm, self).__init__(*args, **kwargs)
        self.fields['choice'] = ModelChoiceField(queryset=queryset, label="Course")


class TaAssignmentForm(Form):

    def __init__(self, sections, tas, *args, **kwargs):
        super(TaAssignmentForm, self).__init__(*args, **kwargs)
        self.fields['section'] = ModelChoiceField(queryset=sections, label="Section")
        self.fields['ta'] = ModelChoiceField(queryset=tas, label="TA")


