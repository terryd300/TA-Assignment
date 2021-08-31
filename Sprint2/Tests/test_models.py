from django.core.exceptions import FieldError, ValidationError, ObjectDoesNotExist
from django.test import TestCase, TransactionTestCase
from django.db import IntegrityError
from Sprint2.models import *
from datetime import time


class TestUser(TransactionTestCase):

    def setUp(self):
        self.admin_user = User(user_name="Admin", password="A1234567", privilege_level="ADMIN")
        self.admin_user.save()
        self.instruct_user = User(user_name="JSmith", password="A1234567", privilege_level="INSTRUCTOR",
                                  first_name="John", last_name="Smith", email="jsmith@uwm.edu", phone="414-123-4567")
        self.instruct_user.save()
        self.ta_user = Ta(user_name="JDoe", password="A1234567", privilege_level="TA")
        self.ta_user.save()

    def test_username_notblank(self):
        new_user = User(password="A1234567", privilege_level="INSTRUCTOR")
        with self.assertRaises(IntegrityError, msg="User name should not be blank."):
            new_user.save()
        new_user.user_name = ""
        with self.assertRaises(IntegrityError, msg="User name should not be blank."):
            new_user.save()

    def test_username_uniqueness(self):
        new_user = User(user_name="JSmith", password="A1234567", privilege_level="INSTRUCTOR")
        with self.assertRaises(IntegrityError, msg="Cannot have duplicate user names"):
            new_user.save(force_insert=True)

    def test_username_typeerrors(self):
        new_user = User(user_name=1, password="A1234567", privilege_level="INSTRUCTOR")
        with self.assertRaises(TypeError, msg="User name must be string"):
            new_user.save()
        new_user.user_name = 1.0
        with self.assertRaises(TypeError, msg="User name must be string"):
            new_user.save()
        new_user.user_name = True
        with self.assertRaises(TypeError, msg="User name must be string"):
            new_user.save()
        new_user.user_name = None
        with self.assertRaises(TypeError, msg="User name should not be null."):
            new_user.save()

    # Since we will eventually be hashing passwords, it might not make sense to enforce
    # constraints on password contents here.

    def test_password_errors(self):
        new_user = User(user_name="APook", privilege_level="INSTRUCTOR")
        with self.assertRaises(IntegrityError, msg="Password should not be blank."):
            new_user.save()
        new_user.password = ""
        with self.assertRaises(IntegrityError, msg="Password should not be blank."):
            new_user.save()

    def test_password_typeerrors(self):
        new_user = User(user_name="APook", password=1, privilege_level="INSTRUCTOR")
        with self.assertRaises(TypeError, msg="Password must be string"):
            new_user.save()
        new_user.password = 1.0
        with self.assertRaises(TypeError, msg="Password must be string"):
            new_user.save()
        new_user.password = True
        with self.assertRaises(TypeError, msg="Password must be string"):
            new_user.save()
        new_user.password = None
        with self.assertRaises(TypeError, msg="Password should not be null."):
            new_user.save()

    def test_privilegelevel_immutable(self):
        self.admin_user.privilege_level = "INSTRUCTOR"
        with self.assertRaises(FieldError, msg="Account privileges should not be changed."):
            self.admin_user.save()

    def test_privilegelevel_notblank(self):
        new_user = User(user_name="APook", password="A1234567")
        with self.assertRaises(IntegrityError, msg="Privilege level should not be blank."):
            new_user.save()
        new_user.privilege_level = ""
        with self.assertRaises(IntegrityError, msg="Privilege level should not be blank."):
            new_user.save()

    def test_privilegelevel_admin(self):
        new_user = User(user_name="APook", password="A1234567", privilege_level="ADMIN")
        with self.assertRaises(FieldError, msg="Only admin account should have admin privileges."):
            new_user.save()

    def test_privilegelevel_invalid(self):
        new_user = User(user_name="APook", password="A1234567", privilege_level="qwerty")
        with self.assertRaises(FieldError, msg="Allowed invalid privilege level."):
            new_user.save()

    def test_privilegelevel_typeerrors(self):
        new_user = User(user_name="APook", password="A1234567", privilege_level=1)
        with self.assertRaises(TypeError, msg="Privilege level must be string"):
            new_user.save()
        new_user.privilege_level = 1.0
        with self.assertRaises(TypeError, msg="Privilege level must be string"):
            new_user.save()
        new_user.privilege_level = True
        with self.assertRaises(TypeError, msg="Privilege level must be string"):
            new_user.save()
        new_user.privilege_level = None
        with self.assertRaises(TypeError, msg="Privilege level must not be null"):
            new_user.save()

    def test_firstname_typeerrors(self):
        self.admin_user.first_name = 1
        with self.assertRaises(TypeError, msg="First name must be string"):
            self.admin_user.save()
        self.admin_user.first_name = 1.0
        with self.assertRaises(TypeError, msg="First name must be string"):
            self.admin_user.save()
        self.admin_user.first_name = True
        with self.assertRaises(TypeError, msg="First name must be string"):
            self.admin_user.save()
        self.admin_user.first_name = None
        with self.assertRaises(TypeError, msg="First name must not be null"):
            self.admin_user.save()

    def test_lastname_typeerrors(self):
        self.admin_user.last_name = 1
        with self.assertRaises(TypeError, msg="Last name must be string"):
            self.admin_user.save()
        self.admin_user.last_name = 1.0
        with self.assertRaises(TypeError, msg="Last name must be string"):
            self.admin_user.save()
        self.admin_user.last_name = True
        with self.assertRaises(TypeError, msg="Last name must be string"):
            self.admin_user.save()
        self.admin_user.last_name = None
        with self.assertRaises(TypeError, msg="Last name must not be null"):
            self.admin_user.save()

    def test_email_typeerrors(self):
        self.admin_user.email = 1
        with self.assertRaises(TypeError, msg="Email must be string"):
            self.admin_user.save()
        self.admin_user.email = 1.0
        with self.assertRaises(TypeError, msg="Email must be string"):
            self.admin_user.save()
        self.admin_user.email = True
        with self.assertRaises(TypeError, msg="Email must be string"):
            self.admin_user.save()
        self.admin_user.email = None
        with self.assertRaises(TypeError, msg="Email must not be null"):
            self.admin_user.save()

    def test_email_validation(self):
        self.admin_user.email = "qwerty12345"
        with self.assertRaises(ValidationError, msg="Should not accept invalid email address"):
            self.admin_user.save()

    def test_phone_typeerrors(self):
        self.admin_user.phone = 1
        with self.assertRaises(TypeError, msg="Phone number must be string"):
            self.admin_user.save()
        self.admin_user.phone = 1.0
        with self.assertRaises(TypeError, msg="Phone number must be string"):
            self.admin_user.save()
        self.admin_user.phone = True
        with self.assertRaises(TypeError, msg="Phone number must be string"):
            self.admin_user.save()
        self.admin_user.phone = None
        with self.assertRaises(TypeError, msg="Phone number must not be null"):
            self.admin_user.save()

    def test_address_typeerrors(self):
        self.admin_user.address = 1
        with self.assertRaises(TypeError, msg="Address must be string"):
            self.admin_user.save()
        self.admin_user.address = 1.0
        with self.assertRaises(TypeError, msg="Address must be string"):
            self.admin_user.save()
        self.admin_user.address = True
        with self.assertRaises(TypeError, msg="Address must be string"):
            self.admin_user.save()
        self.admin_user.address = None
        with self.assertRaises(TypeError, msg="Address must not be null"):
            self.admin_user.save()

        # It's possible to enforce phone number format like email addresses, but django doesn't have the
        # capability by default.  There is code for it on github.

    def test_retrieve_user(self):
        user_x = User.objects.get(user_name="Admin")
        self.assertEqual(user_x.password, "A1234567", msg="Got wrong password.")
        self.assertEqual(user_x.privilege_level, "ADMIN", msg="Got wrong privilege level.")
        self.assertEqual(user_x.first_name, "", msg="Default first name should be blank.")
        self.assertEqual(user_x.last_name, "", msg="Default last name should be blank.")
        self.assertEqual(user_x.email, "", msg="Default email address should be blank.")
        self.assertEqual(user_x.phone, "", msg="Default phone number should be blank.")

        user_x = User.objects.get(user_name="JSmith")
        self.assertEqual(user_x.password, "A1234567", msg="Got wrong password.")
        self.assertEqual(user_x.privilege_level, "INSTRUCTOR", msg="Got wrong privilege level.")
        self.assertEqual(user_x.first_name, "John", msg="Got wrong first name")
        self.assertEqual(user_x.last_name, "Smith", msg="Got wrong last name.")
        self.assertEqual(user_x.email, "jsmith@uwm.edu", msg="Got wrong email address.")
        self.assertEqual(user_x.phone, "414-123-4567", msg="Got wrong phone number.")


