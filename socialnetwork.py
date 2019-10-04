from database import Database, User, Post, Friend


class QuickTouch:
    # constructor
    def __init__(self):
        self.__data = Database()
        self.__cur_user = User()
        self.__users = []
        self.__posts = []

    # functions
    def auth_user(self):
        log = input("Enter your login - ")
        password = input("Enter your password - ")

        if self.check_user(log, password):
            return True
        else:
            print("Incorrect login or password, try again.")
            return False

    def check_user(self, log, password):
        self.__users = self.__data.get_users()
        for line in self.__users:
            if line.get_log() == log and line.get_pass() == password:
                self.__cur_user.set_id(line.get_id())
                self.__cur_user.set_log(line.get_log())
                self.__cur_user.set_name(line.get_name())
                self.__cur_user.set_surname(line.get_surname())
                self.__cur_user.set_pass(line.get_pass())
                self.__cur_user.set_access(line.get_access())
                self.__cur_user.set_friends(line.get_friends())

                return True

        return False

    def check_pass(self, password):
        if all([
                    any(letter.isupper() for letter in password),
                    any(letter.islower() for letter in password),
                    any(letter.isnumeric() for letter in password),
                    len(password) >= 6
               ]):
            return True
        else:
            return False

    def check_log(self, log):
        for usr in self.__users:
            if usr.get_log() == log:
                return False

        if not len(log) >= 1:
            return False

        return True

    def new_user(self):
        user = User()

        while True:
            name = input("Enter your name: ")
            surname = input("Enter your surname: ")
            log = input("Enter your login: ")
            password = input("Enter your password: ")
            self.__users = self.__data.get_users()

            if not self.check_log(log):
                print(
                    "Such login already exists or its",
                    "length is less than 1 character."
                )

            if not self.check_pass(password):
                print(
                    "Your password must be at least 6 characters long and",
                    "contain at least 1 upper, lower case letters and 1 digit."
                )

            if self.check_log(log) and self.check_pass(password):
                # checks if users.txt is empty (ternary doesn't work)
                if self.__users == []:
                    temp = str()
                else:
                    temp = self.__users[-1]

                # to avoid 'index out of range' error (ternary doesn't work)
                if isinstance(temp, str):
                    id = 0
                else:
                    id = temp.get_id()

                user.set_id(id + 1)
                friend = Friend(user.get_id())
                user.set_log(log)
                user.set_name(name)
                user.set_surname(surname)
                user.set_pass(password)
                user.set_friends(friend)

                break
        self.__data.push_user(user)

    def new_post(self):
        post = Post()
        txt = input()
        self.__posts = self.__data.get_posts()

        # checks if posts.txt is empty (ternary doesn't work)
        if self.__posts == []:
            temp = str()
        else:
            temp = self.__posts[-1]

        post.set_crt(self.__cur_user.get_id())

        # to avoid 'index out of range' error (ternary doesn't work)
        if isinstance(temp, str):
            id = 0
        else:
            id = temp.get_id()

        post.set_id(id + 1)
        post.set_txt(txt)
        self.__data.push_post(post)

    def search(self):
        query = input()
        searched = self.__data.search_users(query, self.__cur_user.get_id())

        if searched == []:
            print("No matches were found.")
        else:
            for usr in searched:
                print(
                    f"{usr.get_id()} - {usr.get_name()}",
                    f"{usr.get_surname()} - {usr.get_log()}"
                )

            while True:
                choice = input(
                    "\n1 - See person's wall" +
                    "\n2 - Send friend request" +
                    "\n3 - Back to the profile\n"
                )
                if choice == "1":
                    id = str()
                    while id != "-1":
                        try:
                            id = input("Enter user ID: ")
                            self.__users = self.__data.get_users()

                            if (
                                int(id) == self.__cur_user.get_id() or
                                any([
                                    (int(id) == user.get_id() and
                                     user.get_access()[0].get_count() == 0) or
                                    (int(id) == user.get_id() and
                                     user.get_access()[0].get_count() == 1 and
                                     [self.__cur_user.get_id()] in
                                     [user.get_friends().get_list()[idx][:1]
                                      for idx in range(
                                                    len(
                                                        user.get_friends(
                                                        ).get_list()
                                                    )
                                                 )
                                      ]
                                     )
                                    for user in self.__users
                                ])
                            ):
                                self.show_wall(int(id))
                                break
                            elif id != "-1":
                                print(
                                    "User with such ID was not found,",
                                    "or access is restricted."
                                )
                        except ValueError:
                            pass
                elif choice == "2":
                    id = str()
                    while id != "-1":
                        try:
                            id = input("Enter user ID: ")
                            self.__users = self.__data.get_users()
                            __temp__ = self.__cur_user.get_friends().get_list()
                            x = all(int(id) != p[0]
                                    for p in self.__cur_user.get_friends(
                                    ).get_list()
                                    )
                            if any([
                                    int(id) == user.get_id() and
                                    all(int(id) not in p
                                        for p in self.__cur_user.get_friends(
                                    ).get_list()) and
                                    int(id) != self.__cur_user.get_id() and
                                    not [self.__cur_user.get_id(), 1]
                                    in user.get_friends().get_list() and
                                    not [self.__cur_user.get_id(), 0] in
                                    user.get_friends().get_sent()
                                    for user in self.__users
                            ]) or (not [int(id), 0] in
                                    self.__cur_user.get_friends().get_sent()):

                                self.__data.request_handler(
                                    self.__cur_user.get_id(), int(id), 0
                                )
                                for usr in self.__users:
                                    if usr.get_id() == int(id):
                                        print(
                                            "Friend request to",
                                            f"{usr.get_name()}",
                                            f"{usr.get_surname()}",
                                            "has been sent."
                                        )
                                        break
                                break
                            elif id != "-1":
                                print("Incorrect ID, please try again.")
                        except ValueError:
                            pass
                elif choice == "3":
                    break

    def show_wall(self, id):  # id - id of the user
        posts = self.__data.get_posts(id)

        if posts == [] and id == self.__cur_user.get_id():
            print("Your wall is empty")
        elif posts == [] and id != self.__cur_user.get_id():
            for line in self.__users:
                if line.get_id() == id:
                    print(
                        f"{line.get_name()} {line.get_surname()}'s'",
                        "wall is empty."
                    )
        for post in posts:
            print(str(post.get_id()) + " " + post.get_txt())
        return posts

    def show_my_posts(self):
        posts = self.show_wall(self.__cur_user.get_id())
        choice = input("\n1 - Delete the post\n2 - Back to the profile\n")

        if choice == "1":
            id = int()
            while id != -1:
                try:
                    id = int(input("Enter post ID: "))
                    if any([
                        self.__cur_user.get_id() == post.get_crt() and
                        post.get_id() == id for post in posts
                    ]):
                        self.__data.delete_post(id)
                        break
                    elif id != -1:
                        print(
                            "Post with such ID was not found,",
                            "or you are not allowed to delete it."
                        )
                except ValueError:
                    pass

            self.show_my_posts()
        elif choice == "2":
            pass
        else:
            self.show_my_posts()

    def friend_list(self):
        if self.__cur_user.get_friends().get_list() == []:
            print("\nYour friend list is empty.")
        else:
            print("\nYour friends:")
            for elem in self.__cur_user.get_friends().get_list():
                for usr in self.__users:
                    pass
                    if usr.get_id() in elem[:1]:
                        print(
                            f"{usr.get_id()} -",
                            f"{usr.get_name()} {usr.get_surname()}"
                        )
                        break

        if self.__cur_user.get_friends().get_sent() == []:
            print("\nYou have no friend requests.")
        else:
            print("\nFriend requests:")
            for elem in self.__cur_user.get_friends().get_sent():
                for usr in self.__users:
                    if usr.get_id() in elem[:1]:
                        print(
                            f"{usr.get_id()} -",
                            f"{''.join([usr.get_name(), usr.get_surname()])}"
                        )
                        break

    def show_friends(self):
        self.check_user(self.__cur_user.get_log(), self.__cur_user.get_pass())
        self.friend_list()

        while True:
            try:
                opr = input(
                        "\n1 - Remove friend" +
                        "\n2 - Accept request" +
                        "\n3 - Reject request" +
                        "\n4 - Back to the profile\n")
                if opr == "1":
                    if self.__cur_user.get_friends().get_list() != []:
                        id = str()
                        while id != "-1":
                            try:
                                id = input("Enter user ID: ")
                                if (
                                    [int(id), 1] in
                                        self.__cur_user.get_friends().get_list(
                                        )
                                ):
                                    self.__data.remove_friend(
                                        self.__cur_user.get_id(), int(id)
                                    )
                                    for usr in self.__users:
                                        if usr.get_id() == int(id):
                                            print(
                                                f"{usr.get_name()}",
                                                f"{usr.get_surname()}",
                                                "has been removed from",
                                                "your friend list."
                                            )
                                            break

                                    self.check_user(
                                        self.__cur_user.get_log(),
                                        self.__cur_user.get_pass()
                                    )
                                    self.friend_list()
                                    break
                                elif id != "-1":
                                    print("Incorrect ID, please try again.")
                            except ValueError:
                                pass
                    else:
                        print("Your friend list is empty.")
                elif opr == "2" or opr == "3":
                    if self.__cur_user.get_friends().get_sent() != []:
                        id = str()
                        while id != "-1":
                            try:
                                id = input(
                                    "Enter user ID who sent" +
                                    "you friend request: "
                                )
                                if (
                                    [int(id), 0] in
                                        self.__cur_user.get_friends().get_sent(
                                        )
                                ):
                                    self.__data.request_handler(
                                        int(id),
                                        self.__cur_user.get_id(),
                                        int(opr) - 1
                                    )
                                    for usr in self.__users:
                                        if usr.get_id() == int(id):
                                            print(
                                                "Request from",
                                                f"{usr.get_name()}",
                                                f"{usr.get_surname()}",
                                                "has been",
                                                (
                                                    ("rejected.", "accepted.")
                                                    [opr == "2"]
                                                ),
                                            )
                                            break

                                    self.check_user(
                                        self.__cur_user.get_log(),
                                        self.__cur_user.get_pass()
                                    )
                                    self.friend_list()
                                    break
                                elif id != -1:
                                    print("Incorrect ID, please try again.")
                            except ValueError:
                                pass
                    else:
                        print("You have no friend requests.")
                elif opr == "4":
                    break
            except ValueError:
                pass

    def settings(self):
        opt = input(
            "\n1 - Who can view your wall - " +
            (
                ("Nobody", "Only friends")
                [self.__cur_user.get_access()[0].get_count() == 1], "All users"
            )
            [self.__cur_user.get_access()[0].get_count() == 0] +
            "\n2 - Back to the profile\n")

        if opt == "1":
            self.__data.change_settings(self.__cur_user.get_id(), 0)
            self.check_user(
                self.__cur_user.get_log(),
                self.__cur_user.get_pass()
            )
            self.settings()
        elif opt == "2":
            pass
        else:
            self.settings()

    def show_prof(self):
        print(
            f"\n\n{self.__cur_user.get_name()}",
            f"{self.__cur_user.get_surname()}"
        )
        choice = input(
            "1 - Search for a user" +
            "\n2 - My Wall\n3 - Publish a post" +
            "\n4 - My Friends\n5 - Settings\n6 - Log out\n"
        )

        if choice == "1":
            self.check_user(
                self.__cur_user.get_log(),
                self.__cur_user.get_pass()
            )
            self.search()
            self.show_prof()
        elif choice == "2":
            self.show_my_posts()
            self.show_prof()
        elif choice == "3":
            self.new_post()
            self.show_prof()
        elif choice == "4":
            self.check_user(
                self.__cur_user.get_log(),
                self.__cur_user.get_pass()
            )
            self.show_friends()
            self.show_prof()
        elif choice == "5":
            self.settings()
            self.show_prof()
        elif choice == "6":
            pass
        else:
            self.show_prof()
