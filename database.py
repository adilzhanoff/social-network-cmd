from user import User
from post import Post
from friend import Friend
from enumpy import Enum


class Database:
    # constructor
    def __init__(self):
        self.__users_in = None  # file object to read users.txt
        self.__users_out = None  # file object to write in users.txt
        self.__posts_in = None  # file object to read posts.txt
        self.__posts_out = None  # file object to write in posts.txt
        self.__settings_in = None  # file object to read settings.txt
        self.__settings_out = None  # file object to change settings.txt
        self.__friends_in = None  # file object to read friends.txt
        self.__friends_out = None  # file object to change friends.txt

    # functions
    def get_user_friends(self, usr_id=None):
        """
        returns list of 'Friend' objects,
        of a given user with 'usr_id'
        """
        all_friends = []
        with open("friends.txt", "r") as self.__friends_in:
            for line in self.__friends_in:
                usr_friends = Friend()
                lst_friends = []
                sent_requests = []
                id = int(line[:line.find(' ')])

                if any([id == usr_id, usr_id is None]):
                    usr_friends.set_id(id)
                    line = line[line.find('['):]

                    while line.find(']') != -1:
                        temp = line[line.find('[') + 1:line.find(']')]
                        temp = temp.split()
                        temp = [int(temp[idx]) for idx in range(len(temp))]

                        if 0 in temp[1:]:
                            sent_requests.append(temp)
                        elif 1 in temp[1:]:
                            lst_friends.append(temp)

                        line = line[line.find(']') + 2:]

                    usr_friends.set_list(lst_friends)
                    usr_friends.set_sent(sent_requests)
                    all_friends.append(usr_friends)

        return all_friends

    def get_users(self):
        """
        returns all users as a list of 'User' objects
        """
        users = []
        with open("users.txt", "r") as self.__users_in:
            with open("settings.txt", "r") as self.__settings_in:
                for (usr, sttng) in zip(self.__users_in, self.__settings_in):
                    temp_usr = User()
                    temp_sttng = [Enum(3)]
                    usr = usr.split()
                    sttng = sttng.split()
                    sttng = [int(sttng[i]) for i in range(len(sttng))]

                    for idx in range(len(sttng) - 1):
                        temp_sttng[idx].set_count(sttng[idx + 1])

                    temp_usr.set_id(int(usr[0]))
                    temp_usr.set_log(usr[1])
                    temp_usr.set_name(usr[2])
                    temp_usr.set_surname(usr[3])
                    temp_usr.set_pass(usr[4])
                    temp_usr.set_access(temp_sttng)
                    temp_usr.set_friends(
                        self.get_user_friends(temp_usr.get_id()).pop()
                    )
                    users.append(temp_usr)

        return users

    def get_posts(self, crt=None):
        """
        returns all posts as list of 'Post' objects,
        'crt' - id of the publisher
        """
        posts = []
        with open("posts.txt", "r") as self.__posts_in:
            for line in self.__posts_in:
                temp = Post()
                line = line.split()

                if any([crt is None, int(line[0]) == crt]):
                    temp.set_crt(int(line[0]))
                    temp.set_id(int(line[1]))
                    temp.set_txt(' '.join(line[2:]))

                    posts.append(temp)

        return posts

    def search_users(self, query, usr_id):
        """
        'query' - name/login/surname to search,
        'usr_id' - id of the query sender
        """
        found_users = []
        query = query.lower()

        with open("users.txt", "r") as self.__users_in:
            for line in self.__users_in:
                # creates a temp 'User' object,
                # since the original one will be modified
                line, back_up = line.split(), line.split()
                temp = User()

                for idx in range(1, 4):
                    # converts all uppercase
                    # characters to lower case
                    line[idx] = line[idx].lower()

                if any([
                            # if login contains 'query'
                            line[1].find(query) != -1,
                            # if name contains 'query'
                            line[2].find(query) != -1,
                            # if surname contains 'query'
                            line[3].find(query) != -1,
                            # if name + surname contains 'query'
                            ' '.join(line[2:4]).find(query) != -1,
                            # if surname + name contains 'query'
                            ' '.join(line[3:1:-1]).find(query) != -1
                        # if the query sender and an id
                        # that is searched are not the same
                       ]) and int(line[0]) != usr_id:

                    # if conditions above are met save current user as 'temp'
                    temp.set_id(int(back_up[0]))
                    temp.set_log(back_up[1])
                    temp.set_name(back_up[2])
                    temp.set_surname(back_up[3])
                    temp.set_pass(back_up[4])
                    # append it to 'found_users'
                    found_users.append(temp)

        return found_users

    def request_handler(self, snd_id, rec_id, opr):
        """
        'snd_id' - request sender,
        'rec_id' - request receiver
        """
        friends = []
        if opr == 0:  # sending request
            with open("friends.txt", "r") as self.__friends_in:
                fin = self.__friends_in.readlines()
                with open("friends.txt", "w") as self.__friends_out:
                    for line in fin:
                        if int(line[:line.find(' ')]) == rec_id:
                            line = line[:-1] + " [" + str(snd_id) + " 0]\n"
                            friends.append(line)
                        else:
                            friends.append(line)
                    self.__friends_out.writelines(friends)
        # accepting request
        elif opr == 1:
            with open("friends.txt", "r") as self.__friends_in:
                fin = self.__friends_in.readlines()
                with open("friends.txt", "w") as self.__friends_out:
                    for line in fin:
                        if int(line[:line.find(' ')]) == snd_id:
                            line = line[line.find('['):]
                            line = f"{snd_id} [{rec_id} 1] {line}"
                            friends.append(line)
                        elif int(line[:line.find(' ')]) == rec_id:
                            line = list(
                                line.partition("[" + str(snd_id) + " 0]")
                            )
                            line = line[0] + line[2][1:] + "\n"
                            line = (f"{rec_id} [{snd_id} 1]" +
                                    f"{line[line.find('['):]}")
                            friends.append(line)
                        else:
                            friends.append(line)
                    self.__friends_out.writelines(friends)
        elif opr == 2:
            with open("friends.txt", "r") as self.__friends_in:
                fin = self.__friends_in.readlines()
                with open("friends.txt", "w") as self.__friends_out:
                    for line in fin:
                        if int(line[:line.find(' ')]) == rec_id:
                            line = list(line.partition(f"[{(snd_id)} 0]"))
                            line = line[0] + line[2][1:] + "\n"
                            friends.append(line)
                        else:
                            friends.append(line)
                    self.__friends_out.writelines(friends)

    def remove_friend(self, usr_id, fr_id):
        friends = []
        with open("friends.txt", "r") as self.__friends_in:
            fin = self.__friends_in.readlines()
            with open("friends.txt", "w") as self.__friends_out:
                for line in fin:
                    if int(line[:line.find(' ')]) == usr_id:
                        line = list(line.partition("[" + str(fr_id) + " 1]"))
                        line = str(
                                (line[0], line[0][:-1])
                                [line[0].find('[') == -1] +
                                (line[2][1:], line[2])
                                [line[0].find('[') == -1]
                               )
                        friends.append(line)
                    elif int(line[:line.find(' ')]) == fr_id:
                        line = list(line.partition("[" + str(usr_id) + " 1]"))
                        line = str(
                                (line[0], line[0][:-1])
                                [line[0].find('[') == -1] +
                                (line[2][1:], line[2])
                                [line[0].find('[') == -1]
                               )
                        friends.append(line)
                    else:
                        friends.append(line)
                self.__friends_out.writelines(friends)

    def change_settings(self, usr_id, ind):
        settings = []
        with open("settings.txt", "r") as self.__settings_in:
            fin = self.__settings_in.readlines()
            for idx in range(len(fin)):
                fin[idx] = fin[idx].split()

            with open("settings.txt", "w") as self.__settings_out:
                for idx in range(len(fin)):
                    if fin[idx][:1] == [str(usr_id)]:
                        fin[idx][ind + 1] = (
                            (str(int(fin[idx][ind + 1]) + 1), "0")
                            [fin[idx][ind + 1] == "2"]
                        )
                    settings.append(" ".join(fin[idx]) + "\n")
                self.__settings_out.writelines(settings)

    def push_user(self, usr=User()):
        """
        'usr' - object of the 'User' class
        """
        with open("users.txt", "a") as self.__users_out:
            self.__users_out.write(
                str(usr.get_id()) + " " + usr.get_log() + " " +
                usr.get_name() + " " + usr.get_surname() + " " +
                usr.get_pass() + "\n"
            )

        with open("settings.txt", "a") as self.__settings_out:
            self.__settings_out.write(
                str(usr.get_id()) + " " +
                str(usr.get_access()[0].get_count()) + "\n"
            )

        with open("friends.txt", "a") as self.__friends_out:
            lst = usr.get_friends().get_list()
            sent = usr.get_friends().get_sent()
            lst, sent = str(lst)[1:-1:1], str(sent)[1:-1:1]
            lst, sent = lst.replace(',', ''), sent.replace(',', '')

            self.__friends_out.write(
                str(usr.get_id()) + " " + lst + " " + sent + "\n"
            )

    def push_post(self, pst=Post()):
        """
        'pst' - object of the 'Post' class
        """
        with open("posts.txt", "a") as self.__posts_out:
            self.__posts_out.write(
                str(pst.get_crt()) + " " +
                str(pst.get_id()) + " " +
                pst.get_txt() + "\n"
            )

    def delete_post(self, pst_id):
        """
        'pst_id' - id of the post
        """
        posts = []
        with open("posts.txt", "r") as self.__posts_in:
            fin = self.__posts_in.readlines()
            with open("posts.txt", "w") as self.__posts_out:
                for line in fin:
                    if int((line.split())[1]) != pst_id:
                        posts.append(str(line))
                self.__posts_out.writelines(posts)
