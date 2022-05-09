import database as dat


def test(temp):
    s = temp
    i = 0
    j = len(s) - 1
    flag1 = False
    flag2 = False
    while True:
        if (s[i].isdigit()):
            flag1 = True
        else:
            i += 1
        if (s[j].isdigit()):
            flag2 = True
        else:
            j -= 1
        if (flag1 and flag2):
            break
    return s[i:j + 1]

con = dat.sql_connection("database_dakt.db")
rows = dat.sql_fetch(con, "TinhVN")


if __name__ == "__main__":
    #print(dat.find_e_luubienso(con,(83,"V1",12345)))
    dat.sql_insert_luubienso(con,(83,"V1",12345))
    data = "xgs83-V1\n023.55zz"

    data = test(data)
    data = data.replace(".", "")
    data = data.replace("\n", " ")

    if (((int(data[0:2]) in i) for i in rows) and data[2] == "-" and data[4].isdigit()
    and data[3].isalpha() and (data[6:len(data)].isdigit()) ):
        print("Bien so xe la:", data)
        for i in rows:
            if int(data[0:2])in i:
                print(i[1])
                
        lst = (int(data[0:2]), data[3:5], data[6:])
        print(lst)
        dat.sql_insert_luubienso(con,lst)
        print(dat.find_e_luubienso(con,lst))



