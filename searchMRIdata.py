#!/ccnc_bin/venv/bin/python

import os
import re
import argparse
import textwrap
import pandas as pd

databaseLocation = '/Volumes/promise/CCNC_MRI_3T/database/database.xls'
mriDataLocation = '/Volumes/promise/CCNC_MRI_3T'

def main(args):
    df = pd.ExcelFile(databaseLocation).parse(0)
    inputInfo = giveInfoType(args.input)
    outDf = getLocation(inputInfo,df)
    print outDf[args.type]
    
    outDf.to_excel(args.output,'Sheet1')



def giveInfoType(inputList):
    '''
    Read each line in the inputList text file.
    Then, it assigns a type to each line and return it.
        {'12345678':'patientNumber',
         'KangIkCho':'koreanName',
         '1988-09-16':'DOB'}
    '''

    with open(inputList,'r') as f:
        lines = f.readlines()
        lines = [x.strip('\n') for x in lines]

    returnDict = {}
    for line in lines:
        if re.search('\d{8}',line):
            returnDict[line] = 'patientNumber'
        elif re.search('\d{4}-\d{2}-\d{2}',line):
            returnDict[line] = 'DOB'
        else:
            returnDict[line] = 'koreanName'

    return returnDict

def getLocation(infoDict,df):
    df = df.groupby('timeline').get_group('baseline')
    df = df[~df.group.str.startswith('SNU')]
    subjectInfo = pd.DataFrame()
    for info, infoType in infoDict.iteritems():
        if infoType == 'patientNumber':
            subjectDf = df[df.patientNumber==int(info)]
            subjectInfo = pd.concat([subjectInfo,subjectDf])
        elif infoType == 'DOB':
            subjectDf = df[df.DOB==info]
            subjectInfo = pd.concat([subjectInfo,subjectDf])
        else:
            subjectDf = df[df.koreanName==info.decode('utf-8')]

            if len(subjectDf) < 1:
                print info.decode('utf-8')
            elif len(subjectDf) > 1:
                print info.decode('utf-8')

            subjectInfo = pd.concat([subjectInfo,subjectDf])

    return subjectInfo


if __name__ == '__main__':

    allList = ['koreanName','subjectName','subjectInitial','group','sex','age','DOB','scanDate','timeline','studyname','patientNumber','T1Number','DTINumber','DKINumber','RESTNumber','REST2Number','folderName','backUpBy','note']
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            {codeName} : 
            ========================================
            eg) {codeName} --input {in_put} --output {output}
                {in_put} : List of a type of subject information
                {output} : Location of the data
            '''.format(codeName=os.path.basename(__file__),
                       in_put = '{subjectInfoList}',
                       output = '{outputText}')))

    parser.add_argument(
        '-i', '--input',
        help='Input')

    parser.add_argument(
        '-o', '--output',
        help='Output',
        default=os.path.join(os.getcwd(),'location.txt'))

    parser.add_argument(
        '-t', '--type',
        help="Type of information wanted in list eg) {0}".format(allList),
        default=allList)

    args = parser.parse_args()

    if not args.input or args.input=='':
        parser.error('No information is given')

    main(args)
