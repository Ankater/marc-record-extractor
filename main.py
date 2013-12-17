# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
from pymarc import Field, Reader, Record, MARCWriter, MARCReader

def show_progress(value): sys.stderr.write('Из 6201707 проверено %d\r' % value)


#command_file = raw_input("Введите путь к файлу с заданим: ")
command_file = "c:/web/record_ext.txt"
command_file = open(command_file, 'r')

regAND=re.compile("and|or")
#reg=re.compile('^([001-887][a-zA-Z]{1}),*\s([001-887][a-zA-Z]{1},*\s)*""')
regSearchField = re.compile(',\s')

massiveOfFields = []
orAndMassive = []

for line in command_file:
    statusSearchFields = False
    stepMassiveIndex = 1
    stepMassiveField = []
    stepMassiveFieldRecord = {}
    #stepMassiveSubField = []
    stepRecord = {}
    if regAND.search(line)is not None:
        orAndMassive.append(line.replace('\n',''))
    else:
        #"""
        #stepMassiveIndex=0

        stepMassiveField.append(line[0:4])
        while statusSearchFields != True:
            if regSearchField.search(line[stepMassiveIndex*6 - 2:]) is not None:
                stepMassiveField.append(line[stepMassiveIndex*6:stepMassiveIndex*6+4])
                stepMassiveIndex = stepMassiveIndex + 1
            else:
                statusSearchFields = True
                if(line[stepMassiveIndex*6 - 1:] == 'None'):
                    stepRecord['regExpr'] = "None"
                else:
                    stepRecord['regExpr'] = re.compile(line[stepMassiveIndex*6 - 1:].replace('\n',''))
                stepRecord['field'] = stepMassiveField
        #"""
        massiveOfFields.append(stepRecord)
    stepMassive = []


print massiveOfFields
#print massiveOfExtractFields
print orAndMassive
#print massiveOfExtractRegularExpressions

#marcFile = raw_input("Введите путь к MARC файлу: ")
marcFile = "c:/rsl01_cl.mrc"
marcFile = open(marcFile, 'r')
reader = MARCReader(marcFile)

#inputfile = raw_input("Введите путь к директории, куда будет сохранён файл:")
inputfile = "c:/web/rsl1.mrc"
if inputfile[len(inputfile)-4:]!=".mrc":
    inputfile = inputfile[:len(inputfile)-4] + ".mrc"
inputfile = open(inputfile, 'w')
writer = MARCWriter(inputfile)

#print massiveOfFields[0]['regExpr'].search('')
#print massiveOfFields[1]['field'][2][:-1]
#print type(massiveOfFields[0]['field'][0][:-1])
#print True and True
#'''
i=0
for record in reader:
    numStep = 0
    i=i+1
    show_progress(i)
    if i == 26476:
        print record
    #Проходим весь масив
    while numStep < len(massiveOfFields):
        numField = 0
        #Проходим каждое поле
        while numField < len(massiveOfFields[numStep]['field']):
            #Проверка на существование поля
            if record[massiveOfFields[numStep]['field'][numField][:-1]] is not None:
                #Проверка на существование подполя
                if massiveOfFields[numStep]['regExpr'] == "None":
                    if record[massiveOfFields[numStep]['field'][numField][:-1]][massiveOfFields[numStep]['field'][numField][-1:]] is None:
                        statusField = True
                        numField = len(massiveOfFields[numStep]['field'])
                    else:
                        statusField = False
                else:
                    if record[massiveOfFields[numStep]['field'][numField][:-1]][massiveOfFields[numStep]['field'][numField][-1:]] is not None:
                        #Проверка на регулярное выражение
                        if massiveOfFields[numStep]['regExpr'].search(record[massiveOfFields[numStep]['field'][numField][:-1]][massiveOfFields[numStep]['field'][numField][-1:]]) is not None:
                            statusField = True
                            numField = len(massiveOfFields[numStep]['field'])
                        else:
                            statusField = False
                    else:
                        statusField = False
            else:
                statusField = False
            numField+=1

        if numStep == 0:
            #print statusField
            statusRecord = statusField
        else:
            if orAndMassive[numStep-1] == 'and':
                statusRecord = statusRecord and statusField
                #print statusRecord
            else:
                statusRecord = statusRecord or statusField
                #print statusRecord
        numStep+=1

    if statusRecord == True:
        #print "!2!"
        writer.write(record)
#'''
"""
for record in reader:
    numStep = 0

    while numStep < len(massiveOfFields[]):


    while numStep < len(massiveOfFields):
        numField = 0
        statusField = True

        #Проверяем запись на существование полей и выполнение регулярок
        while numField < len(massiveOfFields[numStep]['field']):
            if record[massiveOfFields[numStep]['field'][numField]] is not None and statusField != False:
                if record[massiveOfFields[numStep]['field'][numField]][massiveOfFields[numStep]['subfield'][numField]] is not None:
                    if massiveOfFields[numStep]['regExpr'].search(record[massiveOfFields[numStep]['field'][numField]][massiveOfFields[numStep]['subfield'][numField]]) is None:
                        statusField = False
                else:
                    statusField = False
            else:
                statusField = False
            numField += 1

        #Создание переменной статуса записи и её обновление после каждого прохода
        if numStep == 0:
            statusWritingRecord = statusField
        else:
            #print numStep
            if orAndMassive[numStep-1] == "and":
                statusWritingRecord = statusWritingRecord and statusField
            else:
                statusWritingRecord = statusWritingRecord or statusField

    print statusWritingRecord
    print "W"
    if statusWritingRecord == True:
        print statusWritingRecord
        print "!"
        writer.write(record)
    numStep += 1
#"""