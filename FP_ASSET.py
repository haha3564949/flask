# -*- coding: UTF-8 -*-

class FP_ASSET:

    def __init__(self, financial_product_id, financial_product_nme,makemodel_group_nme):
        self.financial_product_id = financial_product_id;
        self.financial_product_nme = financial_product_nme;
        self.makemodel_group_nme=makemodel_group_nme;



    def displayFP_ASSET(self):
        print "financial_product_nme : ", self.financial_product_nme, ", asset_model_dsc: ", self.asset_model_dsc


