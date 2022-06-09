from random import randint,uniform,choices
class ScannetteStateMachine:

    def __init__(self,separative_token='_',only_known_ref=True,change=True,proofreading=True,deletion=True,deletion_error=True,not_in_basket_while_rescanning=False):
        self.sp=separative_token
        self.trace=[]
        
        self.ONLY_KNOWN_REF=only_known_ref
        self.CHANGE=change
        self.PROOFREADING=proofreading
        self.DELETION=deletion
        self.DELETION_ERROR=deletion_error
        self.NOT_IN_BASKET_WHILE_RESCANNING=not_in_basket_while_rescanning
        



        self.k_currently_in_basket = 0
        self.u_currently_in_basket = 0




        self.total_de=0
        self.total_u = 0
        self.total_d =0
        self.total_k = randint(2, 6)

        self.k_LTB = self.total_k
        self.u_LTB = 0
        self.d_LTD = 0
        self.de_LTD = 0

        if not(self.ONLY_KNOWN_REF):
            self.total_u=randint(1,3)
            self.u_LTB=self.total_u
        if self.DELETION:
            self.total_d=randint(1,self.total_k-1)
            self.d_LTD=self.total_d
        if self.DELETION_ERROR and not(self.ONLY_KNOWN_REF):
            self.total_de=randint(1,self.total_u)

            self.de_LTD=self.total_de
    def unlock(self):
        self.add_to_trace('debloquer','0')

    def scan_known_ref(self):
        self.add_to_trace('scanner','0')
        self.k_currently_in_basket+=1
        self.k_LTB-=1
    def scan_unknown_ref(self):
        self.add_to_trace('scanner','-2')
        self.u_currently_in_basket+=1
        self.u_LTB-=1
    def delete_ref(self):
        self.add_to_trace('supprimer','0')
        self.k_currently_in_basket-=1
        self.d_LTD-=1

    def delete_ref_fail(self):
        self.add_to_trace('supprimer','-2')
        self.de_LTD-=1
    def transmission_0(self):

        self.add_to_trace('transmission', 0)
        self.add_to_trace('abandon', '?')
        if self.u_currently_in_basket==0:
            return
        else:
            self.add_to_trace('ouvrirSession','0')
            for i in range(self.total_u):
                self.add_to_trace('ajouter','0')

            for j in range(self.total_de):
                self.add_to_trace('supprimer','0')
            self.add_to_trace('fermerSession','0')
            return

    def proofreading(self):
        stop_i=-1
        self.add_to_trace('transmission','1')
        if self.NOT_IN_BASKET_WHILE_RESCANNING:
            stop_i=randint(0,self.k_currently_in_basket)
        for i in range(self.k_currently_in_basket):
            if i == stop_i:
                self.add_to_trace('scanner','-3')
                self.add_to_trace('abandon', '?')

                return False
            self.add_to_trace('scanner','0')
        return True



    def pay(self):

        if self.CHANGE:
            self.add_to_trace('payer','1')
        else:
            self.add_to_trace('payer','0')

    def play(self):

        self.unlock()
        step=0


        total = sum([self.k_LTB, self.u_LTB, self.de_LTD, self.d_LTD])

        while total>0 :

            assert self.u_LTB>=0
            assert self.k_LTB>=0
            assert self.d_LTD>=0
            assert self.de_LTD>=0

            w_k_LTB= self.k_LTB
            w_u_LTB=self.u_LTB
            w_de_LTD=self.de_LTD if self.u_currently_in_basket>=self.de_LTD else 0
            w_d_LTD= self.d_LTD if self.k_currently_in_basket>=self.d_LTD else 0

            w= [w_k_LTB,w_u_LTB,w_de_LTD,w_d_LTD]

            # assert sum(w) !=0

            f = choices([self.scan_known_ref, self.scan_unknown_ref, self.delete_ref_fail,self.delete_ref],weights=w,k=1)
            f[0]()

            assert total - sum([self.k_LTB, self.u_LTB, self.de_LTD, self.d_LTD]) ==1

            total = sum([self.k_LTB, self.u_LTB,self.de_LTD, self.d_LTD])
            step+=1
        if self.PROOFREADING:
            proofreading_ok=self.proofreading()
            if not(proofreading_ok):
                return

        self.transmission_0()
        self.pay()

    def add_to_trace(self,method_name,return_code):
        self.trace.append(method_name+self.sp+str(return_code))

    # def print_prob(self):
    #     print("Known left to buy",self.k_LTB)
    #     print("Unknown left to buy",self.u_LTB)
    #     print("deletion to do",self.d_LTD)
    #     print("deletion fail to do",self.de_LTD)
if __name__=='__main__':
    stm=ScannetteStateMachine()
    for i in range(100):
        stm.play()
        print(i,stm.trace)