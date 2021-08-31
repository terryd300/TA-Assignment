from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from Sprint2.forms import *
from Sprint2 import commands
from hashlib import sha512

# Map urls to their associated forms
form_map = {
    '/passwordchange': ChangePasswordForm,
    '/createuser': CreateUserForm,
    '/createcourse': CreateCourseForm,
    '/createsection': CreateSectionForm,
    '/contactinfo': ContactInfoForm,
    '/taprefs': TaPrefForm,
    '/taAddSchedule': TaEntersSchedule,
    '/instructortocourse': InstructorAssignmentForm,
    '/tatocourse': CourseAssignmentForm,
}

# Map account types to the urls available to them
auth_map = {
    'ADMIN': [
        '/passwordchange',
        '/createuser',
        '/createcourse',
        '/createsection',
        '/contactinfo',
        '/courses',
        '/sections',
        '/users',
        '/instructortocourse',
        '/tatocourse',
        '/viewTaQual',
        '/viewconflicts',
        '/deluser',
        '/reset',
        # '/logout',
    ],
    "INSTRUCTOR": [
        '/passwordchange',
        '/contactinfo',
        '/courses',
        '/sections',
        '/users',
        '/tatosection'
        # '/logout',
    ],
    "TA": [
        '/passwordchange',
        '/contactinfo',
        '/taprefs',
        '/courses',
        '/sections',
        '/users',
        '/taAddSchedule',
        '/taDelSchedule',
        # '/logout',
    ]
}

link_map = {
    'ADMIN': [
        '/courses',
        '/users',
    ],
    "INSTRUCTOR": [
        '/courses',
    ],
    "TA": [
        '/taprefs',
        '/courses',
    ]
}


def user_logged_in(request):
    return 'user' in request.session.keys()

def user_has_access(request):
    return request.path in auth_map[request.session['privilege']]


class Home(View):

    # Labels for the links on home page
    links_map = {
        '/passwordchange': "Change Password",
        '/createuser': "Create User",
        '/createcourse': "Create Course",
        '/createsection': "Create Section",
        '/contactinfo': "Contact Info",
        '/taprefs': "Course Preferences",
        '/logout': "Log Out",
        '/courses': "View Courses",
        '/sections': "View Sections",
        '/users': "View Users",
        '/taAddSchedule': "Add Course to Schedule",
        '/taDelSchedule': "Remove Course from Schedule",
        '/instructortocourse': "Assign Instructor to Course",
        '/tatocourse': "Assign TA to Course",
        '/tatosection': "Assign TA to Section",
        '/viewTaQual': "View TA qualifications",
        '/viewconflicts': "View TA Schedule Conflicts",
        '/deluser': "Delete User",
        '/reset': "Reset System",
    }

    def get(self, request):
        if 'user' not in request.session.keys():
            return redirect('/main/login.html')
        else:
            return render(request, 'main/index.html', {'url_dict': {key: self.links_map[key] for key in auth_map[request.session['privilege']]},
                                                       'username': request.session['user'], 'privilege': request.session['privilege']})

    def post(self, request):
        return redirect('/main/index.html')


class Login(View):

    def get(self, request):
        if user_logged_in(request):
            return redirect('/main/index.html')

        # This is here to automatically create the admin account if it is not in the database.
        try:
            admin = User.objects.get(user_name="Admin")
        except ObjectDoesNotExist:
            hashed_password = sha512(b"qwerty").hexdigest()
            admin = User(user_name="Admin", password=hashed_password, privilege_level="ADMIN")
            admin.save()

        return render(request, 'main/login.html', {'loginform': LoginForm()})

    def post(self, request):
        if user_logged_in(request):
            return redirect('/main/index.html')
        form = LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(user_name=request.POST['username'])
            request.session['user'] = user.user_name
            request.session['privilege'] = user.privilege_level
            return redirect('/main/index.html')
        else:
            return render(request, 'main/login.html', {'loginform': LoginForm(),
                                                       'message': "Invalid user name or password."})


class Logout(View):

    def get(self, request):
        request.session.flush()
        return redirect('/main/login.html')

    def post(self, request):
        return redirect('/logout')


