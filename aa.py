# -*- coding: utf8 -*-
# import pandas as pd
# from  sqlalchemy import create_engine
#
# # engine = create_engine('oracle://snpw:snpw@192.168.137.135/orcl',echo=True)
# engine = create_engine('oracle://bbaf_retail_uat:netsolpk@10.21.135.14/cms',encoding='utf8')
#
# df = pd.read_sql("select  bm.business_partner_nme from bp_main bm where rownum<10",engine)
#
# my_list = df.values.tolist();
# print my_list
# print "啊哈 "
#
import cx_Oracle
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

tns = cx_Oracle.makedsn('10.21.135.14', 1521, 'cms')

db = cx_Oracle.connect('bbaf_retail_uat', 'netsolpk', tns)
cr = db.cursor();
sql= "select  bm.business_partner_nme from bp_main bm where rownum<10";
cr.execute(sql);
rs=cr.fetchall();
for x in rs:
    print x[0].decode('UTF-8')
cr.close()
db.close()

