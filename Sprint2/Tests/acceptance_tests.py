import unittest

from Sprint2.commands import *

com = Commands()


class TestLogin(unittest.TestCase):


    # assume admin account is hard coded in system
    # and this is the 1st login(default password
    # username admin pass 1234 new pass password1
    # new pass must be 8 characters & include 1 numeric character
    def test_admin1st(self):
        self.assertEqual(com.command("login admin 1234"), "Welcome admin, Please enter new password:")
        self.assertEqual(com.command("5678"), "ERROR: Password too short")
        self.assertEqual(com.command("password"), "ERROR: Password does not include any numbers")
        com.command("password1")
        self.assertEqual(com.command("logout"), "Logout Successful")
        self.assertEqual(com.command("login admin password1"), "Welcome admin")


class TestCreateUser(unittest.TestCase):
    # create a user (TA) that does not exist in the system
    # user has default password until login, admin does not set initial password
    def test_create_user1(self):
        self.assertEqual(com.command("adduser user1 ta"), "user1 (TA) added")
    # testing adding the same user again

    def test_create_user1_again(self):
        self.assertEqual(com.command("adduser user1 ta"), "ERROR: user already in system!")
    # create a user (Instructor) that does not exist yet

    def test_create_user2(self):
        self.assertEqual(com.command("adduser user2 instructor"), "user2 (Instructor) added")
    # system does not allow a ta and instructor to have the same username

    def test_TaInstructorSameName(self):
        self.assertEqual(com.command("adduser user1 instructor"), "Error: user already in system")

    def test_TaInstructorSameName2(self):
        self.assertEqual(com.command("adduser user2 ta"), "Error: user already in system")


class TestCreateCourses(unittest.TestCase):
    # assume there are no courses in the system
    def test_AddClass1(self):
        self.assertEqual(com.command("addclass"), "Please enter the class number: ")
        self.assertEqual(com.command("CompSci 361"), "Please enter the section number: ")
        self.assertEqual(com.command("401"), "Please enter the section type (L, O, A, D)" )
        self.assertEqual(com.command("L"), "Please enter the days of the class (MTWRFS): ")
        self.assertEqual(com.command("TR"), "Please enter the times of the class: ")
        self.assertEqual(com.command("1100 - 1150"), "Class has been successfully added. ")

    # attempt to add the same course again
    def test_AddClass1Again(self):
        self.assertEqual(com.command("addclass"), "Please enter the class number: ")
        self.assertEqual(com.command("CompSci 361"), "Please enter the section number: ")
        self.assertEqual(com.command("401"), "ERROR:  This class and section already exist. ")


class TestGetSchedule(unittest.TestCase):

    def test_adminGetAssignments(self):
        # Assume the admin account is logged in
        self.assertEqual(com.command("GETCLASSASSIGNMENTS CS361"), "TA assignments for CS361: ")
        # Lab sections and TA assignments for CS361 are displayed
        self.assertEqual(com.command("GETCLASSASSIGNMENTS all"), "TA assignments for all classes: ")
        # Lab sections and TA assignments for all classes are displayed

    def test_instructorGetAssignments(self):
        # Assume an instructor account is logged in
        self.assertEqual(com.command("GETCLASSASSIGNMENTS CS361"), "TA assignments for CS361: ")
        # Lab sections and TA assignments for CS361 are displayed
        self.assertEqual(com.command("GETCLASSASSIGNMENTS all"), "TA assignments for all classes: ")
        # Lab sections and TA assignments for all classes are displayed

    def test_taGetAssignments(self):
        # Assume a TA account is logged in
        self.assertEqual(com.command("GETCLASSASSIGNMENTS CS361"), "Schedule for CS361: ")
        # Lab sections and TA assignments for CS361 are displayed
        self.assertEqual(com.command("GETCLASSASSIGNMENTS all"), "Schedule for all classes: ")
        # Lab sections and TA assignments for all classes are displayed


class TestGetPending(unittest.TestCase):

    def test_adminPending_commandsroved(self):
        # Assume the admin account is logged in and the assignment of John Smith to CS361,
        # Section 804 is pending commandsroval
        self.assertEqual(com.command("DISPLAYPENDING"),
                         "Pending TA assignments:\nCS361 Section 804 John Smith\ncommandsrove (Y/N)?")
        self.assertEqual(com.command("Y"), "commandsroved.")
        # The assignment should be removed from the pending list

    def test_adminPending_notcommandsroved(self):
        # Assume the admin account is logged in and the assignment of John Smith to CS361,
        # Section 804 is pending commandsroval
        self.assertEqual(com.command("DISPLAYPENDING"),
                         "Pending TA assignments:\nCS361 Section 804 John Smith\ncommandsrove (Y/N)?")
        self.assertEqual(com.command("N"), "Not commandsroved.")
        # The assignment should still be on the pending list

    def test_instructorGetPending(self):
        # Assume an instructor account is logged in
        self.assertEqual(com.command("DISPLAYPENDING"), "Error: You don't have permission to access this command.")

    def test_taGetPending(self):
        # Assume a TA account is logged in
        self.assertEqual(com.command("DISPLAYPENDING"), "Error: You don't have permission to access this command.")


