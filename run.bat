@echo off
call env\Scripts\activate  // Adjust path if necessary
cd voice-talk
cd talkingman
start cmd /k "python manage.py runserver"
timeout /t 5  // Wait for 5 seconds to allow the server to start
start microsoft-edge:http://127.0.0.1:8000 