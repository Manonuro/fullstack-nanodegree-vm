from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Category, Base, Item, User

engine = create_engine('sqlite:///itemCatalogwithusers.db')
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


# Create dummy user
User1 = User(name="Manou Chehr", email="mnochb@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

User2 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User2)
session.commit()

#Item for Soccer
category1 = Category(user_id=1, name = "Soccer")

session.add(category1)
session.commit()

Item1 = Item(user_id=1, title = "Soccer Cleats", description = "The Shoes",
    category = category1)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, title = "Jersey", description = "The Shirt",
    category = category1)

session.add(Item2)
session.commit()

Item3 = Item(user_id=1,title = "Shin Gaurd",
    description = "A shin guard or shin pad, is a piece of equipment worn\
        on the front of a player's shin to protect it from injury. ",
    category = category1)

session.add(Item3)
session.commit()

Item4 = Item(user_id=1, title = "Shingaurds", description = "The Shingaurds",
    category = category1)

session.add(Item4)
session.commit()



#Item for Basketball
category2 = Category(user_id=2, name = "Basketball")

session.add(category2)
session.commit()

Item1 = Item(user_id=2, title = "Basketball", description = "A basketball is a\
    spherical ball used in basketball games. Basketballs typically range in\
    size from very small promotional items only a few inches in diameter to\
    extra large balls nearly a foot in diameter used in training exercises. ",
    category = category2)

session.add(Item1)
session.commit()

#Item for Baseball
category3 = Category(user_id=2, name = "Baseball")

session.add(category3)
session.commit()

Item1 = Item(user_id=2, title = "Bat", description = "A baseball bat is a\
 smooth wooden or metal club used in the sport of baseball to hit the ball\
 after it is thrown by the pitcher. ", category = category3)

session.add(Item1)
session.commit()



#Item for Frisbee
category4 = Category(user_id=1, name = "Frisbee")

session.add(category4)
session.commit()

Item1 = Item(user_id=1, title = "Frisbee", description = "A gliding toy or\
    sporting item that is generally made of injection molded plastic and\
    roughly 8 to 10 inches (20 to 25 cm) in diameter with a pronounced lip.",
    category = category4)

session.add(Item1)
session.commit()


#Item for Snowboarding
category5 = Category(user_id=1, name = "Snowboarding")

session.add(category5)
session.commit()

Item1 = Item(user_id=1, title = "Snowboard", description = "Snowboards are\
    boards where both feet are secured to the\
    same board, which are wider than skis, with the ability to glide\
    on snow.",
    category = category5)

session.add(Item1)
session.commit()

Item2 = Item(user_id=1, title = "Goggles", description = "Goggles, or safety\
    glasses, are forms of protective eyewear that usually enclose or protect\
    the area surrounding the eye in order to prevent particulates, water or\
    chemicals from striking the eyes",
    category = category5)

session.add(Item2)
session.commit()



#Item for Rock Climbing
category6 = Category(user_id=1, name = "Rock Climbing")

session.add(category6)
session.commit()



#Item for Foosball
category7= Category(user_id=1, name = "Foosball")

session.add(category7)
session.commit()



#Item for Skating
category8= Category(user_id=1, name = "Skating")

session.add(category8)
session.commit()



#Item for Hockey
category9= Category(user_id=1, name = "Hockey")

session.add(category9)
session.commit()

Item1 = Item(user_id=1, title = "Stick", description = "A hockey stick is a\
    piece of sport equipment used by the players in all the forms of hockey\
    to move the ball or puck", category = category9)

session.add(Item1)
session.commit()



print ("added category items!")
