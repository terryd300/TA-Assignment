from django.test import TestCase
from Sprint2.models import *
from Sprint2.forms import *


class TestLogin(TestCase):

    def setUp(self):
        self.user = User(user_name="JDoe", password="qwerty", privilege_level="TA")
        self.user.save()

    def test_userdoesnotexist(self):
        form = LoginForm({'username': 'APook', 'password': 'qwerty'})
        self.assertFalse(form.is_valid(), msg="Validated non-existent user.")

    def test_wrongpassword(self):
        form = LoginForm({'username': 'JDoe', 'password': '12345'})
        self.assertFalse(form.is_valid(), msg="Validated wrong password.")

    def test_bad_username(self):
        form = LoginForm({'username': 1, 'password': 'qwerty'})
        self.assertFalse(form.is_valid(), msg="Validated non-string username.")
        form = LoginForm({'username': 1.0, 'password': 'qwerty'})
        self.assertFalse(form.is_valid(), msg="Validated non-string username.")
        form = LoginForm({'username': True, 'password': 'qwerty'})
        self.assertFalse(form.is_valid(), msg="Validated non-string username.")
        form = LoginForm({'username': None, 'password': 'qwerty'})
        self.assertFalse(form.is_valid(), msg="Validated null username.")
        form = LoginForm({'username': "", 'password': 'qwerty'})
        self.assertFalse(form.is_valid(), msg="Validated empty username.")

    def test_bad_password(self):
        form = LoginForm({'username': 'JDoe', 'password': 1})
        self.assertFalse(form.is_valid(), msg="Validated non-string password.")
        form = LoginForm({'username': 'JDoe', 'password': 1.0})
        self.assertFalse(form.is_valid(), msg="Validated non-string password.")
        form = LoginForm({'username': 'JDoe', 'password': True})
        self.assertFalse(form.is_valid(), msg="Validated non-string password.")
        form = LoginForm({'username': 'JDoe', 'password': None})
        self.assertFalse(form.is_valid(), msg="Validated null password.")
        form = LoginForm({'username': 'JDoe', 'password': ""})
        self.assertFalse(form.is_valid(), msg="Validated empty password.")

    def test_successful_login(self):
        form = LoginForm({'username': 'JDoe', 'password': 'qwerty'})
        self.assertTrue(form.is_valid(), msg="Failed to validate correct username and password.")


class TestChangePassword(TestCase):

    def setUp(self):
        self.user = User(user_name="JDoe", password="qwerty", privilege_level="TA")
        self.user.save()

    def test_not_matching(self):
        form = ChangePasswordForm({'user_name': 'JDoe', 'password': 'qwerty', 'password_repeat': 'asdfgh'},
                                  instance=self.user)
        self.assertFalse(form.is_valid(), msg="Validated non matching passwords.")

    def test_bad_format(self):
        form = ChangePasswordForm({'user_name': 'JDoe', 'password': 'qwerty', 'password_repeat': 'qwerty'},
                                  instance=self.user)
        self.assertFalse(form.is_valid(), msg="Validated non too-short password.")

        form = ChangePasswordForm({'user_name': 'JDoe', 'password': 'qwertyui', 'password_repeat': 'qwertyui'},
                                  instance=self.user)
        self.assertFalse(form.is_valid(), msg="Validated password with no numbers.")

        form = ChangePasswordForm({'user_name': 'JDoe', 'password': '12345678', 'password_repeat': '12345678'},
                                  instance=self.user)
        self.assertFalse(form.is_valid(), msg="Validated password with no letters.")

    def test_no_user_name(self):
        form = ChangePasswordForm({'password': 'qwertyu2', 'password_repeat': 'qwertyu2'}, instance=self.user)
        self.assertFalse(form.is_valid(), msg="Validated password change with no associated user name.")

    def test_no_password(self):
        form = ChangePasswordForm({'user_name': 'JDoe', 'password_repeat': 'qwertyu2'}, instance=self.user)
        self.assertFalse(form.is_valid(), msg="Validated password change with no password.")

    def test_no_password_repeat(self):
        form = ChangePasswordForm({'user_name': 'JDoe', 'password': 'qwertyu2'}, instance=self.user)
        self.assertFalse(form.is_valid(), msg="Validated password change with no password repeat.")

    def test_bad_password(self):
        form = ChangePasswordForm({'user_name': 'JDoe', 'password': 1, 'password_repeat': 1}, instance=self.user)
        self.assertFalse(form.is_valid(), msg="Validated non-string password.")
        form = ChangePasswordForm({'user_name': 'JDoe', 'password': 1.0, 'password_repeat': 1.0}, instance=self.user)
        self.assertFalse(form.is_valid(), msg="Validated non-string password.")
        form = ChangePasswordForm({'user_name': 'JDoe', 'password': True, 'password_repeat': True}, instance=self.user)
        self.assertFalse(form.is_valid(), msg="Validated non-string password.")
        form = ChangePasswordForm({'user_name': 'JDoe', 'password': None, 'password_repeat': None}, instance=self.user)
        self.assertFalse(form.is_valid(), msg="Validated null password.")
        form = ChangePasswordForm({'user_name': 'JDoe', 'password': "", 'password_repeat': ""}, instance=self.user)
        self.assertFalse(form.is_valid(), msg="Validated empty password.")

    def test_no_instance(self):
        form = ChangePasswordForm({'user_name': 'JDoe', 'password': 'qwertyu2', 'password_repeat': 'qwertyu2'})
        self.assertFalse(form.is_valid(), msg="Validated form with no provided instance")

    def test_successful_change(self):
        form = ChangePasswordForm({'user_name': 'JDoe', 'password': 'qwertyu2', 'password_repeat': 'qwertyu2'},
                                  instance=self.user)
        self.assertTrue(form.is_valid(), msg="Failed to validate valid password")
        form.save()
        user_x = User.objects.get(user_name="JDoe")
        self.assertEqual(user_x.password, 'qwertyu2')


