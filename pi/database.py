import sqlite3
from sqlite3 import Error
array={11:"Cao Bang",12:"Lang Son",14:"Quang Ninh",17:"Thai Binh",18:"Nam Dinh",19:"Phu Tho",
           20:"Thai Nguyen",21:"Yen Bai",22:"Tuyen Quang",23:"Ha Giang",24:"Lao Cai",25:"Lai Chau",
           26:"Son La",27:"Dien Bien",28:"Hoa Binh",34:"Hai Duong",35:"Ninh Binh",36:"Thanh Hoa",37:"Nghe An",
           38:"Ha Tinh",43:"Da Nang",47:"Dak Lak",48:"Dak Nong",49:"Lam Dong",61:"Binh Duong",62:"Long An",
           63:"Tien Giang",64:"Vinh Long",65:"Can Tho",66:"Dong Thap",67:"An Giang",68:"Kien Giang",69:"Ca Mau",
           70:"Tay Ninh",71:"Ben Tre",72:"Ba Ria Vung Tau",73:"Quang Binh",74:"Quang Tri",75:"Hue",76:"Quang Ngai",
           77:"Binh Dinh",78:"Phu Yen",79:"Khanh Hoa",81:"Gia Lai",82:"Kom Tom",83:"Soc Trang",84:"Tra Vinh",
           85:"Ninh Thuan",86:"Binh Thuan",88:"Vinh Phuc",89:"Hung Yen",90:"Ha Nam",92:"Quang Nam",93:"Binh Phuoc",
           94:"Bac Lieu",95:"Hau Giang",97:"Bac Can",98:"Bac Giang",99:"Bac Ninh",15:"Hai Phong",16:"Hai Phong",
           29:"Ha Noi",30:"Ha Noi",31:"Ha Noi",32:"Ha Noi",33:"Ha Noi",40:"Ha Noi",39:"Dong Nai",60:"Dong Nai",
           41:"TP Ho Chi Minh",50:"TP Ho Chi Minh",51:"TP Ho Chi Minh",52:"TP Ho Chi Minh", 53:"TP Ho Chi Minh",54:"TP Ho Chi Minh",55:"TP Ho Chi Minh",56:"TP Ho Chi Minh",
            57:"TP Ho Chi Minh",58:"TP Ho Chi Minh",59:"TP Ho Chi Minh"}

def sql_connection(data):
    try:
        con = sqlite3.connect(data)
        return con
    except Error:
        print(Error)
        
def sql_table(con):

    cursorObj = con.cursor()

    cursorObj.execute("CREATE TABLE TinhVN(id integer PRIMARY KEY NOT NULL UNIQUE, name text NOT NULL)")

    con.commit()

def sql_insert(con, table, entities):

    cursorObj = con.cursor()
    
    cursorObj.execute('INSERT INTO {0}(id, name) VALUES(?, ?)'.format(table), entities)
    
    con.commit()
    
def sql_insert_luubienso(con, entities):

    cursorObj = con.cursor()
    
    cursorObj.execute('INSERT INTO luubienso (id, kihieu, bienso) VALUES(?, ?, ?)', entities)
    
    con.commit()
    
def sql_fetch(con, table):

    cursorObj = con.cursor()

    cursorObj.execute('SELECT * FROM {0}'.format(table))

    rows = cursorObj.fetchall()
    return rows

    #for row in rows:

        #print(row)
        
def sql_list_table(con):

    cursorObj = con.cursor()

    cursorObj.execute('SELECT name from sqlite_master where type= "table"')

    print(cursorObj.fetchall()) 

def delete_e(con,d):
    cursorObj = con.cursor()
    cursorObj.execute('DELETE FROM luubienso WHERE id = {0} and kihieu = "{1}" and bienso = {2}'.format(d[0],d[1],d[2]))
    con.commit()

def find_e_luubienso(con,d):
    cursorObj = con.cursor()
    cursorObj.execute('Select * FROM luubienso WHERE id = {0} and kihieu = "{1}" and bienso = "{2}"'.format(d[0],d[1],d[2]))
    a = cursorObj.fetchall()
    con.commit()
    if a:
        return True
    else:
        return False
    
if __name__ == "__main__":
    
    con = sql_connection("database_dakt.db")

    #sql_table(con)
    #for i in array:
    #    sql_insert(con,"TinhVN",(i,array[i]))
    #    print(array[i])
    sql_insert_luubienso(con,(83,"V1","02345"))
    #delete_e(con,(83,"V1","12345"))
    print(find_e_luubienso(con,(83,"V1","02345")))
    sql_fetch(con, "luubienso")
    #sql_list_table(con)
    con.close()
