import os
import json
from shop_items import Item, Food, Drink
def get_file_path(path): #Gražinamas pilnas, vartotojo įvestas kelias, jei neegzistuoja aplankalai, juos automatiškai sukuria
        path=path.replace("\.", "/")#visi pasviri bruksniai yra konvertuojami i viena tipa iš pasvirųjų brukšnių
        path_split = path.split("/")#išdalijami aplankalai
        full_path = os.getcwd()#gaunama dabartinė vieta
        for x in path_split:#Kol yra aplankalų pateiktoam kelyje, tol kurti tuos aplankalus
            full_path=os.path.join(full_path,x)
            if not os.path.isdir(full_path) and not "." in x:
                try:
                    os.mkdir(full_path)
                except OSError as e:
                    print(f"Error sukuriant aplankalą {full_path}: {e}")
                    return None
        return full_path


class Customer: #Aprašoma klijento klasė
    identifier = 0
    def __init__(self, name, items=[]): #Konstruktorius
        self.name = name #Kliento vardas 
        self.items = items #Prekiu sarašas
        self.identifier = Customer.identifier + 1#Kliento identifier
        Customer.identifier+=1
        
    def get_identifier(self):  # Grazina klientu identifikatoriu
        return str(self.identifier)

    def add_item(self, item): #Prideda prekes prie krepšelio
        self.items.append(item)

    def remove_item(self, index): #Pašalina prekes iš krepšelio
        try: #Atliekamas klaidų tikrinimas
            self.items.pop(index) #Pašalinamos prekės 
        except IndexError:
            print("Error removing item")

    def get_items(self): #Gražinamas visų prekių sąrašas
        try:
            return [item.full_info() for item in self.items]
        except:
            return f"Neimanoma iteruoti prekes"
    
    def export_to_json(self, path): #Eksportuoja vartotoją ir jo informaciją į json failą su json formatu
        full_path=get_file_path(path) # Gaunamas pilnas kelias iki failo vietos
        if not full_path:#Jeigu neteisingas kelias
            return
        vartotojo_prekes=[]
        for item in self.items: #Įrašomi visi vartotojo prekės
            vartotojo_prekes.append(item.to_dict()) #Sudedama informacija į sąrašą
        vartotojo_duomenys= {"name": self.name, "identifier": self.identifier, "items": vartotojo_prekes} #Įrašomi visi vartotojo duomenys
        try:
            with open(full_path, "w", encoding="utf8") as file_obj:#Sukuriamas(arba perrašomas) failas
                json.dump(vartotojo_duomenys, file_obj, ensure_ascii=False, indent=4) #Eksportuojama informacija
        except OSError as e:#Jeigu klaida įrašant failas
            print(f"Error rašant į failą {full_path}: {e}")
            
    @classmethod
    def from_json(cls, path): #Importuoja duomenis iš json failo ir gražina vartotoją
        try:
            full_path= get_file_path(path)# Gaunamas pilnas kelias iki failo vietos
            with open(full_path, 'r', encoding='utf8') as file_obj:#Atidaromas failas
                data = json.load(file_obj)#Gaunama informacija apie vartotoją
                name = data['name']
                items = []
                for item_data in data['items']: #Gaunama ir išsaugoma informacija apie prekes
                    item = Food(item_data['name'], item_data['quantity'], item_data['price']) if "Maistas" in item_data["full"] else Drink(item_data['name'], item_data['quantity'], item_data['price'])
                    items.append(item)
                vartotojas = cls(name, items)#Sukuriamas vartotojas
                vartotojas.identifier=data['identifier']
                return vartotojas#Gražinamas vartotojas
        except FileNotFoundError: #Jeigu nerastas failas
            print(f"Error atidarant failą {full_path}: failas nerastas")
            vartotojas=cls("Error", None)
            vartotojas.identifier=-1
            return vartotojas
        except json.JSONDecodeError:#Jeigu neteisingas failas
            print(f"Error dekoduojant JSON duomenis iš failo {full_path}")
            vartotojas=cls("Error", None)
            vartotojas.identifier=-1
            return vartotojas
    def full_info(self):#Suteikiama informacija apie vartotoją
        return f"{self.identifier} {self.name}"

c1 = Customer("Jonas Jonaitis", [Food("Batonas", 2, 1.3), Drink("CocaCola", 3, 1.7)])
c2 = Customer("Petras Petraitis", [Food("Sviestas", 1, 1.3), Drink("Sprite", 2, 1.7)])

print("Exporting to json")
print(c1.full_info())
print(c1.get_items())
print(c2.full_info())
print(c2.get_items())
c1.export_to_json("/tmp/c1.json")
c2.export_to_json("/tmp/c2.json")
print("Exported")
print("Importing from json")
c1=Customer.from_json("/tmp/c2.json")
c2=Customer.from_json("/tmp/c1.json")
print(c1.full_info())
print(c1.get_items())
print(c2.full_info())
print(c2.get_items())
