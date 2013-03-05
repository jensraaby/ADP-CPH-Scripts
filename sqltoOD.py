#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
import psycopg2.extras
import sys
from subprocess import check_output,call,Popen
import subprocess
import os

# Settings for LDAP
ldap_host = ""
ldap_user = ""
ldap_pw = ""
primary_gid = ''
group = "" 

# Store the list of current usernames:
existing_users = []
def populateUsers():
    users = subprocess.Popen("dscl /LDAPv3/" + ldap_host + " -list /Users",shell=True,stdout=subprocess.PIPE)
    for user in users.stdout:
        existing_users.append(user.strip())
    
    


def getNextUID():
    # lookup the largest current UID and add 1
    cmd = "dscl /LDAPv3/"+ ldap_host +" -list /Users UniqueID | awk '{print $2}' | sort -ug | tail -1"
    biggest = check_output(cmd,shell=True)
    return int(biggest)+1


# makes the PostgreSQL schema
def createUsersTable(cursor):
    users = "CREATE TABLE AD_users (sAMAccountName varchar(50) PRIMARY KEY, \
    mail varchar(100) UNIQUE NOT NULL,\
    userPrincipalName varchar(100) UNIQUE NOT NULL,\
    givenName varchar(50) NULL,\
    sn varchar(50) NULL,\
    displayName varchar(50) NULL,\
    telephoneNumber varchar(50) NULL,\
    dateAdded timestamp DEFAULT current_timestamp);"
    print 'Creating users table: \n\t', users
    cursor.execute(users)
    


# inserts user object into open directory master
def createODuser(user): 
    #extract the username from the AD principal name by dropping the @yrbrands.com
    username = user['userprincipalname'].split('@')[0]
    first = user['givenname']
    last = user['sn']
    email = user['mail']
    realname =  user['displayname']
    
    # Set the LDAP auth arguments
    ldap_base = "/LDAPv3/" + ldap_host
    base = ["/usr/bin/dscl","-u",ldap_user,"-P",ldap_pw,ldap_base]
    
    # check if user already exists - then skip if that is the case
    if username in existing_users:
        print "User already exists!"
        
    else:
       
        # set all the command strings, then call them
        create_user = base +["-create","/Users/" + username]
                  
        set_shell = create_user + ["UserShell", "/usr/bin/false"]
        set_fn = create_user + ["FirstName",first]
        set_ln = create_user + ["LastName",last]
        set_realname =  create_user + ["RealName",realname]
        set_email =  create_user + ["EMailAddress", email]
        set_home = create_user + ["NFSHomeDirectory","/dev/null"]
        set_gid = create_user + ["PrimaryGroupID",primary_gid]
        # set the UID to the next incremental value
        set_uid =  create_user + ["UniqueID", str(getNextUID())]
        
        add_to_group = base + ["append","/Groups/"+group,"GroupMembership",username]

                      
        call(create_user)
        call(set_shell)
        call(set_fn)
        call(set_ln)
        call(set_realname)
        call(set_email)
        call(set_home)
        call(set_uid)
        call(set_gid)
        call(add_to_group)
        
        print "Created user ",username," (email:",email,")."
    
    

def iterate_users(conn):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("""SELECT * from ad_users""")
    except:
        print "Error getting users"
        
    users = cur.fetchall()
    for user in users:
        # print "\t", user['displayname']
        createODuser(user)
    
    
# add all the users to the (string) group name
def add_all_to_group(groupname):
    ldap_base = "/LDAPv3/" + ldap_host
    base = ["/usr/sbin/dseditgroup","-u",ldap_user,"-P",ldap_pw,"-n",ldap_base,"-o","edit","-a"]
    for user in existing_users:
        add_user = base + [user,"-t","user",groupname]
        # print add_user
        call(add_user)
    
    
def main():
    populateUsers()
    # add_all_to_group(group)
    conn = None
    try:
        conn_string = "host='localhost' dbname='users_sync' user='xadmin' password=''"
      print "Connecting to database\n	->%s" % (conn_string)
        
        conn = psycopg2.connect(conn_string)
        cur = conn.cursor()
        
        iterate_users(conn)

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)

    finally:
        if conn:
            conn.close()
    
if __name__ == '__main__':
   main()
