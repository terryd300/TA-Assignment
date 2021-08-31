# This method is to determine the user's access level and display the appropriate menu and then call
# the next command if the user's access level allows.

def menu(currentuser):

    access = currentuser.access
    command = None

    if access.lower() == "admin":
        displayAdminMenu()

    elif access.lower() == "instructor":
        displayInstructorMenu()

    else:
        displayTAMenu()

    command = input("Please Enter a Command: ")
    command = command.split(" ")

    if command[0].lower() == "createuser":
        if access.lower() != "admin":
            print ("ERROR: You do not have access to add a user!")
            menu(currentuser)
        else:
            createuser(currentuser, command)
    elif command[0].lower() == "addclass":
        if access.lower() != "admin":
            print ("ERROR: You do not have access to add a class!")
            menu(currentuser)
        else:
            addclass(currentuser, command)
    elif command[0].lower() == "assignta":
        if access.lower() == "ta":
            print ("ERROR:  You do not have access to assign TAs!")
            menu(currentuser)
        else:
            assignta(currentuser, command)
    elif command[0].lower() == "assigninstructor":
        if access.lower() != "admin":
            print ("ERROR:  You do not have access to assign instructors!")
            menu(currentuser)
        else:
            assigninstructor(currentuser, command)
    elif command[0].lower() == "getclassassignments":
        if access.lower() == "ta":
            print ("ERROR:  You do not have access to view class assignments!")
            menu(currentuser)
        else:
            getclassassignments(currentuser, command)
    elif command[0].lower() == "viewassignment":
        viewassignment(currentuser, command)
    elif command[0].lower() == "logout":
        logout()
    elif command[0].lower() == "login":
        login(command)
    else:
        print("You have entered an invalid command!")


def displayAdminMenu():
    return ("\n*50" + "Admin Main Menu\n\nCREATEUSER - To Create a New User\nEDITUSER - To Edit a Current User's Information\nDELETEUSER - To Delete a User's Account\nADDCLASS - To Create a new Section of a Class\nASSIGNTA - To Assign a TA to a Lab or Discussion Section\nASSIGNINSTRUCTOR - To Assign an Instructor to a Lecture Section\nEDITINFO - To Edit a User's Contact Information\nGETCLASSASSIGNMENTS - To Display Assignments for a Particular Course\nVIEWASSIGNMENTS - To Display Assignments for a Particular User\nDISPLAYCONFLICTS - To Display All Scheduling Conflicts\nSETFINALDATE - To Set the Final Date to Allow Schedule Changes\nVIEWFINALDATE - To View the Final Date that Schedule Changes are Allowed\nVIEWQUAL - To View the Qualifications for a Specific TA\nDISPLAYPENDING - To View TA Assignments that are Pending Approval\nCHANGEPASSWORD - To Change Your Password\nRESETPASSWORD - To Reset a User's Password\nRESET - To Reset the System for a New Semester\nLOGOUT - To Logout of the system.\n")

def displayInstructorMenu():
    return("\n*50" + "Instructor Main Menu\n\nEDITUSER - To Edit a Current User's Information\nASSIGNTA - To Assign a TA to a Lab or Discussion Section\nEDITINFO - To Edit a User's Contact Information\nGETCLASSASSIGNMENTS - To Display Assignments for a Particular Course\nVIEWASSIGNMENTS - To Display Assignments for a Particular User\nDISPLAYCONFLICTS - To Display All Scheduling Conflicts\nVIEWFINALDATE - To View the Final Date that Schedule Changes are Allowed\nVIEWQUAL - To View the Qualifications for a Specific TA\nCHANGEPASSWORD - To Change Your Password\nLOGOUT - To Logout of the system.\n")

def displayTAMenu():
    return("\n*50" + "TA Main Menu\n\nEDITUSER - To Edit a Current User's Information\nEDITINFO - To Edit a User's Contact Information\nEDITSCHEDULE - To Edit Your Schedule\nVIEWSCHEDULE - To View Your Class And Instructional Schedules\nSETPREFERENCES - To Enter Your Class Preferences\nADDQUAL - To Add Your Qualifications\nVIEWASSIGNMENTS - To Display Assignments for a Particular User\nDISPLAYCONFLICTS - To Display All Scheduling Conflicts\nVIEWFINALDATE - To View the Final Date that Schedule Changes are Allowed\nCHANGEPASSWORD - To Change Your Password\nLOGOUT - To Logout of the system.\n")

def createuser(currentuser, command):
    # This method will verify the correct number of arguments and then call the method to create a new user
    # command[1] should be the user name
    # command[2] should be the access level

    if len(command) == 1:
        print ("ERROR:  You have not provided a user name or access level.")
        menu(currentuser)

    elif len(command) == 2:
        if command[1].lower() == "admin" or command[1].lower() == "instructor" or command[1].lower() == "ta":
            print ("ERROR:  You have not provided a user name.")
            menu(currentuser)
        else:
            print ("ERROR:  You have not provided an access level for the user.")
            menu(currentuser)

    elif command[1].lower() == "admin" or command[1].lower() == "instructor" or command[1].lower() == "ta":
        print ("ERROR:  You did not enter the options in the correct order.")
        menu(currentuser)

    else:
        # Call method to create a user

        pass

def addclass(currentuser, command):
    # This method is to call the add course method

    # Call method to add a class

    pass

def assignta(currentuser, command):
    # This method is to assign a TA to a course

    # command[0] is the assignta command
    # command[1] is the TA name
    # command[2] is the course number
    # command[3] is the section number

    if len(command) == 1:
        print("ERROR:  You did not provide the TA, Class, or Section Information.")
        menu(currentuser)

    elif len(command) == 2 and command[1].isnumeric():
        print("ERROR:  You did not provide a TA or Class Information.")
        menu(currentuser)

    elif len(command) != 4:
        print("ERROR:  You did not provide enough information to assign a TA.")
        print("You must include the TA's user name, Course Number, and Section Number.")
        menu(currentuser)

    # Call method to assign a TA

def assigninstructor(currentuser, command):
    # This method is to assign an instructor to a course

    # Format is still undetermined

    pass

def getclassassignments(currentuser, command):
    # This method is to obtain the assignments for a particular course

    # command[0] is the getclassassignments command
    # command[1] is the course identifier or "all" to list all assignments

    if len(command) == 1:
        print("ERROR:  You have not entered a course.")

    # Call method to get the course assignments

def viewassignment(currentuser, command):
    # This method is to obtain the assignments for a particular instructor or TA

    # command[0] is the viewassignments command
    # command[1] is the user name

    if len(command) == 1:
        command[1] = currentuser

    # Call method to get the user's assignments

def logout():
    # This method is to allow the current user to logout of the system.

    pass

def login(command):
    # This method is to allow a user to login to the system.

    # command[0] is the login command
    # command[1] is the user name
    # command[2] is the password

    if len(command) != 3:
        print ("You have not entered the correct number of arguments.")

    # Call the login method

    pass