class TestTA(TestCase):

    def setUp(self):

        self.cs361 = Course(name="CS361",lecture_num="401")
        self.cs361.save()
        self.cs458 = Course(name="CS458",lecture_num="401")
        self.cs458.save()
        self.cs557 = Course(name="CS557",lecture_num="401")
        self.cs557.save()
        self.ta_user = Ta(user_name="JDoe", password="A1234567", privilege_level="TA", first_name="John",
                          last_name="Doe", email="jdoe@uwm.edu", phone="414-123-4567")
        self.ta_user.save()

    def test_pref1_assignmenterrors(self):
        cs251 = Course(name="CS251",lecture_num="401")
        self.ta_user.pref_1 = cs251
        with self.assertRaises(ObjectDoesNotExist, msg="Non-existant class saved as pref_1"):
            self.ta_user.save()

    def test_pref2_assignmenterrors(self):
        cs251 = Course(name="CS251",lecture_num="401")
        self.ta_user.pref_2 = cs251
        with self.assertRaises(ObjectDoesNotExist, msg="Non-existant class saved as pref_2"):
            self.ta_user.save()

    def test_pref3_assignmenterrors(self):
        cs251 = Course(name="CS251",lecture_num="401")
        self.ta_user.pref_3 = cs251
        with self.assertRaises(ObjectDoesNotExist, msg="Non-existant class saved as pref_3"):
            self.ta_user.save()

    def test_qualifications_typeerrors(self):
        self.ta_user.qualifications = 1
        with self.assertRaises(TypeError, msg="TA qualifications must be string"):
            self.ta_user.save()
        self.ta_user.qualifications = 1.0
        with self.assertRaises(TypeError, msg="TA qualifications must be string"):
            self.ta_user.save()
        self.ta_user.qualifications = True
        with self.assertRaises(TypeError, msg="TA qualifications must be string"):
            self.ta_user.save()
        self.ta_user.qualifications = None
        with self.assertRaises(TypeError, msg="TA qualifications must not be null"):
            self.ta_user.save()

    def test_wrong_user_type(self):
        self.ta_user.privilege_level = "INSTRUCTOR"
        with self.assertRaises(FieldError, msg="TA cannot have instructor privileges."):
            self.ta_user.save()

    def test_retrieve_ta(self):
        ta_x = Ta.objects.get(user_name="JDoe")
        self.assertEqual(ta_x.password, "A1234567", msg="Got wrong password.")
        self.assertEqual(ta_x.privilege_level, "TA", msg="Got wrong privilege level.")
        self.assertEqual(ta_x.first_name, "John", msg="Got wrong first name")
        self.assertEqual(ta_x.last_name, "Doe", msg="Got wrong last name.")
        self.assertEqual(ta_x.email, "jdoe@uwm.edu", msg="Got wrong email address.")
        self.assertEqual(ta_x.phone, "414-123-4567", msg="Got wrong phone number.")
        self.assertEqual(ta_x.pref_1, None, msg="Default TA preference 1 should be blank.")
        self.assertEqual(ta_x.pref_2, None, msg="Default TA preference 2 should be blank.")
        self.assertEqual(ta_x.pref_3, None, msg="Default TA preference 3 should be blank.")
        self.assertEqual(ta_x.qualifications, "", msg="Default TA qualifications should be blank.")

        ta_x.pref_1 = self.cs361
        ta_x.pref_2 = self.cs458
        ta_x.pref_3 = self.cs557
        ta_x.qualifications = "BS in Computer Science from UWM"
        ta_x.save()
        ta_x = Ta.objects.get(user_name="JDoe")
        self.assertEqual(ta_x.pref_1, self.cs361, msg="Got wrong TA preference 1.")
        self.assertEqual(ta_x.pref_2, self.cs458, msg="Got wrong TA preference 2.")
        self.assertEqual(ta_x.pref_3, self.cs557, msg="Got wrong TA preference 3.")
        self.assertEqual(ta_x.qualifications, "BS in Computer Science from UWM")


