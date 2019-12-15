class Cat:
    def __init__ (self,name,age):
        self.name = name
        self.age = age

    def voice(self):
        return "にゃー"

nyan = Cat("にゃん",4)


print(nyan.voice())
