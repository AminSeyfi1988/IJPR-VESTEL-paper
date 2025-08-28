from gurobipy import *
import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as np
import random
import time
import openpyxl
import re
import datetime
from itertools import permutations
import copy
import sys
#%%


def MyCost_Algorithm(ucc, rrr, ptt, dd, l1 ,ins, In1):

    n = 55   # Number of all parts
    f = 33   # Number of finished parts
    j = 16   # Number of machines
    r = rrr  # Number of days
    s = 7   # Number of shift types
    ll = l1   # Number of workers group
    i = n
    k = n
    rr=rrr
    #%%
    
    I = [i for i in range(1,i+1)]    # Set of all parts
    I0 = [i for i in range(0,i+1)]   # Set of all parts + 0  
    K = [k for k in range(1,k+1)]    # Set of all parts 
    W = [w for w in (26,28,30,32,34,36,38,40,42,44,45,46,47,48,49,50,51,52,53,54,55)]
    F = [f for f in (1,2,3,4,5,6,7,8,9,10,22,24,26,28,30,32,34,36,38,40,42,44,45,46,47,48,49,50,51,52,53,54,55)] 
    FF = [f for f in (1,2,3,4,5,6,7,8,9,10,22,24)]   # Set of parts need precursor parts 1
    FFF = [f for f in (26,28,30,32,34,36,38,40,42,44)]   # Set of parts need precursor parts 2 
    J = [j for j in range(1,j+1)]    # Set of machines 
    JJ = [j for j in (1,2,3,4,5,6,7,8,9,10,11,13,14,15,16)]    # Set of machines 
    R = [r for r in range(1,r+1)]    # Set of days
    S = [s for s in range(1,s+1)]    # Set of shift types
    N = [s for s in (3,4,5,6,7)]    # Set of shift types include night working hours
    L = [l for l in range(1,ll+1)]    # Set of workers group
    #%%
    
    #Inventory cost for one unit of part i
    ic = {}
    for i in range(1,i+1):
        ic[i] = 1
        
    
    #Backlogging cost for one unit of part i
    bc = {}
    for i in range(1,i+1):
        bc[i] = 1000
    
    
    #Production cost for one unit of part i on machine j in day r
    random.seed(0)
    p1 = 1000
    pc = {}
    for i in range(1,i+1):
        for j in range(1,j+1):
            for r in R:
                pc[i,j,r] = random.randint(150,200)
                pc[12,3,r] = p1
                pc[14,2,r] = p1
                pc[17,4,r] = p1
                pc[18,1,r] = p1
                pc[20,4,r] = p1
                pc[22,8,r] = p1
                pc[24,8,r] = p1 
                pc[25,9,r] = p1
                pc[26,12,r] = p1
                pc[27,9,r] = p1
                pc[28,12,r] = p1
                pc[29,9,r] = p1
                pc[30,12,r] = p1
                pc[31,9,r] = p1
                pc[32,12,r] = p1
                pc[33,9,r] = p1
                pc[34,12,r] = p1
                pc[35,9,r] = p1
                pc[36,12,r] = p1
                pc[37,9,r] = p1
                pc[38,12,r] = p1
                pc[39,9,r] = p1
                pc[40,12,r] = p1
                pc[41,9,r] = p1
                pc[42,12,r] = p1
                pc[43,9,r] = p1
                pc[44,12,r] = p1
                pc[45,13,r] = p1
                pc[47,15,r] = p1
                pc[50,14,r] = p1
                pc[52,16,r] = p1
                pc[53,15,r] = p1
            
                            
    #Processing time to produce one unit of part i on machine j
    pt = {}
    for i in range(1,i+1):
        for j in range(1,j+1):
            pt[i,j] = ptt  
    
    
    #Setup cost for part i on machine j
    
    # s1 = 7000
    # sc = {}
    # for i in range(1,i+1):
    #     for j in range(1,j+1):
    #         sc[i,j] = random.randint(5000,6000)
    #         sc[12,3] = s1
    #         sc[14,2] = s1
    #         sc[17,4] = s1
    #         sc[18,1] = s1
    #         sc[20,4] = s1
    #         sc[22,8] = s1
    #         sc[24,8] = s1 
    #         sc[25,9] = s1
    #         sc[26,12] = s1
    #         sc[27,9] = s1
    #         sc[28,12] = s1
    #         sc[29,9] = s1
    #         sc[30,12] = s1
    #         sc[31,9] = s1
    #         sc[32,12] = s1
    #         sc[33,9] = s1
    #         sc[34,12] = s1
    #         sc[35,9] = s1
    #         sc[36,12] = s1
    #         sc[37,9] = s1
    #         sc[38,12] = s1
    #         sc[39,9] = s1
    #         sc[40,12] = s1
    #         sc[41,9] = s1
    #         sc[42,12] = s1
    #         sc[43,9] = s1
    #         sc[44,12] = s1
    #         sc[45,13] = s1
    #         sc[47,15] = s1
    #         sc[50,14] = s1
    #         sc[52,16] = s1
    #         sc[53,15] = s1
                      
    
    #Setup time for part i on machine j
    st = {}
    for i in range(1,i+1):
        for j in range(1,j+1):
            st[i,j] = 15 
    
    
    #Setup cost of a changeover from part i to part k on machine j
    # csc = {}
    # for i in range(1,i+1):
    #     for k in range(1,k+1):
    #         for j in range(1,j+1):
    #             csc[i,k,j] = random.randint(3000,4000)         
    
    
    #Setup time of a changeover from part i to part k on machine j
    # cst = {}
    # for i in range(1,i+1):
    #     for k in range(1,k+1):
    #         for j in range(1,j+1):
    #             cst[i,k,j] = 10
    
        
           
    #Compatibility matrix
    cm = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0], 
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0], 
          [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1], 
          [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1], 
          [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],  
          [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]]
             
         
    
    ga = [[0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,1,1,1,1,1,1,1],
          [0,0,0,0,0,0,0,0],
          [0,1,1,1,1,1,1,1],
          [0,1,1,1,1,1,1,1],
          [0,1,1,1,1,1,1,1]]
    
    
    period = rrr  
    seedd = dd  
    
    def generate_demand(period, seedd):
        np.random.seed(seedd)  
        d = {}
    
        for r in range(1, period + 1):
            if r <= 2:
                coef = 0.25
            elif r <= 3:
                coef = 0.4
            elif r <= 4:
                coef = 0.7
            elif r <= 6:
                coef = 0.3
            elif r <= 8:
                coef = 0.6 
            elif r <= 10:
                coef = 0.45
            elif r <= 12:
                coef = 0.7
            elif r <= 15:
                coef = 0.4
            elif r <= 19:
                coef = 0.65
            elif r <= 24:
                coef = 0.35
            elif r <= 28:
                coef = 0.5
            elif r <= 32:
                coef = 0.75
            elif r <= 36:
                coef = 0.3
            elif r <= 45:
                coef = 0.4
            elif r <= 50:
                coef = 0.35
            elif r <= 55:
                coef = 0.55
            elif r <= 60:
                coef = 0.3
            elif r <= 65:
                coef = 0.4
            elif r <= 69:
                coef = 0.5
            elif r <= 72:
                coef = 0.25
            
            d[1, r] = np.random.uniform(630 * coef, 900 * coef)
            d[2, r] = np.random.uniform(760 * coef, 1000 * coef)
            d[3, r] = np.random.uniform(1143 * coef, 1400 * coef)
            d[4, r] = np.random.uniform(878 * coef, 1000 * coef)
            d[5, r] = np.random.uniform(1013 * coef, 1300 * coef)
            d[6, r] = np.random.uniform(428 * coef, 700 * coef)
            d[7, r] = np.random.uniform(291 * coef, 500 * coef)
            d[8, r] = np.random.uniform(191 * coef, 400 * coef)
            d[9, r] = np.random.uniform(453 * coef, 700 * coef)
            d[10, r] = np.random.uniform(506 * coef, 700 * coef)
            
            total_demandd = d[1, r] + d[2, r] + d[3, r] + d[4, r] + d[5, r] + d[6, r] + d[7, r] + d[8, r] + d[9, r] + d[10, r]
            
            d[22, r] = total_demandd
            d[24, r] = total_demandd
            d[26, r] = d[1, r]
            d[28, r] = d[2, r]
            d[30, r] = d[3, r]
            d[32, r] = d[4, r]
            d[34, r] = d[5, r]
            d[36, r] = d[6, r]
            d[38, r] = d[7, r]
            d[40, r] = d[8, r]
            d[42, r] = d[9, r]
            d[44, r] = d[10, r]
            d[45, r] = d[1, r]
            d[46, r] = d[2, r]
            d[47, r] = d[3, r]
            d[48, r] = d[4, r]
            d[49, r] = d[5, r]
            d[50, r] = d[6, r]
            d[51, r] = d[7, r]
            d[52, r] = d[8, r]
            d[53, r] = d[9, r]
            d[54, r] = d[10, r]
            d[55, r] = total_demandd
            
                       
        total_d = sum(d.values())
        return d, total_d
     
    d, total_demand = generate_demand(period, seedd)
    
    
    
    cm = {(i,j): (cm[i][j]) for i in I0 for j in J}
    ga = {(ss,s): (ga[ss][s]) for ss in S for s in S}
    
    
    pi = {1:[0,11,2,2], 2:[0,12,1,3], 3:[0,13,1,1], 4:[0,14,4,4], 5:[0,15,1,1], 6:[0,16,4,4], 7:[0,17,2,4], 8:[0,18,1,3], 9:[0,19,1,1], 10:[0,20,2,4], 
          11:[0,11,3,3], 12:[0,12,2,2], 13:[0,13,2,2], 14:[0,14,1,1], 15:[0,15,1,1], 16:[0,16,1,1], 17:[0,17,1,1], 18:[0,18,2,2], 19:[0,19,2,2], 20:[0,20,1,1], 
          21:[0,21,7,7], 22:[0,21,6,6], 23:[0,23,7,7], 24:[0,23,6,6], 25:[0,25,8,8], 26:[25,26,9,9], 27:[0,27,8,8], 28:[27,28,9,9], 29:[0,29,8,8], 30:[29,30,9,9],
          31:[0,31,8,8], 32:[31,32,9,9], 33:[0,33,8,8], 34:[33,34,9,9], 35:[0,35,8,8], 36:[35,36,9,9], 37:[0,37,8,8], 38:[37,38,9,9], 39:[0,39,8,8], 40:[39,40,9,9],
          41:[0,41,8,8], 42:[41,42,9,9], 43:[0,43,8,8], 44:[43,44,9,9], 45:[0,45,14,14], 46:[0,46,14,14], 47:[0,47,13,13], 48:[0,48,14,14], 49:[0,49,14,14],
          50:[0,50,15,15], 51:[0,51,15,15], 52:[0,52,13,13], 53:[0,53,14,14], 54:[0,54,14,14], 55:[0,55,5,5]}     
          
          
    
    pii = {1:[0,22,24,7,8], 2:[0,22,24,7,8], 3:[0,22,24,7,8], 4:[0,22,24,7,8], 5:[0,22,24,7,8], 6:[0,22,24,7,8], 7:[0,22,24,7,8], 8:[0,22,24,7,8], 9:[0,22,24,7,8], 10:[0,22,24,7,8]}
    
    N = {3:[2,2], 4:[2,2], 5:[2,2], 6:[2,2], 7:[2,3]}
    
    #Big number
    M = total_demand*2
    
    
    #Initial inventory of each part
    
    
    
    In0 = {}
    for i in F:
        In0[i] = sum(d[i, r] for r in range(1, In1+1))
        
    for i in range(1,11):
        In0[i] = sum(d[i, r] for r in range(1, In1+1))*In1
    
    In0[21] = sum(d[i, r] for i in range(1, 11) for r in range(1, In1+1))*In1
    In0[22] = In0[21]
    In0[23] = In0[21]
    In0[24] = In0[21]
    In0[55] = In0[21]
    
    for i in (11,12,13,14,15,16,17,18,19,20):
        In0[i] = sum(d[i-10, r] for r in range(1, In1+1))
          
    for i in (25,27,29,31,33,35,37,39,41,43):
        In0[i] = sum(d[i+1, r] for r in range(1, In1+1))
    
        
        
    summ = 0
    for i in F:
        summ += In0[i]
    
        
    #%%
    
            

    
    mdl = Model('Model (Project)')
    
    # Variables
    
    xb = mdl.addVars(I,J,R, lb=0.0, vtype=GRB.CONTINUOUS)
    xd = mdl.addVars(I,J,R, lb=0.0, vtype=GRB.CONTINUOUS)
    x = mdl.addVars(I,J,R, lb=0.0, vtype=GRB.CONTINUOUS)
    In = mdl.addVars(I,R, lb=0.0, vtype=GRB.CONTINUOUS)
    b = mdl.addVars(I,R, lb=0.0, vtype=GRB.CONTINUOUS)
    # stt = mdl.addVars(I,J,R, lb=0.0, vtype=GRB.CONTINUOUS)
    # ctt = mdl.addVars(I,J,R, lb=0.0, vtype=GRB.CONTINUOUS)
    z = mdl.addVars(I0,I0,J,R, vtype=GRB.BINARY)
    # v = mdl.addVars(I,R, vtype=GRB.BINARY)
    a = mdl.addVars(J,R, lb=0.0, vtype=GRB.CONTINUOUS)
    
    # q = mdl.addVars(I0,I,J,R, vtype=GRB.BINARY)
    tpc = mdl.addVar(vtype=GRB.CONTINUOUS)
    tic = mdl.addVar(vtype=GRB.CONTINUOUS)
    tbc = mdl.addVar(vtype=GRB.CONTINUOUS)
    # tsc = mdl.addVar(vtype=GRB.CONTINUOUS)
    # tchc = mdl.addVar(vtype=GRB.CONTINUOUS)
    tuc = mdl.addVar(vtype=GRB.CONTINUOUS) 
    tshc = mdl.addVar(vtype=GRB.CONTINUOUS)
    
    # u = mdl.addVars(J,R, lb=0.0, vtype=GRB.CONTINUOUS)
    
    
    #%%
    
    mdl.modelSense = GRB.MINIMIZE
    #%%
    
    #Objective Function
    
    mdl.setObjective(quicksum(pc[i,j,r]*x[i,j,r] for i in I for j in J for r in R)              
                    +quicksum(ic[i]*(In[i,r]) for i in I for r in R)
                    +quicksum(bc[i]*b[i,r] for i in I for r in R)
                    +quicksum(ucc*a[j,r] for j in J for r in R))
                    
                    
                    
    #%%
    
    #Constraints
    
    mdl.addConstr(tpc == quicksum(pc[i,j,r]*x[i,j,r] for i in I for j in J for r in R));
    mdl.addConstr(tic == quicksum(ic[i]*(In[i,r]) for i in I for r in R));
    mdl.addConstr(tbc == quicksum(bc[i]*b[i,r] for i in I for r in R));
    mdl.addConstr(tshc == quicksum(ucc*a[j,r] for j in J for r in R));
    
    #%%
    
    mdl.addConstrs(d[i,1] == quicksum(x[i,j,1] for j in J)-In[i,1]+b[i,1]+In0[i] for i in F);
    
    mdl.addConstrs(d[i,r] == quicksum(x[i,j,r] for j in J)+In[i,r-1]-In[i,r]-b[i,r-1]+b[i,r] for i in F for r in R if r>=2); 
    
    mdl.addConstrs(quicksum(x[i,j,1] for j in JJ) <= quicksum(x[pi[i][l],j,1] for j in JJ)+In0[pi[i][l]]-In[pi[i][l],1] for i in FF for l in range(1,2));
    
    mdl.addConstrs(quicksum(x[i,j,r] for j in JJ) <= quicksum(x[pi[i][l],j,r] for j in JJ)+In[pi[i][l],r-1]-In[pi[i][l],r] for i in FF for l in range(1,2) for r in R if r>=2);  
    
    mdl.addConstrs(x[i,12,1] <= x[pi[i][l],9,1]+In0[pi[i][l]]-In[pi[i][l],1] for i in FFF for l in range(0,1));
    
    mdl.addConstrs(x[i,12,r] <= x[pi[i][l],9,r]+In[pi[i][l],r-1]-In[pi[i][l],r] for i in FFF for l in range(0,1) for r in R if r>=2);
    
    mdl.addConstrs(quicksum(x[i,j,r] for j in J for i in (1,2,3,4,5,6,7,8,9,10)) <= quicksum(x[22,j,r] for j in J) for r in R); 
        
    mdl.addConstrs(quicksum(x[i,j,r] for j in J for i in (1,2,3,4,5,6,7,8,9,10)) <= quicksum(x[24,j,r] for j in J) for r in R);
    
    mdl.addConstrs(x[i,j,r] <= M*z[0,i,j,r] for i in I for j in J for r in R);
        
    
    
    
    
    mdl.addConstrs(quicksum(pt[i,j]*x[i,j,r] for i in I)+1*quicksum(st[i,j]*z[0,i,j,r] for i in I) <= 1440*a[j,r] for j in J for r in R);
    
    mdl.addConstrs(pt[i,j]*x[i,j,r]+st[i,j]*z[0,i,j,r]+pt[pi[i][l],pi[i][ll]]*x[pi[i][l],pi[i][ll],r]+st[pi[i][l],pi[i][ll]]*z[0,pi[i][l],pi[i][ll],r] <= 1440 for i in (22,24) for j in (7,8) for l in range(1,2) for ll in range(2,4) for r in R);
    
    mdl.addConstrs(pt[i,j]*x[i,j,r]+st[i,j]*z[0,i,j,r]+pt[pi[i][l],pi[i][ll]]*x[pi[i][l],pi[i][ll],r]+st[pi[i][l],pi[i][ll]]*z[0,pi[i][l],pi[i][ll],r] <= 1440 for i in (1,2,3,4,5,6,7,8,9,10) for j in JJ for l in range(1,2) for ll in range(2,4) for r in R);
    
    mdl.addConstrs(pt[i,j]*x[i,j,r]+st[i,j]*z[0,i,j,r]+quicksum(pt[pii[1][l],pii[1][ll]]*x[pii[1][l],pii[1][ll],r]+st[pii[1][l],pii[1][ll]]*z[0,pii[1][l],pii[1][ll],r] for l in range(1,3)) <= 1440 for i in (1,2,3,4,5,6,7,8,9,10) for j in JJ for ll in range(3,5) for r in R);
    
    mdl.addConstrs(pt[i,12]*x[i,12,r]+pt[pi[i][l],9]*x[pi[i][l],9,r]+st[i,12]*z[0,i,12,r]+st[pi[i][l],9]*z[0,pi[i][l],9,r] <= 1440 for i in FFF for l in range(0,1) for ll in range(2,3) for r in R);







    # mdl.addConstrs(pt[22,7]*x[22,7,r]+st[22,7]*z[0,22,7,r]+pt[21,6]*x[21,6,r]+st[21,6]*z[0,21,6,r] <= 1440 for r in R);
    
    # mdl.addConstrs(pt[22,8]*x[22,8,r]+st[22,8]*z[0,22,8,r]+pt[21,6]*x[21,6,r]+st[21,6]*z[0,21,6,r] <= 1440 for r in R);
      
    # mdl.addConstrs(pt[24,7]*x[24,7,r]+st[24,7]*z[0,24,7,r]+pt[22,7]*x[22,7,r]+st[22,7]*z[0,22,7,r]+pt[21,6]*x[21,6,r]+st[21,6]*z[0,21,6,r]+pt[23,6]*x[23,6,r]+st[23,6]*z[0,23,6,r] <= 1440 for r in R);
    
    # mdl.addConstrs(pt[24,8]*x[24,8,r]+st[24,8]*z[0,24,8,r]+pt[22,8]*x[22,8,r]+st[22,8]*z[0,22,8,r]+pt[21,6]*x[21,6,r]+st[21,6]*z[0,21,6,r]+pt[23,6]*x[23,6,r]+st[23,6]*z[0,23,6,r] <= 1440 for r in R);











    mdl.addConstrs(z[0,i,j,r] <= cm[i,j] for i in I for j in J for r in R);
        
    mdl.addConstrs(b[i,rr] == 0 for i in F);
      
    mdl.addConstrs(a[j,r] <= 1 for j in J for r in R);
    
    
    
    
    mdl.addConstrs(z[0,i,j,r]+z[0,pi[i][l],pi[i][ll],r] <= 1 for i in (22,24) for j in (7,8) for l in range(1,2) for ll in range(2,4) for r in R);

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    # mdl.addConstrs(d[i,1] == quicksum(x[i,j,1] for j in JJ)-In[i,1]+b[i,1]+In0[i] for i in W);

    # mdl.addConstrs(d[i,r] == quicksum(x[i,j,r] for j in JJ)+In[i,r-1]-In[i,r]-b[i,r-1]+b[i,r] for i in W for r in R if r>=2); 
     
    # mdl.addConstrs(d[i,1] == quicksum(x[i,j,1] for j in JJ)+In0[i]-In[i,1]+b[i,1] for i in FF);
    
    # mdl.addConstrs(d[i,r] == quicksum(x[i,j,r] for j in JJ)+In[i,r-1]-In[i,r]-b[i,r-1]+b[i,r] for i in FF for r in R if r>=2); 
     
    # mdl.addConstrs(quicksum(x[i,j,1] for j in JJ) <= In0[pi[i][l]]-In[pi[i][l],1]for i in FF for l in range(1,2));
    
    # mdl.addConstrs(quicksum(x[i,j,r] for j in JJ) <= quicksum(x[pi[i][l],j,r-1] for j in JJ)-In[pi[i][l],r]+In[pi[i][l],r-1] for i in FF for l in range(1,2) for r in R if r>=2);  
    
    # mdl.addConstrs(quicksum(x[i,j,1] for j in JJ) <= In0[pii[i][l]]-In[pii[i][l],1] for i in (1,2,3,4,5,6,7,8,9,10) for l in range(1,3));

    # mdl.addConstrs(quicksum(x[i,j,r] for j in JJ) <= quicksum(x[pii[i][l],j,r-1] for j in JJ)-In[pii[i][l],r]+In[pii[i][l],r-1] for i in (1,2,3,4,5,6,7,8,9,10) for l in range(1,3) for r in R if r>=2);  

    # mdl.addConstrs(x[i,12,1] <= In0[pi[i][l]]-In[pi[i][l],1]for i in FFF for l in range(0,1));
    
    # mdl.addConstrs(x[i,12,r] <= x[pi[i][l],9,r-1]-In[pi[i][l],r]+In[pi[i][l],r-1] for i in FFF for l in range(0,1) for r in R if r>=2);

    
    
     
    # mdl.addConstrs(1440*a[j,r]-quicksum(pt[i,j]*x[i,j,r]+st[i,j]*z[0,i,j,r] for i in I) <= u[j,r] for j in J for r in R);
    
    #%%
    
    mdl.Params.MIPGap = 0.005
    mdl.Params.TimeLimit = 3600 
    start = time.time()
    mdl.optimize()
    
    if mdl.status == GRB.INFEASIBLE:
        # model.computeIIS()
        # model.write("infeasible_model.ilp")
        return
    
    # elif mdl.status == GRB.TIME_LIMIT:
    #     return

    else:
        end = time.time()
        gurobi = end - start
        num_vars = len(mdl.getVars())
        num_binary_vars = len([var for var in mdl.getVars() if var.vType == GRB.BINARY])
        num_cont_vars = len([var for var in mdl.getVars() if var.vType == GRB.CONTINUOUS])
        num_constraints = mdl.NumConstrs
        
        #%%
        
        # print('Solution time:', end-start)
        # print("Objective Value =", mdl.ObjVal)
        # #print('Gap =', mdl.MIPGap)
        # print("Total number of decision variables:", num_vars)
        # print("Number of binary decision variables:", num_binary_vars)
        # print("Number of continuous decision variables:", num_cont_vars)
        # print('Number of constraints', num_constraints)
        # #%%
        
        # list1 = []
        # part = []
        # machine = []
        # day = []
        # value_x = []
        # for i in I:
        #     for j in J:
        #         for r in R:
        #             if x[i,j,r].X>0.1:
        #                 print("x("+str(i)+','+str(j)+','+str(r)+")=", round(x[i,j,r].x))
        #                 part.append(i)
        #                 machine.append(j)
        #                 day.append(r)
        #                 value_x.append(round(x[i,j,r].x))
        #                 if i in F:
        #                     list1.append(round(x[i,j,r].x))
        # print('-------------------------------------------------')
        # print('Total Production Amount:', np.sum(list1))
        # print('Total Production Cost', tpc.x)
        
        # dfx = pd.DataFrame({'Part': part, 'Machine': machine, 'Day': day, 'Value': value_x})
        # dfx['Part'].replace([i for i in range(1,i+1)], ['Tam1', 'Tam2', 'Tam3', 'Tam4', 'Tam5', 'Tam6', 'Tam7', 'Tam8', 'Tam9', 'Tam10',
        #                                                 'ÇT1', 'ÇT2','ÇT3', 'ÇT4', 'ÇT5', 'ÇT6', 'ÇT7', 'ÇT8', 'ÇT9', 'ÇT10', 'ÖKP', 'ÖK',
        #                                                 'AKP', 'AK', 'ÖPB1', 'ÖP1', 'ÖPB2', 'ÖP2', 'ÖPB3', 'ÖP3', 'ÖPB4','ÖP4',
        #                                                 'ÖPB5','ÖP5', 'ÖPB6','ÖP6', 'ÖPB7','ÖP7', 'ÖPB8','ÖP8', 'ÖPB9','ÖP9', 'ÖPB10','ÖP10','GÖ1', 'GÖ2',
        #                                                 'GÖ3', 'GÖ4', 'GÖ5', 'GÖ6', 'GÖ7', 'GÖ8', 'GÖ9', 'GÖ10', 'Ment'], inplace=True)
        # dfx['Machine'].replace([j for j in range(1,j+1)], ['Tam1', 'Tam2', 'Tam3', 'Tam4', 'TamAssm', 'PK', 'Ales', '800_ton', 'BK',
        #                                                                   'ÖP1', 'ÖP2', '1250_trans', 'GÖ1', 'GÖ2', 'GÖ3', 'GÖ4'], inplace=True)
        # dfx['Day'].replace([1,2,3,4,5,6], ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'], inplace=True)
        # #%%
        
        # list12 = []
        # for i in I:
        #     for j in J:
        #         for r in R:
        #             if z[0,i,j,r].X>=0.1:
        #                 if x[i,j,r].X>=0.1:
        #                     print("xb("+str(i)+','+str(j)+','+str(r)+")=", round(x[i,j,r].x))
        #                     if i in F:
        #                         list12.append(x[i,j,r].x)
        # print('-------------------------------------------------')
        # print('Total Production Amount:', np.sum(list12))
        # #%%
        
        # list13 = []
        # for k in I:
        #     for i in I:
        #         for j in J:
        #             for r in R:
        #                 if z[i,k,j,r].X>=0.1:
        #                     if x[k,j,r].X>=0.1:
        #                         print("xd("+str(k)+','+str(j)+','+str(r)+")=", round(x[k,j,r].x))
        #                         if k in F:
        #                                 list13.append(x[k,j,r].x)
        # print('-------------------------------------------------')
        # print('Total Production Amount:', np.sum(list13))
        # #%%
        
        # list2 = []
        # part = []
        # day = []
        # value_In = []
        # for i in I:
        #     for r in R:
        #         if In[i,r].X>0.01:
        #             print("In("+str(i)+','+str(r)+")=", round(In[i,r].X))
        #             part.append(i)
        #             day.append(r)
        #             value_In.append(round(In[i,r].X))
        #             #if r==rr:
        #             list2.append(round(In[i,r].X))
                        
        # print('-------------------------------------------------')
        # print('Total Inventory Amount:', np.sum(list2))
        # print('Total Inventory Cost:', tic.x)
        # dfIn = pd.DataFrame({'Part': part, 'Day': day, 'Value': value_In})
        # dfIn['Part'].replace([i for i in range(1,i+1)], ['Tam1', 'Tam2', 'Tam3', 'Tam4', 'Tam5', 'Tam6', 'Tam7', 'Tam8', 'Tam9', 'Tam10',
        #                                                 'ÇT1', 'ÇT2','ÇT3', 'ÇT4', 'ÇT5', 'ÇT6', 'ÇT7', 'ÇT8', 'ÇT9', 'ÇT10', 'ÖKP', 'ÖK',
        #                                                 'AKP', 'AK', 'ÖPB1', 'ÖP1', 'ÖPB2', 'ÖP2', 'ÖPB3', 'ÖP3', 'ÖPB4','ÖP4',
        #                                                 'ÖPB5','ÖP5', 'ÖPB6','ÖP6', 'ÖPB7','ÖP7', 'ÖPB8','ÖP8', 'ÖPB9','ÖP9', 'ÖPB10','ÖP10','GÖ1', 'GÖ2',
        #                                                 'GÖ3', 'GÖ4', 'GÖ5', 'GÖ6', 'GÖ7', 'GÖ8', 'GÖ9', 'GÖ10', 'Ment'], inplace=True)
        # dfIn['Day'].replace([1,2,3,4,5,6], ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'], inplace=True)
        # #%%
        
        # list3 = []
        # part = []
        # day = []
        # value_b = []
        # for i in I:
        #     for r in R:
        #         if b[i,r].X>0.01:
        #             print("b("+str(i)+','+str(r)+")=", round(b[i,r].X)) 
        #             part.append(i)
        #             day.append(r)
        #             value_b.append(round(b[i,r].X))
        #             #if r==rr:
        #             list3.append(round(b[i,r].X))
        # print('-------------------------------------------------')
        # print('Total Backlogging Amount:', np.sum(list3))
        # print('Total Backlogging Cost:', tbc.x)
        # dfb = pd.DataFrame({'Part': part, 'Day': day, 'Value': value_b})
        # dfb['Part'].replace([i for i in range(1,i+1)], ['Tam1', 'Tam2', 'Tam3', 'Tam4', 'Tam5', 'Tam6', 'Tam7', 'Tam8', 'Tam9', 'Tam10',
        #                                                 'ÇT1', 'ÇT2','ÇT3', 'ÇT4', 'ÇT5', 'ÇT6', 'ÇT7', 'ÇT8', 'ÇT9', 'ÇT10', 'ÖKP', 'ÖK',
        #                                                 'AKP', 'AK', 'ÖPB1', 'ÖP1', 'ÖPB2', 'ÖP2', 'ÖPB3', 'ÖP3', 'ÖPB4','ÖP4',
        #                                                 'ÖPB5','ÖP5', 'ÖPB6','ÖP6', 'ÖPB7','ÖP7', 'ÖPB8','ÖP8', 'ÖPB9','ÖP9', 'ÖPB10','ÖP10','GÖ1', 'GÖ2',
        #                                                 'GÖ3', 'GÖ4', 'GÖ5', 'GÖ6', 'GÖ7', 'GÖ8', 'GÖ9', 'GÖ10', 'Ment'], inplace=True)
        # dfb['Day'].replace([1,2,3,4,5,6], ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'], inplace=True)
        # #%%
        
        # for j in J:
        #     for r in R:
        #         if a[j,r].x > 0.01:
        #             print("a("+str(j)+','+str(r)+")=", a[j,r].X)
                
        #%%
        
        start_time = time.time()
        
        
        setup = np.zeros((len(R),len(J),len(I))).tolist()
        
        
        for i in I:
            for j in J:
                for r in R:
                    if x[i,j,r].x > 0.1:
                        setup[r-1][j-1][i-1] = i
                        
        ##########################################################################################################
        
        
        for row in setup:
            for submatrix in row:
                if all(element == 0 for element in submatrix):
                    submatrix.clear()
                    submatrix.append(-1)
                    
                    
        list1 = [[[elem for elem in sublist if elem != 0] for sublist in row] for row in setup]
        
        ###########################################################################################
        
        list2 = []
        for i in range(len(list1)):
            sublist = []
            for k in range(len(list1[i])):
                sublist1 = []
                for j in range(len(list1[i][k])):
                    list1[i][k][0], list1[i][k][j] = list1[i][k][j], list1[i][k][0]
                    sublist1.append(list(list1[i][k]))
                    list1[i][k][0], list1[i][k][j] = list1[i][k][j], list1[i][k][0]
                sublist.append(sublist1) 
            list2.append(sublist)  
        
        new_list = []
        
        for i in range(len(list2)):
            sublist2 = []
            for k in range(len(list2[i])):
                sublist3 = []
                for j in range(len(list2[i][k])):
                    if len(list2[i][k][j]) > 1:
                        for jj in range(1, len(list2[i][k][j])):
                            list2[i][k][j][jj], list2[i][k][j][-1] = list2[i][k][j][-1], list2[i][k][j][jj]
                            sublist3.append(list(list2[i][k][j]))
                            list2[i][k][j][jj], list2[i][k][j][-1] = list2[i][k][j][-1], list2[i][k][j][jj]
                    else:
                        sublist3.append(list(list2[i][k][j]))
                sublist2.append(sublist3)
            new_list.append(sublist2)
           
        ###############################################################################################
        
        # new_list = []
        
        # for sublist in list1:
        #     permuted_sublist = []
        #     for inner_list in sublist:
        #         permuted_inner_list = [list(x) if isinstance(x, tuple) else [x] for x in permutations(inner_list)]
        #         permuted_sublist.append(permuted_inner_list)
        #     new_list.append(permuted_sublist)
            
            
        ################################################################################################
        
        # Forward Phase
        
        
        neww_list = [[[[0 for _ in sublist] for sublist in inner_list] for inner_list in sublist] for sublist in new_list]
        
        
        for i in range(len(new_list)-1):
            for k in range(len(new_list[i])):
                for j in range(len(new_list[i][k])):
                    for jj in range(len(new_list[i+1][k])):
                        if new_list[i][k][j][-1] == new_list[i+1][k][jj][0]:
                            neww_list[i][k][j] = new_list[i][k][j]
        
                            
        for k in range(len(new_list[-1])):
            for j in range(len(new_list[-1][k])):
                for jj in range(len(new_list[-2][k])):
                    if new_list[-1][k][j][0] == new_list[-2][k][jj][-1]:
                        neww_list[-1][k][j] = new_list[-1][k][j]
        
        ##############################################################################
        
        for i in range(len(neww_list)):
            for k in range(len(neww_list[i])):
                if all(all(element == 0 for element in submatrix_part) for submatrix_part in neww_list[i][k]):
                    neww_list[i][k] = new_list[i][k]
                               
        ##############################################################################
          
        # Backward Phase
        
        neww_list1 = [[[[0 for _ in sublist] for sublist in inner_list] for inner_list in sublist] for sublist in neww_list]
        
                
        for i in range(len(neww_list)-1, 0, -1):
            for k in range(len(neww_list[i])):
                for j in range(len(neww_list[i][k])):
                    for jj in range(len(neww_list[i-1][k])):
                        if neww_list[i][k][j][0] == neww_list[i-1][k][jj][-1]:
                            neww_list1[i][k][j] = neww_list[i][k][j]
                
        
        for k in range(len(neww_list[0])):
            for j in range(len(neww_list[0][k])):
                for jj in range(len(neww_list[1][k])):
                    if neww_list[0][k][j][-1] == neww_list[1][k][jj][0]:
                        neww_list1[0][k][j] = neww_list[0][k][j]
                         
        ##############################################################################
        
        for i in range(len(neww_list1)):
            for k in range(len(neww_list1[i])):
                if all(all(element == 0 for element in submatrix_part) for submatrix_part in neww_list1[i][k]):
                    neww_list1[i][k] = neww_list[i][k]
        
        ##############################################################################
        
        # Removing zero values
        
        neww_list2 = []
        
        for outer_list in neww_list1:
            new_outer_list = []
            for inner_list in outer_list:
                new_inner_list = [sub_list for sub_list in inner_list if any(x != 0 for x in sub_list)]
                if new_inner_list:  
                    new_outer_list.append(new_inner_list)
            if new_outer_list:  
                neww_list2.append(new_outer_list)
        
        ##############################################################################
        
        # If there is more than 1 combination, select 1
        
        
        neww_list3 = [[[[0 for _ in sublist] for sublist in inner_list] for inner_list in sublist] for sublist in neww_list2]
        
        
        n = 0
        for i in range(len(neww_list2)-1):
            for k in range(len(neww_list2[i])):
                jjj = n
                for j in range(jjj, len(neww_list2[i][k])):
                    for jj in range(len(neww_list2[i+1][k])):
                        if neww_list2[i][k][j][-1] == neww_list2[i+1][k][jj][0]:
                            neww_list3[i][k][j] = neww_list2[i][k][j]
                            neww_list3[i+1][k][jj] = neww_list2[i+1][k][jj]
                            n = jj
                            break
                    break 
        
        ##############################################################################
        
        for i in range(len(neww_list3)):
                for k in range(len(neww_list3[i])):
                    if all(all(element == 0 for element in submatrix_part) for submatrix_part in neww_list3[i][k]):
                        neww_list3[i][k][0] = new_list[i][k][0]
        
        ##############################################################################        
        
        # Removing zero values
                
        final_setup = []
        
        for outer_list in neww_list3:
            new_outer_list = []
            for inner_list in outer_list:
                new_inner_list = [sub_list for sub_list in inner_list if any(x != 0 for x in sub_list)]
                if new_inner_list:  
                    new_outer_list.append(new_inner_list)
            if new_outer_list:  
                final_setup.append(new_outer_list)
        ##############################################################################
          
        final_setup1 = copy.deepcopy(final_setup)
        
        for i in range(len(final_setup)-1):
            for k in range(len(final_setup[i])):
                if final_setup[i][k][0][-1] == final_setup[i+1][k][0][0]:
                    final_setup1[i+1][k][0][0] = 0
        
        
        
        for i in range(len(final_setup1)):
            for k in range(len(final_setup1[i])):
                for j in range(len(final_setup1[i][k])):
                    for jj in range(len(final_setup1[i][k][j])):
                        if final_setup1[i][k][j][jj] == -1:
                            final_setup1[i][k][j][jj] = 0
                        if final_setup1[i][k][j][jj] > 0:
                            final_setup1[i][k][j][jj] = 1
                        
        ###############################################################################                  
         
        setup_matrix = copy.deepcopy(final_setup1)
        
        
        T_setup_cost = 0
        T_changeover_cost = 0
              
        for i in range(len(final_setup1)):
            for j in range(len(final_setup1[i])):
                for k in range(len(final_setup1[i][j])):
                    for l in range(len(final_setup1[i][j][k])):
                        if final_setup1[i][j][k][l] == 1:
                            if l == 0:  
                                setup_matrix[i][j][k][l] = 5500
                                T_setup_cost += 5500
                            else: 
                                setup_matrix[i][j][k][l] = 5500
                                T_changeover_cost += 5500
                                
        Total_setup_cost = T_setup_cost + T_changeover_cost-(r-1)*5500                  

                                