class TestCourse(TestCase):

    def setUp(self):
        instruct_user = User(user_name="JSmith", password="A1234567", privilege_level="INSTRUCTOR")
        instruct_user.save()
        self.my_course = Course(name="CS361", lecture_num="401", description="Introduction to Software Engineering",
                                instructor=instruct_user)
        self.my_course.save()

    def test_name_notblank(self):
        new_course = Course(lecture_num="401")
        with self.assertRaises(IntegrityError, msg="Name must not be blank"):
            new_course.save()
        new_course.name = ""
        with self.assertRaises(IntegrityError, msg="Name must not be blank"):
            new_course.save()

    def test_name_typeerrors(self):
        self.my_course.name = 1
        with self.assertRaises(TypeError, msg="Name must be string"):
            self.my_course.save()
        self.my_course.name = 1.0
        with self.assertRaises(TypeError, msg="Name must be string"):
            self.my_course.save()
        self.my_course.name = True
        with self.assertRaises(TypeError, msg="Name must be string"):
            self.my_course.save()
        self.my_course.name = None
        with self.assertRaises(TypeError, msg="Name must not be null"):
            self.my_course.save()

    def test_course_uniqueness(self):
        new_course = Course(name="CS361", lecture_num="401")
        with self.assertRaises(IntegrityError, msg="Course name and lecture number must be unique combination"):
            new_course.save(force_insert=True)

    def test_lecturenum_notblank(self):
        new_course = Course(name="CS361")
        with self.assertRaises(IntegrityError, msg="Lecture number must not be blank"):
            new_course.save()
        new_course.lecture_num = ""
        with self.assertRaises(IntegrityError, msg="Lecture number must not be blank"):
            new_course.save()

    def test_lecturenum_format(self):
        new_course = Course(name="CS361", lecture_num="40")
        with self.assertRaises(FieldError, msg="Lecture number should have length 3."):
            new_course.save()
        new_course.lecture_num = "4011"
        with self.assertRaises(FieldError, msg="Lecture number should have length 3."):
            new_course.save()
        new_course.lecture_num = "abcde"
        with self.assertRaises(FieldError, msg="Lecture number should be numeric characters only."):
            new_course.save()

    def test_lecturenum_typeerrors(self):
        self.my_course.lecture_num = 1
        with self.assertRaises(TypeError, msg="Lecture number must be string"):
            self.my_course.save()
        self.my_course.lecture_num = 1.0
        with self.assertRaises(TypeError, msg="Lecture number must be string"):
            self.my_course.save()
        self.my_course.lecture_num = True
        with self.assertRaises(TypeError, msg="Lecture number must be string"):
            self.my_course.save()
        self.my_course.lecture_num = None
        with self.assertRaises(TypeError, msg="Lecture number must not be null"):
            self.my_course.save()

    def test_description_typeerrors(self):
        self.my_course.description = 1
        with self.assertRaises(TypeError, msg="Course description must be string"):
            self.my_course.save()
        self.my_course.description = 1.0
        with self.assertRaises(TypeError, msg="Course description must be string"):
            self.my_course.save()
        self.my_course.description = True
        with self.assertRaises(TypeError, msg="Course description must be string"):
            self.my_course.save()
        self.my_course.description = None
        with self.assertRaises(TypeError, msg="Course description must not be null"):
            self.my_course.save()

    def test_instructor_assignmenterrors(self):
        ta_user = Ta(user_name="JDoe", password="A1234567", privilege_level="TA")
        ta_user.save()
        self.my_course.instructor = ta_user
        with self.assertRaises(FieldError, msg="TA's should not be assigned as instructors"):
            self.my_course.save()
        self.my_course.instructor = User(user_name="qwerty", password="A1234567", privilege_level="INSTRUCTOR")
        with self.assertRaises(ObjectDoesNotExist, msg="Instructor account not found."):
            self.my_course.save()

    def test_retrieve_course(self):
        my_other_course = Course(name="CS361", lecture_num="402")
        my_other_course.save()

        course_x = Course.objects.get(name="CS361", lecture_num="401")
        self.assertEqual(course_x.instructor.pk, self.my_course.instructor.pk, msg="Got wrong instructor.")
        self.assertEqual(course_x.description, "Introduction to Software Engineering",
                         msg="Got wrong course description")

        course_x = Course.objects.get(name="CS361", lecture_num="402")
        self.assertEqual(course_x.instructor, None, msg="Default instructor should be null.")
        self.assertEqual(course_x.description, "", msg="Default course description should be blank.")


