# Snowflake-and-Salesforce-Connect

This is a Python Class that uses simple_salesforce,  snowflake.connector, smtlib, email.message 

I built this file as a way to connect with snowflake and Veeva data sources. The goal is to use this code as a base file so that anytime a connection from either of
those two sources are needed then a user can quickly copy and paste this info in to get started.

I've added an email feature that has the capibilities of notifcation to a user or user group via Email. The Email uses smtplib and the content of the mail uses html code.  Users can also add a file to the output of the Email if so desired. 


Please note, its recommended that the user will need to create a seperate config file that contains a username and password for both Snowflake and Veeva systems. Additionally, the user will need to know the STMP host information before sending a file via Email. 
