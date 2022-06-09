
"""
scannette csv

steps |timestamp| id_client | id_object | event | parameter | return_code


"""
import time
import random
import csv

allEvents=['debloquer','scanner','transmission','payer','abandon','ouvrirSession','ajouter','fermerSession','supprimer']
scannerEvents=['debloquer','scanner','transmission','abandon','supprimer']
cashierEvents=['payer','ouvrirSession','ajouter','fermerSession']

defined_articles = {
    5410188006711: {"ean": 5410188006711, "prix": 2.15, "libelle": "Tropicana Tonic Breakfast", "rayon": 13},
    3560070048786: {"ean": 3560070048786, "prix": 0.87, "libelle": "Cookies choco", "rayon": 3},
    3017800238592: {"ean": 3017800238592, "prix": 2.20,
                    "libelle": "Daucy Curry vert de légumes riz graines de courge et tournesol", "rayon": 2},
    3560070976478: {"ean": 3560070976478, "prix": 1.94, "libelle": "Poulet satay et son riz", "rayon": 2},
    3046920010856: {"ean": 3046920010856, "prix": 2.01, "libelle": "Lindt Excellence Citron à la pointe de Gingembre",
                    "rayon": 12},
    8715700110622: {"ean": 8715700110622, "prix": 0.96, "libelle": "Ketchup", "rayon": 10},
    3520115810259: {"ean": 3520115810259, "prix": 8.49, "libelle": "Mont d'or moyen Napiot", "rayon": 6},
    3270190022534: {"ean": 3270190022534, "prix": 0.58, "libelle": "Pâte feuilletée", "rayon": 11},
    8718309259938: {"ean": 8718309259938, "prix": 4.65, "libelle": "Soda stream saveur agrumes", "rayon": 14},
    3560071097424: {"ean": 3560071097424, "prix": 2.40, "libelle": "Tartelettes carrées fraise", "rayon": 3},
    3017620402678: {"ean": 3017620402678, "prix": 1.86, "libelle": "Nutella 220g", "rayon": 1},
    3245412567216: {"ean": 3245412567216, "prix": 1.47, "libelle": "Pain de mie", "rayon": 1},
    45496420598: {"ean": 45496420598, "prix": 54.99, "libelle": "Jeu switch Minecraft", "rayon": 7},
    3560070139675: {"ean": 3560070139675, "prix": 1.94, "libelle": "Boîte de 110 mouchoirs en papier", "rayon": 5},
    3020120029030: {"ean": 3020120029030, "prix": 1.70, "libelle": "Cahier Oxford 90 pages petits carreaux", "rayon": 0},
    3474377910724: {"ean": 3474377910724, "prix": 8.60, "libelle": "Sortez couverts !", "rayon": 5},
}
undefined_articles={
7640164630021 : {"ean": 7640164630021, "prix": 229.90, "libelle": "Robot éducatif Thymio", "rayon": 7},
3570590109324 : {"ean": 3570590109324, "prix": 7.48, "libelle": "Vin blanc Arbois Vieilles Vignes", "rayon": 6}
}





