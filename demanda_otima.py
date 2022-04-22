#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 20:49:03 2022

@author: domingos
"""

import numpy as np

Dc = np.linspace(100, 300, num = 21)
tarifa = 22.5
Dm = np.array([189, 165, 205, 180, 220, 150, 135, 190, 177, 195, 208, 243])
fat_min = 1000000000

def multa(Dm):
    fatura = (Dm*tarifa)/0.65 + 2*((Dc - Dm)*tarifa/0.65)
    return fatura

def consumo(Dm):
    fatura = (Dm*tarifa)/0.65 + (Dc - Dm)*tarifa 
    return fatura

def medio(Dm):
    fatura = (Dm*tarifa)/0.65
    return fatura


for n in Dc:
    fatura = np.array([])
    for i in Dm:
        if i < n:
            fatura = np.append(fatura, consumo(i))
            
        elif i > (n*1.05):
            fatura = np.append(fatura, multa(i))
        
        elif n < i < (n*1.05):
            fatura = np.append(fatura, medio(i))

    fat_anual = sum(fatura)
        
    if fat_anual < fat_min:
        fat_min = fat_anual
        D_otima = n
        

print("A demanda ótima é: ", D_otima)

