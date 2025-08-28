from gurobipy import *
import pandas as pd
import numpy as np
import random
import time
import openpyxl
import re
import datetime
#%%

def MyCost_Sensitivity(rrr, ptt, dd, l1 ,ins, In1):
    
    n = 55   # Number of all parts
    f = 33   # Number of finished parts
    j = 17   # Number of machines
    r = rrr    # Number of days
    s = 7   # Number of shift types
    l = l1   # Number of workers group
    i = n
    k = n
    rr=r
    #%%
    
    I = [i for i in range(1,i+1)]    # Set of all parts
    I0 = [i for i in range(0,i+1)]   # Set of all parts + 0  
    K = [k for k in range(1,k+1)]    # Set of all parts 
    W = [w for w in (26,28,30,32,34,36,38,40,42,44,45,46,47,48,49,50,51,52,53,54,55)]
    F = [f for f in (1,2,3,4,5,6,7,8,9,10,22,24,26,28,30,32,34,36,38,40,42,44,45,46,47,48,49,50,51,52,53,54,55)] 
    FF = [f for f in (1,2,3,4,5,6,7,8,9,10,22,24)]   # Set of parts need precursor parts 1
    FFF = [f for f in (26,28,30,32,34,36,38,40,42,44)]   # Set of parts need precursor parts 2 
    J = [j for j in range(1,j+1)]    # Set of machines 
    JJ = [j for j in (1,2,3,4,5,6,7,8,9,10,11,13,14,15,16,17)]    # Set of machines 
    R = [r for r in range(1,r+1)]    # Set of days
    S = [s for s in range(1,s+1)]    # Set of shift types
    S1 = [s1 for s1 in (1,2,3)]    # Set of shift types
    L = [l for l in range(1,l+1)]    # Set of workers group
    #%%
    
    #Inventory cost for one unit of part i
    ic = {}
    for i in range(1,i+1):
        ic[i] = 2
        
    
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
    s1 = 7000
    sc = {}
    for i in range(1,i+1):
        for j in range(1,j+1):
            sc[i,j] = 5500
            sc[12,3] = s1
            sc[14,2] = s1
            sc[17,4] = s1
            sc[18,1] = s1
            sc[20,4] = s1
            sc[22,8] = s1
            sc[24,8] = s1 
            sc[25,9] = s1
            sc[26,12] = s1
            sc[27,9] = s1
            sc[28,12] = s1
            sc[29,9] = s1
            sc[30,12] = s1
            sc[31,9] = s1
            sc[32,12] = s1
            sc[33,9] = s1
            sc[34,12] = s1
            sc[35,9] = s1
            sc[36,12] = s1
            sc[37,9] = s1
            sc[38,12] = s1
            sc[39,9] = s1
            sc[40,12] = s1
            sc[41,9] = s1
            sc[42,12] = s1
            sc[43,9] = s1
            sc[44,12] = s1
            sc[45,13] = s1
            sc[47,15] = s1
            sc[50,14] = s1
            sc[52,16] = s1
            sc[53,15] = s1
                      
    
    #Setup time for part i on machine j
    st = {}
    for i in range(1,i+1):
        for j in range(1,j+1):
            st[i,j] = 15 
    
    
    #Setup cost of a changeover from part i to part k on machine j
    csc = {}
    for i in range(1,i+1):
        for k in range(1,k+1):
            for j in range(1,j+1):
                csc[i,k,j] = 5500        
    
    
    #Setup time of a changeover from part i to part k on machine j
    cst = {}
    for i in range(1,i+1):
        for k in range(1,k+1):
            for j in range(1,j+1):
                cst[i,k,j] = 15
    
    
    
    # Number of working hours of each shift (in minutes)
    #wh = [0,1440,1200,960,1200,960,1320,1080,480,480,720,720,480,1440]    
    
    wh = [0,480,720,1200,960,1320,1080,1440]
    
    #Workers salary
    #wc = [0,3000,2400,1700,1900,1500,2700,2100,700,1000,1300,1600,900,3000]
        
    wc = [0,10000,17000,24000,19000,33000,27000,37000]
    
  
    # Cost of shift s
   
    shc = [0,50000,90000,190000,140000,220000,180000,260000]

    
    
    
    # shc = {}
    # for s in S:
    #     shc [1,s] = 1*shc1[s]  
    #     shc [2,s] = 1.01*shc1[s] 
    #     shc [3,s] = 1.02*shc1[s] 
    #     shc [4,s] = 1.03*shc1[s]
    #     shc [5,s] = 1.04*shc1[s]
    #     shc [6,s] = 1.05*shc1[s]
    #     shc [7,s] = 1.06*shc1[s]
    #     shc [8,s] = 1.07*shc1[s]
    #     shc [9,s] = 1.08*shc1[s]
    #     shc [10,s] = 1.09*shc1[s]
    #     shc [11,s] = 1.05*shc1[s]
    #     shc [12,s] = 1.06*shc1[s]
    #     shc [13,s] = 1.07*shc1[s]
    #     shc [14,s] = 1.08*shc1[s]
    #     shc [15,s] = 1.09*shc1[s]
    #     shc [16,s] = 1.1*shc1[s]
    #     shc [17,s] = 1.11*shc1[s]
    #     shc [18,s] = 1.12*shc1[s]
    #     shc [19,s] = 1.13*shc1[s]
    #     shc [20,s] = 1.14*shc1[s]
    #     shc [21,s] = 1.1*shc1[s]
    #     shc [22,s] = 1.11*shc1[s]
    #     shc [23,s] = 1.12*shc1[s]
    #     shc [24,s] = 1.13*shc1[s]
    #     shc [25,s] = 1.14*shc1[s]
    #     shc [26,s] = 1.1*shc1[s]
    #     shc [27,s] = 1.11*shc1[s]
    #     shc [28,s] = 1.12*shc1[s]
    #     shc [29,s] = 1.13*shc1[s]
    #     shc [30,s] = 1.14*shc1[s]
        
        
    
    aa = 15
    
           
    #Compatibility matrix
    cm = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
          [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
          [0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0], 
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0], 
          [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0], 
          [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0], 
          [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0],
          [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],  
          [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1]]
    
    
    ga = [[0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,0,0,0,0,0,0,0],
          [0,1,1,1,1,1,1,1],
          [0,0,0,0,0,0,0,0],
          [0,1,1,1,1,1,1,1],
          [0,1,1,1,1,1,1,1],
          [0,1,1,1,1,1,1,1]]
    
  
    
    
    # Demand Generation
    
    
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
            
            total_demand = d[1, r] + d[2, r] + d[3, r] + d[4, r] + d[5, r] + d[6, r] + d[7, r] + d[8, r] + d[9, r] + d[10, r]
            
            d[22, r] = total_demand
            d[24, r] = total_demand
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
            d[55, r] = total_demand
            
    
        total_d = sum(d.values())
        return d, total_d
 
    d, total_demand = generate_demand(period, seedd)
    
    
    
    
    cm = {(i,j): (cm[i][j]) for i in I0 for j in J}
    ga = {(ss,s): (ga[ss][s]) for ss in S for s in S}
    
    
    pi = {1:[0,11,2,2], 2:[0,12,1,3], 3:[0,13,1,1], 4:[0,14,4,4], 5:[0,15,1,1], 6:[0,16,4,4], 7:[0,17,2,4], 8:[0,18,1,3], 9:[0,19,1,1], 10:[0,20,2,4], 
          11:[0,11,3,3], 12:[0,12,2,2], 13:[0,13,2,2], 14:[0,14,1,1], 15:[0,15,1,1], 16:[0,16,1,1], 17:[0,17,1,1], 18:[0,18,2,2], 19:[0,19,2,2], 20:[0,20,1,1], 
          21:[0,21,7,7], 22:[0,21,6,17], 23:[0,23,7,7], 24:[0,23,6,17], 25:[0,25,8,8], 26:[25,26,9,9], 27:[0,27,8,8], 28:[27,28,9,9], 29:[0,29,8,8], 30:[29,30,9,9],
          31:[0,31,8,8], 32:[31,32,9,9], 33:[0,33,8,8], 34:[33,34,9,9], 35:[0,35,8,8], 36:[35,36,9,9], 37:[0,37,8,8], 38:[37,38,9,9], 39:[0,39,8,8], 40:[39,40,9,9],
          41:[0,41,8,8], 42:[41,42,9,9], 43:[0,43,8,8], 44:[43,44,9,9], 45:[0,45,14,14], 46:[0,46,14,14], 47:[0,47,13,13], 48:[0,48,14,14], 49:[0,49,14,14],
          50:[0,50,15,15], 51:[0,51,15,15], 52:[0,52,13,13], 53:[0,53,14,14], 54:[0,54,14,14], 55:[0,55,5,5]}    
          
          
    
    pii = {1:[0,22,24,7,8], 2:[0,22,24,7,8], 3:[0,22,24,7,8], 4:[0,22,24,7,8], 5:[0,22,24,7,8], 6:[0,22,24,7,8], 7:[0,22,24,7,8], 8:[0,22,24,7,8], 9:[0,22,24,7,8], 10:[0,22,24,7,8]}
    
    s11 = {1:[1], 2:[1], 3:[1,2], 4:[1,2], 5:[1,2], 6:[1,2], 7:[1,2,3]}


    leg = [0,1,1,2,2,2,2,3]
    
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
    stt = mdl.addVars(I,J,R, lb=0.0, vtype=GRB.CONTINUOUS)
    ctt = mdl.addVars(I,J,R, lb=0.0, vtype=GRB.CONTINUOUS)
    z = mdl.addVars(I0,I0,J,R, vtype=GRB.BINARY)
    v = mdl.addVars(I,R, vtype=GRB.BINARY)
    a = mdl.addVars(J,R,S, vtype=GRB.BINARY)
    q = mdl.addVars(I0,I,J,R, vtype=GRB.BINARY)
    w = mdl.addVars(L,J,R,S,S1, vtype=GRB.BINARY)
    f = mdl.addVars(J,R, vtype=GRB.BINARY)
    tpc = mdl.addVar(vtype=GRB.CONTINUOUS)
    tic = mdl.addVar(vtype=GRB.CONTINUOUS)
    tbc = mdl.addVar(vtype=GRB.CONTINUOUS)
    tsc = mdl.addVar(vtype=GRB.CONTINUOUS)
    tchc = mdl.addVar(vtype=GRB.CONTINUOUS)
    tshc = mdl.addVar(vtype=GRB.CONTINUOUS)
    twc = mdl.addVar(vtype=GRB.CONTINUOUS)
    titc = mdl.addVar(vtype=GRB.BINARY)
    
    #%%
    
    mdl.modelSense = GRB.MINIMIZE
    #%%
    
    #Objective Function
    
    mdl.setObjective(quicksum(pc[i,j,r]*x[i,j,r] for i in I for j in J for r in R)              
                    +quicksum(ic[i]*(In[i,r]) for i in I for r in R)
                    +quicksum(bc[i]*b[i,r] for i in I for r in R)
                    +quicksum(sc[i,j]*(z[0,i,j,r]-q[0,i,j,r]) for i in I for j in J for r in R)
                    +quicksum(csc[i,k,j]*z[i,k,j,r] for i in I for k in K for j in J for r in R)
                    +quicksum(shc[s]*a[j,r,s] for j in J for r in R for s in S)
                    +quicksum(wc[s]*w[l,j,r,s,s1] for l in L for j in J for r in R for s in S for s1 in S1)
                    +quicksum(10000*f[j,r] for j in J for r in R))
    #%%
    
    #Constraints
    
    mdl.addConstr(tpc == quicksum(pc[i,j,r]*x[i,j,r] for i in I for j in J for r in R));
    mdl.addConstr(tic == quicksum(ic[i]*(In[i,r]) for i in I for r in R));
    mdl.addConstr(tbc == quicksum(bc[i]*b[i,r] for i in I for r in R));
    mdl.addConstr(tsc == quicksum(sc[i,j]*(z[0,i,j,r]-q[0,i,j,r]) for i in I for j in J for r in R));
    mdl.addConstr(tchc == quicksum(csc[i,k,j]*z[i,k,j,r] for i in I for k in K for j in J for r in R));
    mdl.addConstr(tshc == quicksum(shc[s]*a[j,r,s] for j in J for r in R for s in S));
    mdl.addConstr(twc == quicksum(wc[s]*w[l,j,r,s,s1] for l in L for j in J for r in R for s in S for s1 in S1));
    mdl.addConstr(titc == quicksum(10000*f[j,r] for j in J for r in R));
    
    #%%
    
    mdl.addConstrs(d[i,1] == quicksum(x[i,j,1] for j in J)-In[i,1]+b[i,1]+In0[i] for i in F);
    
    mdl.addConstrs(d[i,r] == quicksum(x[i,j,r] for j in J)+In[i,r-1]-In[i,r]-b[i,r-1]+b[i,r] for i in F for r in R if r>=2); 
    
    mdl.addConstrs(quicksum(x[i,j,1] for j in JJ) <= quicksum(x[pi[i][l],j,1] for j in JJ)+In0[pi[i][l]]-In[pi[i][l],1] for i in FF for l in range(1,2));
    
    mdl.addConstrs(quicksum(x[i,j,r] for j in JJ) <= quicksum(x[pi[i][l],j,r] for j in JJ)+In[pi[i][l],r-1]-In[pi[i][l],r] for i in FF for l in range(1,2) for r in R if r>=2);  
    
    mdl.addConstrs(x[i,12,1] <= x[pi[i][l],9,1]+In0[pi[i][l]]-In[pi[i][l],1] for i in FFF for l in range(0,1));
    
    mdl.addConstrs(x[i,12,r] <= x[pi[i][l],9,r]+In[pi[i][l],r-1]-In[pi[i][l],r] for i in FFF for l in range(0,1) for r in R if r>=2);
    
    mdl.addConstrs(quicksum(x[i,j,r] for j in J for i in (1,2,3,4,5,6,7,8,9,10)) <= quicksum(x[22,j,r] for j in J) for r in R); 
        
    mdl.addConstrs(quicksum(x[i,j,r] for j in J for i in (1,2,3,4,5,6,7,8,9,10)) <= quicksum(x[24,j,r] for j in J) for r in R); 
    
    mdl.addConstrs(x[i,j,r] <= M*(z[0,i,j,r]+quicksum(z[k,i,j,r] for k in I if k!=i)) for i in I for j in J for r in R);
        
    mdl.addConstrs(quicksum(z[k,i,j,r] for k in I0 if k!=i) == quicksum(z[i,k,j,r] for k in I0 if k!=i) for i in I for j in J for r in R); 
    
    mdl.addConstrs(z[0,i,j,1] >= q[0,i,j,1] for i in I for j in J); 
    
    mdl.addConstrs(z[0,i,j,1] <= 1-q[0,i,j,1] for i in I for j in J); 
    
    mdl.addConstrs(z[i,0,j,r-1]+z[0,i,j,r]-1 <= q[0,i,j,r] for i in I for j in J for r in R if r>=2); 
    
    mdl.addConstrs(q[0,i,j,r] <= z[0,i,j,r] for i in I for j in J for r in R if r>=2);  
    
    mdl.addConstrs(q[0,i,j,r] <= z[i,0,j,r-1] for i in I for j in J for r in R if r>=2);  
    
    mdl.addConstrs(quicksum(a[j,r,s] for s in S) <= 1 for r in R for j in J);
    
    
    
    
    mdl.addConstrs(1+f[j,r+1] >= a[j,r,s]+a[j,r+1,ss]-2*ga[s,ss] for j in J for r in R if r<=rr-1 for s in S for ss in S);
    
    
    
    
    
    mdl.addConstrs(stt[i,j,r] >= st[i,j]*(z[0,i,j,r]-q[0,i,j,r]) for i in W for j in JJ for r in R if r==1); 
    
    mdl.addConstrs(stt[i,j,r] >= st[i,j]*(z[0,i,j,r]-q[0,i,j,r])+aa*f[j,r] for i in W for j in JJ for r in R if r>=2 for s in S);
     
    mdl.addConstrs(stt[i,j,r] >= ctt[pi[i][l],pi[i][ll],r]+st[i,j]*(z[0,i,j,r]-q[0,i,j,r])-1440*(1-(z[0,i,j,r]-q[0,i,j,r])) for i in FF for l in range(1,2) for ll in range(2,4) for j in JJ for r in R if r==1); 
    
    mdl.addConstrs(stt[i,j,r] >= ctt[pi[i][l],pi[i][ll],r]+st[i,j]*(z[0,i,j,r]-q[0,i,j,r])+aa*f[j,r]-1440*(1-(z[0,i,j,r]-q[0,i,j,r])) for i in FF for l in range(1,2) for ll in range(2,4) for j in JJ for r in R if r>=2 for s in S);
    
    mdl.addConstrs(stt[i,j,r] >= ctt[pii[i][l],pii[i][ll],r]+st[i,j]*(z[0,i,j,r]-q[0,i,j,r])-1440*(1-(z[0,i,j,r]-q[0,i,j,r])) for i in (1,2,3,4,5,6,7,8,9,10) for l in range(1,3) for ll in range(3,5) for j in JJ for r in R if r==1); 
    
    mdl.addConstrs(stt[i,j,r] >= ctt[pii[i][l],pii[i][ll],r]+st[i,j]*(z[0,i,j,r]-q[0,i,j,r])+aa*f[j,r]-1440*(1-(z[0,i,j,r]-q[0,i,j,r])) for i in (1,2,3,4,5,6,7,8,9,10) for l in range(1,3) for ll in range(3,5) for j in JJ for r in R if r>=2 for s in S);

    mdl.addConstrs(stt[i,12,r] >= ctt[pi[i][l],pi[i][ll],r]+st[i,12]*(z[0,i,12,r]-q[0,i,12,r]) for i in FFF for l in range(0,1) for ll in range(2,3) for r in R if r==1); 
    
    mdl.addConstrs(stt[i,12,r] >= ctt[pi[i][l],pi[i][ll],r]+st[i,12]*(z[0,i,12,r]-q[0,i,12,r])+aa*f[j,r] for i in FFF for l in range(0,1) for ll in range(3,3) for r in R if r>=2 for s in S);
    
    mdl.addConstrs(stt[i,j,r] >= ctt[k,j,r]+cst[k,i,j]*z[k,i,j,r]-1440*(1-z[k,i,j,r]) for i in I for k in I if i!=k for j in J for r in R); 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # mdl.addConstrs(stt[i,j,r] >= st[i,j]*(z[0,i,j,r]-q[0,i,j,r]) for i in W for j in JJ for r in R if r==1); 
    
    # mdl.addConstrs(stt[i,j,r] >= st[i,j]*(z[0,i,j,r]-q[0,i,j,r])+aa*(1-quicksum(ga[ss,s]*a[j,r-1,ss] for ss in S)) for i in W for j in JJ for r in R if r>=2 for s in S);
     
    # mdl.addConstrs(stt[i,j,r] >= ctt[pi[i][l],pi[i][ll],r]+st[i,j]*(z[0,i,j,r]-q[0,i,j,r])-1440*(1-(z[0,i,j,r]-q[0,i,j,r])) for i in FF for l in range(1,2) for ll in range(2,4) for j in JJ for r in R if r==1); 
    
    # mdl.addConstrs(stt[i,j,r] >= ctt[pi[i][l],pi[i][ll],r]+st[i,j]*(z[0,i,j,r]-q[0,i,j,r])+aa*(1-quicksum(ga[ss,s]*a[j,r-1,ss] for ss in S))-1440*(1-(z[0,i,j,r]-q[0,i,j,r])) for i in FF for l in range(1,2) for ll in range(2,4) for j in JJ for r in R if r>=2 for s in S);
    
    # mdl.addConstrs(stt[i,j,r] >= ctt[pii[i][l],pii[i][ll],r]+st[i,j]*(z[0,i,j,r]-q[0,i,j,r])-1440*(1-(z[0,i,j,r]-q[0,i,j,r])) for i in (1,2,3,4,5,6,7,8,9,10) for l in range(1,3) for ll in range(3,5) for j in JJ for r in R if r==1); 
    
    # mdl.addConstrs(stt[i,j,r] >= ctt[pii[i][l],pii[i][ll],r]+st[i,j]*(z[0,i,j,r]-q[0,i,j,r])+aa*(1-quicksum(ga[ss,s]*a[j,r-1,ss] for ss in S))-1440*(1-(z[0,i,j,r]-q[0,i,j,r])) for i in (1,2,3,4,5,6,7,8,9,10) for l in range(1,3) for ll in range(3,5) for j in JJ for r in R if r>=2 for s in S);

    # mdl.addConstrs(stt[i,12,r] >= ctt[pi[i][l],pi[i][ll],r]+st[i,12]*(z[0,i,12,r]-q[0,i,12,r]) for i in FFF for l in range(0,1) for ll in range(2,3) for r in R if r==1); 
    
    # mdl.addConstrs(stt[i,12,r] >= ctt[pi[i][l],pi[i][ll],r]+st[i,12]*(z[0,i,12,r]-q[0,i,12,r])+aa*(1-quicksum(ga[ss,s]*a[12,r-1,ss] for ss in S)) for i in FFF for l in range(0,1) for ll in range(3,3) for r in R if r>=2 for s in S);
    
    # mdl.addConstrs(stt[i,j,r] >= ctt[k,j,r]+cst[k,i,j]*z[k,i,j,r]-1440*(1-z[k,i,j,r]) for i in I for k in I if i!=k for j in J for r in R);  
    
    mdl.addConstrs(ctt[i,j,r] >= stt[i,j,r]+pt[i,j]*x[i,j,r] for i in I for j in J for r in R);  
    
    mdl.addConstrs(ctt[i,j,r] <= quicksum(wh[s]*a[j,r,s] for s in S) for i in I  for j in J for r in R);
    
    mdl.addConstrs(b[i,rr] == 0 for i in F);
    
    mdl.addConstrs(z[0,i,j,r] <= cm[i,j] for i in I for j in J for r in R);
    
    mdl.addConstrs(z[i,0,j,r] <= cm[i,j] for i in I for j in J for r in R);
    
    mdl.addConstrs(z[i,k,j,r] <= cm[k,j] for i in I for k in I if i!=k for j in J for r in R);
    
    mdl.addConstrs(quicksum(z[0,i,j,r] for i in I) <= 1 for j in J for r in R);
    
    mdl.addConstrs(quicksum(z[i,k,j,r] for k in I if i!=k) <= z[0,i,j,r] for i in I for j in J for r in R);
    
    mdl.addConstrs(quicksum(w[l,j,r,s,s1] for j in J for s in S for s1 in range(1,len(s11[s])+1)) <= 1 for l in L for r in R);
    
    mdl.addConstrs(leg[s]*a[j,r,s] <= quicksum(w[l,j,r,s,s1] for l in L for s1 in range(1,len(s11[s])+1)) for j in J for r in R for s in S);
    
    #mdl.addConstrs(quicksum(w[l,j,r,s,1]+w[l,j,r+1,s,1] for j in J for s in (9,11,12)) <= 1  for l in L for r in R if r<=rr-1);
    
    mdl.addConstrs(quicksum(w[l,j,r,s,2]+w[l,j,r+1,s,2] for j in J for s in (3,4,5,6)) <= 1  for l in L for r in R if r<=rr-1);
    
    mdl.addConstrs(quicksum(w[l,j,r,7,s1]+w[l,j,r+1,7,s1] for j in J for s1 in (2,3)) <= 1  for l in L for r in R if r<=rr-1);
    
    
    
    mdl.addConstrs(quicksum(w[l,j,r,s,s1] for l in L) <= 1 for j in J for s in S for s1 in range(1,len(s11[s])+1) for r in R);
    
    #%%   
    
  
    #mdl.addConstrs((v[i,1]-1)*M <= In0[pi[i][l]]-quicksum(x[i,j,1] for j in JJ) for i in FF for l in range(1,2)); 
    
    #mdl.addConstrs((v[i,r]-1)*M <= In[pi[i][l],r-1]-quicksum(x[i,j,r] for j in JJ) for i in FF for l in range(1,2) for r in R if r>=2); 
    
    #mdl.addConstrs((v[i,1]-1)*M <= In0[pii[i][l]]-quicksum(x[i,j,1] for j in JJ) for i in (1,2,3,4) for l in range(1,3)); 
    
    #mdl.addConstrs((v[i,r]-1)*M <= In[pii[i][l],r-1]-quicksum(x[i,j,r] for j in JJ) for i in (1,2,3,4) for l in range(1,3) for r in R if r>=2);
    
    #mdl.addConstrs((v[i,1]-1)*M <= In0[pi[i][l]]-x[i,12,1] for i in FFF for l in range(0,1)); 
    
    #mdl.addConstrs((v[i,r]-1)*M <= In[pi[i][l],r-1]-x[i,12,r] for i in FFF for l in range(0,1) for r in R if r>=2); 
    
    #mdl.addConstrs(stt[i,j,r]-ctt[pi[i][l],pi[i][ll],r]-st[i,j]*(z[0,i,j,r]-q[0,i,j,r]) >= (-M)*v[i,r] for i in FF for l in range(1,2) for ll in range(2,3) for j in JJ for r in R);  
    
    #mdl.addConstrs(stt[i,j,r]-ctt[pii[i][l],pii[i][ll],r]-st[i,j]*(z[0,i,j,r]-q[0,i,j,r]) >= (-M)*v[i,r] for i in (1,2,3,4) for l in range(1,3) for ll in range(3,5) for j in JJ for r in R);  
    
    #mdl.addConstrs(stt[i,12,r]-ctt[pi[i][l],9,r]-st[i,12]*(z[0,i,12,r]-q[0,i,12,r]) >= (-M)*v[i,r] for i in FFF for l in range(0,1) for r in R);  
    
    
    
                    

    # mdl.addConstrs(stt[i,j,r] >= st[i,j]*(z[0,i,j,r]-q[0,i,j,r]) for i in W for j in JJ for r in R if r==1); 
    
    # mdl.addConstrs(stt[i,j,r] >= st[i,j]*(z[0,i,j,r]-q[0,i,j,r])+aa*(1-quicksum(ga[ss,s]*a[j,r-1,ss] for ss in S)) for i in W for j in JJ for r in R if r>=2 for s in S);
    
    # mdl.addConstrs(stt[i,j,r] >= ctt[pi[i][l],pi[i][ll],r]+st[i,j]*(z[0,i,j,r]-q[0,i,j,r]) for i in FF for l in range(1,2) for ll in range(2,3) for j in JJ for r in R if r==1); 
    
    # mdl.addConstrs(stt[i,j,r] >= ctt[pi[i][l],pi[i][ll],r]+st[i,j]*(z[0,i,j,r]-q[0,i,j,r])+aa*(1-quicksum(ga[ss,s]*a[j,r-1,ss] for ss in S)) for i in FF for l in range(1,2) for ll in range(2,3) for j in JJ for r in R if r>=2 for s in S);
    
    # mdl.addConstrs(stt[i,j,r] >= ctt[pii[i][l],pii[i][ll],r]+st[i,j]*(z[0,i,j,r]-q[0,i,j,r]) for i in (1,2,3,4,5,6,7,8,9,10) for l in range(1,3) for ll in range(3,5) for j in JJ for r in R if r==1); 
    
    # mdl.addConstrs(stt[i,j,r] >= ctt[pii[i][l],pii[i][ll],r]+st[i,j]*(z[0,i,j,r]-q[0,i,j,r])+aa*(1-quicksum(ga[ss,s]*a[j,r-1,ss] for ss in S)) for i in (1,2,3,4,5,6,7,8,9,10) for l in range(1,3) for ll in range(3,5) for j in JJ for r in R if r>=2 for s in S);
    
    # mdl.addConstrs(stt[i,12,r] >= ctt[pi[i][l],pi[i][ll],r]+st[i,12]*(z[0,i,12,r]-q[0,i,12,r]) for i in FFF for l in range(0,1) for ll in range(2,3) for r in R if r==1); 
    
    # mdl.addConstrs(stt[i,12,r] >= ctt[pi[i][l],pi[i][ll],r]+st[i,12]*(z[0,i,12,r]-q[0,i,12,r])+aa*(1-quicksum(ga[ss,s]*a[12,r-1,ss] for ss in S)) for i in FFF for l in range(0,1) for ll in range(3,3) for r in R if r>=2 for s in S);
    
    # mdl.addConstrs(stt[i,j,r] >= ctt[k,j,r]+cst[k,i,j]*z[k,i,j,r]-1440*(1-z[k,i,j,r]) for i in I for k in I if i!=k for j in J for r in R);  
    
    # mdl.addConstrs(ctt[i,j,r] >= stt[i,j,r]+pt[i,j]*x[i,j,r] for i in I for j in J for r in R);  
    
    # mdl.addConstrs(ctt[i,j,r] <= quicksum(wh[s]*a[j,r,s] for s in S) for i in I  for j in J for r in R);
    
        
  
    #%%
    
    mdl.Params.MIPGap = 0.0
    mdl.Params.TimeLimit = 10000 
    start = time.time()
    mdl.optimize()
    
    if mdl.status == GRB.INFEASIBLE:
    # model.computeIIS()
    # model.write("infeasible_model.ilp")
        return

    else:
        end = time.time()
        num_vars = len(mdl.getVars())
        num_binary_vars = len([var for var in mdl.getVars() if var.vType == GRB.BINARY])
        num_cont_vars = len([var for var in mdl.getVars() if var.vType == GRB.CONTINUOUS])
        num_constraints = mdl.NumConstrs
        
        #%%
        
        # print('Solution time:', end-start)
        # print("Objective Value =", mdl.ObjVal)
        # print('Gap =', mdl.MIPGap)
        # print("Total number of decision variables:", num_vars)
        # print("Number of binary decision variables:", num_binary_vars)
        # print("Number of continuous decision variables:", num_cont_vars)
        # print('Number of constraints:', num_constraints)
    #     #%%
        
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
        
    #     dfx = pd.DataFrame({'Part': part, 'Machine': machine, 'Day': day, 'Value': value_x})
    #     dfx['Part'].replace([i for i in range(1,i+1)], ['Tam1', 'Tam2', 'Tam3', 'Tam4', 'Tam5', 'Tam6', 'Tam7', 'Tam8', 'Tam9', 'Tam10',
    #                                                     'ÇT1', 'ÇT2','ÇT3', 'ÇT4', 'ÇT5', 'ÇT6', 'ÇT7', 'ÇT8', 'ÇT9', 'ÇT10', 'ÖKP', 'ÖK',
    #                                                     'AKP', 'AK', 'ÖPB1', 'ÖP1', 'ÖPB2', 'ÖP2', 'ÖPB3', 'ÖP3', 'ÖPB4','ÖP4',
    #                                                     'ÖPB5','ÖP5', 'ÖPB6','ÖP6', 'ÖPB7','ÖP7', 'ÖPB8','ÖP8', 'ÖPB9','ÖP9', 'ÖPB10','ÖP10','GÖ1', 'GÖ2',
    #                                                     'GÖ3', 'GÖ4', 'GÖ5', 'GÖ6', 'GÖ7', 'GÖ8', 'GÖ9', 'GÖ10', 'Ment'], inplace=True)
    #     dfx['Machine'].replace([j for j in range(1,j+1)], ['Tam1', 'Tam2', 'Tam3', 'Tam4', 'TamAssm', 'PK', 'Ales', '800_ton', 'BK',
    #                                                                       'ÖP1', 'ÖP2', '1250_trans', 'GÖ1', 'GÖ2', 'GÖ3', 'GÖ4'], inplace=True)
    #     dfx['Day'].replace([1,2,3,4,5,6], ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'], inplace=True)
    #     #%%
        
    #     list12 = []
    #     for i in I:
    #         for j in J:
    #             for r in R:
    #                 if z[0,i,j,r].X>=0.1:
    #                     if x[i,j,r].X>=0.1:
    #                         print("xb("+str(i)+','+str(j)+','+str(r)+")=", round(x[i,j,r].x))
    #                         if i in F:
    #                             list12.append(x[i,j,r].x)
    #     print('-------------------------------------------------')
    #     print('Total Production Amount:', np.sum(list12))
    #     #%%
        
    #     list13 = []
    #     for k in I:
    #         for i in I:
    #             for j in J:
    #                 for r in R:
    #                     if z[i,k,j,r].X>=0.1:
    #                         if x[k,j,r].X>=0.1:
    #                             print("xd("+str(k)+','+str(j)+','+str(r)+")=", round(x[k,j,r].x))
    #                             if k in F:
    #                                     list13.append(x[k,j,r].x)
    #     print('-------------------------------------------------')
    #     print('Total Production Amount:', np.sum(list13))
    #     #%%
        
    #     list2 = []
    #     part = []
    #     day = []
    #     value_In = []
    #     for i in I:
    #         for r in R:
    #             if In[i,r].X>0.01:
    #                 print("In("+str(i)+','+str(r)+")=", round(In[i,r].X))
    #                 part.append(i)
    #                 day.append(r)
    #                 value_In.append(round(In[i,r].X))
    #                 #if r==rr:
    #                 list2.append(round(In[i,r].X))
                        
    #     print('-------------------------------------------------')
    #     print('Total Inventory Amount:', np.sum(list2))
    #     print('Total Inventory Cost:', tic.x)
    #     dfIn = pd.DataFrame({'Part': part, 'Day': day, 'Value': value_In})
    #     dfIn['Part'].replace([i for i in range(1,i+1)], ['Tam1', 'Tam2', 'Tam3', 'Tam4', 'Tam5', 'Tam6', 'Tam7', 'Tam8', 'Tam9', 'Tam10',
    #                                                     'ÇT1', 'ÇT2','ÇT3', 'ÇT4', 'ÇT5', 'ÇT6', 'ÇT7', 'ÇT8', 'ÇT9', 'ÇT10', 'ÖKP', 'ÖK',
    #                                                     'AKP', 'AK', 'ÖPB1', 'ÖP1', 'ÖPB2', 'ÖP2', 'ÖPB3', 'ÖP3', 'ÖPB4','ÖP4',
    #                                                     'ÖPB5','ÖP5', 'ÖPB6','ÖP6', 'ÖPB7','ÖP7', 'ÖPB8','ÖP8', 'ÖPB9','ÖP9', 'ÖPB10','ÖP10','GÖ1', 'GÖ2',
    #                                                     'GÖ3', 'GÖ4', 'GÖ5', 'GÖ6', 'GÖ7', 'GÖ8', 'GÖ9', 'GÖ10', 'Ment'], inplace=True)
    #     dfIn['Day'].replace([1,2,3,4,5,6], ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'], inplace=True)
    #     #%%
        
    #     list3 = []
    #     part = []
    #     day = []
    #     value_b = []
    #     for i in I:
    #         for r in R:
    #             if b[i,r].X>0.01:
    #                 print("b("+str(i)+','+str(r)+")=", round(b[i,r].X)) 
    #                 part.append(i)
    #                 day.append(r)
    #                 value_b.append(round(b[i,r].X))
    #                 #if r==rr:
    #                 list3.append(round(b[i,r].X))
    #     print('-------------------------------------------------')
    #     print('Total Backlogging Amount:', np.sum(list3))
    #     print('Total Backlogging Cost:', tbc.x)
    #     dfb = pd.DataFrame({'Part': part, 'Day': day, 'Value': value_b})
    #     dfb['Part'].replace([i for i in range(1,i+1)], ['Tam1', 'Tam2', 'Tam3', 'Tam4', 'Tam5', 'Tam6', 'Tam7', 'Tam8', 'Tam9', 'Tam10',
    #                                                     'ÇT1', 'ÇT2','ÇT3', 'ÇT4', 'ÇT5', 'ÇT6', 'ÇT7', 'ÇT8', 'ÇT9', 'ÇT10', 'ÖKP', 'ÖK',
    #                                                     'AKP', 'AK', 'ÖPB1', 'ÖP1', 'ÖPB2', 'ÖP2', 'ÖPB3', 'ÖP3', 'ÖPB4','ÖP4',
    #                                                     'ÖPB5','ÖP5', 'ÖPB6','ÖP6', 'ÖPB7','ÖP7', 'ÖPB8','ÖP8', 'ÖPB9','ÖP9', 'ÖPB10','ÖP10','GÖ1', 'GÖ2',
    #                                                     'GÖ3', 'GÖ4', 'GÖ5', 'GÖ6', 'GÖ7', 'GÖ8', 'GÖ9', 'GÖ10', 'Ment'], inplace=True)
    #     dfb['Day'].replace([1,2,3,4,5,6], ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'], inplace=True)
    #     #%%
        
    #     list4 = []
    #     part = []
    #     machine = []
    #     day = []
    #     for i in I:
    #         for j in J:
    #             for r in R:
    #                 if z[0,i,j,r].X>=0.01:
    #                     #if x[i,j,r].X>=0.1:
    #                     print("zs("+str(i)+','+str(j)+','+str(r)+")=", z[0,i,j,r].X)
    #                     list4.append(z[0,i,j,r].X)
    #                     part.append(i)
    #                     machine.append(j)
    #                     day.append(r)
    #     print('-------------------------------------------------')
    #     print('Total Setup:', np.sum(list4)) 
    #     print('Total Setup Cost:', tsc.x) 
    #     dfs = pd.DataFrame({'Part': part, 'Machine': machine, 'Day': day})
    #     dfs['Part'].replace([i for i in range(1,i+1)], ['Tam1', 'Tam2', 'Tam3', 'Tam4', 'Tam5', 'Tam6', 'Tam7', 'Tam8', 'Tam9', 'Tam10',
    #                                                     'ÇT1', 'ÇT2','ÇT3', 'ÇT4', 'ÇT5', 'ÇT6', 'ÇT7', 'ÇT8', 'ÇT9', 'ÇT10', 'ÖKP', 'ÖK',
    #                                                     'AKP', 'AK', 'ÖPB1', 'ÖP1', 'ÖPB2', 'ÖP2', 'ÖPB3', 'ÖP3', 'ÖPB4','ÖP4',
    #                                                     'ÖPB5','ÖP5', 'ÖPB6','ÖP6', 'ÖPB7','ÖP7', 'ÖPB8','ÖP8', 'ÖPB9','ÖP9', 'ÖPB10','ÖP10','GÖ1', 'GÖ2',
    #                                                     'GÖ3', 'GÖ4', 'GÖ5', 'GÖ6', 'GÖ7', 'GÖ8', 'GÖ9', 'GÖ10', 'Ment'], inplace=True)
    #     dfs['Machine'].replace([j for j in range(1,j+1)], ['Tam1', 'Tam2', 'Tam3', 'Tam4', 'TamAssm', 'PK', 'Ales', '800_ton', 'BK',
    #                                                                       'ÖP1', 'ÖP2', '1250_trans', 'GÖ1', 'GÖ2', 'GÖ3', 'GÖ4'], inplace=True)
    #     dfs['Day'].replace([1,2,3,4,5,6], ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'], inplace=True)
    #     #%%
        
    #     list5 = []
    #     part1 = []
    #     part2 = []
    #     machine = []
    #     day = []
    #     for i in I:
    #         for k in I:
    #             for j in J:
    #                 for r in R:
    #                     if z[i,k,j,r].X>=0.01:
    #                         #if x[k,j,r].X>=0.1:
    #                         print("z("+str(i)+','+str(k)+','+str(j)+','+str(r)+")=", z[i,k,j,r].X)
    #                         list5.append(z[i,k,j,r].X)
    #                         part1.append(i)
    #                         part2.append(k)
    #                         machine.append(j)
    #                         day.append(r)
    #     print('-------------------------------------------------')
    #     print('Total Changeover:', np.sum(list5))
    #     print('Total Changeover Cost', tchc.x)  
    #     dfch = pd.DataFrame({'Part_i': part1, 'Part_k': part2, 'Machine': machine, 'Day': day})
    #     dfch['Part_i'].replace([i for i in range(1,i+1)], ['Tam1', 'Tam2', 'Tam3', 'Tam4', 'Tam5', 'Tam6', 'Tam7', 'Tam8', 'Tam9', 'Tam10',
    #                                                     'ÇT1', 'ÇT2','ÇT3', 'ÇT4', 'ÇT5', 'ÇT6', 'ÇT7', 'ÇT8', 'ÇT9', 'ÇT10', 'ÖKP', 'ÖK',
    #                                                     'AKP', 'AK', 'ÖPB1', 'ÖP1', 'ÖPB2', 'ÖP2', 'ÖPB3', 'ÖP3', 'ÖPB4','ÖP4',
    #                                                     'ÖPB5','ÖP5', 'ÖPB6','ÖP6', 'ÖPB7','ÖP7', 'ÖPB8','ÖP8', 'ÖPB9','ÖP9', 'ÖPB10','ÖP10','GÖ1', 'GÖ2',
    #                                                     'GÖ3', 'GÖ4', 'GÖ5', 'GÖ6', 'GÖ7', 'GÖ8', 'GÖ9', 'GÖ10', 'Ment'], inplace=True)
    #     dfch['Part_k'].replace([i for i in range(1,i+1)], ['Tam1', 'Tam2', 'Tam3', 'Tam4', 'Tam5', 'Tam6', 'Tam7', 'Tam8', 'Tam9', 'Tam10',
    #                                                     'ÇT1', 'ÇT2','ÇT3', 'ÇT4', 'ÇT5', 'ÇT6', 'ÇT7', 'ÇT8', 'ÇT9', 'ÇT10', 'ÖKP', 'ÖK',
    #                                                     'AKP', 'AK', 'ÖPB1', 'ÖP1', 'ÖPB2', 'ÖP2', 'ÖPB3', 'ÖP3', 'ÖPB4','ÖP4',
    #                                                     'ÖPB5','ÖP5', 'ÖPB6','ÖP6', 'ÖPB7','ÖP7', 'ÖPB8','ÖP8', 'ÖPB9','ÖP9', 'ÖPB10','ÖP10','GÖ1', 'GÖ2',
    #                                                     'GÖ3', 'GÖ4', 'GÖ5', 'GÖ6', 'GÖ7', 'GÖ8', 'GÖ9', 'GÖ10', 'Ment'], inplace=True)
    #     dfch['Machine'].replace([j for j in range(1,j+1)], ['Tam1', 'Tam2', 'Tam3', 'Tam4', 'TamAssm', 'PK', 'Ales', '800_ton', 'BK',
    #                                                                       'ÖP1', 'ÖP2', '1250_trans', 'GÖ1', 'GÖ2', 'GÖ3', 'GÖ4'], inplace=True)
    #     dfch['Day'].replace([1,2,3,4,5,6], ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'], inplace=True)
    #     #%%
        
    #     part = []
    #     day = []
    #     shift = []
    #     for i in I:
    #         for r in R:
    #             if v[i,r].X>=0.1:
    #                 print("v("+str(i)+','+str(r)+")=", v[i,r].X)
    #                 part.append(i)
    #                 day.append(r)
        
    #     dfv = pd.DataFrame({'Part': part, 'Day': day})
    #     dfv['Part'].replace([i for i in range(1,i+1)], ['Tam1', 'Tam2', 'Tam3', 'Tam4', 'Tam5', 'Tam6', 'Tam7', 'Tam8', 'Tam9', 'Tam10',
    #                                                     'ÇT1', 'ÇT2','ÇT3', 'ÇT4', 'ÇT5', 'ÇT6', 'ÇT7', 'ÇT8', 'ÇT9', 'ÇT10', 'ÖKP', 'ÖK',
    #                                                     'AKP', 'AK', 'ÖPB1', 'ÖP1', 'ÖPB2', 'ÖP2', 'ÖPB3', 'ÖP3', 'ÖPB4','ÖP4',
    #                                                     'ÖPB5','ÖP5', 'ÖPB6','ÖP6', 'ÖPB7','ÖP7', 'ÖPB8','ÖP8', 'ÖPB9','ÖP9', 'ÖPB10','ÖP10','GÖ1', 'GÖ2',
    #                                                     'GÖ3', 'GÖ4', 'GÖ5', 'GÖ6', 'GÖ7', 'GÖ8', 'GÖ9', 'GÖ10', 'Ment'], inplace=True)
    #     dfv['Day'].replace([1,2,3,4,5,6], ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'], inplace=True)
    #     #%%
        
        
    #     shift1 = np.zeros((len(J),len(R),len(S))).tolist()
    #     machine = []
    #     day = []
    #     shift = []
    #     list7 = []
    #     for j in J:
    #         for r in R:
    #             for s in S:
    #                 if a[j,r,s].X>=0.1:
    #                     print("a("+str(j)+','+str(r)+','+str(s)+")=", a[j,r,s].X)
    #                     shift1[j-1][r-1][s-1] = a[j,r,s].X
    #                     list7.append(a[j,r,s].X)
    #                     machine.append(j)
    #                     day.append(r)
    #                     shift.append(s)
                    
    #     print('-------------------------------------------------')
    #     print('Total Shifts:', np.sum(list7))
    #     print('Total Shift Cost', tshc.x) 
        
    #     dfsh = pd.DataFrame({'Machine':machine, 'Day': day, 'Shift': shift})
        
    #     dfsh['Machine'].replace([j for j in range(1,j+1)], ['Tam1', 'Tam2', 'Tam3', 'Tam4', 'TamAssm', 'PK', 'Ales', '800_ton', 'BK',
    #                                                                       'ÖP1', 'ÖP2', '1250_trans', 'GÖ1', 'GÖ2', 'GÖ3', 'GÖ4'], inplace=True)
    #     dfsh['Day'].replace([1,2,3,4,5,6], ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'], inplace=True)
        
    #     dfsh['Shift'].replace([1,2,3,4,5,6,7,8,9,10,11,12,13],
    #                         ['(08-20)-(20-08)','(08-20)-(24-08)','(08-16)-(24-08)','(08-16)-(20-08)','(08-16)-(16-24)',
    #                         '(08-18)-(20-08)', '(08-18)-(24-08)', '(08-16)', '(24-08)', '(08-20)', '(20-08)', '(16-24)', '(08-16)-(16-24)–(24-08)'], inplace=True)
        
    #     #%%
        
    #     list6 = []
    #     for i in I:
    #         for j in J:
    #             for r in R:
    #                 if q[0,i,j,r].x>=0.1:
    #                     if x[i,j,r].X>0.01:
    #                         print("q("+str(i)+','+str(j)+','+str(r)+")=", q[0,i,j,r].X)
    #                         list6.append(q[0,i,j,r].X)
    #     print('-------------------------------------------------')
    #     print('Total Carryover:', np.sum(list6))
    #     #%%
        
    #     machine = []
    #     day = []
    #     shift = []
    #     labor = []
    #     list8 = []
    #     for l in L:
    #         for j in J:
    #             for r in R:
    #                 for s in S:
    #                     for s1 in range(1,len(s11[s])+1):
    #                         if w[l,j,r,s,s1].X>=0.1:
    #                             print("w("+str(l)+','+str(j)+','+str(r)+','+str(s)+','+str(s1)+")=", w[l,j,r,s,s1].X)
    #                             list8.append(w[l,j,r,s,s1].X)
    #                             day.append(r)
    #                             shift.append(s)
    #                             machine.append(j)
    #                             labor.append(l)
                            
    #     print('-------------------------------------------------')
    #     print('Total worker assignment:', np.sum(list8))
        
    #     dfwc = pd.DataFrame({'Day': day, 'Shift': shift, 'Machine':machine, 'Labor': labor})
        
    #     dfwc['Machine'].replace([j for j in range(1,j+1)], ['Tam1', 'Tam2', 'Tam3', 'Tam4', 'TamAssm', 'PK', 'Ales', '800_ton', 'BK',
    #                                                                       'ÖP1', 'ÖP2', '1250_trans', 'GÖ1', 'GÖ2', 'GÖ3', 'GÖ4'], inplace=True)
    #     dfwc['Day'].replace([1,2,3,4,5,6], ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'], inplace=True)
        
    #     dfwc['Shift'].replace([1,2,3,4,5,6,7,8,9,10,11,12,13],
    #                         ['(08-20)-(20-08)','(08-20)-(24-08)','(08-16)-(24-08)','(08-16)-(20-08)','(08-16)-(16-24)',
    #                         '(08-18)-(20-08)', '(08-18)-(24-08)', '(08-16)', '(24-08)', '(08-20)', '(20-08)', '(16-24)', '(08-16)-(16-24)–(24-08)'], inplace=True)
        
    #     #%%
        
    #     for i in I:
    #         for j in J:
    #             for r in R:
    #                 if z[0,i,j,r].x>=0.1:
    #                     if x[i,j,r].X>0.01:
    #                         print("sttb("+str(i)+','+str(j)+','+str(r)+")=", round(stt[i,j,r].X))
    #     #%%
            
    #     for i in I:
    #         for j in J:
    #             for r in R:
    #                 if z[0,i,j,r].x>=0.1:
    #                     if x[i,j,r].X>0.01:
    #                         print("cttb("+str(i)+','+str(j)+','+str(r)+")=", round(ctt[i,j,r].X))
    #     #%%
        
    #     for k in I:
    #         for i in I:
    #             for j in J:
    #                 for r in R:
    #                     if z[i,k,j,r].X>=0.1:
    #                         if x[k,j,r].X>=0.1:
    #                             print("sttd("+str(k)+','+str(j)+','+str(r)+")=", round(stt[k,j,r].X))
    #     #%%
        
    #     for k in I:
    #         for i in I:
    #             for j in J:
    #                 for r in R:
    #                     if z[i,k,j,r].X>=0.1:
    #                         if x[k,j,r].X>=0.1:
    #                             print("cttd("+str(k)+','+str(j)+','+str(r)+")=", round(ctt[k,j,r].X))
        
    #     #%%
        
    #     # Production seqence
        
    #     order = []
    #     day = []
    #     machine = []
    #     start_finished = []
        
    #     for r in R:
    #         for j in J:
    #             for i in I:
    #                 if z[0,i,j,r].x>=0.01:
    #                     if x[i,j,r].X>0.01:
    #                         hourb = 8 + int((stt[i,j,r].X//60))
    #                         if hourb >= 24:
    #                             hourb -= 24
    #                         Startb_time = datetime.time(hourb,int(stt[i,j,r].X%60))
    #                         Startb_time_str = Startb_time.strftime('%H:%M')
    #                         duration = datetime.timedelta(minutes=ctt[i,j,r].X-stt[i,j,r].X)
    #                         finalb_time = (datetime.datetime.combine(datetime.date.today(), Startb_time) + duration).strftime('%H:%M')                    
    #                         start_finished.append(f"({Startb_time_str}-{finalb_time})")
    #                         order.append(f"{i} ({round(x[i,j,r].x)})")
    #                         day.append(r)
    #                         machine.append(j)
    #                         for k in I:
    #                             for i in I:
    #                                 if z[i,k,j,r].X>=0.01:
    #                                     if x[k,j,r].X>=0.01:
    #                                         hourd = 8 + int((stt[k,j,r].X//60))
    #                                         if hourd >= 24:
    #                                             hourd -= 24        
    #                                         Startd_time = datetime.time(hourd,int(stt[k,j,r].X%60))
    #                                         Startd_time_str = Startd_time.strftime('%H:%M')
    #                                         duration = datetime.timedelta(minutes=ctt[k,j,r].X-stt[k,j,r].X)
    #                                         finald_time = (datetime.datetime.combine(datetime.date.today(), Startd_time) + duration).strftime('%H:%M')                    
    #                                         start_finished.append(f" ({Startb_time_str}-{finalb_time}), ({Startd_time_str}-{finald_time})")
    #                                         order.append(f"{i} ({round(x[i,j,r].x)}), {k} ({round(x[k,j,r].x)})")
    #                                         day.append(r)
    #                                         machine.append(j)
    #                                         break
    #                                     else:
    #                                         continue
    #                                 else:
    #                                     continue
                            
    #     mapping = {
    #         1: 'Tam1', 2: 'Tam2', 3: 'Tam3', 4: 'Tam4', 5: 'Tam5', 6: 'Tam6', 7: 'Tam7', 8: 'Tam8', 9: 'Tam9', 10: 'Tam10',
    #         11: 'ÇT1', 12: 'ÇT2', 13: 'ÇT3', 14: 'ÇT4', 15: 'ÇT5', 16: 'ÇT6', 17: 'ÇT7', 18: 'ÇT8', 19: 'ÇT9', 20: 'ÇT10',
    #         21: 'ÖKP', 22: 'ÖK', 23: 'AKP', 24: 'AK', 25: 'ÖPB1', 26: 'ÖP1', 27: 'ÖPB2', 28: 'ÖP2', 29: 'ÖPB3', 30: 'ÖP3', 
    #         31: 'ÖPB4', 32: 'ÖP4', 33: 'ÖPB5', 34: 'ÖP5', 35: 'ÖPB6', 36: 'ÖP6', 37: 'ÖPB7', 38: 'ÖP7', 39: 'ÖPB8', 40: 'ÖP8',
    #         41: 'ÖPB9', 42: 'ÖP9', 43: 'ÖPB10', 44: 'ÖP10', 45: 'GÖ1', 46: 'GÖ2', 47: 'GÖ3', 48: 'GÖ4', 49: 'GÖ5', 50: 'GÖ6', 
    #         51: 'GÖ7', 52: 'GÖ8', 53: 'GÖ9', 54: 'GÖ10', 55: 'Ment'}
        
    #     pattern = r'\b(\d+)\s*\('
        
    #     for i, s in enumerate(order):
    #         order[i] = re.sub(pattern, lambda m: mapping[int(m.group(1))] + ' (', s)
                                    
                                    
    #     dfseq = pd.DataFrame({'Day': day, 'Machine': machine, 'Sequence (Quantity)': order, 'Start-Finish': start_finished})
    #     dfseq = dfseq.drop_duplicates(subset=['Day', 'Machine'], keep='last')
                                    
    #     dfseq['Day'].replace([1,2,3,4,5,6], ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi'], inplace=True)
    #     dfseq['Machine'].replace([j for j in range(1,j+1)], ['Tam1', 'Tam2', 'Tam3', 'Tam4', 'TamAssm', 'PK', 'Ales', '800_ton', 'BK',
    #                                                                         'ÖP1', 'ÖP2', '1250_trans', 'GÖ1', 'GÖ2', 'GÖ3', 'GÖ4'], inplace=True)                      
    # #%%
    
    #     dfsum = pd.DataFrame({'Total demand': [total_d], 'Total production':[np.sum(list1)],
    #                           'Total inventory':[np.sum(list2)], 'Total backlogging': [np.sum(list3)],
    #                           'Production cost': [np.sum(tpc.x)], 'Inventory cost': [np.sum(tic.x)], 'Backlogging cost': [np.sum(tbc.x)],
    #                           'Setup cost': [np.sum(tsc.x)], 'Changeover cost': [np.sum(tchc.x)], 'Shift cost': [np.sum(tshc.x)], 
    #                           'Worker cost': [np.sum(twc.x)], 'Objective':[mdl.ObjVal] , 'CPU':[end-start],'Gap':[mdl.MIPGap], 
    #                           '# of variables': [num_vars], '# of binary variables': [num_binary_vars], 
    #                           '# of continuous variables': [num_cont_vars], '# of constraints': [num_constraints]})
        
    #     with pd.ExcelWriter('C:/Amin/University/Ph.d/TUBITAK 2244/Project/Results_Model.xlsx') as writer:
    #         dfsum.to_excel(writer, sheet_name='General information', index=False)
    #         dfx.to_excel(writer, sheet_name='Production', index=False)
    #         dfIn.to_excel(writer, sheet_name='Inventory', index=False)
    #         dfb.to_excel(writer, sheet_name='Backlogging', index=False)
    #         dfs.to_excel(writer, sheet_name='Setup', index=False)
    #         dfch.to_excel(writer, sheet_name='Changeover', index=False)
    #         dfv.to_excel(writer, sheet_name='v', index=False)
    #         dfseq.to_excel(writer, sheet_name='Production Sequence', index=False)
    #         dfsh.to_excel(writer, sheet_name='Shift', index=False) 
    #         dfwc.to_excel(writer, sheet_name='Labor', index=False) 
    
    
    #%%
        
        objectives = []  
        OB1 = np.sum(tpc.x)
        OB2 = np.sum(tic.x)
        OB3 = np.sum(tbc.x)
        OB4 = np.sum(tsc.x) + np.sum(tchc.x)
        OB5 = np.sum(tshc.x)
        OB6 = np.sum(twc.x)
        OB7 = np.sum(titc.x)
        TOBV = mdl.ObjVal
        CPU = end-start 
        CPU_Algorithm = '-'
        Gap = mdl.MIPGap
        TVars = num_vars
        TBVars = num_binary_vars
        TCVars = num_cont_vars
        TCons = num_constraints
        
        
        objectives.append([OB1,OB2,OB3,OB4,OB5,OB6,OB7,TOBV,CPU,CPU_Algorithm,Gap,TVars,TBVars, TCVars, TCons]) 
        return(objectives)
     
  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