class FormInput(View):

    def get(self, request):
        if not user_logged_in(request):
            return redirect('/main/login.html')
        if not user_has_access(request):
            return render(request, 'main/message.html', {'message': "You don't have permission to access this page."})
        saved_data = None
        if request.path == '/contactinfo':
            user = User.objects.get(user_name=request.session['user'])
            saved_data = model_to_dict(user, fields=['first_name', 'last_name', 'email', 'phone', 'address'])
        if request.path == '/taprefs':
            ta = Ta.objects.get(user_name=request.session['user'])
            saved_data = model_to_dict(ta, fields=['qualifications', 'pref_1', 'pref_2', 'pref_3'])
        form = form_map[request.path]() if saved_data is None else form_map[request.path](saved_data)
        return render(request, 'main/FormInput.html', {'form': form, 'message': "",
                                                       'url_dict': {key: Home.links_map[key] for key in
                                                                    auth_map[request.session['privilege']]},
                                                       'username': request.session['user']
                                                       })

    def post(self, request):
        if not user_logged_in(request):
            return redirect('/main/login.html')
        if not user_has_access(request):
            return render(request, 'main/message.html', {'message': "You don't have permission to access this page.",
                                                         'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]},
                                                         'username': request.session['user']
                                                         })
        form = form_map[request.path](request.POST)

        # this is to make sure the correct database record is being updated
        # TODO figure out a way to handle this more elegantly
        if form.Meta.model == User and request.path != "/createuser":
            newdict = request.POST.copy()
            newdict['user_name'] = request.session['user']
            form = form_map[request.path](newdict, instance=User.objects.get(user_name=request.session['user']))
        if form.Meta.model == Ta:
            newdict = request.POST.copy()
            newdict['user_name'] = request.session['user']
            form = form_map[request.path](newdict, instance=Ta.objects.get(user_name=request.session['user']))
        if form.Meta.model == Enroll:
            newdict = request.POST.copy()
            newdict['ta'] = Ta.objects.get(user_name=request.session['user'])
            form = form_map[request.path](newdict)

        if form.is_valid():
            form.save()
            return render(request, 'main/message.html', {'message': "Submission successful.",
                                                         'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]},
                                                         'username': request.session['user']
                                                         })
        else:
            return render(request, 'main/FormInput.html', {'form': form, 'message': "",
                                                           'url_dict': {key: Home.links_map[key] for key in
                                                                        auth_map[request.session['privilege']]},
                                                           'username': request.session['user']
                                                           })


class Users(View):

    def get(self, request):
        if not user_logged_in(request):
            return redirect('/main/login.html')
        if not user_has_access(request):
            return render(request, 'main/message.html', {'message': "You don't have permission to access this page.",
                                                         'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]},
                                                         'link_dict': {key: Home.links_map[key] for key in
                                                                       link_map[request.session['privilege']]},
                                                         'username': request.session['user']
                                                         })
        users = User.objects.all()
        return render(request, 'main/users.html', {'users': users,
                                                   'url_dict': {key: Home.links_map[key] for key in
                                                                auth_map[request.session['privilege']]},
                                                   'link_dict': {key: Home.links_map[key] for key in
                                                                 link_map[request.session['privilege']]},
                                                   'username': request.session['user']
                                                   })

    def post(self, request):
        return redirect('/users')


class Classes(View):

    def get(self, request):
        if not user_logged_in(request):
            return redirect('/main/login.html')
        if not user_has_access(request):
            return render(request, 'main/message.html', {'message': "You don't have permission to access this page.",
                                                         'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]},
                                                         'link_dict': {key: Home.links_map[key] for key in
                                                                       link_map[request.session['privilege']]},
                                                         'username': request.session['user'],
                                                         })
        else:
            courses = Course.objects.all()
            return render(request, 'main/courses.html', {'courses': courses,
                                                         'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]},
                                                         'link_dict': {key: Home.links_map[key] for key in
                                                                       link_map[request.session['privilege']]},
                                                         'username': request.session['user']
                                                         })

    def post(self, request):
        return redirect('/courses')


