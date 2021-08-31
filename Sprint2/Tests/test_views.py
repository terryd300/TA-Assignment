from django.test import TestCase, Client
from Sprint2.models import *
from datetime import time


class TestLogin(TestCase):

    def setUp(self):
        self.user = User(user_name="JDoe", password="qwerty", privilege_level="TA")
        self.user.save()

    def test_get_login_page(self):
        response = self.client.get('/main/login.html')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/login.html')

    def test_get_already_logged_in(self):
        session = self.client.session
        session['user'] = "Admin"
        session['privilege'] = "ADMIN"
        session.save()
        response = self.client.get('/main/login.html')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/main/index.html')

    def test_post_already_logged_in(self):
        session = self.client.session
        session['user'] = "Admin"
        session['privilege'] = "ADMIN"
        session.save()
        response = self.client.post('/main/login.html', {})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/main/index.html')

    def test_post_success(self):
        response = self.client.post('/main/login.html', {'username': "JDoe", 'password': "qwerty"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/main/index.html')

    def test_post_no_such_user(self):
        response = self.client.post('/main/login.html', {'username': "APook", 'password': "qwerty"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/login.html')

    def test_post_wrong_password(self):
        response = self.client.post('/main/login.html', {'username': "JDoe", 'password': "12345"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/login.html')


class TestLogout(TestCase):

    def test_get_already_logged_in(self):
        session = self.client.session
        session['user'] = "Admin"
        session.save()
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/main/login.html')
        self.assertFalse('user' in self.client.session.keys())

    def test_not_logged_in(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/main/login.html')
        self.assertFalse('user' in self.client.session.keys())

    def test_post(self):
        response = self.client.post('/logout', {})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/logout', target_status_code=302)


class TestUsers(TestCase):

    def setUp(self):
        self.user = User(user_name="JDoe", password="qwerty", privilege_level="TA")
        self.user.save()

    def test_get_users_page(self):
        session = self.client.session
        session['user'] = "Admin"
        session['privilege'] = "ADMIN"
        session.save()
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/users.html')

    def test_invalid_access_TA(self):
        session = self.client.session
        session['user'] = "JDoe"
        session['privilege'] = "TA"
        session.save()
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/message.html')

    def test_invalid_access_INSTRUCT(self):
        session = self.client.session
        session['user'] = "JDoe"
        session['privilege'] = "INSTRUCTOR"
        session.save()
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/message.html')

    def test_not_logged_in(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/main/login.html')
        self.assertFalse('user' in self.client.session.keys())


class TestClasses(TestCase):

    def setUp(self):
        self.user = User(user_name="JDoe", password="qwerty", privilege_level="TA")
        self.user.save()

    def test_get_classes_page_admin(self):
        session = self.client.session
        session['user'] = "Admin"
        session['privilege'] = "ADMIN"
        session.save()
        response = self.client.get('/courses')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/courses.html')

    def test_get_classes_page_instruct(self):
        session = self.client.session
        session['user'] = "JRock"
        session['privilege'] = "INSTRUCTOR"
        session.save()
        response = self.client.get('/courses')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/courses.html')

    def test_get_classes_page_TA(self):
        session = self.client.session
        session['user'] = "JDoe"
        session['privilege'] = "TA"
        session.save()
        response = self.client.get('/courses')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/courses.html')

    def test_not_logged_in(self):
        response = self.client.get('/courses')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/main/login.html')
        self.assertFalse('user' in self.client.session.keys())


class TestSections(TestCase):

    def setUp(self):
        self.user = User(user_name="JDoe", password="qwerty", privilege_level="TA")
        self.user.save()

    def test_get_sections_page_admin(self):
        session = self.client.session
        session['user'] = "Admin"
        session['privilege'] = "ADMIN"
        session.save()
        response = self.client.get('/sections')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/sections.html')

    def test_get_sections_page_instruct(self):
        session = self.client.session
        session['user'] = "JRock"
        session['privilege'] = "INSTRUCTOR"
        session.save()
        response = self.client.get('/sections')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/sections.html')

    def test_get_sections_page_TA(self):
        session = self.client.session
        session['user'] = "JDoe"
        session['privilege'] = "TA"
        session.save()
        response = self.client.get('/sections')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/sections.html')

    def test_not_logged_in(self):
        response = self.client.get('/sections')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/main/login.html')
        self.assertFalse('user' in self.client.session.keys())


class TestAssignTA(TestCase):

    def setUp(self):
        self.user = User(user_name="JDoe", password="qwerty", privilege_level="TA")
        self.user.save()

    def test_get_assignta_page_admin(self):
        session = self.client.session
        session['user'] = "Admin"
        session['privilege'] = "ADMIN"
        session.save()
        response = self.client.get('/tatocourse')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/FormInput.html')

    def test_post_success_admin(self):
        session = self.client.session
        session['user'] = "Admin"
        session['privilege'] = "ADMIN"
        session.save()
        response = self.client.post('/tatocourse', {'section': "CS999, 401", 'ta': "APook"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/FormInput.html')

    def test_post_failure_admin(self):
        session = self.client.session
        session['user'] = "Admin"
        session['privilege'] = "ADMIN"
        session.save()
        response = self.client.post('/tatocourse', {'section': "CD999, 401", 'ta': "APook"})
        response = self.client.post('/tatocourse', {'section': "CD999, 401", 'ta': "APook"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/FormInput.html')

    def test_get_assignta_page_instruct(self):
        session = self.client.session
        session['user'] = "JRock"
        session['privilege'] = "INSTRUCTOR"
        session.save()
        response = self.client.get('/tatocourse')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/message.html')

    def test_post_success_instruct(self):
        session = self.client.session
        session['user'] = "JRock"
        session['privilege'] = "INSTRUCTOR"
        session.save()
        response = self.client.post('/tatocourse', {'choice': "CS361, 401"})
        response = self.client.post('/tatocourse', {'section': "CS361, 801", 'ta': 'APook'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/message.html')

    def test_invalid_access_TA(self):
        session = self.client.session
        session['user'] = "APook"
        session['privilege'] = "TA"
        session.save()
        response = self.client.get('/tatocourse')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/message.html')

    def test_not_logged_in(self):
        response = self.client.get('/sections')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/main/login.html')
        self.assertFalse('user' in self.client.session.keys())


class TestDeleteEnroll(TestCase):

    def setUp(self):
        self.user = User(user_name="JDoe", password="qwerty", privilege_level="TA")
        self.user.save()

    def test_invalid_access_admin(self):
        session = self.client.session
        session['user'] = "Admin"
        session['privilege'] = "ADMIN"
        session.save()
        response = self.client.get('/taDelSchedule')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/message.html')

    def test_invalid_access_instruct(self):
        session = self.client.session
        session['user'] = "JRock"
        session['privilege'] = "INSTRUCTOR"
        session.save()
        response = self.client.get('/taDelSchedule')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/message.html')

    def test_not_logged_in(self):
        response = self.client.get('/taDelSchedule')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/main/login.html')
        self.assertFalse('user' in self.client.session.keys())

    def test_get_deleteenroll_page_TA(self):
        session = self.client.session
        session['user'] = "APook"
        session['privilege'] = "TA"
        session.save()
        Ta.save(self)
        response = self.client.get('/taDelSchedule')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/FormInput.html')


class TestViewQual(TestCase):

    def setUp(self):
        self.user = User(user_name="JDoe", password="qwerty", privilege_level="TA")
        self.user.save()

    def test_not_logged_in(self):
        response = self.client.get('/sections')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/main/login.html')
        self.assertFalse('user' in self.client.session.keys())

    def test_get_viewqual_page_admin(self):
        session = self.client.session
        session['user'] = "Admin"
        session['privilege'] = "ADMIN"
        session.save()
        response = self.client.get('/viewTaQual')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/viewTaQual.html')

    def test_invalid_access_instruct(self):
        session = self.client.session
        session['user'] = "JRock"
        session['privilege'] = "INSTRUCTOR"
        session.save()
        response = self.client.get('/viewTaQual')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/viewTaQual.html')

    def test_invalid_access_TA(self):
        session = self.client.session
        session['user'] = "APook"
        session['privilege'] = "TA"
        session.save()
        response = self.client.get('/viewTaQual')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/viewTaQual.html')


class TestViewConflicts(TestCase):

    def setUp(self):
        self.user = User(user_name="Admin", password="qwerty", privilege_level="ADMIN")
        self.user.save()
        self.course = Course(name="Intro To Something", lecture_num='101')
        self.course.save()
        self.ta = Ta(user_name="JoeShmoe", password="qwerty", privilege_level="TA")
        self.ta.save()
        self.section1 = Section(course=self.course, number='801', type="LEC", days='T', start_time=time(11,0,0,0), end_time=time(13,0,0,0), ta=self.ta)
        self.section1.save()
        self.section2 = Section(course=self.course, number='802', type="DIS", days='T', start_time=time(10,0,0,0), end_time=time(11,30,0,0))
        self.section2.save()

    def test_no_login(self):
        response = self.client.get('/viewconflicts')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/main/login.html')

    def test_wrong_privelege(self):
        session = self.client.session
        session['user'] = "APook"
        session['privilege'] = "TA"
        session.save()
        response = self.client.get('/viewconflicts')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/main/message.html')

    def test_no_conflicts(self):
        session = self.client.session
        session['user'] = "Admin"
        session['privilege'] = "ADMIN"
        session.save()
        response = self.client.get('/viewconflicts')
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/main/message.html')

    def test_conflicts(self):
        session = self.client.session
        session['user'] = "Admin"
        session['privilege'] = "ADMIN"
        session.save()
        self.user = User(user_name="Admin", password="qwerty", privilege_level="ADMIN")
        self.user.save()
        self.enrl = Enroll(ta= self.ta, section=self.section2)
        self.enrl.save()
        response = self.client.get('/viewconflicts')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '/main/conflicts.html')
        self.assertEqual(response.equals['conflicts'](0), self.section1)
        self.assertEqual(response.equals['conflicts'](1), self.section2)