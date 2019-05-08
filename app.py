# -*- coding:UTF-8-*-
from flask import Flask
import cx_Oracle
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
from flask import render_template
import FP,FP_ASSET,FP_BASIC,FP_DEALER
import tool
from datetime import datetime, date, timedelta

# tns = cx_Oracle.makedsn('10.21.135.14', 1521, 'cms')
tns = cx_Oracle.makedsn('10.21.135.14', 1521, 'cms')

# engine = create_engine('oracle://snpw:snpw@192.168.137.135/orcl',echo=True)
# engine = create_engine('oracle://bbaf_retail_uat:netsolpk@10.21.135.14/cms',echo=True,encoding='UTF-8')
app = Flask(__name__)


@app.route('/')
def hello_world():


    db = cx_Oracle.connect('tony_test', 'test', tns);

    hm_fp= tool.HashMap()
    cr_fp = db.cursor();
    sql_fp= "select cf.financial_product_id||','||cf.term as \"financial_product_id\" , cf.financial_product_nme from  CURRENT_FP cf  " \
                                                                                  "union " \
                                                                                  "select cf.financial_product_id||','||cf.term as \"financial_product_id\", cf.financial_product_nme from  LAST_FP cf ";
    cr_fp.execute(sql_fp);
    rs_fp = cr_fp.fetchall();
    for x in rs_fp:
        fp = FP_BASIC.FP_BASIC(str(x[0]), str(x[1]).decode("utf-8"))
        hm_fp.put(str(x[0]), fp);
    cr_fp.close()

    cr_fp_old = db.cursor();
    sql_fp_old = "select cf.financial_product_id, cf.financial_product_nme,cf.valid_from_dte,cf.valid_to_dte,cf.Minimum_Financing_Amt,cf.Maximum_Financing_Amt,cf.minimum_lease_trm,cf.maximun_lease_trm ," \
          " cf.MAXIMUM_FINANCING_PCT,cf.ACTUAL_RTE,cf.CUSTOMER_RTE,cf.SUBSIDY_RTE,cf.term from  CURRENT_FP cf  " \
          " minus " \
          "  select  lf.financial_product_id, lf.financial_product_nme,lf.valid_from_dte,lf.valid_to_dte,lf.Minimum_Financing_Amt,lf.Maximum_Financing_Amt,lf.minimum_lease_trm,lf.maximun_lease_trm, "\
            " lf.MAXIMUM_FINANCING_PCT,lf.ACTUAL_RTE,lf.CUSTOMER_RTE,lf.SUBSIDY_RTE,lf.term  from  LAST_FP  lf  ";
    hm_fp_old = tool.HashMap()
    cr_fp_old.execute(sql_fp_old);
    rs_fp_old = cr_fp_old.fetchall();
    my_list=[];
    key_list=[]
    for x in rs_fp_old:
        fp_old=FP.FP(str(x[0]),str(x[1]).decode("utf-8"),str(x[2]),str(x[3]),str(x[4]),str(x[5]),str(x[6]),str(x[7]),str(x[8]),str(x[9]),str(x[10]),str(x[11]),str(x[12]))
        hm_fp_old.put(str(x[0])+','+str(x[12]),fp_old);
        key_list.append(str(x[0])+','+str(x[12]));
    cr_fp_old.close()



    sql_fp_new = "select  lf.financial_product_id, lf.financial_product_nme,lf.valid_from_dte,lf.valid_to_dte,lf.Minimum_Financing_Amt,lf.Maximum_Financing_Amt,lf.minimum_lease_trm,lf.maximun_lease_trm,  " \
              " lf.MAXIMUM_FINANCING_PCT,lf.ACTUAL_RTE,lf.CUSTOMER_RTE,lf.SUBSIDY_RTE,lf.term  from  LAST_FP  lf " \