class TestCreateUser(TestCase):

    def test_create_admin(self):
        form = CreateUserForm({'user_name': "APook", 'password': "qwerty", 'privilege_level': 'ADMIN'})
        self.assertFalse(form.is_valid(), msg="Should not validate new admin account.")

    def test_duplicate_user(self):
        user = User(user_name="JDoe", password="qwerty", privilege_level="TA")
        user.save()
        form = CreateUserForm({'user_name': "JDoe", 'password': "qwerty", 'privilege_level': 'TA'})
        self.assertFalse(form.is_valid(), msg="Validated duplicate user.")

    def test_privilege_level_not_in_choices(self):
        form = CreateUserForm({'user_name': "APook", 'password': "qwerty", 'privilege_level': 'UNDERGRAD'})
        self.assertFalse(form.is_valid(), msg="Validated user with bad privilege level.")

    def test_no_user_name(self):
        form = CreateUserForm({'password': "qwerty", 'privilege_level': "TA"})
        self.assertFalse(form.is_valid(), msg="Validated form missing user name.")

    def test_no_password(self):
        form = CreateUserForm({'user_name': "APook", 'privilege_level': "TA"})
        self.assertFalse(form.is_valid(), msg="Validated form missing password.")

    def test_no_privilege_level(self):
        form = CreateUserForm({'user_name': "APook", 'password': "qwerty"})
        self.assertFalse(form.is_valid(), msg="Validated form missing privilege level.")

    def test_bad_user_name(self):
        form = CreateUserForm({'user_name': None, 'password': "qwerty", 'privilege_level': 'TA'})
        self.assertFalse(form.is_valid(), msg="Validated null user name.")
        form = CreateUserForm({'user_name': "", 'password': "qwerty", 'privilege_level': 'TA'})
        self.assertFalse(form.is_valid(), msg="Validated empty user name.")

    def test_bad_password(self):
        form = CreateUserForm({'user_name': "APook", 'password': None, 'privilege_level': 'TA'})
        self.assertFalse(form.is_valid(), msg="Validated null password.")
        form = CreateUserForm({'user_name': "APook", 'password': "", 'privilege_level': 'TA'})
        self.assertFalse(form.is_valid(), msg="Validated empty password.")

    def test_bad_privilege_level(self):
        form = CreateUserForm({'user_name': "APook", 'password': "qwerty", 'privilege_level': None})
        self.assertFalse(form.is_valid(), msg="Validated null privilege level.")
        form = CreateUserForm({'user_name': "APook", 'password': "qwerty", 'privilege_level': ""})
        self.assertFalse(form.is_valid(), msg="Validated empty privilege level.")

    def test_success(self):
        form = CreateUserForm({'user_name': "APook", 'password': "qwerty", 'privilege_level': "TA"})
        self.assertTrue(form.is_valid(), msg="Failed to validate valid user.")
        form.save()
        user_x = User.objects.get(user_name='APook')
        self.assertEqual(user_x.privilege_level, "TA")


class TestCreateCourse(TestCase):

    def test_duplicate_course(self):
        course = Course(name="CS361", lecture_num='401')
        course.save()
        form = CreateCourseForm({'name': "CS361", 'lecture_num': '401'})
        self.assertFalse(form.is_valid(), msg="Validated duplicate course.")

    def test_lecture_num_format(self):
        form = CreateCourseForm({'name': "CS361", 'lecture_num': '40n'})
        self.assertFalse(form.is_valid(), msg="Validated non-numeric lecture number.")
        form = CreateCourseForm({'name': "CS361", 'lecture_num': '40'})
        self.assertFalse(form.is_valid(), msg="Validated too-short lecture number.")
        form = CreateCourseForm({'name': "CS361", 'lecture_num': '4001'})
        self.assertFalse(form.is_valid(), msg="Validated too-long lecture number.")

    def test_no_name(self):
        form = CreateCourseForm({'lecture_num': '401'})
        self.assertFalse(form.is_valid(), msg="Validated course missing name.")

    def test_no_lecture_num(self):
        form = CreateCourseForm({'name': 'CS361'})
        self.assertFalse(form.is_valid(), msg="Validated course missing lecture number.")

    def test_bad_name(self):
        form = CreateCourseForm({'name': None, 'lecture_num': '401'})
        self.assertFalse(form.is_valid(), msg="Validated null name.")
        form = CreateCourseForm({'name': "", 'lecture_num': '401'})
        self.assertFalse(form.is_valid(), msg="Validated empty name.")

    def test_bad_lecture_num(self):
        form = CreateCourseForm({'name': "CS361", 'lecture_num': 'None'})
        self.assertFalse(form.is_valid(), msg="Validated null lecture number.")
        form = CreateCourseForm({'name': "CS361", 'lecture_num': ""})
        self.assertFalse(form.is_valid(), msg="Validated empty lecture number.")

    def test_success(self):
        form = CreateCourseForm({'name': "CS361", 'lecture_num': '401'})
        self.assertTrue(form.is_valid(), msg="Failed to validate valid course.")
        form.save()
        course_x = Course.objects.get(name="CS361", lecture_num='401')

        form = CreateCourseForm({'name': "CS557", 'description': 'Databases', 'lecture_num': '401'})
        self.assertTrue(form.is_valid(), msg="Failed to validate valid course.")
        form.save()
        course_y = Course.objects.get(name="CS361", lecture_num='401')


