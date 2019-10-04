from browser import Browser


users = open("users.txt", "a")
posts = open("posts.txt", "a")
settings = open("settings.txt", "a")
friends = open("friends.txt", "a")

users.close()
posts.close()
settings.close()
friends.close()

obj = Browser()
obj.set_domain()
while True:
    obj.main_menu()
