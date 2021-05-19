import csv
import uuid

def getId(table, value, column):
    return '(select "Id" from ' + '"' + table + '"' + ' where "' + column + '"=' + value + ')'

def getInsert(table, Id, number, subject, category, owner, status, registered, created, response, solutionprovided, priority, supportlevel, serviceitem, servicepact, solutionoverdue, responseoverdue, contact, account, origin, respondedon, satisfactionlevel):
    return 'Insert into "' + table + '"' + '("Id", "Number", "Subject", "CategoryId", "OwnerId", "StatusId", "RegisteredOn", "CreatedOn", "ResponseDate", "SolutionProvidedOn", "PriorityId", "SupportLevelId", "ServiceItemId", "ServicePactId", "SolutionOverdue", "ResponseOverdue", "ContactId", "AccountId", "OriginId", "RespondedOn", "SatisfactionLevelId")' + \
           ' VALUES (' + Id + ',' + number + ',' + subject + ',' + category + ',' + owner + ',' + status + ',' + registered + ',' + created + ',' + response + \
           ', ' + solutionprovided + ', ' + priority + ', ' + supportlevel + ', ' + serviceitem + ', ' + servicepact + ', ' + str(solutionoverdue) +\
           ', ' + str(responseoverdue) + ', ' + contact + ', ' + account + ', ' + origin + ', ' + respondedon + ', ' + satisfactionlevel + ') ON CONFLICT DO NOTHING'

def getDelete(table, id):
    return 'Delete from "' + table + '" where "Id"=' + id

def writeToFile(data):
    headers = []
    for rcrds in data[0]:
        headers.append(rcrds)
    insertResultDataFile = open('result.sql', 'a')
    deleteResultDataFile = open('delete_result.sql', 'a')
    for line in data:
        line['Category'] = getId('CaseCategory', "'" + line['Category'].replace("'", "''") + "'", 'Name')
        line['Assignee'] = getId('Contact', "'" + line['Assignee'].replace("'", "''") + "'", 'Name')
        line['Status'] = getId('CaseStatus', "'" + line['Status'].replace("'", "''") + "'", 'Name')
        line['Priority'] = getId('CasePriority', "'" + line['Priority'].replace("'", "''") + "'", 'Name')
        line['Support line'] = getId('SupportLevel', "'" + line['Support line'].replace("'", "''") + "'", 'Name')
        line['Service'] = getId('ServiceItem', "'" + line['Service'].replace("'", "''") + "'", 'Name')
        line['SLA'] = getId('ServicePact', "'" + line['SLA'].replace("'", "''") + "'", 'Name')
        line['Contact'] = getId('Contact', "'" + line['Contact'].replace("'", "''") + "'", 'Name')
        line['Account'] = getId('Account', "'" + line['Account'].replace("'", "''") + "'", 'Name')
        line['Source'] = getId('CaseOrigin', "'" + line['Source'].replace("'", "''") + "'", 'Name')
        line['Satisfaction level'] = getId('SatisfactionLevel', "'" + line['Satisfaction level'] + "'", 'Name')
        line['Id'] = str(uuid.uuid4()) if not line['Id'] else line['Id']
        line['Registration date'] = 'null' if not line['Registration date'] else "'" + line['Registration date'] + "'"
        line['Created on'] = 'null' if not line['Created on'] else "'" + line['Created on'] + "'"
        line['Response time'] = 'null' if not line['Response time'] else "'" + line['Response time'] + "'"
        line['Actual resolution time'] = 'null' if not line['Actual resolution time'] else "'" + line['Actual resolution time'] + "'"
        line['Actual response time'] = 'null' if not line['Actual response time'] else "'" + line['Actual response time'] + "'"
        insertQuery = getInsert('Case', "'" + line['Id'] + "'", "'" + line['Number'].replace("'", "''") + "'", "'" + line['Subject'].replace("'", "''") + "'", line['Category'], line['Assignee'],
                                line['Status'], line['Registration date'], line['Created on'],
                                line['Response time'], line['Actual resolution time'],
                                line['Priority'], line['Support line'], line['Service'], line['SLA'], 'True' if line['Overdue resolution'] == 'Yes' else 'False', 'True' if line['Overdue response'] == 'Yes' else 'False',
                                line['Contact'], line['Account'], line['Source'], line['Actual response time'], line['Satisfaction level'])
        insertResultDataFile.write(insertQuery + ";\r\n")
        deleteQuery = getDelete('Case', "'" + line['Id'] + "'")
        deleteResultDataFile.write(deleteQuery + ";\r\n")
    insertResultDataFile.close()
    deleteResultDataFile.close()

if __name__ == '__main__':
    data = []
    with open('case.csv', newline='') as File:
        reader = csv.DictReader(File)
        for row in reader:
            data.append(row)
    writeToFile(data)
