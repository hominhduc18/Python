import csv
def write_CSV(lst, data):
    fields = ['Bien so', 'Ki hieu', 'Ma Tinh', 'Thoi gian nhan dien','Trang thai']
    file = "{0}-{1}-{2}".format(lst[0],lst[1],lst[2])
    filename = "/home/pi/Downloads/New/DAKR provip/fileCSV/{0}.csv".format(file)
    with open(filename, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(fields) 
            
        # writing the data rows 
        csvwriter.writerows(data)
