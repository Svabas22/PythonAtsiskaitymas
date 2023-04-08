
class Item:
    def __init__(self, name, quantity=1, price=float(10)): #Sukuriamas klases konstruktorius, su numatomom reiksmem 1 ir 10
        if not isinstance(name, str):   #tikrinama ar pavadinimas yra string
            raise TypeError('Name must be a string.')
        if not isinstance(quantity, int) or quantity < 1:   #Tirkinama ar kiekis yra sveikas skaicius
            raise ValueError('Quantity must be a positive integer.')
        if not isinstance(price, float) or price < float('0.00'):   #Tikrinama ar kaina yra teigiamas skaicius
            raise ValueError('Price must be a positive decimal.')
        self.name = name
        self.quantity = quantity
        self.price = price
    def get_total_price(self):
        return float(self.quantity * self.price)    #Grazinama prekiu kaina
    def full_info(self):
        return self.name + " " + str(self.price) + " " + str(self.quantity) + " " + str(self.get_total_price()) #Grazinamas rezultatas: preke, kaina, kiekis, visa kaina
    def to_dict(self):
        new_dict = { #Sukuriamas naujas zodynas
            'name': self.name,  #Rezultatai padalinami ir sustatomi i name, quantity, price, total_price
            'quantity': self.quantity,
            'price': float(self.price),
            'total_price': float(self.get_total_price()),
            "full": self.full_info()
        }
        return new_dict #Grazinamas zodynas
    
class Food(Item): #Aprašoma Maisto klasė
    def full_info(self): #Gražina teksta, sudaryta iš produkto pavadinimo kainos kiekio ir bendros kainos
        return f"Maistas {self.name} {self.price} {self.quantity} {self.price * self.quantity:.1f}"

class Drink(Item): #Aprašoma gėrimų klasė, ji yra "Food" vaikas
    def full_info(self): #Gražina teksta, sudaryta iš produkto pavadinimo kainos kiekio ir bendros kainos
        return f"Gėrimas {self.name} {self.price} {self.quantity} {self.price * self.quantity:.1f}"


f1 = Food("Batonas", 2, 1.3)
f2 = Food("Sviestas", 1, 1.3)

d1 = Drink("CocaCola", 3, 1.7)
d2 = Drink("Sprite", 2, 1.7)

print(f1.full_info())
print(f2.full_info())
print(d1.full_info())
print(d2.full_info())