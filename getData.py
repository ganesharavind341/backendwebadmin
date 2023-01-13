import pymongo
from pymongo import MongoClient
import datetime



def getUri():
    uri = 'mongodb+srv://jojopaysdev:Greatindianfest@cluster0.41rimgo.mongodb.net/?retryWrites=true&w=majority'
    # uri = "mongodb://localhost:27017"
    return uri

def getMongoConn():
    mongo = MongoClient(getUri())
    return mongo

def connectdb():
    conn = getMongoConn()
    db = conn['jojopays']
    return db


def connectCompanyData():
    db = connectdb()
    coll = db['companyData']
    return coll

def connectTripSchema():
    db = connectdb()
    coll = db['TripSchema']
    return coll


def connectUsers():
    db = connectdb()
    coll = db['user']
    return coll

def getNumberOfCompanies():
    coll = connectCompanyData()
    data = coll.count_documents({})
    return data


# def getTripDatas(jojoId):
#     coll = connectTripSchema()
#     for x in coll.find():
#         print(x)


# getTripDatas("jojoId1001me")

def connectCompanySchema():
    db = connectdb()
    coll = db['CompanySchema']
    return coll


def connectBusSchema():
    db = connectdb()
    coll = db['BusSchema']
    return coll


def connectChat():
    db = connectdb()
    coll = db['Chat']
    return coll


def connectDeskStaffSchema():
    db = connectdb()
    coll = db['DeskStaffSchema']
    return coll


def connectDriverDetailSchema():
    db = connectdb()
    coll = db['DriverDetailSchema']
    return coll


def connectTransactionSchema():
    db = connectdb()
    coll = db['TransactionSchema']
    return coll


def connectUserSchema():
    db = connectdb()
    coll = db['UserSchema']
    return coll                


def getProfileData(jojoId):
    coll = connectCompanyData()
    data = coll.find_one({'jojoId': jojoId},{'_id': False})
    return data



# def chat(senderId, recieverId, message):
#     connectChat.insert_one({'senderId': senderId, 'recieverId': recieverId, 'message': message, 'created_at': datetime.now()})