" minus  " \
" select cf.financial_product_id, cf.financial_product_nme,cf.valid_from_dte,cf.valid_to_dte,cf.Minimum_Financing_Amt,cf.Maximum_Financing_Amt,cf.minimum_lease_trm,cf.maximun_lease_trm ," \
" cf.MAXIMUM_FINANCING_PCT,cf.ACTUAL_RTE,cf.CUSTOMER_RTE,cf.SUBSIDY_RTE,cf.term " \
" from  CURRENT_FP cf " ;

    hm_fp_new=tool.HashMap()
    cr_fp_new = db.cursor();
    cr_fp_new.execute(sql_fp_new);
    rs_fp_new = cr_fp_new.fetchall();
    my_list1=[];
    for x in rs_fp_new:
        fp_new=FP.FP(str(x[0]),str(x[1]).decode("utf-8"),str(x[2]),str(x[3]),str(x[4]),str(x[5]),str(x[6]),str(x[7]),str(x[8]),str(x[9]),str(x[10]),str(x[11]),str(x[12]))
        hm_fp_new.put(str(x[0])+','+str(x[12]),fp_new);
        # my_list1.append(fp1)
        key_list.append(str(x[0])+','+str(x[12]));
    cr_fp_new.close()

    sql_fp_asset_old = "select cf.financial_product_id||','||cf.term  ,cfas.financial_product_nme,cfas.makemodel_group_nme,cfas.asset_model_dsc "\
    " from current_fp cf left join current_fp_asset_series cfas on cf.financial_product_id = cfas.financial_product_id  " \
                    " minus  " \
                    " select lf.financial_product_id||','||lf.term  ,lfas.financial_product_nme,lfas.makemodel_group_nme,lfas.asset_model_dsc from last_fp lf " \
                       " left join last_fp_asset_series lfas on lf.financial_product_id = lfas.financial_product_id ";

    hm_fp_asset_old = tool.HashMap()
    cr_fp_asset_old = db.cursor();
    cr_fp_asset_old.execute(sql_fp_asset_old);
    rs_fp_asset_old = cr_fp_asset_old.fetchall();
    fp_asset_old_list = [];
    for x in rs_fp_asset_old:

        fp_asset_old_list= hm_fp_asset_old.get(str(x[0]));
        if fp_asset_old_list == None:
            fp_asset_old_list = [];
        fp_asset_old = FP_ASSET.FP_ASSET(str(x[0]), str(x[1]).decode("utf-8"), str(x[2]).decode("utf-8"))
        fp_asset_old_list.append(fp_asset_old);
        hm_fp_asset_old.put(str(x[0]), fp_asset_old_list);
        # my_list1.append(fp1)
        key_list.append(str(x[0]));


    cr_fp_asset_old.close()

    sql_fp_asset_new =  "select lf.financial_product_id||','||lf.term ,lfas.financial_product_nme,lfas.makemodel_group_nme,lfas.asset_model_dsc " \
                       " from last_fp lf left join last_fp_asset_series lfas on lf.financial_product_id = lfas.financial_product_id  " \
                        " minus   select cf.financial_product_id||','||cf.term ,cfas.financial_product_nme,cfas.makemodel_group_nme,cfas.asset_model_dsc  " \
                       "from current_fp cf left join current_fp_asset_series cfas on cf.financial_product_id = cfas.financial_product_id "  ;
    hm_fp_asset_new = tool.HashMap()
    cr_fp_asset_new = db.cursor();
    cr_fp_asset_new.execute(sql_fp_asset_new);
    rs_fp_asset_new = cr_fp_asset_new.fetchall();
    fp_asset_new_list = [];
    for x in rs_fp_asset_new:

        fp_asset_new_list=hm_fp_asset_new.get(str(x[0]));
        if fp_asset_new_list == None:
            fp_asset_new_list = [];
        fp_asset_new = FP_ASSET.FP_ASSET(str(x[0]), str(x[1]).decode("utf-8"), str(x[2]).decode("utf-8"))
        fp_asset_new_list.append(fp_asset_new)
        key_list.append(str(x[0]));
        hm_fp_asset_new.put(str(x[0]), fp_asset_new_list);

    cr_fp_asset_new.close()

    sql_fp_dealer_old = "select cf.financial_product_id||','||cf.term ,cfd.dealer_name from current_fp cf " \
                        "left join current_fp_dealer cfd on cf.financial_product_id = cfd.financial_product_id " \
                        " minus " \
                        " select lf.financial_product_id||','||lf.term  ,lfd.dealer_name from last_fp lf left join last_fp_dealer lfd " \
                        "on lf.financial_product_id = lfd.financial_product_id ";

    hm_fp_dealer_old = tool.HashMap();
    cr_fp_dealer_old = db.cursor();
    cr_fp_dealer_old.execute(sql_fp_dealer_old);
    rs_fp_dealer_old = cr_fp_dealer_old.fetchall();
    fp_dealer_old_list = [];
    for x in rs_fp_dealer_old:

        fp_dealer_old_list = hm_fp_dealer_old.get(str(x[0]));
        if fp_dealer_old_list == None:
            fp_dealer_old_list = [];
        fp_dealer_old = FP_DEALER.FP_DEALER(str(x[0]), str(x[1]).decode("utf-8"))
        fp_dealer_old_list.append(fp_dealer_old);
        hm_fp_dealer_old.put(str(x[0]), fp_dealer_old_list);
        # my_list1.append(fp1)
        key_list.append(str(x[0]));

    cr_fp_dealer_old.close()

    sql_fp_dealer_new = "select lf.financial_product_id||','||lf.term  ,lfd.dealer_name from last_fp lf left join last_fp_dealer lfd  on lf.financial_product_id = lfd.financial_product_id  " \
                        " minus " \
                        "select cf.financial_product_id||','||cf.term  ,cfd.dealer_name from current_fp cf left join current_fp_dealer cfd on cf.financial_product_id = cfd.financial_product_id ";

    hm_fp_dealer_new = tool.HashMap()
    cr_fp_dealer_new = db.cursor();
    cr_fp_dealer_new.execute(sql_fp_dealer_new);
    rs_fp_dealer_new = cr_fp_dealer_new.fetchall();
    fp_dealer_new_list = [];
    for x in rs_fp_dealer_new:

        fp_dealer_new_list = hm_fp_dealer_new.get(str(x[0]));
        if fp_dealer_new_list == None:
            fp_dealer_new_list = [];
        fp_dealer_new = FP_DEALER.FP_DEALER(str(x[0]), str(x[1]).decode("utf-8"))
        fp_dealer_new_list.append(fp_dealer_new)
        key_list.append(str(x[0]));
        hm_fp_dealer_new.put(str(x[0]), fp_dealer_new_list);

    cr_fp_dealer_new.close()


    db.close()
    key_list=list(set(key_list));
    # key_list=map(int, key_list)
    key_list.sort();
    # key_list = map(str, key_list)
    title='金融产品变化明细';
    today=date.today().strftime("%Y-%m-%d");
    yesterday = (date.today() + timedelta(days = -1)).strftime("%Y-%m-%d");


    num = len(key_list);

    return render_template(

        'helloworld.html',
        title=title.decode("utf-8"),
        hm_fp=hm_fp,
        hm_fp_old=hm_fp_old,
        hm_fp_new=hm_fp_new,
        hm_fp_asset_old=hm_fp_asset_old,
        hm_fp_asset_new=hm_fp_asset_new,
        hm_fp_dealer_old=hm_fp_dealer_old,
        hm_fp_dealer_new=hm_fp_dealer_new,
        key_list=key_list,
        today=today,
        yesterday=yesterday,
        num=num
    )
# def getdata(str):
#     db = cx_Oracle.connect('snpw', 'snpw', tns)
#     cr = db.cursor();
#     cr1.execute(sql_new);
#     rs1 = cr1.fetchall();
#     for x in rs1:
#         fp_new = FP.FP(str(x[0]), str(x[1]).decode("utf-8"), str(x[2]), str(x[3]), str(x[4]), str(x[5]), str(x[6]),
#                        str(x[7]), str(x[8]), str(x[9]), str(x[10]), str(x[11]), str(x[12]))
#         hm_new.put(str(x[0]), fp_new);
#         # my_list1.append(fp1)
#         key_list.append(str(x[0]));
#     cr1.close()
#     db.close()

if __name__ == '__main__':
    # hello_world()
    app.run(debug=True)
