from os.path import join
from xlrd import open_workbook
import xml.etree.ElementTree as ET
import csv
# def readExcel():
# 	rb = open_workbook(join(test_fiiles'testall.xls'), formatting_info=True, on_demand=True)
#     rb.sheet_by_index(0).cell(0,1).value

def writeToExcel(root, height, width): #iterates through entry values and returns comma-delimited file
    data = getValues(root, height, width)
    f1 = open('CSVDraft.csv', 'w')
    writer=csv.writer(f1, delimiter=',', lineterminator='\n')
    for i in range(height+1): #rows
        row = data[i]
        writer.writerow(row)
    f1.close()

def writeToXML(root, height, width): #iterates through entry values and returns xml tree
    messageId = ""
    intObjName = "CNE Web Plan Leg"
    messageType = "Integration Object"
    intObjFormat = "Siebel Hierarchical"
    header = ET.Element("SiebelMessage")
    header.set("MessageId", messageId)
    header.set("IntObjectName", intObjName)
    header.set("MessageType", messageType)
    header.set("IntObjectFormat", intObjFormat)
    listOfPlanLeg = ET.SubElement(header, "ListOfPlanLeg")

    data = getValues(root, height, width)
    for i in range(height):
        planLeg = ET.Element("PlanLeg")
        for attribute in range(width):
            subElem = ET.SubElement(planLeg, str(data[0][attribute]))
            subElem.text = str(data[i+1][attribute])
        listOfPlanLeg.append(planLeg)   

    f1 = open('XMLMockup.xml', 'w')
    ET.ElementTree(header).write('XMLMockup.xml', encoding='UTF-8', xml_declaration=True)
    f1.close()

def getValues(root, height, width): #iterates through values and tacks on ID heads
    values = [[0 for x in range(width)] for x in range(height+1)] 
    values[0][0] = "REGION"
    values[0][1] = "GOVAGG"
    values[0][2] = "STATUS"
    values[0][3] = "ID"
    values[0][4] = "NUMBER"

    for i in range(height): #rows
        for j in range(width): #columns
            values[i+1][j] = find_in_grid(root, i+1, j).get()
            cell = values[i+1][j]
    return(values)

def find_in_grid(frame, row, column): #returns the entry objects gridded on the grid
    for children in frame.children.values():
        info = children.grid_info()
        #note that rows and column numbers are stored as string                                                                         
        if info['row'] == str(row) and info['column'] == str(column):
            return children
    return None
