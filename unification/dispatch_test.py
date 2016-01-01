from fs_dispatch import *


@dispatch_or("[a=1]", "[a=2]")
def say_hello(fs):
  print fs



say_hello("[a=2]")

# @dispatch("[level='morph']")
# def say_hello(fs):
#     print "Hello"



# try:
#     say_hello("[level='syntax']")
# except Exception as e:
#     print e


# try:
#     @inherit(say_hello, "[synsem=[cat='noun']]")
#     def say_hello_world(fs):
#         print "Hello World"
#     say_hello_world("[]")
# except Exception as e:
#     print e
