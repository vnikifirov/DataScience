import Cat as CatModel
import Cattery as CatteryModel

# Info ℹ️
# Lib pyrserve: https://anaconda.org/conda-forge/pyrserve

#INIT------------------------------------------- 
cat = CatModel.Cat("Scoda", "British", "6 KG")
staff = ["FirstName: Amelia"]
pets = [cat]
cattery = CatteryModel.Сattery("British Cats Cattery", staff, pets)

print(cattery.ToString())