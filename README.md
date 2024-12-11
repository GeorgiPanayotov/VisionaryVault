# VisionaryVault

# 1. Visionary Vault App

       This is a platform for art lovers to upload, explore, and engage with through art.


# 2. Description
* VisionaryVault is a web application connecting art enthusiasts with stunning pieces. Users can create profiles to track interactions, browse collections, engage through comments and likes, and securely purchase art. The platform allows easy profile management, enabling users to edit or delete their profiles and artworks as needed.

# 3. Technologies Used

* **Django** – Web framework used to build the application.
* **Python** – Programming language for the backend.
* **Django REST Framework** – For building the API for interactions like comments, likes, and reporting, etc.
* **JavaScript** – For client-side interactions.
* **PostgreSQL** – Database used to store user data and art pieces.
* **HTML/CSS** – For frontend design and layout.
* **Cloudinary** - For better handling of media files

# 4. Installation
   **Step-by-step guide to setting up the project locally:** 


* **Clone the repository**

       git clone https://github.com/GeorgiPanayotov/VisionaryVault


* **Navigate into the project folder**

       cd your-project

* **Create and activate a virtual environment**

*      python -m venv venv
*      source venv/bin/activate  # On Windows: venv\Scripts\activate

* **Configure Environment Variables**

* Edit the.env file and fill in the required values, such as:

**SECRET_KEY:** A secret key for Django.

**Database connection settings:** (DB_NAME, DB_USER, DB_PASSWORD, etc.).

**DEBUG:** Set to True for development, False for production.

**ALLOWED_HOSTS:** Add your allowed hosts, separated by commas.



### - **Setup the Database:** 

**Install dependencies**


*     pip install -r requirements.txt


**Create migrations and then run them**

*     python manage.py makemigrations 
*     python manage.py migrate

**Run the development server**
*     python manage.py runserver


**Create a Superuser**
*     python manage.py createsuperuser


* _By default, the server runs on_

*     http://127.0.0.1:8000/.

**Running Tests**

* _Create a Superuser_
* _Tests are located in the tests package directories in Art & Accounts applications._


* _To run the tests:_

*     python manage.py test



# 5. User experience

#### **After user either Register or Log-in:**
![Screenshot of login and register](docs/img.png)


#### **Navigation bar appears on top for:** 
![Screenshot of the navigation bar](docs/img_1.png)


#### **Upload art: Share art pieces in various categories.**
![Screenshot of uploading art piece](docs/img_10.png)

#### **Interact with art: Like or comment on art pieces, even buy one:**
![Screenshot of like, comment, buy and report functionalities](docs/img_11.png)

#### **Report content: Report inappropriate art or users:**
![Screenshot of Report form](docs/img_12.png)

#### **Manage profile: Edit username, email, and password:**
![Screenshot of Profile details](docs/img_13.png)
![Screenshot of editable information in Profile](docs/img_5.png)

#### **Basket for better managing of user's purchases**
![Screenshot of the Basket view ](docs/img_14.png)

#### **View and follow reported content: Moderators and shift managers can manage content reports and user bans.**
![Screenshot of a view of reported content](docs/img_16.png)

#### **Password reset: Customers can reset their password via email.**
![Screenshot of password reset functionality](docs/img_15.png)

# 6. Contributing

_Contributions to improve VisionaryVault are very welcome!  To contribute:_

* Fork the repository.
* Create a new branch for your feature or bug fix.
* Make your changes and commit them.
* Push to your forked repository.
* Open a pull request to the main branch of the original repository.

# 7. License
 _This project is licensed under the MIT License. See the LICENSE file for more details._

# 8. Contact

_For any questions or feedback, feel free to contact:_
* **Email:** georgipanayotov1995@gmail.com
* **GitHub:** https://github.com/GeorgiPanayotov/VisionaryVault