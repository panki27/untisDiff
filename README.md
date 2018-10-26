# untisDiff - Get alerted on your mobile when your schools' WebUntis timetable changes!

Tired of getting up in the morning and drive all the way to school, only to realize that your teacher is sick and the first 2 lessons are omitted?

Always end up infront of the wrong room because the lesson got inexplicably moved to a different one?

If you have these problems, this is the right tool for you!

## How it works

1. Open asopo.webuntis.com with a POST request specifying your school.
2. Store the resulting cookie.
3. Use this cookie to GET the print preview of todays timetable (this has nicer, but still horrible, HTML)
4. Extracts the table including the associated style and stores it in a pickle file.
5. Compares the checksum of this file with the one generated last time.
6. If the checksums don't match (i.e. something has changed in the timetable), alert the user with a PUSH notification.

## Requirements

0. [Google Firebase Cloud Messaging API Access for PUSH notifications](https://firebase.google.com/docs/cloud-messaging/)
1. Python3
2. [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) (pip3 install beautifulsoup4)
3. [pyfcm](https://pypi.org/project/pyfcm/) (pip3 install pyfcm)
4. Some client capable of receiving PUSH notifications (Android app, browser etc.)

## Setup

1. Clone this repository.
2. Put your FCM API key and user keys into the provided keyfile template. 
2. Edit the file "untisDiff.py"
3. Replace "PATH\_TO\_FILLED\_KEYFILE\_TEMPLATE" with a fully qualified path to the keyfile you just edited.
4. Visit [this site](https://webuntis.com/) and find your school by using the provided search box. Select it. Copy the parameter after '?school=' from the resulting URL (without the #). 
5. Replace 'YOUR\_SCHOOLNAME\_HERE' with this value
6. Now select the timetable for your class and hit the little "print" button. Copy the URL.
7. Replace 'URL\_TO\_PRINT\_PREVIEW' with this link. Replace the date parameter within with '%s'

Done! Try running it. 

`./untisDiff.py`

When running for the first time, the script will always send an alert (because it's comparing the timetable to nothing.) Subsequents runs should not send any more alerts, unless something has changed in the timetable.

If it works, you can set up a cronjob or similar. Basic logging is being printed to std_out.