class Sections(View):

    def get(self, request):
        if not user_logged_in(request):
            return redirect('/main/login.html')
        if not user_has_access(request):
            return render(request, 'main/message.html', {'message': "You don't have permission to access this page.",
                                                         'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]},
                                                         'link_dict': {key: Home.links_map[key] for key in
                                                                       link_map[request.session['privilege']]},
                                                         'username': request.session['user']
                                                         })
        else:
            sections = Section.objects.all().order_by('course', 'number')
            return render(request, 'main/sections.html', {'sections': sections,
                                                          'url_dict': {key: Home.links_map[key] for key in
                                                                       auth_map[request.session['privilege']]},
                                                          'link_dict': {key: Home.links_map[key] for key in
                                                                        link_map[request.session['privilege']]},
                                                          'username': request.session['user']
                                                          })

    def post(self, request):
        return redirect('/sections')


class AssignTA(View):

    def get(self, request):
        if not user_logged_in(request):
            return redirect('/main/login.html')
        if not user_has_access(request):
            return render(request, 'main/message.html', {'message': "You don't have permission to access this page.",
                                                         'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]},
                                                         'username': request.session['user']
                                                         })
        queryset = Course.objects.filter(instructor=request.session['user'])
        return render(request, 'main/SelectionInput.html', {'selectform': SelectionForm(queryset), 'dependentform': "",
                                                            'url_dict': {key: Home.links_map[key] for key in
                                                                         auth_map[request.session['privilege']]},
                                                            'username': request.session['user']
                                                            })

    def post(self, request):
        if not user_logged_in(request):
            return redirect('/main/login.html')
        if not user_has_access(request):
            return render(request, 'main/message.html', {'message': "You don't have permission to access this page.",
                                                         'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]},
                                                         'username': request.session['user']
                                                         })
        queryset = Course.objects.filter(instructor=request.session['user'])
        form = SelectionForm(queryset, request.POST)
        if 'choice' in request.POST:
            request.session['choice'] = request.POST['choice']
            section_choices = Section.objects.filter(course=request.POST['choice'])
            ta_choices = CourseAssignment.objects.filter(course=request.POST['choice'])
            return render(request, 'main/SelectionInput.html',
                          {'selectform': form, 'dependentform': TaAssignmentForm(section_choices, ta_choices),
                           'url_dict': {key: Home.links_map[key] for key in auth_map[request.session['privilege']]},
                           'username': request.session['user']
                           })
        else:
            section_choices = Section.objects.filter(course=request.session['choice'])
            ta_choices = CourseAssignment.objects.filter(course=request.session['choice'])
            dependent = TaAssignmentForm(section_choices, ta_choices, request.POST)
            if dependent.is_valid():
                section = dependent.cleaned_data['section']
                ta = dependent.cleaned_data['ta']
                section.ta = ta.ta
                section.save()
                request.session.pop('choice')
            return render(request, 'main/message.html', {'message': "Submission successful.",
                                                         'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]},
                                                         'username': request.session['user']
                                                         })


class DeleteEnroll(View):

    def get(self, request):
        if not user_logged_in(request):
            return redirect('/main/login.html')
        if not user_has_access(request):
            return render(request, 'main/message.html', {'message': "You don't have permission to access this page.",
                                                         'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]},
                                                         'username': request.session['user']
                                                         })
        ta = Ta.objects.get(user_name=request.session['user'])
        enrolls = Enroll.objects.filter(ta=ta)
        form = SelectionForm(enrolls)
        return render(request, 'main/SelectionInput.html', {'selectform': form, 'dependentform': "",
                                                            'url_dict': {key: Home.links_map[key] for key in
                                                                         auth_map[request.session['privilege']]},
                                                            'username': request.session['user']
                                                            })

    def post(self, request):
        if not user_logged_in(request):
            return redirect('/main/login.html')
        if not user_has_access(request):
            return render(request, 'main/message.html', {'message': "You don't have permission to access this page.",
                                                         'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]},
                                                         'username': request.session['user']
                                                         })
        ta = Ta.objects.get(user_name=request.session['user'])
        enrolls = Enroll.objects.filter(ta=ta)
        form = SelectionForm(enrolls, request.POST)
        if form.is_valid():
            this_enroll = form.cleaned_data['choice']
            this_enroll.delete()
        return render(request, 'main/message.html', {'message': "Submission successful.",
                                                     'url_dict': {key: Home.links_map[key] for key in
                                                                  auth_map[request.session['privilege']]},
                                                     'username': request.session['user']

                                                     })


