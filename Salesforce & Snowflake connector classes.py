import pandas as pd
import numpy as np
import snowflake.connector
from simple_salesforce import Salesforce
import time
import smtplib
from email.message import EmailMessage




def SMTP_Emailer(content, receiver):
    msg = EmailMessage()
    msg['Subject'] = "Insert subject"
    msg['From'] = 'to@email.com'
    msg['To'] = [receiver, 'receiver@receiver.com']

    msg.set_content( f""" <p>Content goes here<br /> 

<br /> {content}
""",  subtype='html')


    with smtplib.SMTP('sendsmtp', 587 ) as s:
                s.send_message(msg)
                
                

class SnowReader:

    def __init__(self, user, passwordSNOW):
        self.user = user
        self.password = passwordSNOW
        self.account = "account"
        self.warehouse = 'warehouse'
        self.database = 'database'
        self.role = 'role'
        self.schema = 'schema'

    def __connect__(self):
        try:
            self.ctx = snowflake.connector.connect(
                                        user = self.user, 
                                        password = self.password,
                                        account = self.account,
                                        warehouse = self.warehouse,
                                        database = self.database,
                                        role = self.role,
                                        schema = self.schema
                                        )
            print("You are connected to Snowflake") 
        except Exception as ex:
            if ex.errno == 250001:
                print(f"Invalid username/password, please re-enter username and password..")
    
    def GetSnowSQL(self,sql):
        self.__connect__()
        self.cur = self.ctx.cursor()

        print ("sending sql statement to Snowflake...")

        try:
            grab_data= self.cur.execute(sql)
            print("Converting data to dataframe..")
            self.data_in_frame = grab_data.fetch_pandas_all()
        except Exception as e:
            print(e)
            print('Error {0} ({1}): {2} ({3})'.format(e.errno, e.sqlstate, e.msg, e.sfqid))

        return self.data_in_frame
    
    def CloseConnection(self):
        self.ctx.close()



class SF_Reader:
    def __init__(self) -> None:
        self.instance_url = 'salesforce.com'
        self.username = user
        self.password = passwordSF
        self.orgId = 'orgID'
    
    def ConnectSF(self):
        self.sf= Salesforce ( instance_url = self.instance_url,
                         username = self.username, 
                         password = self.password,
                         organizationId = self.orgId) 
        print("Connected to Salesforce") 

    def GetSFSQL(self,sql, columnfix=None):
        '''Use this to pull Salesforce Queries
        If your column is a nested dictonary type, use columnfix.

        columnfix uses pd.json_normalize'''
        self.ConnectSF()
        print('Grabbing data, please wait...')
        self.sf = self.sf.query_all(sql)
        self.sfdf = pd.DataFrame(self.sf['records']).drop(['attributes'], axis=1)
        if columnfix == None:
            return self.sfdf        
        else:
            self.sfdf[columnfix] = self.sfdf[columnfix].fillna({i: {} for i in self.sfdf.index})
            self.sfdf = pd.json_normalize(self.sfdf[columnfix])
            print(self.sfdf)
            return self.sfdf


#optional timing info
#start_time = time.time()
#print("My program took", time.time() - start_time, "seconds to run")
       