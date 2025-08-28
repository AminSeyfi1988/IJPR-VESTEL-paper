import pandas as pd
from Model_Larg import MyCost_Model
import gc
import random


period = (24,48,72)   
instances = (0.25, 0.35, 0.45)
seed = (14,3,15,13,7,1,16) 
workers = (20,16)
Invent1 = (4,7,8)



MyFinalObjectives = []

for t in range(1, len(period)):
    for ins in range(2, len(instances)):
        for d in range(len(seed)-6): 
            for w in range(len(workers)-1):
                rrr = period[t]
                ptt = instances[ins]
                dd = seed[d]
                l1 = workers[w]
                In1 = Invent1[t]
                # In2 = Invent2[t]
                Objectives = MyCost_Model(rrr, ptt, dd, l1 ,ins, In1)
                MyFinalObjectives.append(Objectives)
                gc.collect()
            
dfres = pd.DataFrame(MyFinalObjectives)
with pd.ExcelWriter('C:/Amin/University/Ph.d/TUBITAK 2244/Project/Final Results Model/Results_Model1.xlsx') as writer:
      dfres.to_excel(writer, sheet_name='General information', index=False)

            