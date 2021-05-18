import csv

def getId(table, value, column):
    return '(select "Id" from ' + '"' + table + '"' + ' where "' + column + '"=' + value + ')'

def getInsert(table, Id, number, subject, category, owner, status, registered, created, response, solutionprovided, priority, supportlevel, serviceitem, servicepact, solutionoverdue, responseoverdue, contact, account, origin, respondedon, satisfactionlevel):
    return 'Insert into "' + table + '"' + '("Id", "Number", "Subject", "CategoryId", "OwnerId", "StatusId", "RegisteredOn", "CreatedOn", "ResponseDate", "SolutionProvidedOn", "PriorityId", "SupportLevelId", "ServiceItemId", "ServicePactId", "SolutionOverdue", "ResponseOverdue", "ContactId", "AccountId", "OriginId", "RespondedOn", "SatisfactionLevelId")' + \
           ' VALUES (' + Id + ',' + number + ',' + subject + ',' + category + ',' + owner + ',' + status + ',' + registered + ',' + created + ',' + response + \
           ', ' + solutionprovided + ', ' + priority + ', ' + supportlevel + ', ' + serviceitem + ', ' + servicepact + ', ' + str(solutionoverdue) +\
           ', ' + str(responseoverdue) + ', ' + contact + ', ' + account + ', ' + origin + ', ' + respondedon + ', ' + satisfactionlevel + ')'

def writeToFile(data):
    headers = []
    for rcrds in data[0]:
        headers.append(rcrds)
    datafile = open('result.sql', 'a')
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
        insertQuery = getInsert('Case', "'" + line['Id'] + "'", "'" + line['Number'].replace("'", "''") + "'", "'" + line['Subject'].replace("'", "''") + "'", line['Category'], line['Assignee'],
                                line['Status'], "'" + line['Registration date'].replace("'", "''") + "'", "'" + line['Created on'].replace("'", "''") + "'",
                                "'" + line['Response time'].replace("'", "''") + "'", "'" + line['Actual resolution time'].replace("'", "''") + "'",
                                line['Priority'], line['Support line'], line['Service'], line['SLA'], 'True' if line['Overdue resolution'] == 'Yes' else 'False', 'True' if line['Overdue response'] == 'Yes' else 'False',
                                line['Contact'], line['Account'], line['Source'], "'" + line['Actual response time'].replace("'", "''") + "'", line['Satisfaction level'])
        datafile.write(insertQuery + ";\r\n")
    datafile.close()

if __name__ == '__main__':
    data = []
    with open('case.csv', newline='') as File:
        reader = csv.DictReader(File)
        for row in reader:
            data.append(row)
    writeToFile(data)
