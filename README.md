# ***Witamy w oficjalnej dokumetacji strony internetowej projektu ZP!***

_**Szybkie uruchomienie**_

Mając pobrane nasze repozytorium  musimy zainstalować wwszystkie potrzebne bilbioteki do tego wykorzystujemy komendę: 
- pip install -r requiments.txt

Następnie musimy określić zmienne środowiskowe
Aby to zrobić należy wpisać w naszym środowsku (dla systemu windows):

- _set FLASK_APP=zp.py_
- _set SECRET_KEY=[SECRET KEY] // Podajmy tutaj nasz klucz który będzie szyfrować nam informacje_
- _set MAIL_USERNAME=[GMAIL EMAIL]_ //Podajemy swój email na portalu gmail. Należy pamiętać aby pozwolić aplikacją na dostęp do konta
- _set MAIL_PASSWORD=[GMAIL PASSWORD]_ // Podajemy hasło
- _set SQL_IP=[SQL_IP]_ // Podajemy IP naszej bazy danych (Narazie tylko mysql)
- _set SQL_DB=[SQL_DB]_ // Podajemy nazwe bazy danych na której bedziemy pracować
- _set SQL_NAME=[SQL_NAME]_ // Podajemy nazwe naszego użytkownika
- _set SQL_PASSWORD=[SQL_PASSWORD]_ // Podajemy hasło naszego użytkownika
***Discraimer*** Jeżeli nasz użytkownik nie ma hasło wpisujemy _set SQL_NAME=[SQL_PASSWORD_MODE]_= 0
- _set ADMIN=[ADMIN]_ // podajemy maila który po zarajestrowaniu będzie automatycznie administatorem

***Uruchomienie na localhoscie z użytkownikiem root bez hasła w db zp, powinno wyglądać nastepująco:***
- set SQL_PASSWORD_MODE=1
- set SQL_NAME=root 
- set SQL_DB =zp
- set SQL_IP=localhost


Dla systemu Linux lub MacOS

- _export FLASK_APP=sensopark.py_
- _export MAIL_USERNAME=[GMAIL EMAIL]_ 
- _export  MAIL_PASSWORD=[GMAIL PASSWORD]_
- _export  SQL_IP=[SQL_IP]_
- _export  SQL_DB=[SQL_DB]_ 
- _export  SQL_NAME=[SQL_NAME]_ 
- _export SQL_NAME=[SQL_PASSWORD]_ // Podajemy hasło naszego użytkownika
***Discraimer*** Jeżeli nasz użytkownik nie ma hasło wpisujemy _set SQL_NAME=[SQL_PASSWORD_MODE]_= 0
- _export  ADMIN=[ADMIN]_ 

### **Wybór innej bazy danych niż mysql**
W pliku config należy zmienić linijkę 34,39,43 (Domyślnie jest wybrana baza Mysql+pymysql)

postgresql://nazwa_użytkownika:hasło@nazwa_hosta/baza_danych

SQLite (Linux, macOS) sqlite:////bezwzględna/ścieżka/do/bazy_danych

SQLite (Windows) sqlite:///c:/bezwzględna/ścieżka/do/bazy_danych
### Utworzenie wszystkich tabel w bazie danych

**Kiedy nasz program połączy się z bazą danych należy wejść ponownie w nasze środowisko i wpisać komendy**
- _flask shell_
- _from app import db_
- _db.create_all()_
### Utworzenie wszystkich ról w bazie danych
- _from app import models_
- __models.Role.better_insert_role()__
- __models.Stats.stats_setup()__


### Znaczenie ról w naszym systemie
Administator
- Ma dostęp do wszystkiego tj. Panelu administatora gdzie może zmieniać informacje użytkowników, parkingów, rezerwacji etc.

Zarządca
- Ma dostęp do zarządzania swoim parkingiem tj. zmienianiem danych, rezerwacji itp.

