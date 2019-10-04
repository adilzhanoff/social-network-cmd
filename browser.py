from socialnetwork import QuickTouch


class Browser:
    # constructor
    def __init__(self):
        self.__social = None

    # functions
    def set_domain(self):
        while True:
            domain_name = input("https://")

            if domain_name == "quicktouch.com":
                break

    def main_menu(self):
        while True:
            self.__social = QuickTouch()
            choice = input("1 - Sign In\n2 - Sign Up\n3 - Exit\n")

            if choice == "1":
                while True:
                    if self.__social.auth_user():
                        break
                self.__social.show_prof()
            elif choice == "2":
                self.__social.new_user()
            elif choice == "3":
                quit(0)
