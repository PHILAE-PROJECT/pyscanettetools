from random import choice
from ScannetteStateMachine import ScannetteStateMachine
from Postprocessing import Postprocessing
import json


class ScannetteGenerator:

    def __init__(self,number_of_sessions=1000):
        self.traces=[]

        # self.scenarios={
        # ('only_known_ref','proofreading'): 150}
        # X=int(1000000/20)
        self.number_of_sessions=number_of_sessions
        self.scenarios={
        ('unknown_ref', 'deletion'): 578,
         ('only_known_ref', 'deletion'): 639,
         ('proofreading', 'deletion', 'scanner_not_in_basket_while_rescanning'): 4,
         ('unknown_ref', 'deletion', 'deletion_error'): 28,
         ('only_known_ref',
          'proofreading',
          'deletion',
          'scanner_not_in_basket_while_rescanning'): 3,
         ('only_known_ref', 'proofreading'): 641,
         ('only_known_ref', 'proofreading', 'deletion_error'): 1,
         ('unknown_ref', 'proofreading'): 541,
         ('only_known_ref',
          'proofreading',
          'scanner_not_in_basket_while_rescanning'): 39,
         ('proofreading',
          'deletion_error',
          'scanner_not_in_basket_while_rescanning'): 1,
         ('proofreading', 'scanner_not_in_basket_while_rescanning'): 34,
         ('unknown_ref', 'proofreading', 'deletion', 'deletion_error'): 3,
         ('unknown_ref',): 5292,
         ('only_known_ref',): 6384,
         ('unknown_ref', 'proofreading', 'deletion'): 52,
         ('only_known_ref', 'proofreading', 'deletion'): 78,
         ('unknown_ref', 'deletion_error'): 108,
         ('only_known_ref', 'deletion_error'): 9,
         ('unknown_ref', 'proofreading', 'deletion_error'): 8}

    def balanced_dataset(self):
        for key in self.scenarios.keys():
            self.scenarios[key]=int(self.number_of_sessions/len(list(self.scenarios.keys())))

    def create_raw_dataset(self):
        for tags, number_of_sessions in self.scenarios.items():

            ONLY_KNOWN_REF = 'only_known_ref' in tags
            PROOFREADING = 'proofreading' in tags
            DELETION = 'deletion' in tags
            DELETION_ERROR = 'deletion_error' in tags
            NOT_IN_BASKET_WHILE_RESCANNING = 'scanner_not_in_basket_while_rescanning' in tags
            CHANGE= choice([True,False])
            for i in range(number_of_sessions):

                stm=ScannetteStateMachine(only_known_ref=ONLY_KNOWN_REF,change=CHANGE,deletion=DELETION,deletion_error=DELETION_ERROR,not_in_basket_while_rescanning=NOT_IN_BASKET_WHILE_RESCANNING,proofreading=PROOFREADING)
                stm.play()
                self.traces.append(stm.trace)

    def print_hyperparameters(self):
        pass
    def export_dataset(self,path):
        p = Postprocessing()
        for i,trace in enumerate(self.traces):
            # print('\n '.join(trace))
            decoded_trace = p.decode(trace)
        p.export_csv(path)
    def export_json(self,path):
        with open(path, "w") as outfile:
            json.dump(self.traces, outfile)
if __name__=='__main__':
    import time
    b=time.time()
    g=ScannetteGenerator(number_of_sessions=150)
    g.balanced_dataset()
    g.create_raw_dataset()
    # g.export_json("40000-steps.json")
    g.export_dataset(path='../csv/fake_generation_150.csv')
    print(time.time()-b)