class TestRemoveEnroll(unittest.TestCase):

    def test_taRemoveEnroll_success(self):
        # Assume a TA account is logged in, and that TA is enrolled in CS361
        self.assertEqual(com.command("REMOVEENROLL CS361"), "CS361 removed from schedule.")

    def test_taRemoveEnroll_failure(self):
        # Assume a TA account is logged in, and that TA is not currently enrolled in CS361
        self.assertEqual(com.command("REMOVEENROLL CS361"), "Error: You are not enrolled in CS361")

    def test_adminRemoveEnroll(self):
        # Assume the admin account is logged in
        self.assertEqual(com.command("REMOVEENROLL CS361"), "Error: You don't have permission to access this command")

    def test_instructorRemoveEnroll(self):
        # Assume an instructor account is logged in
        self.assertEqual(com.command("REMOVEENROLL CS361"), "Error: You don't have permission to access this command")


class TestChangePassword(unittest.TestCase):

    def test_changePassword_success(self):
        # Assume a user is logged in, and their password is oldpassword1
        self.assertEqual(com.command("CHANGEPASSWORD"), "Enter old password: ")
        self.assertEqual(com.command("oldpassword1"), "Enter new password: ")
        self.assertEqual(com.command("newpassword1"), "Password reset.")

    def test_changePassword_oldPasswordWrong(self):
        # Assume a user is logged in, and their password is oldpassword1
        self.assertEqual(com.command("CHANGEPASSWORD"), "Enter old password: ")
        self.assertEqual(com.command("qwerty"), "Error: Incorrect password.")

    def test_changePassword_tooShort(self):
        # Assume a user is logged in, and their password is oldpassword1
        self.assertEqual(com.command("CHANGEPASSWORD"), "Enter old password: ")
        self.assertEqual(com.command("oldpassword1"), "Enter new password: ")
        self.assertEqual(com.command("new"), "Error: Password too short.")

    def test_changePassword_noNumber(self):
        # Assume a user is logged in, and their password is oldpassword1
        self.assertEqual(com.command("CHANGEPASSWORD"), "Enter old password: ")
        self.assertEqual(com.command("oldpassword1"), "Enter new password: ")
        self.assertEqual(com.command("newpassword"), "Error: Password does not include any numbers.")


class TestReset(unittest.TestCase):

    def test_reset(self):
        # This test is to confirm the functionality of the resetting of the system for a new semester.
        # The function is designed to delete the entire class schedule from the system.
        # The function will also delete all TA assignments from the system.
        # The function will not affect any of the user accounts or personal user data.
        self.assertEqual(com.command("RESET"), "Do you want to reset the system for a new semester?")
        self.assertEqual(com.command("y"), "This will delete ALL class and assignment data from the system. ARE YOU SURE?")
        self.assertEqual(com.command("y"), "Please enter Admin password: ")
        #commands.command(admin.password)
        #self.assert_("Deleting class schedules...")
        #self.assert_("Deleting TA Assignments...")
        #self.assert_("The system has been successfully reset.")
        # This following block confirms that the system has been reset.
        # If these error messages are not displayed, then the reset was not completely successful.
        self.assertEqual(com.command("DISPLAYASSIGNMENTS"), "ERROR: There are no TA assignments.")
        self.assertEqual(com.command("DISPLAYCLASSES"), "ERROR: There are no classes scheduled.")
        self.assertEqual(com.command("ASSIGNTA"), "ERROR: There are no classes scheduled.")
        self.assertEqual(com.command("ASSIGNINSTRUCTOR"), "ERROR: There are no classes scheduled.")

    def test_resetinvalidpassword(self):
        # This test is to confirm that if the admin password is not entered correctly,
        # that the system will not reset itself.
        self.assertEqual(com.command("RESET"), "Do you want to reset the system for a new semester?")
        self.assertEqual(com.command("y"), "This will delete ALL class and assignment data from the system. ARE YOU SURE?")
        self.assertEqual(com.command("y"), "Please enter Admin password: ")
        self.assertEqual(com.command("not_the_password"), "ERROR: You have entered an incorrect password. The system will not be reset.")

    def test_resetnotconfirmedone(self):
        # This test is to confirm that if the user selects no at the first confirmation prompts that the system
        # does not reset.
        self.assertEqual(com.command("RESET"), "Do you want to reset the system for a new semester?")
        self.assertEqual(com.command("n"), "The system will not be reset.")

    def test_resetnotconfirmedtwo(self):
        # This test is to confirm that if the user selects no at the second confirmation prompts that the system
        # does not reset.
        self.assertEqual(com.command("RESET"), "Do you want to reset the system for a new semester?")
        self.assertEqual(com.command("y"), "This will delete ALL class and assignment data from the system. ARE YOU SURE?")
        self.assertEqual(com.command("n"), "The system will not be reset.")


