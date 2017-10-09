from flask import Flask,render_template
from flask_bootstrap import Bootstrap
from flask import *
import pyodbc


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
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server Native Client 11.0};SERVER=GD-XX-M7100Z\MSSQLSERVER2012;DATABASE=精准扶贫;UID=sa;PWD=123456')
    cursor = cnxn.cursor()
    jsonData = []

    sql = '''use [精准扶贫]
    declare @增长率2018 float,@增长率2019 float,@once   float,@年份 float,@序号   int ,@id varchar(100),@once2   float,@序号2   int ,@id2 varchar(100),
    @once3   float,@序号3   int ,@id3 varchar(100),@once4   float,@序号4   int ,@id4 varchar(100),@二级基本医疗给付 float,@三级基本医疗给付 float,@定点基本医疗给付 float,
    @2017职工年增长率 float,@2018职工年增长率 float,@2019职工年增长率 float,@2017年起赔 float,@职工增长率 float,@居民增长率 float,
    @2017居民年增长率 float,@2018居民年增长率 float,@2019居民年增长率 float,@一档基本医疗封顶 float,@二档基本医疗封顶 float,@一档大病封顶 float,@二档大病封顶 float,
    @一档第一段 float,@二档第一段 float,@一级起付线 float,@二级起付线 float,@三级起付线 float,@基层起付线 float,@定点起付线 float,@约定起付线 float,
    @居民非定点非约定起付线 float,@职工非定点非约定起付线 float,@2018年起赔 float,@2019年起赔 float,
    @每年增量 float,@定点医疗机构给付 float,@约定医疗机构给付 float,@非定点医疗机构给付 float,@一级基本医疗给付 float,@约定基本医疗给付 float,@非定点基本医疗给付 float,
    @精准扶贫增长率 float,@2017年精准扶贫增长率 float,@2018年精准扶贫增长率 float,@2019年精准扶贫增长率 float
    set @年份=2016
    set @一级基本医疗给付=0.85
    set @二级基本医疗给付=0.8
    set @三级基本医疗给付=0.55
    set @约定基本医疗给付=0.4
    set @非定点基本医疗给付=0.4
    set @职工增长率=1.0
    set @居民增长率=1.0
    set @精准扶贫增长率=1.1
    set @每年增量=0
    set @一档大病封顶=240000
    set @二档大病封顶=240000
    set @一档第一段=120000
    set @二档第一段=120000
    set @一档基本医疗封顶=200000
    set @二档基本医疗封顶=200000
    set @2017年起赔=10000
    set @2018年起赔=10000
    set @2019年起赔=10000
    set @一级起付线=500
    set @基层起付线=500
    set @二级起付线=600
    set @三级起付线=900
    set @定点起付线=900
    set @约定起付线=1500
    set @居民非定点非约定起付线=1500
    set @职工非定点非约定起付线=1500


    set @2017职工年增长率=power(@职工增长率,2017-@年份)
    set @2018职工年增长率=power(@职工增长率,2018-@年份)
    set @2019职工年增长率=power(@职工增长率,2019-@年份)
    set @2017居民年增长率=power(@居民增长率,2017-@年份)
    set @2018居民年增长率=power(@居民增长率,2018-@年份)
    set @2019居民年增长率=power(@居民增长率,2019-@年份)
    set @2017年精准扶贫增长率=power(@精准扶贫增长率,2017-@年份)
    set @2018年精准扶贫增长率=power(@精准扶贫增长率,2018-@年份)
    set @2019年精准扶贫增长率=power(@精准扶贫增长率,2019-@年份)

    set @定点基本医疗给付=@三级基本医疗给付

    select 区域,[社保局（月结）],证件号码,姓名,医院名称,医疗类别,出院日期,入院诊断,出院诊断,就诊病种代码,医疗费用总额,起付标准,范围内费用,基本医疗统筹支付,[大病（补充）医疗统筹支付],结算类别,级别,建档立卡,特困供养 into #建模数据
    from [dbo].[汇总]
    where left(出院日期,4)=@年份 

    alter table #建模数据 add 年份 varchar(20)

    update #建模数据
    set 年份=left(出院日期,4)
    from #建模数据

    select rank()over(partition by 年份,证件号码 order by 出院日期 asc)as 序号,* into #模型一
    from #建模数据

    select * into #tmp模型
    from #模型一 where 年份=@年份


    ----------------------变体--------------


    select * into #tmp2019
    from #tmp模型
    where 特困供养 is null and 建档立卡 is null

    update #tmp2019
    set 年份='2019'
    from #tmp2019


    -------------------------------------开始计算2019---------------------------
    alter table #tmp2019  add 首次范围内自付费用 float 
    alter table #tmp2019  add 累计自付 float
    alter table #tmp2019  add 超过起赔线 int
    alter table #tmp2019 add 当次大病范围内费用 float
    alter table #tmp2019 add 累计大病范围内费用1 float
    alter table #tmp2019 add 累计大病范围内费用2 float
    alter table #tmp2019  add 累计大病支付 float
    alter table #tmp2019 add 大病保险剩余额度 float
    alter table #tmp2019 add 累计基本医疗支付 float
    alter table #tmp2019  add 基本医疗剩余额度 float
    alter table #tmp2019 add 当次二档范围内费用 float
    alter table #tmp2019 add 累计二档范围内费用 float
    alter table #tmp2019 add 当次二档赔付费用 float
    alter table #tmp2019 add 年度内累计二档赔付费用 float
    alter table #tmp2019 add 二档剩余额度 float

    update #tmp2019
    set [大病（补充）医疗统筹支付]=0
    from #tmp2019

    update #tmp2019
    set 起付标准=case when 级别='基层' then @基层起付线
                      when 级别='一级' then @一级起付线
    				   when 级别='一级及基层'then @一级起付线
    				  when 级别='二级' then @二级起付线
    				  when 级别='三级' then @三级起付线
    				  when 级别='定点' then @定点起付线
    				  when 级别='非定点' then @约定起付线
    				  when 级别='非约定' then @居民非定点非约定起付线
    				  end
    from #tmp2019 where 医疗类别 in('普通住院','家庭病床')




    update #tmp2019
    set 基本医疗统筹支付=case when 范围内费用>起付标准  and 级别 in ('一级','基层') then (范围内费用-起付标准)*@一级基本医疗给付
                              when 范围内费用>起付标准 and 级别 in ('二级') then (范围内费用-起付标准)*@二级基本医疗给付
    						  when 范围内费用>起付标准 and 级别 in ('三级') then (范围内费用-起付标准)*@三级基本医疗给付
    						  when 范围内费用>起付标准 and 级别 in ('定点') then (范围内费用-起付标准)*@定点基本医疗给付
    						  when 范围内费用>起付标准 and 级别 in ('非定点','约定','非约定')and 结算类别='居民' then (范围内费用-起付标准)*@非定点基本医疗给付
    						  when 范围内费用>起付标准 and 级别 in ('约定')and 结算类别='职工' then (范围内费用-起付标准)*@约定基本医疗给付
    						  when 范围内费用>起付标准 and 级别 in ('非定点','非约定')and 结算类别='职工' then (范围内费用-起付标准)*@非定点基本医疗给付
    						  when 医疗类别='门诊慢性病' and 级别 in ('非定点')and 结算类别='居民' then (范围内费用-起付标准)*@非定点基本医疗给付
    						  when 医疗类别='门诊慢性病'and 级别 in ('非定点')and 结算类别='职工' then (范围内费用-起付标准)*@非定点基本医疗给付
    						  else 0
    						  end
    from #tmp2019

    update #tmp2019
    set 当次大病范围内费用=0
    from #tmp2019

    update #tmp2019
    set 累计大病范围内费用1=0
    from #tmp2019

    update #tmp2019
    set 累计大病范围内费用2=0
    from #tmp2019

    update #tmp2019
    set 当次二档范围内费用=0
    from #tmp2019

    update #tmp2019
    set 累计二档范围内费用=0
    from #tmp2019

    update #tmp2019
    set 当次二档赔付费用=0
    from #tmp2019


    select @once=累计基本医疗支付,@序号=序号,@id=证件号码 from #tmp2019  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #tmp2019     
    set   @once   =   case   when   @序号   =   序号-1   then     @once   +   基本医疗统筹支付 else 基本医疗统筹支付  end,   
          @序号   =   序号,   
          累计基本医疗支付   =case  when @once<200000 or @once=200000 then @once else 200000 end
    update #tmp2019
    set 基本医疗剩余额度 = case when 累计基本医疗支付<200000 then 200000-累计基本医疗支付 else 0 end
    from #tmp2019
    --查看更新后的结果

    update #tmp2019
    set 首次范围内自付费用=case when 基本医疗统筹支付>0 then 范围内费用-基本医疗统筹支付-起付标准
                            else 0
    						end
    from #tmp2019 where 序号=1 

    select 证件号码 into #2019先累计二档tmp from #tmp2019 where 首次范围内自付费用<@2019年起赔

    select * into #2019先累计二档 from #tmp2019 where 证件号码 in (select 证件号码 from #2019先累计二档tmp)

    update #2019先累计二档
    set 当次二档范围内费用=case when 结算类别='职工' and 基本医疗统筹支付<>0 then 范围内费用-基本医疗统筹支付-起付标准
                            else 0
    						end
    from #2019先累计二档 




    select @once=当次二档范围内费用,@序号=序号,@id=证件号码 from #2019先累计二档  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #2019先累计二档     
    set   @once   =   case   when   @序号   =   序号-1   then     @once   +   当次二档范围内费用 else 当次二档范围内费用  end,   
          @序号   =   序号,   
          累计二档范围内费用   =   @once   
    --查看更新后的结果
    --------------先计算大病起赔线以下部分的二档--------------



    update #2019先累计二档
    set 当次二档赔付费用=case when 累计二档范围内费用 between 0 and 5000 and 级别<>'非定点' then 当次二档范围内费用*0.5
                              when 累计二档范围内费用 between 0 and 5000 and 级别='非定点' then 当次二档范围内费用*0.4
    						  when 累计二档范围内费用 between 5000 and 200000 and 级别<>'非定点' 
    						  then (5000)*0.5+(累计二档范围内费用-5000)*0.85
    						 when 累计二档范围内费用 between 5000 and 200000 and 级别='非定点' 
    						  then 当次二档范围内费用*0.75
    						  when 累计二档范围内费用 > 200000 and 级别<>'非定点' 
    						  then 5000*0.5+(200000-5000)*0.85+(累计二档范围内费用-200000)*0.9
    						  when 累计二档范围内费用 > 200000 and 级别='非定点' 
    						  then 5000*0.5+(200000-5000)*0.85+(累计二档范围内费用-200000)*0.9
    						  else 0
    						  end
    from #2019先累计二档 where 序号=1 and 结算类别='职工'

    select * into #临时20192 from #2019先累计二档

    update #2019先累计二档
    set 当次二档赔付费用=case when a.累计二档范围内费用 between 0 and 5000
                               and b.累计二档范围内费用 between 0 and 5000  and a.级别<>'非定点' then a.当次二档范围内费用*0.5
                              when b.累计二档范围内费用 between 0 and 5000 and 
    						  a.累计二档范围内费用 between 5000 and 200000 and a.级别<>'非定点'
    						   then (5000-b.累计二档范围内费用)*0.5+(a.累计二档范围内费用-5000)*0.85

    						   when a.累计二档范围内费用 between 5000 and 200000 and a.级别<>'非定点' and
    						   b.累计二档范围内费用 between 5000 and 200000 then (a.当次二档范围内费用)*0.85

    						  when b.累计二档范围内费用 between 5000 and 200000 
    						  and a.累计二档范围内费用 >200000 and a.级别<>'非定点' 
    						  then (200000-b.累计二档范围内费用)*0.85+(a.当次二档范围内费用-200000)*0.9 

    						   when b.累计二档范围内费用>200000 and
    						  a.累计二档范围内费用 >200000 and a.级别<>'非定点' 
    						  then  (a.当次二档范围内费用)*0.9

    						when a.累计二档范围内费用 between 0 and 5000
                               and b.累计二档范围内费用 between 0 and 5000  and a.级别='非定点' then a.当次二档范围内费用*0.4
                              when b.累计二档范围内费用 between 0 and 5000 and 
    						  a.累计二档范围内费用 between 5000 and 200000 and a.级别='非定点'
    						   then (5000-b.累计二档范围内费用)*0.4+(a.累计二档范围内费用-5000)*0.75

    						   when a.累计二档范围内费用 between 5000 and 200000 and a.级别='非定点' and
    						   b.累计二档范围内费用 between 5000 and 200000 then (a.当次二档范围内费用)*0.75

    						  when b.累计二档范围内费用 between 5000 and 200000 
    						  and a.累计二档范围内费用 >200000 and a.级别='非定点' 
    						  then (200000-b.累计二档范围内费用)*0.75+(a.当次二档范围内费用-200000)*0.8 

    						   when b.累计二档范围内费用>200000 and
    						  a.累计二档范围内费用 >200000 and a.级别='非定点' 
    						  then  (a.当次二档范围内费用)*0.8
    						  else 0
    						  end
    from #2019先累计二档 a join #临时20192 b on a.序号=b.序号+1 and a.证件号码=b.证件号码 where a.结算类别='职工' and b.结算类别='职工'


    update #2019先累计二档
    set 当次大病范围内费用=范围内费用-基本医疗统筹支付-当次二档赔付费用-起付标准
    from #2019先累计二档 
    where 结算类别='职工'

    update #2019先累计二档
    set 当次大病范围内费用=范围内费用-基本医疗统筹支付-起付标准
    from #2019先累计二档 
    where 结算类别='居民'



    select @once=当次大病范围内费用,@序号=序号,@id=证件号码 from #2019先累计二档  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #2019先累计二档     
    set   @once   =   case   when   @序号   =   序号-1  then     @once   +   当次大病范围内费用 else 当次大病范围内费用  end,   
          @序号   =   序号,   
          累计大病范围内费用1   =   @once   
    --查看更新后的结果



    select rank()over(partition by 年份,证件号码 order by 累计大病范围内费用1 asc) as 大病序号,序号,年份,证件号码,出院日期
     into #起赔线排序三
    from #2019先累计二档 a
    where 累计大病范围内费用1>=@2019年起赔
    order by 证件号码 asc,年份 asc ,序号 asc,大病序号 asc

    update #2019先累计二档 
    set 超过起赔线=b.大病序号
    from #2019先累计二档  a left join #起赔线排序三 b on a.年份=b.年份 and a.证件号码=b.证件号码 and a.出院日期=b.出院日期 and a.序号=b.序号



    update #2019先累计二档
    set 累计大病范围内费用1=0
    from #2019先累计二档 where 超过起赔线 is null

    update #2019先累计二档
    set 当次大病范围内费用=范围内费用-基本医疗统筹支付-起付标准
    from #2019先累计二档 where (超过起赔线>1 or  超过起赔线=1)

    select @once=当次大病范围内费用,@序号=序号,@id=证件号码 from #2019先累计二档  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #2019先累计二档     
    set   @once   =   case   when   @序号   =   序号-1  then     @once   +   当次大病范围内费用 else 当次大病范围内费用  end,   
          @序号   =   序号,   
          累计大病范围内费用2   =   @once   
    --查看更新后的结果

    update #2019先累计二档
    set [大病（补充）医疗统筹支付]=case when 超过起赔线=1 and 累计大病范围内费用2 between @2019年起赔 and 120000 and 级别<>'非定点'
                                        then (累计大病范围内费用2-@2019年起赔)*0.6
    									when 超过起赔线=1 and 累计大病范围内费用2 between @2019年起赔 and 120000 and 级别='非定点'
                                        then (累计大病范围内费用2-@2019年起赔)*0.5

    									when 超过起赔线=1 and 累计大病范围内费用2>120000  and 级别<>'非定点'
    									then (累计大病范围内费用2-120000)*0.7+(120000-@2019年起赔)*0.6
    									when 超过起赔线=1 and 累计大病范围内费用2>120000  and 级别='非定点'
    									then (累计大病范围内费用2-120000)*0.6+(120000-@2019年起赔)*0.5
    									else 0
    									end
    									from #2019先累计二档 where 超过起赔线=1 and 建档立卡 is null and 特困供养 is null

    update #2019先累计二档
    set [大病（补充）医疗统筹支付]=case when 超过起赔线=1 and 累计大病范围内费用2 between @2019年起赔*0.3 and 120000 and 级别<>'非定点'
                                        then (累计大病范围内费用2-@2019年起赔)*0.7
    									when 超过起赔线=1 and 累计大病范围内费用2 between @2019年起赔*0.3 and 120000 and 级别='非定点'
                                        then (累计大病范围内费用2-@2019年起赔)*0.6

    									when 超过起赔线=1 and 累计大病范围内费用2>120000  and 级别<>'非定点'
    									then (累计大病范围内费用2-120000)*0.8+(120000-@2019年起赔*0.3)*0.7
    									when 超过起赔线=1 and 累计大病范围内费用2>120000  and 级别='非定点'
    									then (累计大病范围内费用2-120000)*0.7+(120000-@2019年起赔*0.3)*0.6
    									else 0
    									end
    									from #2019先累计二档 where 超过起赔线=1 and 建档立卡='建档立卡' and 特困供养 is null

    update #2019先累计二档
    set [大病（补充）医疗统筹支付]=case when 超过起赔线=1 and 累计大病范围内费用2 between @2019年起赔*0.2 and 120000 and 级别<>'非定点'
                                        then (累计大病范围内费用2-@2019年起赔)*0.8
    									when 超过起赔线=1 and 累计大病范围内费用2 between @2019年起赔*0.2 and 120000 and 级别='非定点'
                                        then (累计大病范围内费用2-@2019年起赔)*0.7

    									when 超过起赔线=1 and 累计大病范围内费用2>120000  and 级别<>'非定点'
    									then (累计大病范围内费用2-120000)*0.9+(120000-@2019年起赔*0.2)*0.8
    									when 超过起赔线=1 and 累计大病范围内费用2>120000  and 级别='非定点'
    									then (累计大病范围内费用2-120000)*0.8+(120000-@2019年起赔*0.2)*0.7
    									else 0
    									end
    									from #2019先累计二档 where 超过起赔线=1 and 特困供养='特困供养' and 建档立卡 is null




    select * into #临时大病2019 from #2019先累计二档 

    update #2019先累计二档
    set [大病（补充）医疗统筹支付]=case when a.累计大病范围内费用2 between  @2019年起赔 and 120000 
                                             and b.累计大病范围内费用2 between  @2019年起赔 and 120000  and a.级别<>'非定点'
    									then a.当次大病范围内费用*0.6
    									when a.累计大病范围内费用2 between 120000 and 240000 and b.累计大病范围内费用2 between 120000 and 240000
    									 and a.级别<>'非定点'
    									then a.当次大病范围内费用*0.7

    									when b.累计大病范围内费用2 between @2019年起赔  and 120000 and a.累计大病范围内费用2 between 120000 and 240000
    									and  a.级别<>'非定点' then (120000-b.累计大病范围内费用2)*0.6+(a.累计大病范围内费用2-120000)*0.7

    									when a.累计大病范围内费用2 between  @2019年起赔 and 120000 
                                             and b.累计大病范围内费用2 between  @2019年起赔 and 120000  and a.级别='非定点'
    									then a.当次大病范围内费用*0.5
    									when a.累计大病范围内费用2 between 120000 and 240000 and b.累计大病范围内费用2 between 120000 and 240000
    									 and a.级别='非定点'
    									then a.当次大病范围内费用*0.6

    									when b.累计大病范围内费用2 between @2019年起赔  and 120000 and a.累计大病范围内费用2 between 120000 and 240000
    									and  a.级别='非定点' then (120000-b.累计大病范围内费用2)*0.5+(a.累计大病范围内费用2-120000)*0.6
    									else 0
    									end
    									from #2019先累计二档 a join #临时大病2019 b on a.序号=b.序号+1 and a.证件号码=b.证件号码 
    									 where a.超过起赔线>1 and a.序号>1 and a.建档立卡 is null and a.特困供养 is null

    update #2019先累计二档
    set [大病（补充）医疗统筹支付]=case when a.累计大病范围内费用2 between  @2019年起赔*0.3 and 120000 
                                             and b.累计大病范围内费用2 between  @2019年起赔*0.3 and 120000  and a.级别<>'非定点'
    									then a.当次大病范围内费用*0.7
    									when a.累计大病范围内费用2 between 120000 and 240000 and b.累计大病范围内费用2 between 120000 and 240000
    									 and a.级别<>'非定点'
    									then a.当次大病范围内费用*0.8

    									when b.累计大病范围内费用2 between @2019年起赔*0.3  and 120000 and a.累计大病范围内费用2 between 120000 and 240000
    									and  a.级别<>'非定点' then (120000-b.累计大病范围内费用2)*0.7+(a.累计大病范围内费用2-120000)*0.8

    									when a.累计大病范围内费用2 between  @2019年起赔*0.3 and 120000 
                                             and b.累计大病范围内费用2 between  @2019年起赔*0.3 and 120000  and a.级别='非定点'
    									then a.当次大病范围内费用*0.6
    									when a.累计大病范围内费用2 between 120000 and 240000 and b.累计大病范围内费用2 between 120000 and 240000
    									 and a.级别='非定点'
    									then a.当次大病范围内费用*0.7

    									when b.累计大病范围内费用2 between @2019年起赔*0.3  and 120000 and a.累计大病范围内费用2 between 120000 and 240000
    									and  a.级别='非定点' then (120000-b.累计大病范围内费用2)*0.6+(a.累计大病范围内费用2-120000)*0.7
    									else 0
    									end
    									from #2019先累计二档 a join #临时大病2019 b on a.序号=b.序号+1 and a.证件号码=b.证件号码 
    									 where a.超过起赔线>1 and a.序号>1 and a.建档立卡='建档立卡' and a.特困供养 is null

    update #2019先累计二档
    set [大病（补充）医疗统筹支付]=case when a.累计大病范围内费用2 between  @2019年起赔*0.2 and 120000 
                                             and b.累计大病范围内费用2 between  @2019年起赔*0.2 and 120000  and a.级别<>'非定点'
    									then a.当次大病范围内费用*0.8
    									when a.累计大病范围内费用2 between 120000 and 240000 and b.累计大病范围内费用2 between 120000 and 240000
    									 and a.级别<>'非定点'
    									then a.当次大病范围内费用*0.9

    									when b.累计大病范围内费用2 between @2019年起赔*0.2  and 120000 and a.累计大病范围内费用2 between 120000 and 240000
    									and  a.级别<>'非定点' then (120000-b.累计大病范围内费用2)*0.8+(a.累计大病范围内费用2-120000)*0.9

    									when a.累计大病范围内费用2 between  @2019年起赔*0.2 and 120000 
                                             and b.累计大病范围内费用2 between  @2019年起赔*0.2 and 120000  and a.级别='非定点'
    									then a.当次大病范围内费用*0.7
    									when a.累计大病范围内费用2 between 120000 and 240000 and b.累计大病范围内费用2 between 120000 and 240000
    									 and a.级别='非定点'
    									then a.当次大病范围内费用*0.8

    									when b.累计大病范围内费用2 between @2019年起赔*0.2  and 120000 and a.累计大病范围内费用2 between 120000 and 240000
    									and  a.级别='非定点' then (120000-b.累计大病范围内费用2)*0.7+(a.累计大病范围内费用2-120000)*0.8
    									else 0
    									end
    									from #2019先累计二档 a join #临时大病2019 b on a.序号=b.序号+1 and a.证件号码=b.证件号码 
    									 where a.超过起赔线>1 and a.序号>1 and a.建档立卡 is null  and a.特困供养='特困供养'




    select @once=累计大病支付,@序号=序号,@id=证件号码 from #2019先累计二档  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #2019先累计二档     
    set   @once   =   case   when   @序号   =   序号-1   then     @once   +   [大病（补充）医疗统筹支付] else [大病（补充）医疗统筹支付]  end,   
          @序号   =   序号,   
          累计大病支付   =case when [大病（补充）医疗统筹支付]=0 then 0 
    	                       when @once<240000 or @once=240000 then @once else 240000 end 
    --查看更新后的结果

    update #2019先累计二档
    set 大病保险剩余额度 = case when [大病（补充）医疗统筹支付]=0 then 240000
                                when 累计大病支付<240000 then 240000-累计大病支付 else 0 end
    from #2019先累计二档

    update #2019先累计二档
    set 当次二档范围内费用=case when (范围内费用-起付标准-基本医疗统筹支付-[大病（补充）医疗统筹支付])>0 then 范围内费用-起付标准-基本医疗统筹支付-[大病（补充）医疗统筹支付]
                                else 0 end
    from #2019先累计二档 where 累计大病范围内费用2>@2019年起赔 and 结算类别='职工'


    select @once=当次二档范围内费用,@序号=序号,@id=证件号码 from #2019先累计二档  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #2019先累计二档     
    set   @once   =   case   when   @序号   =   序号-1   then     @once   +   当次二档范围内费用 else 当次二档范围内费用  end,   
          @序号   =   序号,   
          累计二档范围内费用   =   @once   

    select * into #2019先算二档大病后二档计算 from #2019先累计二档 


    update #2019先累计二档
    set 当次二档赔付费用=case when a.累计二档范围内费用 between 0 and 5000
                               and b.累计二档范围内费用 between 0 and 5000  and a.级别<>'非定点' then a.当次二档范围内费用*0.5
                              when b.累计二档范围内费用 between 0 and 5000 and 
    						  a.累计二档范围内费用 between 5000 and 200000 and a.级别<>'非定点'
    						   then (5000-b.累计二档范围内费用)*0.5+(a.累计二档范围内费用-5000)*0.85

    						   when a.累计二档范围内费用 between 5000 and 200000 and a.级别<>'非定点' and
    						   b.累计二档范围内费用 between 5000 and 200000 then (a.当次二档范围内费用)*0.85

    						  when b.累计二档范围内费用 between 5000 and 200000 
    						  and a.累计二档范围内费用 >200000 and a.级别<>'非定点' 
    						  then (200000-b.累计二档范围内费用)*0.85+(a.当次二档范围内费用-200000)*0.9 

    						   when b.累计二档范围内费用>200000 and
    						  a.累计二档范围内费用 >200000 and a.级别<>'非定点' 
    						  then  (a.当次二档范围内费用)*0.9

    						when a.累计二档范围内费用 between 0 and 5000
                               and b.累计二档范围内费用 between 0 and 5000  and a.级别='非定点' then a.当次二档范围内费用*0.4
                              when b.累计二档范围内费用 between 0 and 5000 and 
    						  a.累计二档范围内费用 between 5000 and 200000 and a.级别='非定点'
    						   then (5000-b.累计二档范围内费用)*0.4+(a.累计二档范围内费用-5000)*0.75

    						   when a.累计二档范围内费用 between 5000 and 200000 and a.级别='非定点' and
    						   b.累计二档范围内费用 between 5000 and 200000 then (a.当次二档范围内费用)*0.75

    						  when b.累计二档范围内费用 between 5000 and 200000 
    						  and a.累计二档范围内费用 >200000 and a.级别='非定点' 
    						  then (200000-b.累计二档范围内费用)*0.75+(a.当次二档范围内费用-200000)*0.8 

    						   when b.累计二档范围内费用>200000 and
    						  a.累计二档范围内费用 >200000 and a.级别='非定点' 
    						  then  (a.当次二档范围内费用)*0.8
    						  else 0
    						  end
    from #2019先累计二档 a join #2019先算二档大病后二档计算 b on a.序号=b.序号 and a.证件号码=b.证件号码
     where a.累计大病范围内费用2>@2019年起赔 and a.结算类别='职工'

    select @once=当次二档赔付费用,@序号=序号,@id=证件号码 from #2019先累计二档  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #2019先累计二档     
    set   @once   =   case   when   @序号   =   序号-1   then     @once   +   当次二档赔付费用 else 当次二档赔付费用  end,   
          @序号   =   序号,   
          [年度内累计二档赔付费用]   =   @once  

    update #2019先累计二档
    set 二档剩余额度 = case when 年度内累计二档赔付费用<200000 then 200000-年度内累计二档赔付费用 else 0 end
    from #2019先累计二档

    select * into #临时2019 from #2019先累计二档
    update #2019先累计二档
    set 基本医疗统筹支付=case when b.累计基本医疗支付=200000 and b.基本医疗剩余额度=0 then 0
                         else b.基本医疗剩余额度
    					 end
    from #2019先累计二档 a join #临时2019 b on a.证件号码=b.证件号码 and a.序号=b.序号+1
    where a.基本医疗剩余额度=0

    update #2019先累计二档
    set 当次大病范围内费用=范围内费用-起付标准-基本医疗统筹支付
    									from #2019先累计二档
    									where 基本医疗剩余额度=0

    select @once=当次大病范围内费用,@序号=序号,@id=证件号码 from #2019先累计二档  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #2019先累计二档     
    set   @once   =   case   when   @序号   =   序号-1  then     @once   +   当次大病范围内费用 else 当次大病范围内费用  end,   
          @序号   =   序号,   
          累计大病范围内费用2   =   @once   
    --查看更新后的结果


    update #2019先累计二档
    set [大病（补充）医疗统筹支付]=case when a.累计大病范围内费用2 >120000 and b.累计大病范围内费用2 between @2019年起赔 and 120000
                                       and a.基本医疗剩余额度=0 and a.级别='非定点' 
    								     then (a.累计大病范围内费用2-120000)*0.6+(120000-b.累计大病范围内费用2)*0.5
                                        when a.累计大病范围内费用2 >120000 and b.累计大病范围内费用2 between @2019年起赔 and 120000
                                       and a.基本医疗剩余额度=0 and a.级别<>'非定点' 
    								    then (a.累计大病范围内费用2-120000)*0.7+(120000-b.累计大病范围内费用2)*0.6

    									when a.累计大病范围内费用2>120000 and b.累计大病范围内费用2>120000 and a.级别='非定点'
    									then (a.范围内费用-a.起付标准-a.基本医疗统筹支付)*0.6
    									when a.累计大病范围内费用2>120000 and b.累计大病范围内费用2>120000 and a.级别<>'非定点'
    									then (a.范围内费用-a.起付标准-a.基本医疗统筹支付)*0.7
    									end
    from #2019先累计二档 a join #临时2019 b on a.证件号码=b.证件号码 and a.序号=b.序号+1
    where a.基本医疗剩余额度=0 and a.建档立卡 is null and a.特困供养 is null

    update #2019先累计二档
    set [大病（补充）医疗统筹支付]=case when a.累计大病范围内费用2 >120000 and b.累计大病范围内费用2 between @2019年起赔*0.3 and 120000
                                       and a.基本医疗剩余额度=0 and a.级别='非定点' 
    								     then (a.累计大病范围内费用2-120000)*0.7+(120000-b.累计大病范围内费用2)*0.6
                                        when a.累计大病范围内费用2 >120000 and b.累计大病范围内费用2 between @2019年起赔*0.3 and 120000
                                       and a.基本医疗剩余额度=0 and a.级别<>'非定点' 
    								    then (a.累计大病范围内费用2-120000)*0.8+(120000-b.累计大病范围内费用2)*0.7

    									when a.累计大病范围内费用2>120000 and b.累计大病范围内费用2>120000 and a.级别='非定点'
    									then (a.范围内费用-a.起付标准-a.基本医疗统筹支付)*0.7
    									when a.累计大病范围内费用2>120000 and b.累计大病范围内费用2>120000 and a.级别<>'非定点'
    									then (a.范围内费用-a.起付标准-a.基本医疗统筹支付)*0.8
    									end
    from #2019先累计二档 a join #临时2019 b on a.证件号码=b.证件号码 and a.序号=b.序号+1
    where a.基本医疗剩余额度=0 and a.建档立卡='建档立卡' and a.特困供养 is null

    update #2019先累计二档
    set [大病（补充）医疗统筹支付]=case when a.累计大病范围内费用2 >120000 and b.累计大病范围内费用2 between @2019年起赔*0.2 and 120000
                                       and a.基本医疗剩余额度=0 and a.级别='非定点' 
    								     then (a.累计大病范围内费用2-120000)*0.8+(120000-b.累计大病范围内费用2)*0.7
                                        when a.累计大病范围内费用2 >120000 and b.累计大病范围内费用2 between @2019年起赔*0.2 and 120000
                                       and a.基本医疗剩余额度=0 and a.级别<>'非定点' 
    								    then (a.累计大病范围内费用2-120000)*0.9+(120000-b.累计大病范围内费用2)*0.8

    									when a.累计大病范围内费用2>120000 and b.累计大病范围内费用2>120000 and a.级别='非定点'
    									then (a.范围内费用-a.起付标准-a.基本医疗统筹支付)*0.8
    									when a.累计大病范围内费用2>120000 and b.累计大病范围内费用2>120000 and a.级别<>'非定点'
    									then (a.范围内费用-a.起付标准-a.基本医疗统筹支付)*0.9
    									end
    from #2019先累计二档 a join #临时2019 b on a.证件号码=b.证件号码 and a.序号=b.序号+1
    where a.基本医疗剩余额度=0 and a.建档立卡 is null  and a.特困供养='特困供养'



    update #2019先累计二档
    set [大病（补充）医疗统筹支付]=case when b.累计大病支付=240000 and b.大病保险剩余额度=0 then 0
                                   else b.大病保险剩余额度
    							   end
    from #2019先累计二档 a join #临时2019 b on a.证件号码=b.证件号码 and a.序号=b.序号+1
    where a.大病保险剩余额度=0

    update #2019先累计二档
    set 当次二档范围内费用=范围内费用-基本医疗统筹支付-[大病（补充）医疗统筹支付]-起付标准
    from #2019先累计二档
    where 基本医疗剩余额度=0

    update #2019先累计二档
    set 当次二档赔付费用=case when 级别<>'非定点' then (范围内费用-基本医疗统筹支付-[大病（补充）医疗统筹支付]-起付标准)*0.85
                              when 级别='非定点' then (范围内费用-基本医疗统筹支付-[大病（补充）医疗统筹支付]-起付标准)*0.75
    						  end
    from #2019先累计二档
    where 基本医疗剩余额度=0


    update #2019先累计二档
    set 当次二档赔付费用=case when b.年度内累计二档赔付费用=200000 and b.二档剩余额度=0 then 0
                         else b.二档剩余额度
    					 end
    from #2019先累计二档 a join #临时2019 b on a.证件号码=b.证件号码 and a.序号=b.序号+1
    where a.二档剩余额度=0

    update #2019先累计二档
    set 当次二档赔付费用=0
    from #2019先累计二档
    where 结算类别='居民'

    update #2019先累计二档
    set 二档剩余额度=0
    from #2019先累计二档
    where 结算类别='居民'

    update #2019先累计二档
    set 当次二档范围内费用=0
    from #2019先累计二档
    where 结算类别='居民'

    select @once=当次二档范围内费用,@序号=序号,@id=证件号码 from #2019先累计二档  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #2019先累计二档     
    set   @once   =   case   when   @序号   =   序号-1   then     @once   +   当次二档范围内费用 else 当次二档范围内费用  end,   
          @序号   =   序号,   
          累计二档范围内费用   =   @once   

    select @once=当次大病范围内费用,@序号=序号,@id=证件号码 from #2019先累计二档  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #2019先累计二档     
    set   @once   =   case   when   @序号   =   序号-1  then     @once   +   当次大病范围内费用 else 当次大病范围内费用  end,   
          @序号   =   序号,   
          累计大病范围内费用2   =   @once   
    --查看更新后的结果
    --drop table #临时2017
    drop table #临时2019
    --drop table #临时2019
    --drop table #临时20172
    drop table #临时20192
    --drop table #临时20192
    --drop table #临时大病2017
    drop table #临时大病2019
    --drop table #临时大病2019
    --drop table #汇总明细
    --drop table #tmp20191
    --drop table #tmp20193
    --drop table #起赔线排序一
    --drop table #起赔线排序二
    drop table #2019先累计二档tmp


    select * into #汇总  from #2019先累计二档





    --------------------------------------------------------------------------------
    ----------------------------------------------------------------------------------
    select 证件号码 into #2019先累计大病tmp from #tmp2019 where 首次范围内自付费用>@2019年起赔

    select * into #2019先累计大病 from #tmp2019 where 证件号码 in (select 证件号码 from #2019先累计大病tmp)



    update #2019先累计大病
    set 当次大病范围内费用=case when  基本医疗统筹支付<>0 then 范围内费用-基本医疗统筹支付-起付标准
                            else 0
    						end
    from #2019先累计大病 


    select @once=当次大病范围内费用,@序号=序号,@id=证件号码 from #2019先累计大病  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #2019先累计大病     
    set   @once   =   case   when   @序号   =   序号-1  then     @once   +   当次大病范围内费用 else 当次大病范围内费用  end,   
          @序号   =   序号,   
          累计大病范围内费用1   =   @once   
    --查看更新后的结果



    select rank()over(partition by 年份,证件号码 order by 累计大病范围内费用1 asc) as 大病序号,序号,年份,证件号码,出院日期
     into #起赔线排序三大病
    from #2019先累计大病 a
    where 累计大病范围内费用1>=@2019年起赔
    order by 证件号码 asc,年份 asc ,序号 asc,大病序号 asc

    update #2019先累计大病 
    set 超过起赔线=b.大病序号
    from #2019先累计大病  a left join #起赔线排序三大病 b on a.年份=b.年份 and a.证件号码=b.证件号码 and a.出院日期=b.出院日期 and a.序号=b.序号



    update #2019先累计大病
    set 累计大病范围内费用1=0
    from #2019先累计大病 where 超过起赔线 is null

    update #2019先累计大病
    set 当次大病范围内费用=范围内费用-基本医疗统筹支付-起付标准
    from #2019先累计大病 where 超过起赔线=1

    select @once=当次大病范围内费用,@序号=序号,@id=证件号码 from #2019先累计大病  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #2019先累计大病     
    set   @once   =   case   when   @序号   =   序号-1  then     @once   +   当次大病范围内费用 else 当次大病范围内费用  end,   
          @序号   =   序号,   
          累计大病范围内费用2   =   @once   
    --查看更新后的结果

    update #2019先累计大病
    set [大病（补充）医疗统筹支付]=case when 超过起赔线=1 and 累计大病范围内费用2 between @2019年起赔 and 120000 and 级别<>'非定点'
                                        then (累计大病范围内费用2-@2019年起赔)*0.6
    									when 超过起赔线=1 and 累计大病范围内费用2 between @2019年起赔 and 120000 and 级别='非定点'
                                        then (累计大病范围内费用2-@2019年起赔)*0.5

    									when 超过起赔线=1 and 累计大病范围内费用2>120000  and 级别<>'非定点'
    									then (累计大病范围内费用2-120000)*0.7+(120000-@2019年起赔)*0.6
    									when 超过起赔线=1 and 累计大病范围内费用2>120000  and 级别='非定点'
    									then (累计大病范围内费用2-120000)*0.6+(120000-@2019年起赔)*0.5
    									else 0
    									end
    									from #2019先累计大病 where 超过起赔线=1 and 特困供养 is null and 建档立卡 is null

    update #2019先累计大病
    set [大病（补充）医疗统筹支付]=case when 超过起赔线=1 and 累计大病范围内费用2 between @2019年起赔*0.3 and 120000 and 级别<>'非定点'
                                        then (累计大病范围内费用2-@2019年起赔)*0.7
    									when 超过起赔线=1 and 累计大病范围内费用2 between @2019年起赔*0.3 and 120000 and 级别='非定点'
                                        then (累计大病范围内费用2-@2019年起赔)*0.6

    									when 超过起赔线=1 and 累计大病范围内费用2>120000  and 级别<>'非定点'
    									then (累计大病范围内费用2-120000)*0.8+(120000-@2019年起赔*0.3)*0.7
    									when 超过起赔线=1 and 累计大病范围内费用2>120000  and 级别='非定点'
    									then (累计大病范围内费用2-120000)*0.7+(120000-@2019年起赔*0.3)*0.6
    									else 0
    									end
    									from #2019先累计大病 where 超过起赔线=1 and 建档立卡='建档立卡' and 特困供养 is null

    update #2019先累计大病
    set [大病（补充）医疗统筹支付]=case when 超过起赔线=1 and 累计大病范围内费用2 between @2019年起赔*0.2 and 120000 and 级别<>'非定点'
                                        then (累计大病范围内费用2-@2019年起赔)*0.8
    									when 超过起赔线=1 and 累计大病范围内费用2 between @2019年起赔*0.2 and 120000 and 级别='非定点'
                                        then (累计大病范围内费用2-@2019年起赔)*0.7

    									when 超过起赔线=1 and 累计大病范围内费用2>120000  and 级别<>'非定点'
    									then (累计大病范围内费用2-120000)*0.9+(120000-@2019年起赔*0.2)*0.8
    									when 超过起赔线=1 and 累计大病范围内费用2>120000  and 级别='非定点'
    									then (累计大病范围内费用2-120000)*0.8+(120000-@2019年起赔*0.2)*0.7
    									else 0
    									end
    									from #2019先累计大病 where 超过起赔线=1 and 特困供养='特困供养' and 建档立卡 is null


    select * into #临时大病2019先大病 from #2019先累计大病 

    update #2019先累计大病
    set [大病（补充）医疗统筹支付]=case when a.累计大病范围内费用2 between  @2019年起赔 and 120000 
                                             and b.累计大病范围内费用2 between  @2019年起赔 and 120000  and a.级别<>'非定点'
    									then a.当次大病范围内费用*0.6
    									when a.累计大病范围内费用2 between 120000 and 240000 and b.累计大病范围内费用2 between 120000 and 240000
    									 and a.级别<>'非定点'
    									then a.当次大病范围内费用*0.7

    									when b.累计大病范围内费用2 between @2019年起赔  and 120000 and a.累计大病范围内费用2 between 120000 and 240000
    									and  a.级别<>'非定点' then (120000-b.累计大病范围内费用2)*0.6+(a.累计大病范围内费用2-120000)*0.7

    									when a.累计大病范围内费用2 between  @2019年起赔 and 120000 
                                             and b.累计大病范围内费用2 between  @2019年起赔 and 120000  and a.级别='非定点'
    									then a.当次大病范围内费用*0.5
    									when a.累计大病范围内费用2 between 120000 and 240000 and b.累计大病范围内费用2 between 120000 and 240000
    									 and a.级别='非定点'
    									then a.当次大病范围内费用*0.6

    									when b.累计大病范围内费用2 between @2019年起赔  and 120000 and a.累计大病范围内费用2 between 120000 and 240000
    									and  a.级别='非定点' then (120000-b.累计大病范围内费用2)*0.5+(a.累计大病范围内费用2-120000)*0.6
    									else 0
    									end
    									from #2019先累计大病 a join #临时大病2019先大病 b on a.序号=b.序号+1 and a.证件号码=b.证件号码 
    									 where a.超过起赔线>1 and a.序号>1 and a.建档立卡 is null and a.特困供养 is null

    update #2019先累计大病
    set [大病（补充）医疗统筹支付]=case when a.累计大病范围内费用2 between  @2019年起赔*0.3 and 120000 
                                             and b.累计大病范围内费用2 between  @2019年起赔*0.3 and 120000  and a.级别<>'非定点'
    									then a.当次大病范围内费用*0.7
    									when a.累计大病范围内费用2 between 120000 and 240000 and b.累计大病范围内费用2 between 120000 and 240000
    									 and a.级别<>'非定点'
    									then a.当次大病范围内费用*0.8

    									when b.累计大病范围内费用2 between @2019年起赔*0.3  and 120000 and a.累计大病范围内费用2 between 120000 and 240000
    									and  a.级别<>'非定点' then (120000-b.累计大病范围内费用2)*0.7+(a.累计大病范围内费用2-120000)*0.8

    									when a.累计大病范围内费用2 between  @2019年起赔*0.3 and 120000 
                                             and b.累计大病范围内费用2 between  @2019年起赔*0.3 and 120000  and a.级别='非定点'
    									then a.当次大病范围内费用*0.6
    									when a.累计大病范围内费用2 between 120000 and 240000 and b.累计大病范围内费用2 between 120000 and 240000
    									 and a.级别='非定点'
    									then a.当次大病范围内费用*0.7

    									when b.累计大病范围内费用2 between @2019年起赔*0.3  and 120000 and a.累计大病范围内费用2 between 120000 and 240000
    									and  a.级别='非定点' then (120000-b.累计大病范围内费用2)*0.6+(a.累计大病范围内费用2-120000)*0.7
    									else 0
    									end
    									from #2019先累计大病 a join #临时大病2019先大病 b on a.序号=b.序号+1 and a.证件号码=b.证件号码 
    									 where a.超过起赔线>1 and a.序号>1 and a.建档立卡='建档立卡' and a.特困供养 is null

    update #2019先累计大病
    set [大病（补充）医疗统筹支付]=case when a.累计大病范围内费用2 between  @2019年起赔*0.2 and 120000 
                                             and b.累计大病范围内费用2 between  @2019年起赔*0.2 and 120000  and a.级别<>'非定点'
    									then a.当次大病范围内费用*0.8
    									when a.累计大病范围内费用2 between 120000 and 240000 and b.累计大病范围内费用2 between 120000 and 240000
    									 and a.级别<>'非定点'
    									then a.当次大病范围内费用*0.9

    									when b.累计大病范围内费用2 between @2019年起赔*0.2  and 120000 and a.累计大病范围内费用2 between 120000 and 240000
    									and  a.级别<>'非定点' then (120000-b.累计大病范围内费用2)*0.8+(a.累计大病范围内费用2-120000)*0.9

    									when a.累计大病范围内费用2 between  @2019年起赔*0.2 and 120000 
                                             and b.累计大病范围内费用2 between  @2019年起赔*0.2 and 120000  and a.级别='非定点'
    									then a.当次大病范围内费用*0.7
    									when a.累计大病范围内费用2 between 120000 and 240000 and b.累计大病范围内费用2 between 120000 and 240000
    									 and a.级别='非定点'
    									then a.当次大病范围内费用*0.8

    									when b.累计大病范围内费用2 between @2019年起赔*0.2  and 120000 and a.累计大病范围内费用2 between 120000 and 240000
    									and  a.级别='非定点' then (120000-b.累计大病范围内费用2)*0.7+(a.累计大病范围内费用2-120000)*0.8
    									else 0
    									end
    									from #2019先累计大病 a join #临时大病2019先大病 b on a.序号=b.序号+1 and a.证件号码=b.证件号码 
    									 where a.超过起赔线>1 and a.序号>1 and a.建档立卡 is null  and a.特困供养='特困供养'


    select @once=累计大病支付,@序号=序号,@id=证件号码 from #2019先累计大病  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #2019先累计大病     
    set   @once   =   case   when   @序号   =   序号-1   then     @once   +   [大病（补充）医疗统筹支付] else [大病（补充）医疗统筹支付]  end,   
          @序号   =   序号,   
          累计大病支付   =case when [大病（补充）医疗统筹支付]=0 then 0 
    	                       when @once<240000 or @once=240000 then @once else 240000 end  
    --查看更新后的结果

    update #2019先累计大病
    set 大病保险剩余额度 = case  when [大病（补充）医疗统筹支付]=0 then 240000
                                 when 累计大病支付<240000 then 240000-累计大病支付 else 0 end
    from #2019先累计大病


    update #2019先累计大病
    set 当次二档范围内费用=case when (范围内费用-起付标准-基本医疗统筹支付-[大病（补充）医疗统筹支付])>0 then 范围内费用-起付标准-基本医疗统筹支付-[大病（补充）医疗统筹支付]
                                else 0 end
    from #2019先累计大病 where 累计大病范围内费用2>@2019年起赔 and 结算类别='职工'



    select @once=当次二档范围内费用,@序号=序号,@id=证件号码 from #2019先累计大病  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #2019先累计大病     
    set   @once   =   case   when   @序号   =   序号-1   then     @once   +   当次二档范围内费用 else 当次二档范围内费用  end,   
          @序号   =   序号,   
          累计二档范围内费用   =   @once   
    --查看更新后的结果
    --------------先计算大病起赔线以下部分的二档--------------



    update #2019先累计大病
    set 当次二档赔付费用=case when 累计二档范围内费用 between 0 and 5000 and 级别<>'非定点' then 当次二档范围内费用*0.5
                              when 累计二档范围内费用 between 0 and 5000 and 级别='非定点' then 当次二档范围内费用*0.4
    						  when 累计二档范围内费用 between 5000 and 200000 and 级别<>'非定点' 
    						  then (5000)*0.5+(累计二档范围内费用-5000)*0.85
    						 when 累计二档范围内费用 between 5000 and 200000 and 级别='非定点' 
    						  then 当次二档范围内费用*0.75
    						  when 累计二档范围内费用 > 200000 and 级别<>'非定点' 
    						  then 5000*0.5+(200000-5000)*0.85+(累计二档范围内费用-200000)*0.9
    						  when 累计二档范围内费用 > 200000 and 级别='非定点' 
    						  then 5000*0.5+(200000-5000)*0.85+(累计二档范围内费用-200000)*0.9
    						  else 0
    						  end
    from #2019先累计大病 where 序号=1 and 结算类别='职工'

    select * into #临时20192先大病 from #2019先累计大病

    update #2019先累计大病
    set 当次二档赔付费用=case when a.累计二档范围内费用 between 0 and 5000
                               and b.累计二档范围内费用 between 0 and 5000  and a.级别<>'非定点' then a.当次二档范围内费用*0.5
                              when b.累计二档范围内费用 between 0 and 5000 and 
    						  a.累计二档范围内费用 between 5000 and 200000 and a.级别<>'非定点'
    						   then (5000-b.累计二档范围内费用)*0.5+(a.累计二档范围内费用-5000)*0.85

    						   when a.累计二档范围内费用 between 5000 and 200000 and a.级别<>'非定点' and
    						   b.累计二档范围内费用 between 5000 and 200000 then (a.当次二档范围内费用)*0.85

    						  when b.累计二档范围内费用 between 5000 and 200000 
    						  and a.累计二档范围内费用 >200000 and a.级别<>'非定点' 
    						  then (200000-b.累计二档范围内费用)*0.85+(a.当次二档范围内费用-200000)*0.9 

    						   when b.累计二档范围内费用>200000 and
    						  a.累计二档范围内费用 >200000 and a.级别<>'非定点' 
    						  then  (a.当次二档范围内费用)*0.9

    						when a.累计二档范围内费用 between 0 and 5000
                               and b.累计二档范围内费用 between 0 and 5000  and a.级别='非定点' then a.当次二档范围内费用*0.4
                              when b.累计二档范围内费用 between 0 and 5000 and 
    						  a.累计二档范围内费用 between 5000 and 200000 and a.级别='非定点'
    						   then (5000-b.累计二档范围内费用)*0.4+(a.累计二档范围内费用-5000)*0.75

    						   when a.累计二档范围内费用 between 5000 and 200000 and a.级别='非定点' and
    						   b.累计二档范围内费用 between 5000 and 200000 then (a.当次二档范围内费用)*0.75

    						  when b.累计二档范围内费用 between 5000 and 200000 
    						  and a.累计二档范围内费用 >200000 and a.级别='非定点' 
    						  then (200000-b.累计二档范围内费用)*0.75+(a.当次二档范围内费用-200000)*0.8 

    						   when b.累计二档范围内费用>200000 and
    						  a.累计二档范围内费用 >200000 and a.级别='非定点' 
    						  then  (a.当次二档范围内费用)*0.8
    						  else 0
    						  end
    from #2019先累计大病 a join #临时20192先大病 b on a.序号=b.序号+1 and a.证件号码=b.证件号码 where a.结算类别='职工' and b.结算类别='职工'



    select @once=当次二档赔付费用,@序号=序号,@id=证件号码 from #2019先累计大病  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #2019先累计大病     
    set   @once   =   case   when   @序号   =   序号-1   then     @once   +   当次二档赔付费用 else 当次二档赔付费用  end,   
          @序号   =   序号,   
          [年度内累计二档赔付费用]   =   @once  

    update #2019先累计大病
    set 二档剩余额度 = case when 年度内累计二档赔付费用<200000 then 200000-年度内累计二档赔付费用 else 0 end
    from #2019先累计大病

    select * into #临时2019先大病 from #2019先累计大病
    update #2019先累计大病
    set 基本医疗统筹支付=case when b.累计基本医疗支付=200000 and b.基本医疗剩余额度=0 then 0
                         else b.基本医疗剩余额度
    					 end
    from #2019先累计大病 a join #临时2019先大病 b on a.证件号码=b.证件号码 and a.序号=b.序号+1
    where a.基本医疗剩余额度=0

    update #2019先累计大病
    set 当次大病范围内费用=范围内费用-起付标准-基本医疗统筹支付
    									from #2019先累计大病
    									where 基本医疗剩余额度=0

    select @once=当次大病范围内费用,@序号=序号,@id=证件号码 from #2019先累计大病  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #2019先累计大病     
    set   @once   =   case   when   @序号   =   序号-1  then     @once   +   当次大病范围内费用 else 当次大病范围内费用  end,   
          @序号   =   序号,   
          累计大病范围内费用2   =   @once   
    --查看更新后的结果


    update #2019先累计大病
    set [大病（补充）医疗统筹支付]=case when a.累计大病范围内费用2 >120000 and b.累计大病范围内费用2 between @2019年起赔 and 120000
                                       and a.基本医疗剩余额度=0 and a.级别='非定点' 
    								     then (a.累计大病范围内费用2-120000)*0.6+(120000-b.累计大病范围内费用2)*0.5
                                        when a.累计大病范围内费用2 >120000 and b.累计大病范围内费用2 between @2019年起赔 and 120000
                                       and a.基本医疗剩余额度=0 and a.级别<>'非定点' 
    								    then (a.累计大病范围内费用2-120000)*0.7+(120000-b.累计大病范围内费用2)*0.6

    									when a.累计大病范围内费用2>120000 and b.累计大病范围内费用2>120000 and a.级别='非定点'
    									then (a.范围内费用-a.起付标准-a.基本医疗统筹支付)*0.6
    									when a.累计大病范围内费用2>120000 and b.累计大病范围内费用2>120000 and a.级别<>'非定点'
    									then (a.范围内费用-a.起付标准-a.基本医疗统筹支付)*0.7
    									end
    from #2019先累计大病 a join #临时2019先大病 b on a.证件号码=b.证件号码 and a.序号=b.序号+1
    where a.基本医疗剩余额度=0 and a.建档立卡 is null and a.特困供养 is null

    update #2019先累计大病
    set [大病（补充）医疗统筹支付]=case when a.累计大病范围内费用2 >120000 and b.累计大病范围内费用2 between @2019年起赔*0.3 and 120000
                                       and a.基本医疗剩余额度=0 and a.级别='非定点' 
    								     then (a.累计大病范围内费用2-120000)*0.7+(120000-b.累计大病范围内费用2)*0.6
                                        when a.累计大病范围内费用2 >120000 and b.累计大病范围内费用2 between @2019年起赔*0.3 and 120000
                                       and a.基本医疗剩余额度=0 and a.级别<>'非定点' 
    								    then (a.累计大病范围内费用2-120000)*0.8+(120000-b.累计大病范围内费用2)*0.7

    									when a.累计大病范围内费用2>120000 and b.累计大病范围内费用2>120000 and a.级别='非定点'
    									then (a.范围内费用-a.起付标准-a.基本医疗统筹支付)*0.7
    									when a.累计大病范围内费用2>120000 and b.累计大病范围内费用2>120000 and a.级别<>'非定点'
    									then (a.范围内费用-a.起付标准-a.基本医疗统筹支付)*0.8
    									end
    from #2019先累计大病 a join #临时2019先大病 b on a.证件号码=b.证件号码 and a.序号=b.序号+1
    where a.基本医疗剩余额度=0 and a.建档立卡='建档立卡' and a.特困供养 is null

    update #2019先累计大病
    set [大病（补充）医疗统筹支付]=case when a.累计大病范围内费用2 >120000 and b.累计大病范围内费用2 between @2019年起赔*0.2 and 120000
                                       and a.基本医疗剩余额度=0 and a.级别='非定点' 
    								     then (a.累计大病范围内费用2-120000)*0.8+(120000-b.累计大病范围内费用2)*0.7
                                        when a.累计大病范围内费用2 >120000 and b.累计大病范围内费用2 between @2019年起赔*0.2 and 120000
                                       and a.基本医疗剩余额度=0 and a.级别<>'非定点' 
    								    then (a.累计大病范围内费用2-120000)*0.9+(120000-b.累计大病范围内费用2)*0.8

    									when a.累计大病范围内费用2>120000 and b.累计大病范围内费用2>120000 and a.级别='非定点'
    									then (a.范围内费用-a.起付标准-a.基本医疗统筹支付)*0.8
    									when a.累计大病范围内费用2>120000 and b.累计大病范围内费用2>120000 and a.级别<>'非定点'
    									then (a.范围内费用-a.起付标准-a.基本医疗统筹支付)*0.9
    									end
    from #2019先累计大病 a join #临时2019先大病 b on a.证件号码=b.证件号码 and a.序号=b.序号+1
    where a.基本医疗剩余额度=0 and a.建档立卡 is null  and a.特困供养='特困供养'


    update #2019先累计大病
    set [大病（补充）医疗统筹支付]=case when b.累计大病支付=240000 and b.大病保险剩余额度=0 then 0
                                   else b.大病保险剩余额度
    							   end
    from #2019先累计大病 a join #临时2019先大病 b on a.证件号码=b.证件号码 and a.序号=b.序号+1
    where a.大病保险剩余额度=0

    update #2019先累计大病
    set 当次二档范围内费用=范围内费用-基本医疗统筹支付-[大病（补充）医疗统筹支付]-起付标准
    from #2019先累计大病
    where 基本医疗剩余额度=0

    update #2019先累计大病
    set 当次二档赔付费用=case when 级别<>'非定点' then (范围内费用-基本医疗统筹支付-[大病（补充）医疗统筹支付]-起付标准)*0.85
                              when 级别='非定点' then (范围内费用-基本医疗统筹支付-[大病（补充）医疗统筹支付]-起付标准)*0.75
    						  end
    from #2019先累计大病
    where 基本医疗剩余额度=0


    update #2019先累计大病
    set 当次二档赔付费用=case when b.年度内累计二档赔付费用=200000 and b.二档剩余额度=0 then 0
                         else b.二档剩余额度
    					 end
    from #2019先累计大病 a join #临时2019先大病 b on a.证件号码=b.证件号码 and a.序号=b.序号+1
    where a.二档剩余额度=0

    update #2019先累计大病
    set 当次二档赔付费用=0
    from #2019先累计大病
    where 结算类别='居民'

    update #2019先累计大病
    set 二档剩余额度=0
    from #2019先累计大病
    where 结算类别='居民'

    update #2019先累计大病
    set 当次二档范围内费用=0
    from #2019先累计大病
    where 结算类别='居民'

    select @once=当次二档范围内费用,@序号=序号,@id=证件号码 from #2019先累计大病  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #2019先累计大病     
    set   @once   =   case   when   @序号   =   序号-1   then     @once   +   当次二档范围内费用 else 当次二档范围内费用  end,   
          @序号   =   序号,   
          累计二档范围内费用   =   @once   

    select @once=当次大病范围内费用,@序号=序号,@id=证件号码 from #2019先累计大病  where 序号=1  
    --开始更新,注意SQL执行更新时，是一行行更新数据.  
    update   #2019先累计大病     
    set   @once   =   case   when   @序号   =   序号-1  then     @once   +   当次大病范围内费用 else 当次大病范围内费用  end,   
          @序号   =   序号,   
          累计大病范围内费用2   =   @once   

    insert into #汇总
    select *  from #2019先累计大病

    --select * from #汇总 where 年份='2018' order by 序号 asc

    select  年份,证件号码,结算类别,sum(医疗费用总额)as 医疗总费用
    ,sum(范围内费用)as 范围内费用,sum(当次大病范围内费用) as 累计大病范围内费用,
    sum(基本医疗统筹支付) as 基本医疗支付,sum([大病（补充）医疗统筹支付])as 大病支付,
    sum(当次二档赔付费用)as 二档赔付 into #tmp2
    from #汇总
    --where  left(出院日期,4)in('2014','2015','2016')
    group by  年份 ,证件号码,结算类别

    alter table #tmp2 add 分段 varchar(10)
    update #tmp2
    set 分段=case
    -- --when 年份='2017' and  累计自付 <2000 then '<2千'
    -- --             when 年份='2017' and 累计自付 >2000 or 累计自付=2000 then '>2千'
    			  when 
    			  --年份 in ('2018','2019') and  
    			  累计大病范围内费用<10000 then '<1万'
    			  when 
    			  --年份 in ('2018','2019') and  
    			  累计大病范围内费用>10000 or 累计大病范围内费用=10000 then '>1万'
    			  end
    update #tmp2
    set 分段=case when 分段 is null then '<1万'
    end
    from #tmp2
    where 分段 is null
    '''

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