class TestSection(TestCase):

    def setUp(self):
        self.my_course = Course(name="CS361", lecture_num="401")
        self.my_course.save()
        self.my_section = Section(course=self.my_course, number="801", type="LAB", days="T",
                                  start_time=time(12, 0), end_time=time(13, 45))
        self.my_section.save()

    def test_course_notnull(self):
        new_section = Section(number="802", type="LAB", days="T",
                              start_time=time(12, 0), end_time=time(13, 45))
        with self.assertRaises(ObjectDoesNotExist, msg="Course must not be null"):
            new_section.save()
        new_section.course = None
        with self.assertRaises(ObjectDoesNotExist, msg="Course must not be null"):
            new_section.save()

    def test_course_assignmenterrors(self):
        self.my_section.course = Course(name="CS250", lecture_num="401")
        with self.assertRaises(ObjectDoesNotExist, msg="Don't allow non-existent courses."):
            self.my_section.save()

    def test_number_notblank(self):
        new_section = Section(course=self.my_course, type="LAB", days="T",
                              start_time=time(12, 0), end_time=time(13, 45))
        with self.assertRaises(IntegrityError, msg="Section number must not be blank"):
            new_section.save()
        new_section.number = ""
        with self.assertRaises(IntegrityError, msg="Section number must not be blank"):
            new_section.save()

    def test_number_format(self):
        self.my_section.number = "80"
        with self.assertRaises(FieldError, msg="Section number should have length 3."):
            self.my_section.save()
        self.my_section.number = "8011"
        with self.assertRaises(FieldError, msg="Section number should have length 3."):
            self.my_section.save()
        self.my_section.number = "abcde"
        with self.assertRaises(FieldError, msg="Section number should be numeric characters."):
            self.my_section.save()

    def test_section_uniqueness(self):
        new_section = Section(course=self.my_course, number="801", type="LAB", days="T",
                              start_time=time(12, 0), end_time=time(13, 45))
        with self.assertRaises(IntegrityError, msg="No duplicate section numbers for same course."):
            new_section.save(force_insert=True)

    def test_number_typeerrors(self):
        self.my_section.number = 1
        with self.assertRaises(TypeError, msg="Section number must be string"):
            self.my_section.save()
        self.my_section.number = 1.0
        with self.assertRaises(TypeError, msg="Section number must be string"):
            self.my_section.save()
        self.my_section.number = True
        with self.assertRaises(TypeError, msg="Section number must be string"):
            self.my_section.save()
        self.my_section.number = None
        with self.assertRaises(TypeError, msg="Section number must not be null"):
            self.my_section.save()

    def test_type_immutable(self):
        self.my_section.type = "LEC"
        with self.assertRaises(FieldError, msg="Section type must not change."):
            self.my_section.save()

    def test_type_notblank(self):
        new_section = Section(course=self.my_course, number="802", days="T",
                              start_time=time(12, 0), end_time=time(13, 45))
        with self.assertRaises(IntegrityError, msg="Section type must not be blank"):
            new_section.save()
        new_section.type = ""
        with self.assertRaises(IntegrityError, msg="Section type must not be blank"):
            new_section.save()

    def test_type_invalid(self):
        self.my_section.type = "abcde"
        with self.assertRaises(FieldError, msg="Allowed invalid section type"):
            self.my_section.save()

    def test_type_typeerrors(self):
        self.my_section.type = 1
        with self.assertRaises(TypeError, msg="Section type must be string"):
            self.my_section.save()
        self.my_section.type = 1.0
        with self.assertRaises(TypeError, msg="Section type must be string"):
            self.my_section.save()
        self.my_section.type = True
        with self.assertRaises(TypeError, msg="Section type must be string"):
            self.my_section.save()
        self.my_section.type = None
        with self.assertRaises(TypeError, msg="Section type must not be null"):
            self.my_section.save()

    def test_days_notblank(self):
        new_section = Section(course=self.my_course, number="802", type="LAB",
                              start_time=time(12, 0), end_time=time(13, 45))
        with self.assertRaises(IntegrityError, msg="Days must not be blank"):
            new_section.save()
        new_section.days = ""
        with self.assertRaises(IntegrityError, msg="Days must not be blank"):
            new_section.save()

    def test_days_format(self):
        self.my_section.days = "E"
        with self.assertRaises(FieldError, msg="Days should only be MTWRF"):
            self.my_section.save()
        self.my_section.days = "MM"
        with self.assertRaises(FieldError, msg="No duplicate days in a week."):
            self.my_section.save()

    def test_days_typeerrors(self):
        self.my_section.days = 1
        with self.assertRaises(TypeError, msg="Days must be string"):
            self.my_section.save()
        self.my_section.days = 1.0
        with self.assertRaises(TypeError, msg="Days must be string"):
            self.my_section.save()
        self.my_section.days = True
        with self.assertRaises(TypeError, msg="Days must be string"):
            self.my_section.save()
        self.my_section.days = None
        with self.assertRaises(TypeError, msg="Days must not be null"):
            self.my_section.save()

    def test_starttime_notnull(self):
        new_section = Section(course=self.my_course, number="802", type="LAB", days="T",
                              end_time=time(13, 45))
        with self.assertRaises(TypeError, msg="Start time must not be blank"):
            new_section.save()

    def test_starttime_typeerrors(self):
        self.my_section.start_time = 1
        with self.assertRaises(TypeError, msg="Start time must be datetime.time"):
            self.my_section.save()
        self.my_section.start_time = 1.0
        with self.assertRaises(TypeError, msg="Start time must be datetime.time"):
            self.my_section.save()
        self.my_section.start_time = True
        with self.assertRaises(TypeError, msg="Start time must be datetime.time"):
            self.my_section.save()
        self.my_section.start_time = "qwerty"
        with self.assertRaises(TypeError, msg="Start time must be datetime.time"):
            self.my_section.save()
        self.my_section.start_time = None
        with self.assertRaises(TypeError, msg="Start time must not be null"):
            self.my_section.save()

    def test_endtime_notnull(self):
        new_section = Section(course=self.my_course, number="802", type="LAB", days="T",
                              start_time=time(12, 0))
        with self.assertRaises(TypeError, msg="End time must not be blank"):
            new_section.save()

    def test_endtime_consistency(self):
        self.my_section.end_time = time(11, 0)
        with self.assertRaises(FieldError, msg="End time must not be before start time."):
            self.my_section.save()

    def test_endtime_typeerrors(self):
        self.my_section.end_time = 1
        with self.assertRaises(TypeError, msg="End time must be datetime.time"):
            self.my_section.save()
        self.my_section.end_time = 1.0
        with self.assertRaises(TypeError, msg="End time must be datetime.time"):
            self.my_section.save()
        self.my_section.end_time = True
        with self.assertRaises(TypeError, msg="End time must be datetime.time"):
            self.my_section.save()
        self.my_section.end_time = "qwerty"
        with self.assertRaises(TypeError, msg="End time must be datetime.time"):
            self.my_section.save()
        self.my_section.end_time = None
        with self.assertRaises(TypeError, msg="End time must not be null"):
            self.my_section.save()

    def test_ta_assignmenterrors(self):
        self.my_section.ta = Ta(user_name="qwertyuiop", password="A1234567", privilege_level="TA")
        with self.assertRaises(ObjectDoesNotExist, msg="TA not found"):
            self.my_section.save()

    def test_retrieve_section(self):
        ta_user = Ta(user_name="JDoe", password="A1234567", privilege_level="TA")
        ta_user.save()

        section_x = Section.objects.get(course=self.my_course, number="801")
        self.assertEqual(section_x.type, "LAB", msg="Got wrong section type.")
        self.assertEqual(section_x.days, "T", msg="Got wrong days.")
        self.assertEqual(section_x.start_time, time(12, 0), msg="Got wrong start time.")
        self.assertEqual(section_x.end_time, time(13, 45), msg="Got wrong end time.")
        self.assertEqual(section_x.ta, None, msg="Default ta should be null.")

        section_x.ta = ta_user
        section_x.save()
        section_x = Section.objects.get(course=self.my_course, number="801")
        self.assertEqual(section_x.ta.user_name, ta_user.user_name, msg="Got wrong ta.")


