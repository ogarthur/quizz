# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 19:33:24 2019

@author: potato
"""

import io, re,os

question = 0;
file_path = "C-BLOQUE2(1,2,3).txt"
regpregunta= "\d"
reganswerwrong = "*"
reganswerright="-"
file = io.open(file_path,  encoding="utf-8")
file_d = dict(enumerate(file))
file = io.open(file_path, newline='', encoding="ISO-8859-1")
file2 = io.open("C-BLOQUE2(1,2,3).csv", 'w',newline='', encoding="ISO-8859-1")
file2.write("{},{},{},{}".format("BLOQUE2","TEMAS1-2-3","","0"))
file2.write("\n")
pregunta =""
for key, line in enumerate(file):
    if key>100:
        break

    if line[0] is "*":
        #file2.write("{},1,".format(line[4:]))
         pregunta+='"{}","1",'.format(line[4:])
         print("correctanswer",line[4:])
    elif line[0] is "-":
       # file2.write("{},0,".format(line[4:]))
        pregunta+='"{}","0",'.format(line[4:])
        print("wrong",line[4:])
    elif re.search(r'\d+.',line[:3]):
        delete=re.search(r'\d+.',line)
        result = re.sub(r'\d+.', "", line)  
        #file2.write("{},".format(result[1:]))
        pregunta+='"{}",'.format(result[1:])
        print("pregunta", result )
    else:
        print(".......",pregunta.replace('\n', '').replace('\r', ''))
        file2.write(pregunta.replace('\n', '').replace('\r', ''))
        file2.write("\n")
        pregunta = ''
        print("white",line[:6])
        
        ['(GSI PI  ¿De qué orden de complejidad es la búsqueda dicotómica en una tabla ordenada? ', ',Logarítmica. ', ',1,Lineal. ', ',0,Exponencial. ', ',0,Cuadrática.', ',0,']
        """
for line in file:
    if(len(line)>3):
        if "." in line[:4] and ")" not in line[:1]:
            print("===>{}".format(line))
            file2.write("\n")
            pregunta = line
            file2.write(pregunta)
            question += 1
        elif line[1] == ")":
            #print(answers[question].lower(),line[0])
            print(question)
            print(line)
            if line[0] == answers[question].lower():
                file2.write("*{}".format(line))
 
            else:
                file2.write("-{}".format(line))
       """
file2.close()