class TestConflicts(unittest.TestCase):
    def test_conflicts(self):
        # This test is to confirm that if there are any schedule conflicts that they will be displayed
        # THis test will also confirm that any over or under scheduled TAs will also be displayed
        self.assertEqual(com.command("DISPLAYCONFLICTS"), "Here are the current scheduling conflicts:")

    def test_noconflicts(self):
        # This test is to confirm that if there are no conflicts, that the commandsropriate message will be displayed.
        self.assertEqual(com.command("DISPLAYCONFLICTS"), "There are no current scheduling conflicts.")

    def test_scheduleonly(self):
        # This test is to confirm that if there are only scheduling conflicts that they will be displayed
        # There are no TAs that are over or under scheduled in this scenario.
        self.assertEqual(com.command("DISPLAYCONFLICTS"), "Here are the current scheduling conflicts:")

    def test_overonly(self):
        # This test is to confirm that if there are only over-scheduled TAs that they will be displayed
        # There will be no scheduling conflicts or under-scheduled TAs in this scenario.
        self.assertEqual(com.command("DISPLAYCONFLICTS"), "There are no current scheduling conflicts.")

    def test_underonly(self):
        # This test is to confirm that if there are only under-scheduled TAs that they will be displayed
        # There will be no scheduling conflicts or under-scheduled TAs in this scenario.
        self.assertEqual(com.command("DISPLAYCONFLICTS"), "There are no current scheduling conflicts.")


class TestPreferences(unittest.TestCase):
    def test_preferences(self):
        # This test is to confirm the functionality of a TA being able to set their class preferences.
        self.assertEqual(com.command("SETPREFERENCES"), "Here are the classes that you are eligible for:")
        #self.assertEqual("Please enter your first preference: ")
        self.assertEqual(com.command("preference1"), "Please enter your second preference: ")
        self.assertEqual(com.command("preference2"), "Please enter your third preference: ")
        self.assertEqual(com.command("preference3"), "Your preferences have been set.")

    def test_preferencesone(self):
        # This test is to confirm proper functioning of entering -1 to exit preferences early
        # This would be used in the event that a TA has less than three preferences.
        self.assertEqual(com.command("SETPREFERENCES"), "Here are the classes that you are eligible for:")
        #self.assertEqual("Please enter your first preference: ")
        self.assertEqual(com.command("preference1"), "Please enter your second preference: ")
        self.assertEqual(com.command("-1"), "Your one preference has been set.")

    def test_preferencestwo(self):
        # This test is to confirm proper functioning of entering -1 to exit preferences early
        # This would be used in the event that a TA has less than three preferences.
        self.assertEqual(com.command("SETPREFERENCES"), "Here are the classes that you are eligible for:")
        #self.assertEqual("Please enter your first preference: ")
        self.assertEqual(com.command("preference1"), "Please enter your second preference: ")
        self.assertEqual(com.command("preference2"), "Please enter your third preference: ")
        self.assertEqual(com.command("-1"), "Your two preferences have been set.")

    def test_preferencesnoneavailable(self):
        # This test would be to confirm the proper error message if a TA does not have any classes available
        # to choose from.  This would be a result of class schedule and availability conflicts.
        self.assertEqual(com.command("SETPREFERENCES"), "ERROR: You are not eligible for any classes.")

# TAs enter their qualifications
# Admin views TA qualifications
# TAs & Instructors enter contact info

# Assuming testing accounts are created for the testing purposes
# Assuming qualifications are presented as the valid courses the TA can be assigned to


