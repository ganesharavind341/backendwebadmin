import random
from getData import getNumberOfCompanies
import string

def genJojoId(companyName):
    print("here")
    NumberOfCompanies = getNumberOfCompanies()
    return "jojoId" + str(1000 + NumberOfCompanies)

def genCompanyId(companyName):
    print("here")
    NumberOfCompanies = getNumberOfCompanies()
    return "jojoId" + str(1000 + NumberOfCompanies) + companyName[:2] 
