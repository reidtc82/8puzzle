import tkinter as tk

# Singleton class as main of program
class Main:
    msg = 'This is main.'

    class __Main:
        def __init__(self, arg):
            self.val = arg
        def __str__(self):
            return repr(self) + self.val
    instance = None
    def __init__(self, arg):
        if not Main.instance:
            Main.instance = Main.__Main(arg)
        else:
            Main.instance.val = arg
    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __run__(self, arg):
        print(arg)

m = Main('Im Main')

m.__run__('Hello')