Użytkownik
- Ma dostęp do zmieniania swoich informacji jak i do rezerwacji
## Funkcje strony Internetowej
- Rejestracja
-  Wysyłanie linków z potwierdzeniem konta
-  Logowanie
-  Obsługę Sesji użytkownika
-  Walidacje danych np. w logowaniu, rejestracji, tworzeniu parkingu
-  Stworzenie nowego Parkingu
-  Rezerwacji parkingów na daną godzinę i datę wraz ze specjalnym 
algorytmem uniemożliwiającym zarezerwowanie miejsca kiedy nie ma 
miejsca
- Obsługę uprawnień
- Zabezpieczenie Hasła za pomocą funkcji jednostronnej SHA256
- Panel Administatora
- Panel Menadżera
- Panel Użytkownika
- API (np. wykorzystywane m.in. do rezerwacji parkingu)
- Tworzenie odpowiednich dostępów dla danego typu użytkownika
- Stópka oraz pasek nawigacyjny są dziedziczone na każdej podstronie, 
umieszczone są w specjalnym pliku głównym
- Wyszukiwarkę po słowie kluczowym: Parkingu, użytkownika, zarządców 
itp.
- W zależności od uprawnienia możliwość modyfikacji danych (np. 
zarządca może zmieniać informacje tylko o swoim parkingu, admin do 
wszystkiego)
- I wiele wiele więcej!

# English

### Welcome to website SensoPark documentation!

## Fast Setup
Having downloaded our repository we must define local environ. Open local cmd and type the commands (For windows):
- _set FLASK_APP=sensopark.py_ 
- _set SECRET_KEY=[SECRET KEY] // Here we type the secret key
- _set_ MAIL_USERNAME=[GMAIL EMAIL]_ // Here we type the gmail adress (Remember to turn on a third person access in account settings) 
- _set_ MAIL_PASSWORD=[GMAIL PASSWORD] _// Type the password
- _set_ SQL_IP=[SQL_IP] _ // We enter the IP address in our database
- _set_ SQL_DB=[SQL_DB]_ // Here we type the name of database
- __set_ SQL_NAME=[SQL_NAME]_ // Here we enter the name of instance
- __set_ ADMIN=[ADMIN]_ // Here we enter mail adress that will automatically be the administrator after registration

For linux or MacOS
-_export FLASK_APP=sensopark.py_
-_export _ MAIL_USERNAME=[GMAIL EMAIL]_ 
-_export _ MAIL_PASSWORD=[GMAIL PASSWORD] _
-_export _ SQL_IP=[SQL_IP] _
-_export _ SQL_DB=[SQL_DB]_ 
-__export _ SQL_NAME=[SQL_NAME]_ 
-__export _ ADMIN=[ADMIN]_ 

### **Choosing a database other than MySQL**
In config file lines 34,39,43 should be changed to: (Deafult is Mysql+pymsql)

Postgresql://username:password@hostname/database

SQLite (Linux, macOS) sqlite:////absolute/path/to/the_file

SQLite (Windows) sqlite:///c:////absolute/path/to/the_file

### Create all of tabels in database
**When our program connects to database, open a local cmd and type: **
- _flask shell_
- _from app import db_
- _db.create_all()_

### Create all of Roles in database
- _from app import models_
- __models.Role.better_insert_role()__
- __models.Stats.stats_setup()__

### Types of Roles
Administator
- Has access to everything: 
- Admin Panel, where he can change the user's/parking's data, rezervations

Manager
- Has access to manage your parking lots, change data, rezervations etc.

User
- Has access to changes yours data, rezervations 
## Website functions
- Account registration
- Sending confirmation email
- Account login
- User session handling
- Data validation 
- Create a new parking
- Reservation for date and time with a special validation algorythm
- Handling of permissions
- Password protection with SHA256 one-way function
- Admin Panel
- Manager Panel
- User Panel
- API 
- Creating appropriate accesses for a given type of user
- Inherit navbar/sidebar
- Search engine by keyword: Parking lot, user, managers etc.
- And much much more!
