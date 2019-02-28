#coding: utf-8
import xlsxwriter
def  excelChart(arrw,path):
    f = open(path, 'w')
    f.close()        
    #-----------------------------------------------------------
    num = ['B','C']
    time_arrw = []
    pass_arrw = []
    fail_arrw = []
    for i in range(0,len(arrw),3):
        time_arrw.append(arrw[i])
        pass_arrw.append(arrw[i+1])
        fail_arrw.append(arrw[i+2])
    #--------------------------------------------------------------
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})        
    headings = ['time', 'pass','failed']
    data = [time_arrw,pass_arrw,fail_arrw]
    worksheet.write_row('A1', headings, bold)
    worksheet.write_column('A2', data[0])
    worksheet.write_column('B2', data[1])        
    worksheet.write_column('C2', data[2])   
    chart1 = workbook.add_chart({'type': 'column'})
    ca = '=Sheet1!$A$2:$A$' + str(len(data[0])+1)
    for i in range(0,len(num)):
        na = '=Sheet1!$'+str(num[i])+'$1'
        va = '=Sheet1!$'+str(num[i])+'$2:$'+str(num[i])+'$' + str(len(data[1])+1)
        chart1.add_series({
            'name':       na,
            'categories': ca,
            'values':     va,
        })        
    chart1.set_title ({'name': u'产线测试用例执行情况'})
    chart1.set_style(2)
    worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})    
    workbook.close()  
    
#excelChart(arrw, path)