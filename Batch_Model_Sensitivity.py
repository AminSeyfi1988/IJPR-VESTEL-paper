import pandas as pd
from Model_Sensitivity import MyCost_Sensitivity
import gc
import random


period = (4,6,24,48,72)   
instances = (0.25, 0.35, 0.45)
seed = (14,3,15,13,7,1,16) 
workers = (16,20)
Invent1 = (2,3,4,6,8)



MyFinalObjectives = []

for t in range(3, len(period)):
    for ins in range(len(instances)):
        for d in range(2, len(seed)): 
            for w in range(len(workers)-1):
                rrr = period[t]
                ptt = instances[ins]
                dd = seed[d]
                l1 = workers[w]
                In1 = Invent1[t]
                # In2 = Invent2[t]
                Objectives = MyCost_Sensitivity(rrr, ptt, dd, l1 ,ins, In1)
                MyFinalObjectives.append(Objectives)
                gc.collect()
            
dfres = pd.DataFrame(MyFinalObjectives)
with pd.ExcelWriter('C:/Amin/University/Ph.d/TUBITAK 2244/Project/Final Results Model/Results_Model1.xlsx') as writer:
      dfres.to_excel(writer, sheet_name='General information', index=False)







            
