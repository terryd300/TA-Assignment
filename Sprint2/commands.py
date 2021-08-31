from Sprint2.models import *

class Commands:
    current_user = None
    current_username = ''
    current_permissions = None

    def updateUser(user_object):
        Commands.current_user = user_object
        Commands.current_username = ''
        if user_object is not None:
            Commands.current_username = user_object.__str__().split("(")[1].split(")")[0]
            Commands.current_permissions = Commands.current_user.__getattribute__("privilege_level")

    def command(self, com):
        com = com.split(" ")

        command_options = {
            "login": self.login(com),
            "logout": self.logout(com),
            "printmyinfo": self.printmyinfo(com),
            "printusers": self.printusers(com),
            "printcourses": self.printcourses(com),
            "createuser": self.createuser(com),
            "createcourse": self.createcourse(com),
            "viewcourse": self.viewcourses(com),
            "addclass": self.addclass(com),
            "exit": exit(0)
        }

        # Determine menu option chosen

        if com[0] in command_options:
            command_options[com[0]]
        else:
            return "No command for " + com[0] + ". Try the command \"help\" for a list of commands"

    def login(com):
        if len(com) != 3:
            return "Incorrect format for login (login <username> <password>)"
        if Commands.current_user is not None:
            return "Login Failed: " + Commands.current_username + " is already logged in"
        user = None
        try:
            user = User.objects.get(user_name=com[1])
        except ObjectDoesNotExist:
            return "Login Failed: user does not exist"
        if user.password == com[2]:
            Commands.updateUser(user)
            return com[1]+" logged in"
        else:
            return "Login Failed: Incorrect password"

    def logout(com):
        if Commands.current_user is None:
            return "Logout Failed: No one was logged in"
        else:
            name = Commands.current_username
            Commands.updateUser(None)
            return name + " logged out"

    def printmyinfo(com):
        if(Commands.current_user is not None):
            return "Name: " + Commands.current_username + "\nPermissions: " + Commands.current_permissions
        else:
            return "Print Failed: No one was logged in"

    def printusers(com):
            ret = ""
            for users in User.objects.all():
                ret += users.__str__().split("(")[1].split(")")[0] + "\r\n"
            if ret == "":
                ret = "No registered users"
            return ret

    def printcourses(com):
            ret = ""
            for courses in Course.objects.all():
                ret += courses.name.__str__() + "-" + courses.lecture_num.__str__()+ "\n"
            if ret == "":
                ret = "No registered users"
            return ret

    def createuser(com):
        if Commands.current_permissions != "ADMIN":
            return "You do not have permission to add users."
        if User.objects.filter(user_name=com[1]).count() != 0:
            return "User Creation Failed: Username \"" + com[1] + "\" is already in use."
        else:
            if len(com) >= 3:
                pswrd = "temp123"
                prms = com[2].upper()
                if len(com) == 4:
                    pswrd = com[2]
                    prms = com[3].upper()

                if prms != "TA" and prms != "ADMIN" and prms != "INSTRUCTOR":
                    return "User Creation Failed: Privilege Level must be either TA, ADMIN, or INSTRUCTOR"
                User(user_name=com[1], password=pswrd, privilege_level=prms).save(force_insert=True)
                return "User \"" + com[1] + "\" created!"
            else:
                return "User Creation Failed: Format is ( createuser <Username> <Password(Optional)> <Permissions>)"

    def createcourse(com):
        if(Commands.current_permissions != "ADMIN"):
            return "You do not have permission to add classes."
        if len(com) >= 3:
            if not com[2].isnumeric() or len(com[2]) != 3:
                return "User Creation Failed: Section must be a 3-digit number"
            if len(com) == 4:
                return "No implementation for assigning instructor yet.." #TODO
            Course(name=com[1], lecture_num=com[2]).save(force_insert=True)
            return "Course \"" + com[1] + " - " + com[2] + "\" created!"
        else:
          return "User Creation Failed: Format is ( createcourse <Department/Number> <Section Number> <Instructor(Optional)>)"

    def viewcourses(com):
        return ":("

    def addclass(com):
        if len(com) == 3:
            if Course.objects.filter(name=com[1]).exists():
                return "ERROR:  This class and section already exist. "
            else: Course.objects.create(name=com[1], number=com[2])
        elif len(com) == 7:
            if Course.objects.filter(name=com[1]).exists():
                if Section.objects.filter(course=com[1]+" "+com[2], number=com[3]):
                    return "ERROR:  This class and section already exist. "
                else:
                    Section.objects.create(course=com[0]+" "+com[1], number=com[3],
                                       type=com[4], start_time=com[5], end_time=[6])
                    return "The section was successfully added"
            else:
                Course.objects.create(name=com[1], number=com[2])
                return "The class was successfully added"
        else: return "Wrong number of arguments"

