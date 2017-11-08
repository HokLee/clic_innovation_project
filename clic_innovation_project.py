from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask import *
import pyodbc
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import os
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')


app = Flask(__name__)


#首页为登录界面
@app.route('/',methods=['POST','GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'sorry'
        else:
            return redirect(url_for('index'))  # 返回的是函数
    return render_template('login.html', error=error)


#系统主界面
@app.route('/index')
def index():
     return render_template('index.html')


#转到查询界面
@app.route('/welcome')
def hello():
    # cnxn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=GD-XX-M7100Z\MSSQLSERVER2012;DATABASE=student;UID=sa;PWD=123456')
    # cursor = cnxn.cursor()
    # sql = 'select * from students'
    # jsonData = []
    # for row in cursor.execute(sql):
    #     result = {}
    #     result['id'] = row[0]
    #     result['name'] = row[1]
    #     result['age'] = row[2]
    #     jsonData.append(result)
    #     print(row)
    #     print(u'init:',jsonData)
    return render_template('welcome.html')


@app.route('/selectSpecialData',methods=['POST'])
def selectSpecialData():
    data = json.loads(request.get_data())
    name = data["name"]
    ID = data["ID"]

    sql = "select top 100 * from 汇总 where 姓名 = '"+name+"'"

    cnxn = pyodbc.connect(
        'DRIVER={SQL Server Native Client 11.0};SERVER=GD-XX-M7100Z\MSSQLSERVER2012;DATABASE=精准扶贫;UID=sa;PWD=123456')
    cursor = cnxn.cursor()

    jsonData = []
    for row in cursor.execute(sql):
        result = {}
        result['区域'] = row[0]
        result['社保局（月结）'] = row[1]
        result['证件号码'] = row[2]
        result['姓名'] = row[3]
        result['医院名称'] = row[4]
        result['医疗类别'] = row[5]
        result['出院日期'] = row[6]
        result['结算时间'] = row[7]
        result['入院诊断'] = row[8]
        result['出院诊断'] = row[9]
        result['就诊病种代码'] = row[10]
        result['医疗费用总额'] = row[11]
        result['起付标准'] = row[12]
        result['范围内费用'] = row[13]
        result['基本医疗统筹支付'] = row[14]
        result['大病（补充）医疗统筹支付'] = row[15]
        result['结算类别'] = row[16]
        result['级别'] = row[17]
        result['就医类型'] = row[18]
        result['建档立卡'] = row[19]
        result['特困供养'] = row[20]

        jsonData.append(result)
        # print(row)
        # print(u'init:', jsonData)
    return jsonify(jsonData)


#查询数据函数
@app.route('/selectData',methods=['POST'])
def selectData():
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server Native Client 11.0};SERVER=GD-XX-M7100Z\MSSQLSERVER2012;DATABASE=精准扶贫;UID=sa;PWD=123456')

    # cnxn = pyodbc.connect(
    #     'DRIVER={SQL Server Native Client 11.0};SERVER=DESKTOP-GMNHVRP;DATABASE=精准扶贫;UID=sa;PWD=123456')
    cursor = cnxn.cursor()

    #获取前台发来的参数,page:当前页数,rows:每页显示行数
    page = request.form.get('page')
    rows = request.form.get('rows')
    print(page)
    print(rows)
    if(page==1):
        start = 0
    else:
        start = (int(page)-1)*int(rows)

    sql = 'select * from 汇总 order by 结算时间 offset '+str(start)+'Row Fetch Next '+str(rows)+' Rows Only'
    # sql = '''SELECT TOP 100 [区域]
    #       ,[社保局（月结）]
    #       ,[证件号码]
    #       ,[姓名]
    #       ,[医院名称]
    #       ,[医疗类别]
    #       ,[出院日期]
    #       ,[结算时间]
    #       ,[入院诊断]
    #       ,[出院诊断]
    #       ,[就诊病种代码]
    #       ,[医疗费用总额]
    #       ,[起付标准]
    #       ,[范围内费用]
    #       ,[基本医疗统筹支付]
    #       ,[大病（补充）医疗统筹支付]
    #       ,[结算类别]
    #       ,[级别]
    #       ,[就医类型]
    #       ,[建档立卡]
    #       ,[特困供养]
    #   FROM [精准扶贫].[dbo].[汇总]'''

    jsonData = []
    for row in cursor.execute(sql):
        result = {}
        result['区域'] = row[0]
        result['社保局（月结）'] = row[1]
        result['证件号码'] = row[2]
        result['姓名'] = row[3]
        result['医院名称'] = row[4]
        result['医疗类别'] = row[5]
        result['出院日期'] = row[6]
        result['结算时间'] = row[7]
        result['入院诊断'] = row[8]
        result['出院诊断'] = row[9]
        result['就诊病种代码'] = row[10]
        result['医疗费用总额'] = row[11]
        result['起付标准'] = row[12]
        result['范围内费用'] = row[13]
        result['基本医疗统筹支付'] = row[14]
        result['大病（补充）医疗统筹支付'] = row[15]
        result['结算类别'] = row[16]
        result['级别'] = row[17]
        result['就医类型'] = row[18]
        result['建档立卡'] = row[19]
        result['特困供养'] = row[20]

        jsonData.append(result)
        # print(row)
        # print(u'init:', jsonData)

    #构造json数据,把总数据条数toal和每页显示的数据传到前台
    jsonresult={'total':len(jsonData),'rows':jsonData}
    print(jsonresult)
    return jsonify(jsonresult)

#转到数据测算页面
@app.route('/measuring')
def dataMeasuring():
    return render_template('dataMeasuring.html')

#开始测算数据
@app.route('/measureData',methods=['POST'])
def measureData():

    data = json.loads(request.get_data())
    year = data["year"]
    first_basic_pay = data["first_basic_pay"]
    second_basic_pay = data["second_basic_pay"]
    third_basic_pay = data["third_basic_pay"]
    appoint_basic_pay = data["appoint_basic_pay"]
    unfixed_basic_pay = data["unfixed_basic_pay"]
    staff_growth = data["staff_growth"]
    resident_growth = data["resident_growth"]
    accurate_growth = data["accurate_growth"]
    every_year_growth = data["every_year_growth"]
    first_illness_top = data["first_illness_top"]
    second_illness_top = data["second_illness_top"]
    first_grade_first_section = data["first_grade_first_section"]
    second_grade_first_section = data["second_grade_first_section"]
    first_basic_illness_top = data["first_basic_illness_top"]
    second_basic_illness_top = data["second_basic_illness_top"]
    indemnity2017 = data["indemnity2017"]
    indemnity2018 = data["indemnity2018"]
    indemnity2019 = data["indemnity2019"]
    first_grade_pay = data["first_grade_pay"]
    basic_grade_pay = data["basic_grade_pay"]
    second_grade_pay = data["second_grade_pay"]
    third_grade_pay = data["third_grade_pay"]
    fixed_pay = data["fixed_pay"]
    appoint_pay = data["appoint_pay"]
    resident_unfixed_unappoint_pay = data["resident_unfixed_unappoint_pay"]
    staff_unfixed_unappoint_pay = data["staff_unfixed_unappoint_pay"]
    print(data["year"])



    cnxn = pyodbc.connect(
        'DRIVER={SQL Server Native Client 11.0};SERVER=GD-XX-M7100Z\MSSQLSERVER2012;DATABASE=精准扶贫;UID=sa;PWD=123456')
    cursor = cnxn.cursor()
    jsonData = []

    try:
        file = open(os.path.join(APP_STATIC,'measure_sql1.txt'), 'r', encoding='UTF-8')
        sql1 = file.read()
    finally:
        if file:
            file.close()

    try:
        file2 = open(os.path.join(APP_STATIC,'measure_sql2.txt'), 'r', encoding='UTF-8')
        sql2 = file2.read()
    finally:
        if file2:
            file2.close()


    sql = sql1+'set @年份= ' + year+"set @一级基本医疗给付='" + first_basic_pay + "'"+"set @二级基本医疗给付='" + second_basic_pay + "'"+"set @三级基本医疗给付='" + third_basic_pay + "'"+"set @约定基本医疗给付='" + appoint_basic_pay + "'"+"set @非定点基本医疗给付='" + unfixed_basic_pay + "'"+"set @职工增长率='" + staff_growth + "'"+"set @居民增长率='" + resident_growth + "'"+"set @精准扶贫增长率='" + accurate_growth + "'"+"set @每年增量='" + every_year_growth + "'"+"set @一档大病封顶='" + first_illness_top + "'"+"set @二档大病封顶='" + second_illness_top + "'"+"set @一档第一段='" + first_grade_first_section + "'"+"set @二档第一段='" + second_grade_first_section + "'"+"set @一档基本医疗封顶='" + first_basic_illness_top + "'"+"set @二档基本医疗封顶='" + second_basic_illness_top + "'"+"set @2017年起赔='" + indemnity2017 + "'"+"set @2018年起赔='" + indemnity2018 + "'"+"set @2019年起赔='" + indemnity2019 + "'"+"set @一级起付线='" + first_grade_pay + "'"+"set @基层起付线='" + basic_grade_pay + "'"+"set @二级起付线='" + second_grade_pay + "'"+"set @三级起付线='" + third_grade_pay + "'"+"set @定点起付线='" + fixed_pay + "'"+"set @约定起付线='" + appoint_pay + "'"+"set @居民非定点非约定起付线='" + resident_unfixed_unappoint_pay + "'"+"set @职工非定点非约定起付线='" + staff_unfixed_unappoint_pay + "'"+sql2
    print(sql)


    cursor.execute(sql)
    cursor.commit()
    cursor.close()
    cursor = cnxn.cursor()
    for row in cursor.execute('''
    select 年份,分段,结算类别,count(distinct 证件号码)as 人数,
    round(sum(医疗总费用)/10000,2)as 医疗总费用,
    round(sum(基本医疗支付)/10000,2)as 基本医疗支付,
    round(sum(范围内费用)/10000,2)as 范围内费用,
    round(sum(累计大病范围内费用)/10000,2)as 累计大病范围内费用,
    round(sum(大病支付)/10000,2)as 大病支付,
    round(sum(二档赔付)/10000,2)as 二档赔付
    from #tmp2
    group by 年份,分段,结算类别
    order by 年份 asc,结算类别 asc,
    charindex(convert(varchar,分段)+',',',<1万,>1万,')
    '''):
        result = {}
        result['年份'] = row[0]
        result['分段'] = row[1]
        result['结算类别'] = row[2]
        result['人数'] = row[3]
        result['医疗总费用'] = row[4]
        result['基本医疗支付'] = row[5]
        result['范围内费用'] = row[6]
        result['累计大病范围内费用'] = row[7]
        result['大病支付'] = row[8]
        result['二挡赔付'] = row[9]
        jsonData.append(result)
        # print(row)
        print(u'init:', jsonData)
    return jsonify(jsonData)






if __name__ == '__main__':
    app.run()
