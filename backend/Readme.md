{\rtf1\ansi\ansicpg1252\cocoartf1671\cocoasubrtf600
{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\froman\fcharset0 Times-Roman;\f2\fnil\fcharset0 Menlo-Regular;
}
{\colortbl;\red255\green255\blue255;\red0\green0\blue233;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c93333;\csgray\c0;}
\paperw11900\paperh16840\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # ATM\
\
ATM is a Flask application that is used to update balance and denomination after transaction in atm and for user\
\
## Installation\
```\
First install the required packages using pip3 install -r requirements.txt.\
Then install Postgres in the system based on your os {\field{\*\fldinst{HYPERLINK "https://www.postgresql.org/download/"}}{\fldrslt 
\f1 \cf2 \expnd0\expndtw0\kerning0
\ul \ulc2 \outl0\strokewidth0 \strokec2 https://www.postgresql.org/download}}
\f1 \cf2 \expnd0\expndtw0\kerning0
\ul \ulc2 \outl0\strokewidth0 \strokec2 . 
\f0 \cf0 \kerning1\expnd0\expndtw0 \ulnone \outl0\strokewidth0 \
```\
```\
After install go to psql shell which is installed along with the postgre.\
Then give username, password and after that create db using\
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0

\f2\fs22 \cf3 \CocoaLigature0 CREATE DATABASE atm;\
Connect to database using \
\\c atm;\
Create schema transactions using\
CREATE SCHEMA transactions;\
\
Create two tables customer and amount_atm using\
\
CREATE TABLE transactions.customer(                                       id serial PRIMARY KEY,branch_name VARCHAR(8) UNIQUE NOT NULL,denom_2000 Integer,denom_500 Integer,denom_200 Integer,denom_100 Integer);\
\
CREATE TABLE transactions.amount_atm(                                     id serial PRIMARY KEY,branch_name VARCHAR(50) UNIQUE NOT NULL,denom_2000 Integer,denom_500 Integer,denom_200 Integer,denom_100 Integer);\
 \
```\
```Now database is ready to use\
```\
\
```\
Upload environment variables using\
export USERNAME=<username>\
export PASSWORD=<password>\
export URL=<url>\
export db=<db_name>\
\
```
\f0\fs24 \cf0 \CocoaLigature1 \
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0
\cf0 \
\
## Running\
```\
Run the application using \
Python3 app.py\
```}