class ParametersFiller:


    def __init__(self,encoding_type=0,separative_token='_',export_separative_token=','):
        """

        :param encoding_type:
            0: event + return_code
            1: event + return_code + parameter

        """
        self.separative_token=separative_token

        self.current_step=0
        self.encoding_type=encoding_type
        self.current_customer_id=0
        self.decoded_traces=[]
    def decode(self,trace):

        seq=self.import_trace(trace)

        next_u_to_delete_i=0
        l=[0,1,2,3]
        scanner_id=random.choice(l)
        cashier_id=random.choice(l)
        rows=[]
        price = 0
        beforeProofreading = True
        beforeSession=True
        scanned_ean = []
        undefined_ean_to_delete=[]
        undefined_ean = []

        for event in seq:

            method_name = event[0]
            return_code = event[1]
            parameter=''
            row=[]
            cashierDeleting = False
            #adding step_id to row
            row.append(self.current_step)
            self.current_step+=1

            #adding current timestamp to row
            row.append(self.current_step)

            #adding client_id to row
            row.append("client"+str(self.current_customer_id))



            if method_name=='scanner' and return_code=='0' and beforeProofreading:
                ean=random.choice(list(defined_articles.keys()))
                scanned_ean.append(ean)
                price+=float(defined_articles[ean]['prix'])
                parameter=str(ean)



            if method_name=='scanner' and return_code=='-2' and beforeProofreading:
                ean = random.choice(list(undefined_articles.keys()))
                undefined_ean.append(ean)
                price += float(undefined_articles[ean]['prix'])
                parameter = str(ean)



            if method_name=="supprimer" and return_code =='0':
                if beforeSession:
                    ean=random.choice(scanned_ean)
                    scanned_ean.remove(ean)
                    price -= defined_articles[ean]['prix']
                else:
                    cashierDeleting=True
                    ean=random.choice(undefined_ean_to_delete)
                    undefined_ean_to_delete.remove(ean)
                    price -= undefined_articles[ean]['prix']

                parameter = str(ean)
            if method_name=='supprimer' and return_code=='-2':
                ean=undefined_ean[next_u_to_delete_i]
                next_u_to_delete_i+=1
                parameter = str(ean)
                undefined_ean_to_delete.append(ean)
            if method_name=='transmission' and return_code =="1":
                beforeProofreading=False

            if method_name=='scanner' and return_code=='0' and not(beforeProofreading):
                ean=scanned_ean.pop(0)
                parameter=str(ean)
            if method_name=='ajouter' and return_code=='0':
                ean=undefined_ean.pop(0)
                parameter = str(ean)
            if method_name =='scanner' and return_code=='-3':
                if len(scanned_ean)==0:
                    ean=random.choice(list(defined_articles.keys()))
                    parameter=str(ean)
                else:
                    ean=random.choice(list(set(defined_articles.keys())-set(scanned_ean)))
                    parameter=str(ean)
            if method_name=='payer':
                if 0==random.choice([0,1]):
                    more=float(round(random.random()*100,2))
                else:
                    more=0
                parameter=str(price+more)
                return_code=str(more)
            if method_name == 'transmission':
                parameter = 'caisse' + str(cashier_id)

            if method_name =='ouvrirSession':
                beforeSession=False



            if method_name in scannerEvents and not(cashierDeleting):
                row.append('scan'+str(scanner_id))
            elif method_name in cashierEvents or cashierDeleting:
                row.append('caisse'+str(cashier_id))
            else:
                raise ValueError('the method name havent been identified as a scanAction or caisseAction, '+str(event[0])+"is undefined")
            row.append(method_name)
            row.append('['+str(parameter)+']')
            row.append(return_code)
            rows.append(row)
            self.current_step+=1


        self.decoded_traces+=rows

        self.current_customer_id +=1
        return rows

    def import_trace(self,trace):
        seq=[]
        for event in trace:
            seq.append(event.split(self.separative_token))

        return seq

    def export_csv(self,path='.data/out.csv'):
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.decoded_traces)
    def export_list_of_traces(self):
        return self.decoded_traces
if __name__=='__main__':
    # trace_w_p=['debloquer__0', 'scanner_8718309259938_0', 'scanner_3020120029030_0', 'scanner_3020120029030_0', 'scanner_3474377910724_0', 'scanner_3020120029030_0', 'scanner_3020120029030_0', 'scanner_3560071097424_0', 'scanner_3046920010856_0', 'scanner_3017800238592_0', 'scanner_3020120029030_0', 'scanner_45496420598_0', 'scanner_3020120029030_0', 'scanner_45496420598_0', 'transmission_caisse1_0', 'abandon__?', 'payer_1_0']
    # traces=[['debloquer_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'transmission_0', 'abandon_?', 'payer_1'],['debloquer_0', 'scanner_0', 'transmission_0', 'abandon_?', 'payer_1']]


    # for t in traces:
    #     p.decode(t)
    # print(p)

    # p.export_csv('./demo_1811.csv')


    trace=['debloquer_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'scanner_0', 'transmission_0', 'abandon_?', 'payer_1']

    p = ParametersFiller()
    decoded_trace = p.decode(trace)
    for event in decoded_trace:
        print(event, '\n')