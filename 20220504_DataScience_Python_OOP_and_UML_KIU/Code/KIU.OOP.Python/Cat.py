class Cat(object):
    def __init__(self, name, breed, weight):
        self.Name = name
        self.Breed = breed
        self.Weight = weight

    def Play(self):
        return 'The cat with name {name} is playing 🎲'.format(name=self.Name)

    def Eat(self):
        return 'The cat with name {name} is eating 🍽️'.format(name=self.Name)

    def Speak(self):
        return 'The cat with name {name} tels "May! May! May!"'.format(name=self.Name)

    def ToString(self):
        return 'The cat with name {name}, cat has weight {weight}, cat has breed {breed}'.format(name=self.Name, breed = self.Breed, weight = self.Weight)




