from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Manufacturer, Base, Car, User

engine = create_engine('postgresql://grader:grader@localhost/catalog')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

user1 = User(username = 'Vikrant Kadian', email = 'kadianvik@gmail.com')
session.add(user1)
session.commit()

manuf1 = Manufacturer(manufacturer="Toyota")
session.add(manuf1)
session.commit()

car1 = Car(user_id = user1.id, name = "Fortuner",
            description = "The Toyota Fortuner, also known as the Toyota SW4,is a mid-size SUV manufactured by Toyota.",
            manufacturer = manuf1.manufacturer)
session.add(car1)
session.commit()
car2 = Car(user_id = user1.id, name = "Camry",
            description = '''HYBRID ELECTRIC VEHICLE EXCLUSIVE INTERIOR ORNAMENTATION, HIGH DENSITY DASH SILENCER & ACOUSTIC WINDSHIELD GLASS''',
            manufacturer = manuf1.manufacturer)
session.add(car2)
session.commit()
car3 = Car(user_id = user1.id, name = "Inova",
            description = '''Automatically controls the brakes suppressing vehicle rollback when starting off on a slope, reducing the burden on the driver''',
            manufacturer = manuf1.manufacturer)
session.add(car3)
session.commit()

manuf2 = Manufacturer(manufacturer="Mercedes-Benz")
session.add(manuf2)
session.commit()

car4 = Car(user_id = user1.id, name = "Mercedes-Benz A-class",
            description = '''The Mercedes-Benz A-Class is a subcompact executive car (subcompact in its first two generations) produced by the German automobile manufacturer Mercedes-Benz''',
            manufacturer = manuf2.manufacturer)
session.add(car4)
session.commit()

manuf3 = Manufacturer(manufacturer="BMW")
session.add(manuf3)
session.commit()

car5 = Car(user_id = user1.id, name = "BMW i3 electric car",
            description = '''The BMW i3 is a B-class, high-roof hatchback manufactured and marketed by BMW with an electric powertrain using rear wheel drive via a single-speed transmission''',
            manufacturer = manuf3.manufacturer)
session.add(car5)
session.commit()
car6 = Car(user_id = user1.id, name = "BMW i8 plug-in hybrid",
            description = '''A plug-in hybrid electric vehicle (PHEV) is a hybrid electric vehicle whose battery can be recharged by plugging it in to an external source of electric power as well by its on-board engine and generator.''',
            manufacturer = manuf3.manufacturer)
session.add(car6)
session.commit()
car7 = Car(user_id = user1.id, name = "BMW M4 (F82)",
            description = '''BMW produce a number of high-performance derivatives of their cars developed by their BMW M GmbH (previously BMW Motorsport GmbH) subsidiary.''',
            manufacturer = manuf3.manufacturer)
session.add(car7)
session.commit()
car8 = Car(user_id = user1.id, name = "BMW M5 (F90)",
            description = '''BMW produce a number of high-performance derivatives of their cars developed by their BMW M GmbH (previously BMW Motorsport GmbH) subsidiary.''',
            manufacturer = manuf3.manufacturer)
session.add(car8)
session.commit()

manuf4 = Manufacturer(manufacturer="Audi")
session.add(manuf4)
session.commit()

car9 = Car(user_id = user1.id, name = "Audi A3",
            description = '''The Audi A3 was untouched since its launch in India back in 2015.''',
            manufacturer = manuf4.manufacturer)
session.add(car9)
session.commit()
car10 = Car(user_id = user1.id, name = "Audi A4",
            description = '''The battle between the Audi A4, BMW 3 Seriesand Mercedes-Benz C-Class has been chronicled over the last two decades''',
            manufacturer = manuf4.manufacturer)
session.add(car10)
session.commit()
car11 = Car(user_id = user1.id, name = "Audi A5",
            description = '''The new Audi A5 further expands the German car manufacturer presence in the country.''',
            manufacturer = manuf4.manufacturer)
session.add(car11)
session.commit()
car12 = Car(user_id = user1.id, name = "Audi A5 Cabriolet",
            description = '''The vehicle shares the engine and features from the A5 Sportback. To keep the price in check, Audi continues to offer most of the electronics from the A4''',
            manufacturer = manuf4.manufacturer)
session.add(car12)
session.commit()

manuf5 = Manufacturer(manufacturer="Ferrari")
session.add(manuf5)
session.commit()

car13 = Car(user_id = user1.id, name = "Ferrari 166 Inter",
            description = '''Ferrari 166 Inter Stabilimenti Farina Coupe. The Ferrari 166 Inter was Ferrari's first true grand tourer''',
            manufacturer = manuf5.manufacturer)
session.add(car13)
session.commit()

manuf6 = Manufacturer(manufacturer="Hyundai")
session.add(manuf6)
session.commit()

car14 = Car(user_id = user1.id, name = "Creta",
            description = '''CRETA Dual Tone comes with black roof and sporty black spoiler 
            to match your style statement.''',
            manufacturer = manuf6.manufacturer)
session.add(car14)
session.commit()

manuf7 = Manufacturer(manufacturer="Volkswagen")
session.add(manuf7)
session.commit()

car15 = Car(user_id = user1.id, name = "Beetle",
            description = '''The need for a people's car (Volkswagen in German), its concept and its functional 
            objectives, was formulated by the leader of Nazi Germany, Adolf Hitler''',
            manufacturer = manuf7.manufacturer)
session.add(car15)
session.commit()