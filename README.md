# DjangoRestFW
Django RestApi Development Project.

This is a Django Practice Project for creating WebApi's without using the Django Rest FrameWork.
Requirements :
LANGUAGE: Python 3.6.5 
FRAMEWORK : Django Latest Version 
DATABASE : sqlite3

Steps to Execute Project:

Install VirtualEnv : pip install virtalenv 
Create VirtualEnv : virtualenv venv 
Install requirements : Navigate to~~~~ requirements file path and execute the following command. pip install -r requirements.txt

This project is created to perform CRUD operations using the djangorestframework's serializers concept.
In this project 2 kinds of serializers are used , one is normal serializer and another one is ModelSerializer.
In Normal Serializer - 
     We need to write code to post and update the data into the database , we need to specify those methods manually.
In Model Serializer - 
    We don't need to specify create() and update() methods, automatically ModelSerializer will take care.
    
    URL : {localhost}/api - to access all api methods.
