class Сattery(object):
    def __init__(self, name, staff, pets):
        self.Name = name
        self.Staff = staff
        self.Pets = pets

    def GetPets(self):
        return ["".join(pet.ToString()) for pet in self.Pets]

    def GetStaff(self):
        return ["".join(person) for person in self.Staff]

    def ToString(self):
        return "Cattery name: {name} \n Pets in cattery {pets} \n Staff in cattery {staff}".format(name = self.Name, pets = self.GetPets(), staff = self.GetStaff())

