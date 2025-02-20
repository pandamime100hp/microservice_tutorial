# microservice_tutorial

A microservice based application which I built while following along the tutorial found on freeCodeCamp.org. The application is a video to mp3 converter tool which is built using Python, rabbitmq, MongoDB and MySQL. The application is broken down into several services as below:

 - auth
 -- Authentication service providing a method for handling users when uploading and downloading.
 - authdb
 -- Authentication database which contains the user authentication data.
 - converter
 -- Converter service consumes the messages found in the queue which uses the input video file to generate the output mp3 file.
 - gateway
 -- Gateway service enables a frontend for end users to interact with the application, enabling users to upload/download.
 - mediadb
 -- Media database is the MongoDB BLOB database which handles the file storage.
 - notification
 -- Notification service is used to notify the end user when their uploaded file has completed the conversion and is ready to download by sending the user an email.
 - queue
 -- Queue service is the messaging event bus where events are passed around between services to process data.