class viewTaQual(View):
    def get(self, request):
        if not user_logged_in(request):
            return redirect('/main/login.html')
        if not user_has_access(request):
            return render(request, 'main/message.html', {'message': "You don't have permission to access this page.",
                                                         'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]},
                                                         'username': request.session['user']
                                                         })
        listOfTAs = Ta.objects.all()
        return render(request, 'main/viewTaQual.html', {'listOfTAs': listOfTAs,
                                                        'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]}})


class ViewConflicts(View):

    def get(self, request):
        if not user_logged_in(request):
            return redirect('/main/login.html')
        if not user_has_access(request):
            return render(request, 'main/message.html', {'message': "You don't have permission to access this page."})
        sections = list()
        tas = Ta.objects.all()
        for ta in tas:
            enrolled = Enroll.objects.select_related('section').filter(ta=ta)
            taSections = Section.objects.filter(ta=ta)
            for section in enrolled:
                enrolledSection = section.section
                for section in taSections:
                    if (enrolledSection.start_time <= section.end_time) & (enrolledSection.start_time <= section.end_time):
                        if enrolledSection.days == section.days:
                            sections.append((enrolledSection, section))
        if not sections:  # no conflicts found
            return render(request, 'main/message.html', {'message': "No  Schedule Conflicts Found."})
        else:
            return render(request, 'main/conflicts.html',  {'conflicts': sections})

    def post(self,request):
        return redirect('/viewconflicts')


class DelUser(View):
    def get(self, request):
        if not user_logged_in(request):
            return redirect('/main/login.html')
        if not user_has_access(request):
            return render(request, 'main/message.html', {'message': "You don't have permission to access this page.",
                                                         'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]},
                                                         'username': request.session['user']
                                                         })
        users = []
        for user in User.objects.all():
            if user.privilege_level != 'ADMIN':
                users.append(user)

        return render(request, 'main/deluser.html', {'url_dict': {key: Home.links_map[key] for key in
                                                                auth_map[request.session['privilege']]},
                                                   'username': request.session['user'],
                                                   'users': User.objects.all()
                                                   })

    def post(self, request):
        if not user_logged_in(request):
            return redirect('/main/login.html')
        if not user_has_access(request):
            return render(request, 'main/message.html', {'message': "You don't have permission to access this page.",
                                                         'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]},
                                                         'username': request.session['user']
                                                         })
        User.objects.get(user_name=request.POST['username']).delete()
        return render(request, 'main/message.html', {'message': 'User \'' + request.POST['username'] + '\' deleted.',
                                                     'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]},
                                                      'username': request.session['user']})


class Reset(View):
    def get(self, request):
        if not user_logged_in(request):
            return redirect('/main/login.html')
        if not user_has_access(request):
            return render(request, 'main/message.html', {'message': "You don't have permission to access this page.",
                                                         'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]},
                                                         'username': request.session['user']
                                                         })
        return render(request, 'main/reset.html', {'url_dict': {key: Home.links_map[key] for key in
                                                                  auth_map[request.session['privilege']]},
                                                        'username': request.session['user']
                                                        })

    def post(self, request):
        if not user_logged_in(request):
            return redirect('/main/login.html')
        if not user_has_access(request):
            return render(request, 'main/message.html', {'message': "You don't have permission to access this page.",
                                                         'url_dict': {key: Home.links_map[key] for key in
                                                                      auth_map[request.session['privilege']]},
                                                         'username': request.session['user']
                                                         })
        if 'Yes' in request.POST:
            for model in {User, Course, Ta, Section, Enroll, CourseAssignment}:
                for obj in model.objects.all():
                    if obj != User.objects.filter(privilege_level='ADMIN'):
                        obj.delete()
            return render(request, 'main/message.html', {'message': 'System Reset'})
        else:
            return redirect('/main/login.html')
