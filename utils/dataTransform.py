def stockIDtusharToBaostock(str):
    return str.split('.')[1].lower() + '.' + str.split('.')[0]

def stockIDBaostockToDB(str):
    return str.split('.')[0]+str.split('.')[1]