class TestEnterQualifications(unittest.TestCase):
    def test_loginAndPrivileges(self):
        com.command("login TestAdmin Pass1234")
        self.assertEqual(com.command("ADDQUAL"), "ERROR: You don't have permission to access this command.")
        com.command("logout")

        com.command("login TestInstructor Pass1234")
        self.assertEqual(com.command("ADDQUAL"), "ERROR: You don't have permission to access this command.")
        com.command("logout")

        com.command("login TestTA Pass1234")
        self.assertEqual(com.command("ADDQUAL"), "Enter your qualifications, 'q' to stop: ")
        self.assertEqual(com.command("q"), "Please enter a command: ")
        com.command("logout")

    def test_invalidEntries(self):
        com.command("login TestTA Pass1234")
        self.assertEqual(com.command("ADDQUAL"), "Enter your qualifications, 'q' to stop: ")
        self.assertEqual(com.command(""), "ERROR: invalid entry./nEnter your qualifications, 'q' to stop: ")
        self.assertEqual(com.command("CS"), "ERROR: invalid entry./nEnter your qualifications, 'q' to stop: ")
        self.assertEqual(com.command("CS 361 3"), "ERROR: invalid entry./nEnter your qualifications, 'q' to stop: ")
        self.assertEqual(com.command("361CS"), "ERROR: invalid entry./nEnter your qualifications, 'q' to stop: ")
        self.assertEqual(com.command("CS 361"), "ERROR: invalid entry./nEnter your qualifications, 'q' to stop: ")
        self.assertEqual(com.command("CompSci 361"), "Qualification Added./nEnter your qualifications, 'q' to stop: ")
        self.assertEqual(com.command("CRM JST 105"), "Qualification Added./nEnter your qualifications, 'q' to stop: ")
        self.assertEqual(com.command("q"), "Your qualifications have been updated./nPlease enter a command: ")

    def test_invalidQualifications(self):
        self.assertEqual(com.command("ADDQUAL"), "Enter your qualifications, 'q' to stop: ")
        self.assertEqual(com.command("COMPSCI 361"), "ERROR: duplicate entry./nEnter your qualifications, 'q' to stop: ")
        self.assertEqual(com.command("CompSci 100"), "ERROR: No such course exists./nEnter your qualifications, 'q' to stop: ")
        self.assertEqual(com.command("CHEM 105"), "Qualification Added./nEnter your qualifications, 'q' to stop: ")
        self.assertEqual(com.command("Q"), "Your qualifications have been updated./nPlease enter a command: ")


class TestViewQualifications(unittest.TestCase):
    def test_loginAndPrivileges(self):
        com.command("login TestTA Pass1234")
        self.assertEqual(com.command("VIEWQUAL OtherTA"), "ERROR: You don't have permission to access this command.")
        com.command("logout")

        com.command("login TestTA Pass1234")
        self.assertEqual(com.command("VIEWQUAL TestTA"), "Qualifications:/n")
        com.command("logout")

        com.command("login TestInstructor Pass1234")
        self.assertEqual(com.command("VIEWQUAL TestTA"), "Qualifications:/n")
        com.command("logout")

        com.command("login TestAdmin Pass1234")
        self.assertEqual(com.command("VIEWQUAL TestTA"), "Qualifications:/n")
        com.command("logout")

    def test_view(self):
        com.command("login TestInstructor Pass1234")
        self.assertEqual(com.command("VIEWQUAL TestTA"), "CompSci 361")
        self.assertEqual(com.command("VIEWQUAL TestTA"), "CRM JST 105")
        com.command("logout")

        com.command("login TestTA Pass1234")
        self.assertEqual(com.command("VIEWQUAL TestTA"), "CompSci 361")
        self.assertEqual(com.command("VIEWQUAL TestTA"), "CRM JST 105")
        com.command("logout")

        com.command("login TestTA2 Pass1234")
        self.assertEqual(com.command("VIEWQUAL TestTA2"), "Qualifications:/n")
        com.command("logout")

        com.command("login TestAdmin Pass1234")
        self.assertEqual(com.command("VIEWQUAL TestTA2"), "Qualifications:/n")
        com.command("logout")


