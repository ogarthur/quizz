# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 00:17:00 2019

@author: potato
"""
import io, re

class test_extractor:
    
    def __init__(self):
        self.x = 'Hello'
    
    def test_answers(self,file_path):
        file_path2 = "{}-test.csv".format(file_path[:-4])
        
        file = io.open(file_path,  encoding="ISO-8859-1")
        file2 = io.open(file_path2,  "a", encoding="ISO-8859-1")
        answer_key = {}
        for line in file:
            sol = line.split(".-")
         
            answer_key[sol[0]] = sol[1][0].lower()
        print(answer_key)
        return(answer_key)
        
    
    def test_general(self,file_path,answer_path):
        answer_key = self.test_answers(answer_path)
        print(answer_key)
        file_path2 = "{}-test.csv".format(file_path[:-4])
        
        file = io.open(file_path,  encoding="ISO-8859-1")
        file_d = dict(enumerate(file))
        file = io.open(file_path,  encoding="ISO-8859-1")
    
        file2 = io.open(file_path2,  "a", encoding="ISO-8859-1")
        
        question = True
        last = False
        cont = 0
        val = 0
        print("START")
        
        for key, line in enumerate(file):
            
            if key+2<len(file_d):
                if file_d[key+1][0:6]=="Página":
                    if re.search(r'\d-',file_d[key+2][:4]):
                        check=key+3
                    else:
                        check=key+2
                else:
                    check=key+1
            if line[0] == " " or line[0:6]=="Página" or re.search(r'\d-',line[:4]):
                print("======================================")
                continue
            
            elif re.search(r'\d+.-',line[:6]) and not re.search(r'\w\)',line[:2]):
                last = False
                print(line[:6],"=>NEW QUESTION,JUMP OF LINE")
                cont+=1
                file2.write("\n")
            
                pregunta = '"{}'.format(line.split(".-")[1])
                #Comprobar si la siguiente linea forma parte 
                if re.search(r'\w\)', file_d[check][:3]) : 
                    print("there is not question continuation")
                    pregunta = '{}",'.format(pregunta)
                file2.write( pregunta )
                continue
            
            elif re.search(r'\w\)', line[:4]) : 
                question = False    
                if line[0]==answer_key[str(cont)]:
                    val = 1
                else:
                    val = 0
                respuesta = '"{}'.format(line)       
                last_answer = True if re.search(r'\d+.-',file_d[check][:6]) else False
                if last_answer:  
                    last = True
                    print("IS LAST CHOICE")
                if re.search(r'\w\)', file_d[check][:3]) or re.search(r'\d+.-', file_d[check]) or key+2==len(file_d):
                    print("there is not answer continuation")
                    respuesta  = '{}","{}",'.format(respuesta,val)
                    if last:
                        question = True  
                file2.write( respuesta )      
                print(line[:6],"ES RESPUESTA",last)
                continue
            else:
                texto = ' {}'.format(line)
                
                if re.search(r'\w\)', file_d[check][:3]) or re.search(r'\d+.-', file_d[check]) or key+2==len(file_d) :
                           
                    print("no more continuation")
                    if not question:
                        texto = '{}","{}",'.format(texto,val)
                        last_answer = True if re.search(r'\d+.-',file_d[check][:6]) else False
                        if last_answer:  
                            last = True
                            print("IS LAST CHOICE")
                    else:
                        texto = '{}",'.format(texto)
                    if last:
                        print("IS LAST CHOICE")
                        question = True
                file2.write( texto )
                            
                continue
            
        
        file2.close()
        
        '''
        match = re.search(r'\d+.-', line)
        if match:
            print('found', match.group()) ## 'found word:cat'
        else:
            print('did not find')
        '''
if __name__ == '__main__':
    test_extractor().test_answers("answers.txt")
    test_extractor().test_general("testfile3.txt","answers.txt")