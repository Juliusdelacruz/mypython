Login Endpoint: POST http://localhost:5000/api/users/login
{"email": "admintest@yahoo.com", "password": "pythontest1"}

List all Users: GET http://localhost:5000/api/users

Create New User: POST http://localhost:5000/api/users/newuser
{"name": "testuser1", "password": "testpass1", "email": "testuser1@yahoo.com"}   

Change Password: POST http://localhost:5000/api/users/changepassword

{"email": " testuser1@yahoo.com ", "newpassword": "change1"}

Delete user: POST http://localhost:5000/api/users/deleteuser
{"email": "testuser1@yahoo.com"}   

Logout: GET http://localhost:5000/api/users/logout

