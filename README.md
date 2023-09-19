#  Pomodoro Watching iOS App

Pomodoro Watching iOS App is a productivity app, which builds on pomodoro technique, to help user focus on present and planning future. While this app have basic functionality such as timer, to-do list, records, notification, just like others productivity app. However, unlike traditional productivity app, Pomodoro Watching are more capable than that. By combining image recognition and Internet Of Things, Pomodoro Watching App can __actively monitor__ user outside the phone to the real world (by RPi4 camera). And determine the result of this pomodoro clock iteration is successful or not. 

## Note
Because the backend AWS cloud have been shutdown, so the app right now is not working.

## Main features
* Simple, beautiful, and intuitive interface.
* Task Management that sort tasks by time.
* Each task will track its dedicated completed pomodoro cycles and can marked as completed.
* Customize focus sessions and goals.
* Track your productivity with insightful charts.
* E-mail notification will be sent 5 mins before the task begin.
* Everyday's todos will be sent at user selected time.
* App's Pomodoro clock will automatically start when user sit in front RPi's camera (passive mode).
* App's Pomodoro clock will start if user click countdown(計時) button in main page (active mode).
* App's Pomodoro clock will restart if user left the camera.
* When pomodoro cycle ended, RPi will alarm