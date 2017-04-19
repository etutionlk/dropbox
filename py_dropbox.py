#!/usr/bin/python3
import dropbox
import pymysql


# Open database connection
db = pymysql.connect("localhost","root","letmein","crmaccou_cbrm" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print ("Database version : %s " % data)

# disconnect from server
db.close()



# Get your app key and secret from the Dropbox developer website
app_key = 'ig6i3s3tb57trzi'
app_secret = 'gkkd7chtgusaoz7'

flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

# Have the user sign in and authorize this token
authorize_url = flow.start()
print ('1. Go to: ' + authorize_url)
print ('2. Click "Allow" (you might have to log in first)')
print ('3. Copy the authorization code.')
code = input("Enter the authorization code here: ").strip()


# This will fail if the user enters an invalid authorization code
access_token, user_id = flow.finish(code)

client = dropbox.client.DropboxClient(access_token)


#folder_metadata = client.metadata('/AAS CLIENTS')

f = open('python_db.sql','w',encoding='utf-8')

def insert_db(path,file_type,date,mcreate_date) :
    if file_type :
        type_f = '1'
    else :
        type_f = '0'
        
    sql = "REPLACE INTO dropbox_filelog(filepath,file_type,modified_time,client_modifiedtime) VALUES(\""+path+"\",\""+str(type_f)+"\",\""+str(date)+"\",\""+str(mcreate_date)+"\");"

    f.write(sql+"\n")
    print (path)

def recursive (path) :
    folder_metadata = client.metadata(path)

    for content in folder_metadata['contents'] :

        if 'client_mtime' in content:
            content['client_mtime'] = content['client_mtime']
        else :
            content['client_mtime'] = ""
            
        if content['is_dir'] == 1 :
            insert_db(content['path'],content['is_dir'],content['modified'],content['client_mtime'])
            recursive(content['path'])
        else :
            insert_db(content['path'],content['is_dir'],content['modified'],content['client_mtime'])
            

            

recursive ('/AAS CLIENTS')