class TestContactInfo(unittest.TestCase):
    def test_editInfo(self):
        com.command("login TestAdmin Pass1234")
        self.assertEqual(com.command("EDITINFO"), "ERROR: You don't have permission to access this command.")
        com.command("logout")

        com.command("login TestTA Pass1234")
        self.assertEqual(com.command("EDITINFO email"), "Enter your email address: ")
        self.assertEqual(com.command("testta@uwm.edu"), "ERROR: the UWM email is already in file.")
        self.assertEqual(com.command("EDITINFO email"), "Enter your email address: ")
        self.assertEqual(com.command("testta@somehing."), "ERROR: invalid email format.")
        self.assertEqual(com.command("EDITINFO email"), "Enter your email address: ")
        self.assertEqual(com.command("testta-somehing.com"), "ERROR: invalid email format.")
        self.assertEqual(com.command("EDITINFO email"), "Enter your email address: ")
        self.assertEqual(com.command("testtaATsomehing.0rg"), "ERROR: invalid email format.")
        self.assertEqual(com.command("EDITINFO email"), "Enter your email address: ")
        self.assertEqual(com.command("testta@somehing.com"), "Your email has been updated successfully.")

        self.assertEqual(com.command("EDITINFO phone"), "Enter your phone number: ")
        self.assertEqual(com.command("012345678910"), "ERROR: invalid phone number.")
        self.assertEqual(com.command("EDITINFO phone"), "Enter your phone number: ")
        self.assertEqual(com.command("012345678"), "ERROR: invalid phone number.")
        self.assertEqual(com.command("EDITINFO phone"), "Enter your phone number: ")
        self.assertEqual(com.command("01234-678"), "ERROR: invalid phone number.")
        self.assertEqual(com.command("EDITINFO phone"), "Enter your phone number: ")
        self.assertEqual(com.command("a2345678z"), "ERROR: invalid phone number.")
        self.assertEqual(com.command("EDITINFO phone"), "Enter your phone number: ")
        self.assertEqual(com.command("0123456789"), "Your phone number has been updated successfully.")


class TestViewAssignments(unittest.TestCase):
    # assume that user "BILL" is assigned to CS251 Lab 801
    # assume that user "TED" has no assignments
    def test_view_assignments_assigned(self):
        self.assertEqual(com.command("VIEWASSIGNMENT BILL"), "Assigned to CS251 Section 801")

    def test_view_assignments_unassigned(self):
        self.assertEqual(com.command("VIEWASSIGNMENT TED"), "No Current Assignments")


class TestAcceptRejectAssignment(unittest.TestCase):
    # after TAs reccive assignments, they can view with the VIEWASSIGNMENT
    # command. after this command, they are prompted to accept(Y), or deny (N).
    def test_accept(self):
        com.command("VIEWASSIGNMENT")  # setup
        self.assertEqual(com.command("Y"), "Assignment accepted")

    def test_reject(self):
        com.command("VIEWASSIGNMENT")
        self.assertEqual(com.command("N"), "Assignment rejected")


class TestAccountDelete(unittest.TestCase):
    # assume user "BILL" exists
    # assume user "TED" does not exist
    def test_deleteUser_exists(self):
        self.assertEqual(com.command("DELETEUSER BILL"), "User 'BILL' deleted")

    def test_deleteUser_does_not_exist(self):
        self.assertEqual(com.command("DELETEUSER TED"), "ERROR! User 'TED' does not exist!")

    def test_deleteUser_noargs(self):
        self.assertEqual(com.command("DELETEUSER"), "ERROR! No user specified!")


class testSetFinalDate(unittest.TestCase):
    # admin sets a final date for TAs to accept or reject assignments
    def test_check_initial_date(self):
        # initial date set to "NO DATE SET"
        # assume no date set before tests are run
        self.assertEqual(com.command("VIEWFINALDATE"), "NO DATE SET")

    def test_set_date(self):
        self.assertEqual(com.command("SETFINALDATE 1/1/20"), "Final Date set to 1/1/20")

    def test_check_set_date(self):
        self.assertEqual(com.command("VIEWFINALDATE"), "Final Date set to 1/1/20")

    def test_set_date_different(self):
        self.assertEqual(com.command("SETFINALDATE 2/1/20"), "Final Date set to 2/1/20")
        self.assertEqual(com.command("VIEWFINALDATE"), "Final Date set to 2/1/20")

    def test_set_date_incomplete(self):
        self.assertEqual(com.command("SETFINALDATE 1/1"), "ERROR! Incorrect format")

    def test_set_date_noargs(self):
        self.assertEqual(com.command("SETFINALDATE"), "ERROR! Incorrect format")

    def test_set_date_badformat(self):
        self.assertEqual(com.command("SETFINALDATE 1-1-20"), "ERROR! Incorrect format")
        self.assertEqual(com.command("SETFINALDATE 1120"), "ERROR! Incorrect format")
        self.assertEqual(com.command("SETFINALDATE January 1st 2020"), "ERROR! Incorrect format")
        self.assertEqual(com.command("SETFINALDATE 20/1/1"), "ERROR! Incorrect format")
        self.assertEqual(com.command("SETFINALDATE $%^&"), "ERROR! Incorrect format")


if __name__ == '__main__':
    unittest.main()
