## <div align="center">Virtual Xperience</div>

---

## <div align="center">Advanced programming project</div>


---

### Introduction:

Welcome to the Virtual Xperience project! In the wake of the global COVID-19 pandemic, the way we live, work, and connect with others has undergone a profound transformation. With restrictions on physical gatherings and a shift towards remote work and education, the demand for effective virtual collaboration tools has never been higher.

Virtual Xperience emerges as a response to this new reality, providing a versatile platform for organizing, managing, and participating in virtual events. As remote work and online learning become increasingly common, the need for reliable and immersive virtual event solutions has become more apparent than ever.

Our platform is designed to empower users to create and join virtual events seamlessly, whether it's a team meeting, a professional conference, or a virtual social gathering. By harnessing the latest web technologies and real-time communication tools, Virtual Xperience offers a dynamic and interactive environment for users to connect and collaborate remotely.

Join us on this journey as we navigate the evolving landscape of remote work and education, and discover new ways to foster engagement and interaction in the virtual space. Together, we can redefine the future of virtual events and unlock new opportunities for remote collaboration and community building.

---

### Usage:

#### 1. Registration and Login

- Registration: Users can create an account by providing a unique username, email, and password. This process ensures secure access to the platform.
- Login: Registered users can log in using their credentials to access their personalized dashboard.

#### 2. Event Creation and Management

- Create Events: Organizers can create virtual events by providing details such as event name, date, description, and privacy settings (public or private).
- Manage Events: Organizers can add activities, assignments, and materials (documents and videos) to their events. They can also manage participants and restrict access to certain users.

#### 3. Participating in Events

- Event Sign-Up: Participants can browse and sign up for public events. For private events, participants need to enter a password provided by the organizer.
- Activity Interaction: Participants can view and interact with activities and assignments associated with the events they have joined.

#### 4. Real-Time Interaction

- Comments and events: The platform provides real-time communication tools, such as chat and forums, to facilitate interaction among participants and organizers.
- Feedback Submission: Participants can provide feedback and suggestions about the events, which organizers can review to make improvements.

#### 5. Dashboard and Calendar

- Dashboard: Users can view their upcoming events, activities, and assignments on their personalized dashboard.
- Calendar: The built-in calendar allows users to keep track of their schedule, including all registered events and related activities.

#### 6. Administrative and Security Features

- User Management: Only registered users can access the platform. Organizers can manage event participants and control access to event materials.
- Privacy and Security: The platform ensures user data security with password hashing and secure authentication methods.

#### 7. Viewing and Submitting Activities

- Activity Submission: Participants can submit their assignments through the platform. Organizers can set deadlines and monitor submissions.
- Viewing Activities: Participants can view details of each activity, including deadlines and submission statuses.

#### 8. Announcements

- Publishing Announcements: Organizers can publish announcements to keep participants informed about important updates and deadlines.
- Accessing Announcements: Participants can view announcements related to their events and activities on the event page.

#### 9. Navigation

- User Interface: The platform features a clean and intuitive interface with a predominantly black and white color scheme for enhanced readability and accessibility.
- Navigation: Users can easily navigate through the platform using a structured URL system, making it simple to access different sections like the home page, login, register, dashboard, and event pages.

---

### Class diagram

---

![alt text](<diagrmas de actividad-Página-18.drawio.png>)

this diagram explain the interactions between classes

---

### Dependences:

#### Backend

- Python: Version 3.8 or higher
- Django: For web framework
- Django REST framework: For building APIs
- SQLAlchemy: ORM for database interaction
- PostgreSQL: Database management
- Django CORS Headers: For handling Cross-Origin Resource Sharing
- bcrypt: For password hashing

#### Frontend

- HTML/CSS/JavaScript: Basic web technologies
- djangorestframework-jwt: For JSON Web Token authentication

#### Database

- PostgreSQL: Relational database management system

#### Docker

- Docker Engine: For containerization

All this requirements are written in .txt files, so you can install them easier.

---

### Installation

To install all dependencies, follow these steps:

#### Backend:


pip install -r requirements_backend.txt


#### Frontend:


pip install -r requirements.txt


#### Docker:



docker-compose up --build


This setup ensures that all necessary dependencies are installed for both development and production environments.

---
### Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

### Authors

- Sergio Nicolás Mendivelso - @SaiLord28 - snmendivelsom@udistrital.edu.co
- Daniel Santiago Pérez - @dspm2212 - dsperezm@udistrital.edu.co

---

### LICENSE

This project was developed as part of a Universidad Distrital Francisco Jose de Caldas course and is intended for educational purposes only. Redistribution and use of this code, with or without modification, are permitted provided that the following conditions are met:

1. Proper attribution must be given to the original authors.
2. The code may not be used for commercial purposes.
3. This notice must be included in all copies or substantial portions of the code.

The project is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the project or the use or other dealings in the project.