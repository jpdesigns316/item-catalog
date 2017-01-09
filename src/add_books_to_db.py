from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Books, Base, Language, User

engine = create_engine('postgresql://catalog:catalog123@localhost/catalog')
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


# Adding initial Admin for the generated books
admin = User(name="Jonathan Peterson",
             email="preachingsquirrel@yahoo.com",
             picture="https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M/photo.jpg")
session.add(admin)
session.commit()

languages = ["C++",
             "HTML",
             "Java",
             "Javascript",
             "Python/Django",
             "Ruby/Rails"]

for lang in range(0,len(languages)):
    language = Language(language=languages[lang])
    session.commit()
    session.add(language)

books = [Books(book_img="https://images-na.ssl-images-amazon.com/images/I/515iBchIIzL._SX379_BO1,204,203,200_.jpg",
               book_title="Learning-Python-,5th Edition",
               book_author="Mark Lutz",
               book_description="Get a",
               book_url="https://www.amazon.com/Learning-Python-5th-Mark-Lutz/dp/1449355730/ref=sr_1_1?ie=UTF8&qid=1468705267",
               language_id=5,
               user_id=1),
               Books(book_img="https://images-na.ssl-images-amazon.com/images/I/51V2KZzUFhL._SX382_BO1,204,203,200_.jpg",
               book_title="Learning Python the Hard Way",
               book_description="In Learn Python the Hard Way, Third Edition, you'll learn Python by working through 52 brilliantly crafted exercises. Read them. Type their code precisely. (No copying and pasting!) Fix your mistakes. Watch the programs run. As you do, you'll learn how software works; what good programs look like; how to read, write, and think about code; and how to find and fix your mistakes using tricks professional programmers use.",
               book_author="Zed C. Shaw",
               book_url="https://www.amazon.com/Learn-Python-Hard-Way-Introduction/dp/0321884914/ref=sr_1_10?ie=UTF8&qid=1468705474",
               language_id=5,
               user_id=1),
               Books(book_img="https://images-na.ssl-images-amazon.com/images/I/516CL5AVKVL._SX406_BO1,204,203,200_.jpg",
               book_title="Java: The Complete Reference, Ninth Edition",
               book_author="Herbert Schildt",
               book_description="<p>Fully updated for Java SE 8, <i>Java: The Complete Reference</i>, Ninth Edition explains how to develop, compile, debug, and run Java programs. Bestselling programming author Herb Schildt covers the entire Java language, including its syntax, keywords, and fundamental programming principles, as well as significant portions of the Java API library. JavaBeans, servlets, applets, and Swing are examined and real-world examples demonstrate Java in action. New Java SE 8 features such as lambda expressions, the stream library, and the default interface method are discussed in detail. This Oracle Press resource also offers a solid introduction to JavaFX.</p>  <p><b>Coverage includes:</b><ul> <li>Data types, variables, arrays, and operators <li>Control statements <li>Classes, objects, and methods <li>Method overloading and overriding <li>Inheritance <li>Interfaces and packages <li>Exception handling <li>Multithreaded programming <li>Enumerations, autoboxing, and annotations <li>The I/O classes <li>Generics <li>Lambda expressions <li>String handling <li>The Collections Framework <li>Networking <li>Event handling <li>AWT and Swing <li>The Concurrent API <li>The Stream API <li>Regular expressions <li>JavaFX <li>JavaBeans <li>Applets and servlets <li>Much, much more</ul></p>",
               book_url="https://www.amazon.com/Java-Complete-Reference-Herbert-Schildt/dp/0071808558/ref=sr_1_2?ie=UTF8&qid=1468705604&sr=8-2",
               language_id=3,
               user_id=1),
               Books(book_img="https://images-na.ssl-images-amazon.com/images/I/41lk-OhRE7L._SX331_BO1,204,203,200_.jpg",
               book_title="C++: The Ultimate Beginner's Guide",
               book_author="Anderw Johansen",
               book_description="<h2>C++... Master It Today! </h2><br />This book is written for people who want to learn the basics of the C++ programming language. If you are looking for a comprehensive book that will teach you everything you need to know about C++, this just might be what you&#x2019;re looking for.<br /><br />By reading this book, you&#x2019;ll learn the basics of C++. You&#x2019;ll discover the ideas, concepts, techniques, and methods used by expert C++ programmers. For example, this book will discuss variables, strings, functions, and data structures. That means you&#x2019;ll be able to write programs using the C++ language after reading this material.<br /><br /><ul><li> The Basic Syntax of the C++ Programming Language </li><li>The Different Data Types and Variable Types in C++ </li><li>The Operators in the C++ Language</li><li>The Different Types of Loops in C++</li> <li>The Different Functions in C++</li> <li> Much, much more!",
               book_url="https://www.amazon.com/Ultimate-Beginners-Guide-Andrew-Johansen/dp/1523416920/ref=sr_1_2?ie=UTF8&qid=1468705721",
               language_id=1,
               user_id=1),
               Books(book_img="https://images-na.ssl-images-amazon.com/images/I/41jRdedMPIL._SX403_BO1,204,203,200_.jpg",
               book_title="Learn Ruby On Rails For Web Development: Learn Rails The Fast And Easy Way!",
               book_author="John Elder",
               book_description="Learning Ruby on Rails has never been this fast and easy, or fun!<br> <br> Veteran Codemy.com programmer John Elder walks you step by step through the ins and outs of Rails for Web Development. &#xA0;Written for the absolute beginner, you don't need any programming experience to dive in and get started with this book.&#xA0;<br> <br> Follow along as John builds a Pinterest-style website from start to finish that allows people to sign up, log in and out, edit their profile, upload images to the database and style those images on the screen.<br> <br> By the end, you'll be well on your way to becoming a professional Ruby on Rails coder!",
               book_url="https://www.amazon.com/Learn-Ruby-Rails-Web-Development/dp/0692364218/ref=sr_1_2?s=books&ie=UTF8&qid=1471300734&sr=1-2",
               language_id=6,
               user_id=1),
               Books(book_img="https://images-na.ssl-images-amazon.com/images/I/51lUPcbwFHL._SX348_BO1,204,203,200_.jpg",
               book_title="Beginning Python Games Development, Second Edition: With PyGame 2nd ed. Edition",
               book_author="Will McGugan ",
               book_description="Beginning Python Games Development, Second Edition teaches you how to create compelling games using Python and the PyGame games development library. It will teach you how to create visuals, do event handling, create 3D games, add media elements, and integrate OpenGL into your Python game.",
               book_url="https://www.amazon.com/Beginning-Python-Games-Development-Second/dp/1484209710/ref=sr_1_6?s=books&ie=UTF8&qid=1471796295&sr=1-6",
               language_id=5,
               user_id=1),
               Books(book_img="https://images-na.ssl-images-amazon.com/images/I/51LH36eCyaL._SX376_BO1,204,203,200_.jpg",
               book_title="Beginning Python: From Novice to Professional 1st Edition",
               book_author="Magnus Lie Hetland",
               book_description="Beginning Python: From Novice to Professional is the most comprehensive book on the Python ever written. Based on Practical Python, this newly-revised book is both an introduction and practical reference for a swath of Python-related programming topics, including addressing language internals, database integration, network programming, and web services. Advanced topics, such as extending Python and packaging/distributing Python applications, are also covered.",
               book_url="https://www.amazon.com/Beginning-Python-Professional-Magnus-Hetland/dp/159059519X/ref=sr_1_2?s=books&ie=UTF8&qid=1471796398&sr=1-2",
               language_id=6,
               user_id=1),
               Books(book_img="https://images-na.ssl-images-amazon.com/images/I/41bHkcO7MbL._SX402_BO1,204,203,200_.jpg",
               book_title="Beginning C++ Through Game Programming 3rd Edition",
               book_author="Michael Dawson",
               book_description="BEGINNING C++ THROUGH GAME PROGRAMMING, THIRD EDITION approaches learning C++ from the unique and fun perspective of games. Written for the beginning game developer or programmer, the book assumes no previous programming experience and each new skill and concept is taught using simple language and step-by-step instructions. Readers will complete small projects in each chapter to reinforce what they've learned and a final project at the end combines all of the major topics covered in the book. Featuring twenty five percent new material, this third edition covers all the latest technology and advances.",
               book_url="https://www.amazon.com/Beginning-C-Through-Game-Programming/dp/1435457420/ref=sr_1_2?s=books&ie=UTF8&qid=1471796566&sr=1-2",
               language_id=1,
               user_id=1),
               Books(book_img="https://images-na.ssl-images-amazon.com/images/I/51b5ByiFZjL._SX379_BO1,204,203,200_.jpg",
               book_title="Killer Game Programming in Java 1st Edition",
               book_author="Andrew Davison",
               book_description="Although the number of commercial Java games is still small compared to those written in C or C++, the market is expanding rapidly. Recent updates to Java make it faster and easier to create powerful gaming applications-particularly Java 3D-is fueling an explosive growth in Java games. Java games like Puzzle Pirates, Chrome, Star Wars Galaxies, Runescape, Alien Flux, Kingdom of Wars, Law and Order II, Roboforge, Tom Clancy's Politika, and scores of others have earned awards and become bestsellers.Java developers new to graphics and game programming, as well as game developers new to Java 3D, will find Killer Game Programming in Java invaluable. This new book is a practical introduction to the latest Java graphics and game programming technologies and techniques. It is the first book to thoroughly cover Java's 3D capabilities for all types of graphics and game development projects.Killer Game Programming in Java is a comprehensive guide to everything you need to know to program cool, testosterone-drenched Java games. It will give you reusable techniques to create everything from fast, full-screen action games to multiplayer 3D games. In addition to the most thorough coverage of Java 3D available, Killer Game Programming in Java also clearly details the older, better-known 2D APIs, 3D sprites, animated 3D sprites, first-person shooter programming, sound, fractals, and networked games. Killer Game Programming in Java is a must-have for anyone who wants to create adrenaline-fueled games in Java.",
               book_url="https://www.amazon.com/Killer-Game-Programming-Andrew-Davison/dp/0596007302/ref=sr_1_2?s=books&ie=UTF8&qid=1471796657&sr=1-2",
               language_id=3,
               user_id=1),
               Books(book_img="https://images-na.ssl-images-amazon.com/images/I/41Z2swEmwaL._SX396_BO1,204,203,200_.jpg",
               book_title="HTML and CSS: Design and Build Websites 1st Edition",
               book_author="John Duckett",
               book_description="Every day, more and more people want to learn some HTML and CSS. Joining the professional web designers and programmers are new audiences who need to know a little bit of code at work (update a content management system or e-commerce store) and those who want to make their personal blogs more attractive. Many books teaching HTML and CSS are dry and only written for those who want to become programmers, which is why this book takes an entirely new approach.",
               book_url="https://www.amazon.com/HTML-CSS-Design-Build-Websites/dp/1118008189/ref=sr_1_1?s=books&ie=UTF8&qid=1471796740",
               language_id=2,
               user_id=1),
               Books(book_img="https://images-na.ssl-images-amazon.com/images/I/41oa41LdNdL._SX400_BO1,204,203,200_.jpg",
               book_title="JavaScript and JQuery: Interactive Front-End Web Development 1st Edition",
               book_author="John Duckett",
               book_description="",
               book_url="https://www.amazon.com/JavaScript-JQuery-Interactive-Front-End-Development/dp/1118531647/ref=sr_1_1?s=books&ie=UTF8&qid=1471796827&sr=1-1",
               language_id=4,
               user_id=1)
               ]


for book in range(0,len(books)):
    session.add(books[book])
    session.commit()
