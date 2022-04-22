#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 09:58:36 2022

@author: domingos
"""

import numpy as np
import pandas as pd

D_p = np.array([70, 128, 130, 67, 90, 136, 46, 87, 97, 138, 69, 90])
D_fp = np.array([443, 415, 433, 450, 500, 390, 380, 378, 392, 410, 464, 409])
E_p = np.array([4620, 8448, 8580, 4422, 5940, 8976, 3036, 5742, 6402, 9108, 4554, 5940])
E_fp = np.array([70880, 66400, 69280, 72000, 80000, 62400, 60800, 60480, 62720, 65600, 74240, 65440])
PI = 600 #POTÊNCIA INSTALADA
Dc = 500 #DEMANDA CONTRATADA


FD = max(np.concatenate((D_fp, D_p)))/PI #FATOR DE DEMANDA
Dm_p = sum(D_p)/12 #DEMANDA MÉDIA PONTA
Dm_fp = sum(D_fp)/12 #DEMANDA MÉDIA FORA PONTA


def demanda_multa(Dm, Ti):
    fatura = (Dm*Ti) + 2*((Dc - Dm)*Ti)
    return fatura

def demanda_consumo(Dm, Ti, Tsi):
    fatura = (Dm*Ti) + (Dc - Dm)*Tsi
    return fatura

def demanda_tolerada(Dm, Ti):
    fatura = (Dm*Ti)
    return fatura


def HSV():
    
    #TARIFAS:
    TDi = 25.4 #TARIFA DE DEMANDA COM IMPOSTO
    TDsi = 17.07 #TARIFA DE DEMANDA SEM IMPOSTO
    TE_p = 2.08 #TARIFA DE ENERGIA PONTA
    TE_fp = 0.533 #TARIFA DE ENERGIA FORA PONTA

    #FATURA DE DEMANDA PONTA
    fatura_Dp = np.array([])
    for i in D_p:
        if i < Dc:
            fatura_Dp = np.append(fatura_Dp, demanda_consumo(i, TDi, TDsi))

        elif i > (Dc*1.05):
            fatura_Dp = np.append(fatura_Dp, demanda_multa(i, TDi))

        elif Dc <= i < (Dc*1.05):
            fatura_Dp = np.append(fatura_Dp, demanda_tolerada(i, TDi))


    #FATURA DE DEMANDA FORA PONTA
    fatura_Dfp = np.array([])
    for i in D_fp:
        if i < Dc:
            fatura_Dfp = np.append(fatura_Dfp, demanda_consumo(i, TDi, TDsi))

        elif i > (Dc*1.05):
            fatura_Dfp = np.append(fatura_Dfp, demanda_multa(i, TDi))

        elif Dc <= i < (Dc*1.05):
            fatura_Dfp = np.append(fatura_Dfp, demanda_tolerada(i, TDi))


    #FATURA DE ENERGIA PONTA
    fatura_Ep = np.array([])
    for i in E_p:
        fatura_Ep = np.append(fatura_Ep, i*TE_p)


    #FATURA DE ENERGIA FORA PONTA
    fatura_Efp = np.array([])
    for i in E_fp:
        fatura_Efp = np.append(fatura_Efp, i*TE_fp)


    df = pd.DataFrame({'Fatura D_p': fatura_Dp,
                      'Fatura D_fp': fatura_Dfp,
                      'Fatura E_p': fatura_Ep,
                      'Fatura E_fp': fatura_Efp},
                      index = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'])

    df['TOTAL_MES'] = df.sum(axis=1)

    df_mes = pd.DataFrame({'Fatura D_p': [df['Fatura D_p'].sum()],
                      'Fatura D_fp': [df['Fatura D_fp'].sum()],
                      'Fatura E_p': [df['Fatura E_p'].sum()],
                      'Fatura E_fp': [df['Fatura E_fp'].sum()],
                      'TOTAL_MES': [df['TOTAL_MES'].sum()]})

    df = pd.concat([df, df_mes], axis=0)
    df.rename(index={0: 'TOTAL_ANO'}, inplace=True)

    return df


def HSA():
    
    #TARIFAS:
    TDfp_i = 25.4 #TARIFA DE DEMANDA FORA PONTA COM IMPOSTO
    TDfp_si = 17.07 #TARIFA DE DEMANDA FORA PONTA SEM IMPOSTO
    TDp_i = 53.69 #TARIFA DE DEMANDA PONTA COM IMPOSTO
    TDp_si = 39.08 #TARIFA DE DEMANDA PONTA SEM IMPOSTO
    TE_p = 0.775 #TARIFA DE ENERGIA PONTA
    TE_fp = 0.533 #TARIFA DE ENERGIA FORA PONTA

    #FATURA DE DEMANDA PONTA
    fatura_Dp = np.array([])
    for i in D_p:
        if i < Dc:
            fatura_Dp = np.append(fatura_Dp, demanda_consumo(i, TDp_i, TDp_si))

        elif i > (Dc*1.05):
            fatura_Dp = np.append(fatura_Dp, demanda_multa(i, TDp_i))

        elif Dc <= i < (Dc*1.05):
            fatura_Dp = np.append(fatura_Dp, demanda_tolerada(i, TDp_si))


    #FATURA DE DEMANDA FORA PONTA
    fatura_Dfp = np.array([])
    for i in D_fp:
        if i < Dc:
            fatura_Dfp = np.append(fatura_Dfp, demanda_consumo(i, TDfp_i, TDfp_si))

        elif i > (Dc*1.05):
            fatura_Dfp = np.append(fatura_Dfp, demanda_multa(i, TDfp_i))

        elif Dc <= i < (Dc*1.05):
            fatura_Dfp = np.append(fatura_Dfp, demanda_tolerada(i, TDfp_i))


    #FATURA DE ENERGIA PONTA
    fatura_Ep = np.array([])
    for i in E_p:
        fatura_Ep = np.append(fatura_Ep, i*TE_p)


    #FATURA DE ENERGIA FORA PONTA
    fatura_Efp = np.array([])
    for i in E_fp:
        fatura_Efp = np.append(fatura_Efp, i*TE_fp)


    df = pd.DataFrame({'Fatura D_p': fatura_Dp,
                      'Fatura D_fp': fatura_Dfp,
                      'Fatura E_p': fatura_Ep,
                      'Fatura E_fp': fatura_Efp},
                      index = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'])

    df['TOTAL_MES'] = df.sum(axis=1)

    df_mes = pd.DataFrame({'Fatura D_p': [df['Fatura D_p'].sum()],
                      'Fatura D_fp': [df['Fatura D_fp'].sum()],
                      'Fatura E_p': [df['Fatura E_p'].sum()],
                      'Fatura E_fp': [df['Fatura E_fp'].sum()],
                      'TOTAL_MES': [df['TOTAL_MES'].sum()]})

    df = pd.concat([df, df_mes], axis=0)
    df.rename(index={0: 'TOTAL_ANO'}, inplace=True)

    return df


verde = HSV()

azul = HSA()
