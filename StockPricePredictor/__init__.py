import mysql.connector
import shutil
import os
import numpy as np
from numpy import array

mydb_spp = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1505076",
    database="stock_price_prediction",
    auth_plugin='mysql_native_password'
)
mycursor_spp = mydb_spp.cursor()


NUM_TOP = 5
NUM_DAYS = 30

###################################################################################

infoArr = np.empty(shape=[0, 5])  # tradecode, last_price, percent_change, pred, pred_change

incArr = np.empty(shape=[0, 3])  # tradecode, last_day_closing_price, percent_change
decArr = np.empty(shape=[0, 3])  # tradecode, last_day_closing_price, percent_change
predArr = np.empty(shape=[0, 4])  # tradecode, last_day_closing_price, prediction after 7 days, percent_change

num_inc_thirty = 0
num_dec_thirty = 0

num_inc_last = 0
num_dec_last = 0


sql = "select trade_code from home_company"

mycursor_spp.execute(sql)
myResult = mycursor_spp.fetchall()

for i in range(len(myResult)):
    tradecode = myResult[i][0]
   # print(tradecode)

    sql = "select * from home_sharehistory where trade_code = %s order by date desc LIMIT %s"
    val = (tradecode, NUM_DAYS)

    mycursor_spp.execute(sql, val)
    company_history_results = mycursor_spp.fetchall()

    sql = "select * from home_shareprediction where trade_code = %s order by date desc LIMIT 1"
    val = (tradecode, )

    mycursor_spp.execute(sql, val)
    company_pred_results = mycursor_spp.fetchall()

    last_price = company_history_results[0][6]
    prev_price = company_history_results[NUM_DAYS-1][6]
    pred_price = company_pred_results[0][3]

    # print(last_price)
    # print(prev_price)
    # print(pred_price)

    change = 100*(last_price - prev_price)/prev_price
    pred_change = 100*(pred_price - last_price)/last_price

    # print("=---------------")
    # print(change)
    # print(pred_change)

    if change > 0:
        num_inc_thirty = num_inc_thirty + 1
    else:
        num_dec_thirty = num_dec_thirty + 1

    if last_price > company_history_results[1][6]:
        num_inc_last = num_inc_last + 1
    else:
        num_dec_last = num_dec_last + 1

    newRow = new_row = [[i, float(last_price), float(change), float(pred_price), float(pred_change)]]

    infoArr = np.append(infoArr, new_row, axis=0)

# print(infoArr)
# Sort 2D numpy array by 2nd Column
sortedArr = infoArr[infoArr[:, 2].argsort()]
sortedPred = infoArr[infoArr[:, 4].argsort()]

# for entry in sortedArr:
#     print(entry)
#
# for entry in sortedPred:
#     print(entry)

for i in range(NUM_TOP):
    new_row = [[myResult[int(sortedArr[i][0])][0], sortedArr[i][1], sortedArr[i][2]]]
    decArr = np.append(decArr, new_row, axis=0)

    size = len(sortedArr)-1
    new_row = [[myResult[int(sortedArr[size-i][0])][0], sortedArr[size-i][1], sortedArr[size-i][2]]]
    incArr = np.append(incArr, new_row, axis=0)

    new_row = [[myResult[int(sortedPred[size - i][0])][0], sortedPred[size - i][1], sortedPred[size - i][3], sortedPred[size - i][4]]]
    predArr = np.append(predArr, new_row, axis=0)


# print(predArr)

np.save('predArr', predArr)
np.save('incArr', incArr)
np.save('decArr', decArr)
print("the array is saved in the file predArr.npy")
# print(incArr)
# print(decArr)

# predArrFromFile = np.load('predArr.npy')


# # for pie chart

# print(num_inc_thirty)
# print(num_dec_thirty)
#
# print(num_inc_last)
# print(num_dec_last)

arr1 = np.empty(shape=[0, 1])
new_row = [[num_inc_thirty]]
arr1 = np.append(arr1, new_row, axis=0)
new_row = [[num_dec_thirty]]
arr1 = np.append(arr1, new_row, axis=0)

arr2 = np.empty(shape=[0, 1])
new_row = [[num_inc_last]]
arr2 = np.append(arr2, new_row, axis=0)
new_row = [[num_dec_last]]
arr2 = np.append(arr2, new_row, axis=0)

print('done')
np.save('doughnut30', arr1)
np.save('doughnutLast', arr2)

#######################################################

sql = 'select trade_code, total_volume from home_sharehistory where date = (select max(date) from home_sharehistory ) order by total_volume desc limit %s'
val = (NUM_TOP,)
mycursor_spp.execute(sql, val)
top_sell = mycursor_spp.fetchall()
#
# print('top sell')
# print(top_sell)

top_sell_numpy = array(top_sell)
np.save('topSell', top_sell_numpy)

sql = "select trade_code, closing_price " \
      "from home_sharehistory " \
      "where date = (select max(date) from home_sharehistory )" \
      "order by closing_price desc " \
      "limit %s"
val = (NUM_TOP,)
mycursor_spp.execute(sql, val)
top_price = mycursor_spp.fetchall()

# print('top price')
# print(top_price)
# print(top_price.__class__)

top_price_numpy = array(top_price)
np.save('topPrice', top_price_numpy)
