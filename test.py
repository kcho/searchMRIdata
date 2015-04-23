import searchMRIdata
import pandas as pd
databaseLocation = '/Volumes/promise/CCNC_MRI_3T/database/database.xls'

args = {'input':'inputList.txt', 'output':'/ccnc_bin/searchMRIdata/location.txt'}

searchMRIdata.main(args)



#searchMRIdata.getLocation(searchMRIdata.giveInfoType('inputList.txt'),pd.ExcelFile(databaseLocation).parse(0))
