from lineasAbsorcion import linea



def Harvard(valleysarray):

    """
    Harvard
    =======
    Esta función clasifica la estrella en función de las líneas de absorción en su espectrograma normalizado

    Parameters
    ==========
    -valleysarray: array con los mínimos del espectrograma

    """

    #Llamadas a las posibles líneas 
    hg, hGIntensity = linea(valleysarray,'Balmer')
    fhK,kIntensity = linea(valleysarray,'FraunhoferK')
    fhH, hIntensity = linea(valleysarray,'FraunhoferH')
    gb, gBandIntensity = linea(valleysarray,'GBand')
    mn, mnIntensity = linea(valleysarray,'ManganMn')
    tiO, tiOIntensity = linea(valleysarray,'Titanoxide')
    feI, feIntensity = linea(valleysarray,'FeI')

    if fhK and hg:
        coef1 = kIntensity/hGIntensity
    if fhK and fhH:
        coef2 = kIntensity/hIntensity
    if feI and hg:
        coef3 = feIntensity/hGIntensity
    if gb and tiO:
        coef4 = gBandIntensity/tiOIntensity


    # Bucle que asigna un tipo a una estrella un función de las líneas y sus intensidades.

    if fhK and fhH:
        if hg:
            if kIntensity/hGIntensity < 0.6:
                print("Stellar class is A0-A5")
            elif 0.6 < kIntensity/hGIntensity < 1.22:
                print("Stellar class is A5 - A9")
            elif kIntensity/hGIntensity > 1.22:
                if feI:
                    if feIntensity/hGIntensity < 0.64:
                        if gb:
                            print("Stellar class is F3-F9")
                        else:
                            print("Stellar class is F0-F3") 
                    elif 0.64 < feIntensity/hGIntensity < 1.05:
                        print("Stellar class is G0-G4")
                    else:
                        if mn and mnIntensity >0.21 and kIntensity<0.862:
                            if tiO and tiOIntensity>0.45:
                                if gBandIntensity/tiOIntensity > 1:
                                    print("Stellar class is K3-K9")
                                if gBandIntensity/tiOIntensity < 1:
                                    print("Stellar class is M")
                            else:
                                print("Stellar class is K0-K2")
                        else:
                            print("Stellar class is G5-G9")
                else:
                    if kIntensity/hGIntensity <2:
                        if gb and gBandIntensity >0.28:
                            print("Stellar class is F3-F9")
                        else:
                            print("Stellar class is F0-F3")
                    elif kIntensity/hGIntensity >2:
                        print("Stellar class is G")
        else:
            if tiO:    
                if gBandIntensity/tiOIntensity > 1:
                    print("Stellar class is later K")
                elif gb == False or gBandIntensity/tiOIntensity < 1:
                    print("Stellar type is M")
            else:
                print("STellar class is K0-K3")
    elif fhK and fhH == False or fhH and fhK == False:
        print("Stellar class is M")
    else:
        if hg:
            print("Stellar class is B")
        else:
            print("Stellar class is O")        


    return
