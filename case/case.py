import csv

def getId(table, value, column):
    return '(select "Id" from ' + '"' + table + '"' + ' where "' + column + '"=' + value + ')'

def getInsert(table, Id, number, subject, category, owner, status, registered, created, response, solutionprovided, priority, supportlevel, serviceitem, servicepact, solutionoverdue, responseoverdue, contact, account, origin, respondedon, satisfactionlevel):
    return 'Insert into "' + table + '"' + '("Id", "Number", "Subject", "CategoryId", "OwnerId", "StatusId", "RegisteredOn", "CreatedOn", "ResponseDate", "SolutionProvidedOn", "PriorityId", "SupportLevelId", "ServiceItemId", "ServicePactId", "SolutionOverdue", "ResponseOverdue", "ContactId", "AccountId", "OriginId", "RespondedOn", "SatisfactionLevelId")' + \
           ' VALUES (' + Id + ',' + number + ',' + subject + ',' + category + ',' + owner + ',' + status + ',' + registered + ',' + created + ',' + response + \
           ', ' + solutionprovided + ', ' + priority + ', ' + supportlevel + ', ' + serviceitem + ', ' + servicepact + ', ' + str(solutionoverdue) +\
           ', ' + str(responseoverdue) + ', ' + contact + ', ' + account + ', ' + origin + ', ' + respondedon + ', ' + satisfactionlevel + ')'

def writeToFile(data):
    with open('case_result.csv', 'w', newline='') as csv_file:
        headers = []
        for rcrds in data[0]:
            headers.append(rcrds)
        datafile = open('result.sql', 'a')
        for line in data:
            line['Category'] = getId('CaseCategory', "'" + line['Category'] + "'", 'Name')
            line['Assignee'] = getId('Contact', "'" + line['Assignee'] + "'", 'Name')
            line['Status'] = getId('CaseStatus', "'" + line['Status'] + "'", 'Name')
            line['Priority'] = getId('CasePriority', "'" + line['Priority'] + "'", 'Name')
            line['Support line'] = getId('SupportLevel', "'" + line['Support line'] + "'", 'Name')
            line['Service'] = getId('ServiceItem', "'" + line['Service'] + "'", 'Name')
            line['SLA'] = getId('ServicePact', "'" + line['SLA'] + "'", 'Name')
            # line['"Overdue resolution"'] = getId('SolutionOverdue', line['"Overdue resolution"'], 'Name')
            # line['"Overdue response"'] = getId('ResponseOverdue', line['"Overdue response"'], 'Name')
            line['Contact'] = getId('Contact', "'" + line['Contact'] + "'", 'Name')
            line['Account'] = getId('Account', "'" + line['Account'] + "'", 'Name')
            line['Source'] = getId('CaseOrigin', "'" + line['Source'] + "'", 'Name')
            line['Satisfaction level'] = getId('SatisfactionLevel', "'" + line['Satisfaction level'] + "'", 'Name')
            insertQuery = getInsert('Case', "'" + line['Id'] + "'", "'" + line['Number'] + "'", "'" + line['Subject'] + "'", line['Category'], line['Assignee'],
                                    line['Status'], "'" + line['Registration date'] + "'", "'" + line['Created on'] + "'", "'" + line['Response time'] + "'", "'" + line['Actual resolution time'] + "'",
                                    line['Priority'], line['Support line'], line['Service'], line['SLA'], 1 if line['Overdue resolution'] == 'Yes' else 0, 1 if line['Overdue response'] == 'Yes' else 0,
                                    line['Contact'], line['Account'], line['Source'], "'" + line['Actual response time'] + "'", line['Satisfaction level'])
            datafile.write(insertQuery + ";\r\n")
        datafile.close()

if __name__ == '__main__':
    data = []
    with open('case.csv', newline='') as File:
        reader = csv.DictReader(File)
        for row in reader:
            data.append(row)
    writeToFile(data)