################################################################################

        setup_matrix_time = copy.deepcopy(final_setup1)
        
        
        for i in range(len(final_setup1)):
            for j in range(len(final_setup1[i])):
                for k in range(len(final_setup1[i][j])):
                    for l in range(len(final_setup1[i][j][k])):
                        if final_setup1[i][j][k][l] == 1:
                            if l == 0:  
                                setup_matrix_time[i][j][k][l] = 15
                            else: 
                                setup_matrix_time[i][j][k][l] = 15
        
        
        
        
        T_setup_time = np.zeros((len(R),len(J))).tolist()
        
        for i in range(len(final_setup1)):
            for j in range(len(final_setup1[i])):
                T_setup_time[i-1][j-1] = sum(setup_matrix_time[i-1][j-1][0]) if isinstance(setup_matrix_time[i-1][j-1][0], list) else setup_matrix_time[i-1][j-1][0]

        
        for i in range(1, len(final_setup1)):
            T_setup_time[i][6] = T_setup_time[i][6]-15
        #%%
           
        #Workers salary
        wc = [0,10000,17000,24000,19000,33000,27000,37000]
        
        # Number of working hours of each shift (in minutes)
        wh = [0,480,720,1200,960,1320,1080,1440]
        
            
        # Cost of shift s    
        # shc1 = [0,90000,150000,350000,240000,390000,320000,405000]
        
        
        shc1 = [0,50000,90000,190000,140000,220000,180000,260000]

        
        # tt = [0,1,1.01,1.02,1.03,1.04,1.05,1.06,1.07,1.08,1.09,1.05,1.06,1.07,1.08,1.09,1.1,1.11,
        #       1.12,1.13,1.14,1.1,1.11,1.12,1.13,1.14,1.1,1.11,1.12,1.13,1.14]
        
        #shc = [[element * multiplier for element in shc1] for multiplier in tt]
        
        wcs = sorted(wc)
        
        whs = sorted(wh)
        
        shcs = sorted(shc1)
        
        # shcs = {}
        # for r in R:
        #     shcs[r] = sorted(shc[r])
        
        
        machine = np.zeros((len(R),len(J))).tolist()
        machine1 = np.zeros((len(R),len(J))).tolist()
        day = []
        shc_f = np.zeros((len(R),len(J))).tolist()
        sh_index = np.zeros((len(R),len(J))).tolist()
        day1 = []
        
        
        ptm = np.zeros((len(R),len(J))).tolist()
        
        
        
        for r in R:
            for j in J:
                ptm[r-1][j-1] = sum(pt[i,j]*x[i,j,r].x for i in I)
        
        
        
        
        for r in R:
            for j in J:
                for i in I:
                    if x[i,j,r].x > 0.1:
                        if a[j,r].x >= 0.01:
                            if ptm[r-1][j-1]+T_setup_time[r-1][j-1] > 1440+0.01:
                                print(f'Model is infeasible due to insufficient capacity on day {r} and machine {j}')
                                sys.exit()
                            else:
                                for s in S: 
                                    if ptm[r-1][j-1]+T_setup_time[r-1][j-1] <= whs[s]+0.01:
                                        shc_f[r-1][j-1] = shcs[s]
                                        machine[r-1][j-1] = j
                                        machine1[r-1][j-1] = 1
                                        day.append(r)
                                        index = shcs.index(shcs[s])
                                        sh_index[r-1][j-1] = index
                                        break 
        
            day1.append(r)
                             
        
        shc_t = 0        
        for row in shc_f:
            for element in row: 
                shc_t += element
        
        sh_leg = np.zeros((len(R),len(J),len(S),3)).tolist()
        
                
        for r in day1:
            for j in J:
                if sh_index[r-1][j-1] > 0.5:
                    if sh_index[r-1][j-1] in (1,2):
                        sh_leg[r-1][j-1][sh_index[r-1][j-1]-1][0] = 1
                        
                    elif sh_index[r-1][j-1] in (3,4,5,6):
                        sh_leg[r-1][j-1][sh_index[r-1][j-1]-1][0] = 1
                        sh_leg[r-1][j-1][sh_index[r-1][j-1]-1][1] = 2
                    else:
                        sh_leg[r-1][j-1][sh_index[r-1][j-1]-1][0] = 1
                        sh_leg[r-1][j-1][sh_index[r-1][j-1]-1][1] = 2
                        sh_leg[r-1][j-1][sh_index[r-1][j-1]-1][2] = 3
                  
                    
        labor = np.zeros((len(R),len(J),len(S),3)).tolist()
        
        req_worker = []
    
        for sublist1 in sh_leg:
            sublist1_count = 0
            for sublist2 in sublist1:
                for sublist3 in sublist2:
                    for element in sublist3:
                        if isinstance(element, (int, float)) and element > 0:
                            sublist1_count += 1
            req_worker.append(sublist1_count)
        
                    
        for r in R:
            if ll >= req_worker[r-1]:
                l=1
                for j in J:
                    if sh_index[0][j-1] > 0.5:
                        if sh_index[0][j-1] in (1,2):
                            labor[0][j-1][sh_index[0][j-1]-1][0] = l
                            l+=1
                        elif sh_index[0][j-1] in (3,4,5,6): 
                            labor[0][j-1][sh_index[0][j-1]-1][0] = l
                            l+=1
                            labor[0][j-1][sh_index[0][j-1]-1][1] = l
                            l+=1
                        else:
                            labor[0][j-1][sh_index[0][j-1]-1][0] = l
                            l+=1
                            labor[0][j-1][sh_index[0][j-1]-1][1] = l
                            l+=1
                            labor[0][j-1][sh_index[0][j-1]-1][2] = l
                            l+=1
                            
                sh_N = np.zeros((len(R),len(J),len(S),3)).tolist()
                
                for j in J:
                    for s in S:
                        for leg in (1,2,3):
                            if s in (1,2):
                                sh_N[r-1][j-1][s-1][leg-1] = 0  
            
                            elif s in (3,4,5,6):
                                sh_N[r-1][j-1][s-1][1] = 1
                                
                            else:
                                sh_N[r-1][j-1][s-1][1] = 1
                                sh_N[r-1][j-1][s-1][2] = 1
                
                            
                for r in range(2,len(day1)+1):
                    if r in day1:
                        for j in J:
                            for s in S:
                                for leg in (1,2,3):
                                    if sh_leg[r-1][j-1][s-1][leg-1] > 0.5:
                                        l=1
                                        if sh_N[r-2][j-1][s-1][leg-1] and sh_N[r-1][j-1][s-1][leg-1] == 1:
                                            while l in labor[r-2][j-1][s-1][leg-1]:
                                                l+=1
                                            else:
                                                for j in J:
                                                    for s in S:
                                                        for leg in (1,2,3):
                                                            if sh_leg[r-1][j-1][s-1][leg-1] > 0.5:
                                                                labor[r-1][j-1][s-1][leg-1] = l
                                                                l+=1
                                                       
                                        else:
                                            for j in J:
                                                for s in S:
                                                    for leg in (1,2,3):
                                                        if sh_leg[r-1][j-1][s-1][leg-1] > 0.5:
                                                            if sh_index[r-1][j-1] in (1,2): 
                                                                labor[r-1][j-1][s-1][0] = l
                                                                l+=1
                                                            elif sh_index[r-1][j-1] in (3,4,5,6): 
                                                                labor[r-1][j-1][s-1][0] = l
                                                                l+=1
                                                                labor[r-1][j-1][s-1][1] = l
                                                                l+=1
                                                            else:
                                                                labor[r-1][j-1][s-1][0] = l
                                                                l+=1
                                                                labor[r-1][j-1][s-1][1] = l
                                                                l+=1
                                                                labor[r-1][j-1][s-1][2] = l
                                                                l+=1
             
            else:
                print('*****************************************************************************')
                print('Model is infeasible due to the insufficient worker in day', r)
                print('*****************************************************************************')
                sys.exit()
            
        wc_t = 0
        for r in range (1,len(sh_index)+1):
            for j in J:
                if sh_index[r-1][j-1]>0:
                    if sh_index[r-1][j-1]==1:
                        wc_t+=wcs[1]
                    elif sh_index[r-1][j-1]==2:
                        wc_t+=wcs[2]
                    elif sh_index[r-1][j-1]==3:
                        wc_t+=wcs[3]*2
                    elif sh_index[r-1][j-1]==4:
                        wc_t+=wcs[4]*2
                    elif sh_index[r-1][j-1]==5:
                        wc_t+=wcs[5]*2
                    elif sh_index[r-1][j-1]==6:
                        wc_t+=wcs[6]*2
                    elif sh_index[r-1][j-1]==7:
                        wc_t+=wcs[7]*3
                
                                
                              
       
        
        end_time = time.time()
        runtime = end_time - start_time
        
        
        
        #dfsh = pd.DataFrame({'Day': day, 'Shift': sh_index})
        
        #dfsh['Day'].replace([1,2,3,4,5,6], ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'], inplace=True)
            
        #dfsh['Shift'].replace([1,2,3,4,5,6,7,8,9,10,11,12,13],
        #                    ['(08-16)','(16-24)','(24-08)','(08-20)','(20-08)','(08-16)-(16-24)','(08-16)-(24-08)','(08-18)-(24-08)', 
        #                     '(08-16)-(20-08)','(08-20)-(24-08)','(08-18)-(20-08)','(08-20)-(20-08)','(08-16)-(16-24)–(24-08)'], inplace=True)
                                                                                                      
            
            
            
            
            
            
         
            
        Objective = mdl.ObjVal + Total_setup_cost + wc_t + shc_t - tshc.x
        
        
        objectives = []  
        OB1 = np.sum(tpc.x)
        OB2 = np.sum(tic.x)
        OB3 = np.sum(tbc.x)
        OB4 = Total_setup_cost
        OB5 = np.sum(shc_t)
        OB6 = np.sum(wc_t)
        OB7 = 0
        TOBV = Objective
        CPU_Gurobi = gurobi 
        CPU_Algorithm = runtime
        Gap = 0
        TVars = num_vars
        TBVars = num_binary_vars
        TCVars = num_cont_vars
        TCons = num_constraints
        
        
        objectives.append([OB1,OB2,OB3,OB4,OB5,OB6,OB7,TOBV,CPU_Gurobi,CPU_Algorithm,Gap,TVars,TBVars, TCVars, TCons]) 
        return(objectives)

    
    
    
    
    
    
    
                
                # dfsum = pd.DataFrame({'Total demand': [total_d], 'Total production':[np.sum(list1)],
                #                       'Total inventory':[np.sum(list2)], 'Total backlogging': [np.sum(list3)],
                #                       'Production cost': [np.sum(tpc.x)], 'Inventory cost': [np.sum(tic.x)], 'Backlogging cost': [np.sum(tbc.x)],
                #                       'Setup cost': [setup_cost], 'Changeover cost': [changeover_cost],'Shift cost': [shc_t], 'Worker cost': [wc_t], 'Objective':[Objective] ,
                #                       'CPU':[end-start], 'Gap': [0], '# of variables': [num_vars],
                #                       '# of binary variables': [num_binary_vars], '# of continuous variables': [num_cont_vars], '# of constraints': [num_constraints]})
                
                # with pd.ExcelWriter('C:/Amin/University/Ph.d/TUBITAK 2244/Project/Results_Algorithm.xlsx') as writer:
                #     dfsum.to_excel(writer, sheet_name='General information', index=False)
                #     dfx.to_excel(writer, sheet_name='Production', index=False)
                #     dfIn.to_excel(writer, sheet_name='Inventory', index=False)
                #     dfb.to_excel(writer, sheet_name='Backlogging', index=False)
                #     #dfs.to_excel(writer, sheet_name='Setup', index=False)
                #     #dfch.to_excel(writer, sheet_name='Changeover', index=False)
                #     #dfv.to_excel(writer, sheet_name='v', index=False)
                #     #dfseq.to_excel(writer, sheet_name='Production Sequence', index=False)
                #     #dfsh.to_excel(writer, sheet_name='Shift', index=False) 
                
    

                    


             
