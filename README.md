# Django Channels Chat
A small functional group message center application built using Django Channels.
![3](https://user-images.githubusercontent.com/20891667/80091830-97127280-8583-11ea-8668-415f4205db64.gif)


  ## Architecture ##
  - To use the system user should registered
  - When user logged in system redirect the user to a form page and ones input him/her respective room name
  - When user input the room name,he/she then enter the room chat and see the previous message they've exchanged in room chat.
  - The user status(online/offline) is dynamic.When user enter the chat room, status show online and when user left then the status show offline.
  - User can change him/her status manually.When user changed her status offline,all other member in the same room are see the user in offline through channel
  - When user send a message it can send to the other member in the same room
  - And when user type anything it notify to the other member that the user is typing as like facebook/whatsapp notify.
  
  ## Flow ##
  ```bash
  login ----> input chat room ---> start chatting
  ```
  
  ## Run ##
  
  1. Install requirements
  ```bash
  pip install -r requirements.txt
  ```
  2. Start Redis Server
  3. Migrate the changes of Database
  ```bash
  python manage.py migrate
  ```
  4. Create superuser
  ```bash
  python manage.py createsuperuser
  ```
  5. Run development server
  ```bash
  python manage.py runserver
  ```
  6. Open this url
  ```bash
  127.0.0.1:8000
  ```
