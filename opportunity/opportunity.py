import csv

def getId(table, value, column):
    return '(select "Id" from ' + '"' + table + '"' + ' where "' + column + '"=' + value + ')'

def getInsert(table, Id, name, customerneed, stage, account, budget, opportunityamount, category, type, contact, owner, source, predictiveprobability, predictedopportunity):
    return 'Insert into "' + table + '"' + '("Id", "Title", "LeadTypeId", "StageId", "AccountId", "Bubget", "Amount", "CategoryId", "TypeId", "ContactId", "OwnerId", "SourceId", "PredictiveProbability", "labPreOpAm")' + \
           ' VALUES (' + Id + ',' + name + ',' + customerneed + ',' + stage + ',' + account + ',' + budget + ',' + opportunityamount + ',' + category + ',' + type + \
           ', ' + contact + ', ' + owner + ', ' + source + ', ' + predictiveprobability + ', ' + predictedopportunity + ')'

def writeToFile(data):
    headers = []
    for rcrds in data[0]:
        headers.append(rcrds)
    datafile = open('result.sql', 'a')
    for line in data:
        line['Customer need'] = getId('LeadType', "'" + line['Customer need'].replace("'", "''") + "'", 'Name')
        line['Stage'] = getId('OpportunityStage', "'" + line['Stage'].replace("'", "''") + "'", 'Name')
        line['Account'] = getId('Account', "'" + line['Account'].replace("'", "''") + "'", 'Name')
        line['Category'] = getId('OpportunityCategory', "'" + line['Category'].replace("'", "''") + "'", 'Name')
        line['Type'] = getId('OpportunityType', "'" + line['Type'].replace("'", "''") + "'", 'Name')
        line['Contact'] = getId('Contact', "'" + line['Contact'].replace("'", "''") + "'", 'Name')
        line['Owner'] = getId('Contact', "'" + line['Owner'].replace("'", "''") + "'", 'Name')
        line['Source'] = getId('OpportunitySource', "'" + line['Source'].replace("'", "''") + "'", 'Name')
        insertQuery = getInsert('Opportunity', "'" + line['Id'] + "'", "'" + line['Name'].replace("'", "''") + "'", line['Customer need'], line['Stage'], line['Account'],
                                line['Budget'], line['Opportunity amount'], line['Category'], line['Type'], line['Contact'],
                                line['Owner'], line['Source'], line['Predictive probability'], line['Predicted opportunity amount'])
        datafile.write(insertQuery + ";\r\n")
    datafile.close()

if __name__ == '__main__':
    data = []
    with open('opportunity.csv', newline='') as File:
        reader = csv.DictReader(File)
        for row in reader:
            data.append(row)
    writeToFile(data)
