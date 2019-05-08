# -*- coding: UTF-8 -*-

class FP:

    def __init__(self, financial_product_id, financial_product_nme,valid_from_dte,valid_to_dte,Minimum_Financing_Amt,Maximum_Financing_Amt,minimum_lease_trm,maximun_lease_trm ,MAXIMUM_FINANCING_PCT,ACTUAL_RTE,CUSTOMER_RTE,SUBSIDY_RTE,term):
        self.financial_product_id = financial_product_id;
        self.financial_product_nme = financial_product_nme;
        self.valid_from_dte=valid_from_dte;
        self.valid_to_dte=valid_to_dte;
        self.Minimum_Financing_Amt=Minimum_Financing_Amt;
        self.Maximum_Financing_Amt=Maximum_Financing_Amt;
        self.minimum_lease_trm=minimum_lease_trm;
        self.maximun_lease_trm=maximun_lease_trm;
        self.MAXIMUM_FINANCING_PCT=MAXIMUM_FINANCING_PCT;
        self.ACTUAL_RTE=ACTUAL_RTE;
        self.CUSTOMER_RTE=CUSTOMER_RTE;
        self.SUBSIDY_RTE=SUBSIDY_RTE;
        self.term=term;

    def displayFP(self):
        print "financial_product_nme : ", self.financial_product_nme, ", term: ", self.term