class TestEnroll(TestCase):

    def setUp(self):
        self.ta_user = Ta(user_name="JDoe", password="A1234567", privilege_level="TA")
        self.ta_user.save()
        self.my_course = Course(name="CS361", lecture_num="401")
        self.my_course.save()
        self.my_section = Section(course=self.my_course, number="801", type="LAB", days="T",
                                  start_time=time(12, 0), end_time=time(13, 45))
        self.my_section.save()
        self.my_enroll = Enroll(ta=self.ta_user, section=self.my_section)
        self.my_enroll.save()

    def test_ta_notnull(self):
        new_enroll = Enroll(section=self.my_section)
        with self.assertRaises(ObjectDoesNotExist, msg="Ta must not be blank"):
            new_enroll.save()

    def test_ta_assignmenterrors(self):
        self.my_enroll.ta = Ta(user_name="qwertyuiop", password="A1234567", privilege_level="TA")
        with self.assertRaises(ObjectDoesNotExist, msg="TA not found"):
            self.my_enroll.save()

    def test_section_notnull(self):
        new_enroll = Enroll(ta=self.ta_user)
        with self.assertRaises(ObjectDoesNotExist, msg="Section must not be blank"):
            new_enroll.save()

    def test_section_assignmenterrors(self):
        self.my_enroll.section = Section(course=self.my_course, number="802", type="LAB", days="T",
                                         start_time=time(12, 0), end_time=time(13, 45))
        with self.assertRaises(ObjectDoesNotExist, msg="Section not found"):
            self.my_enroll.save()

    def test_enroll_uniqueness(self):
        new_enroll = Enroll(ta=self.ta_user, section=self.my_section)
        with self.assertRaises(IntegrityError, msg="Duplicate enrollments should not be allowed"):
            new_enroll.save(force_insert=True)

    def test_retrieve_enroll(self):
        enroll_x=Enroll.objects.get(ta=self.my_enroll.ta, section=self.my_enroll.section)
        self.assertEqual(enroll_x.ta.user_name, "JDoe")
        self.assertEqual(enroll_x.section.course, self.my_course)
        self.assertEqual(enroll_x.section.number, "801")


class TestCourseAssignment(TestCase):

    def setUp(self):
        self.ta_user = Ta(user_name="JDoe", password="A1234567", privilege_level="TA")
        self.ta_user.save()
        self.my_course = Course(name="CS361", lecture_num="401")
        self.my_course.save()
        self.my_courseassign = CourseAssignment(course=self.my_course, ta=self.ta_user)
        self.my_courseassign.save()

    def test_course_notnull(self):
        new_courseassign = CourseAssignment(ta=self.ta_user)
        with self.assertRaises(ObjectDoesNotExist, msg="Course must not be blank"):
            new_courseassign.save()

    def test_course_assignmenterrors(self):
        self.my_courseassign.course = Course(name="CS999", lecture_num="401")
        with self.assertRaises(ObjectDoesNotExist, msg="Course not found"):
            self.my_courseassign.save()

    def test_ta_notnull(self):
        new_courseassign = CourseAssignment(course=self.my_course)
        with self.assertRaises(ObjectDoesNotExist, msg="Ta must not be blank"):
            new_courseassign.save()

    def test_ta_assignmenterrors(self):
        self.my_courseassign.ta = Ta(user_name="qwertyuiop", password="A1234567", privilege_level="TA")
        with self.assertRaises(ObjectDoesNotExist, msg="TA not found"):
            self.my_courseassign.save()

    def test_courseassign_uniqueness(self):
        new_courseassign = CourseAssignment(course=self.my_course, ta=self.ta_user)
        with self.assertRaises(IntegrityError, msg="Duplicate course assignment allowed"):
            new_courseassign.save(force_insert=True)

    def test_retrieve_courseassign(self):
        courseassign_x = CourseAssignment.objects.get(course=self.my_course, ta=self.ta_user)
        self.assertEqual(courseassign_x.course.name, "CS361")
        self.assertEqual(courseassign_x.course.lecture_num, "401")
        self.assertEqual(courseassign_x.ta.user_name, "JDoe")
