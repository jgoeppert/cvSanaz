#!/bin/python3

import pandas as pd
import os
import codecs 
import shutil
import numpy as np
from PyPDF2 import PdfWriter, PdfReader
# import ntpath
# ntpath.realpath = ntpath.abspath
# import sys
import argparse

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


gauth = GoogleAuth()           
drive = GoogleDrive(gauth)  

# print(f"Name of the script      : {sys.argv[0]=}")
# print(f"Arguments of the script : {sys.argv[1:]=}")

argParser = argparse.ArgumentParser()
argParser.add_argument("-s", "--start",   default=1 , type=int,  help="number of applications to generate")
argParser.add_argument("-e", "--employer",default='', type=str,  help="employer to be generated")
argParser.add_argument("-p", "--skipPdf" ,default=False, type=bool,  help="employer to be generated")

args = argParser.parse_args()
print(args)
# if args.start       != 'None' : start=int(args.start)
# if args.employer    != 'None' : buildEmployer=args.employer

# quit()

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ-JxpwsP1t5ceEK4esRpF32rTx1J5ztuvQvcmxEzMEAXzuYuODILMYWIbjiPvhErubapziUV4XbNxH/pub?gid=0&single=true&output=csv'
print(url)
# df = pd.read_excel(r'./Sanaz Bewerbungen.xlsx',dtype=str)
# df = pd.read_csv(r,dtype=str)
df = pd.read_csv(url,dtype=str)
# df = pd.read_csv(r'./SanazBewerbungen.csv')
# df = pd.read_csv('SanazBewerbungen.csv',sep='|')
df = df.fillna('')
# df = df.replace('&','\\&')
# df = df.replace('%','3')



fields=[
    'lfd.Nr',
    'firma',
    'firmaSatz',
    'land',
    'ortschaft',
    'strasse',
    'geschlecht',
    'titel',
    'name',
    'vorname',
    'typ',
    'gehalt',
    'eintritt',
    'stelleText',
    'stelleHead',
    'artikelFirma',
    'textEnde',
]

def genStelleText(field,bewerbung):
    file = codecs.open(r"sections/stelleNow.tex", "w","utf-8")
    for field in fields[1:]:
        # print(bewerbung[field.index(field)])
        # print(bewerbung[field])
        val = str(bewerbung[field])
        val = replaceStringChars(val)
        print("%20s: %s", (field,val))
        writeString = '\def\\' + field + '{%s}\n' % val
        # if val == nan: val = ''
        file.write(writeString)
    # input('waiting')
    file.close()


def makePDF():
    osStr = str(os.name)
    osSuf = {'posix': '', 'nt': '.exe'}
    texString = 'pdflatex%s Z_main.tex' % osSuf[osStr]
    # texString = 'pdflatex.exe -jobname=%s -output-dir=outputs .\Z_main.tex' % bewerbung['firma'].replace(' ', '_')
    print(texString)
    os.system(texString)


def replacePathChars(strIn):
    tmp = strIn.replace(':','-')
    tmp = tmp.replace(' ','_')
    tmp = tmp.replace('/','')
    tmp = tmp.replace('*','')
    tmp = tmp.replace('%','')
    tmp = tmp.replace(',','')
    tmp = tmp.replace('.','')
    tmp = tmp.replace('(','')
    tmp = tmp.replace(')','')
    tmp = tmp.replace('\n','')
    tmp = tmp.replace('#','\#')
    return tmp

def replaceStringChars(strIn):
    tmp = strIn.replace(':','-')
    # tmp = tmp.replace(' ','_')
    # tmp = tmp.replace('/','')
    # tmp = tmp.replace('*','')
    # tmp = tmp.replace('%','')
    # tmp = tmp.replace(',','')
    # tmp = tmp.replace('.','')
    # tmp = tmp.replace('(','')
    # tmp = tmp.replace(')','')
    # tmp = tmp.replace('\n','')
    tmp = tmp.replace('%','\\%')
    tmp = tmp.replace('&','\\&')
    tmp = tmp.replace('_','\\_')
    tmp = tmp.replace('#','\#')
    return tmp


def processPDF(bewerbung):
    # input(bewerbung['firma'])
    name = 'Sanaz_Goeppert_Asadollahpour'
    bewPath = '%03d_%s_%s' % (int(bewerbung[fields[0]]), bewerbung['firma'], bewerbung['stelleText'][:9])
    bewPath = replacePathChars(bewPath)
    # bewName = replacePathChars('%s_%s' % (bewerbung['firma'],bewerbung['stelle Original']))
    # print(bewName)
    # target = os.path.join(os.getcwd(), 'outputs', bewName)#[:82])
    target = os.path.join('outputs', bewPath)#[:82])
    tPath = target
    shutil.rmtree(target, ignore_errors=True)
    os.mkdir(target)
    target=os.path.join(target, name)
    # extender = '\\\\?'
    # targetF=os.path.join(target,bewName)
    targetF=target + '_Bewerbung.pdf'
    # source = os.path.join(os.getcwd(), 'Z_main.pdf')
    source = 'Z_main.pdf'
    # input(target)
    print(targetF)
    shutil.copyfile(source,targetF)
    pdfReader = PdfReader(open(targetF, "rb"))
    pdfWriter = PdfWriter()
    # fName = os.path.join(target,'Anschreiben_' + bewName + '.pdf')
    fName = target + '_Anschreiben.pdf'
    for page in range(0,1) : pdfWriter.add_page(pdfReader.pages[page])
    with open(fName,'wb') as f: pdfWriter.write(f) 
    pdfWriter = PdfWriter()
    # fName = os.path.join(target,'Lebenslauf_' + bewName + '.pdf')
    fName = target + '_Lebenslauf.pdf'
    for page in range(1,3) : pdfWriter.add_page(pdfReader.pages[page])
    with open(fName,'wb') as f: pdfWriter.write(f) 
    # pdfReader.close()
    # input(target)
    # upload_file_list = [tPath]
    # for upload_file in upload_file_list:
    #     gfile = drive.CreateFile({'parents': [{'id': '1gNfkaIkhgM8SZYAITeFmCzAEq_o3QjVM'}]})
    #     # Read file and set it as the content of this instance.
    #     gfile.SetContentFile(upload_file)
    #     gfile.Upload() # Upload the file.



start=2
# print("sys: %s" % sys.argv)
# if len(sys.argv) > 1 : start=int(sys.argv[1])
if args.start       != 'None' : start=int(args.start)
if args.employer    != 'None' : buildEmployer=args.employer

# print(start)
# quit()

for idx,bewerbung in df.iloc[-args.start:].iterrows():
    print(idx)
    if args.employer not in bewerbung['firma'] : continue 
    genStelleText(fields,bewerbung)
    # quit()
    if not args.skipPdf : makePDF()
    processPDF(bewerbung)


# for bewerbung in df.iterrows():
#     print(bewerbung)
#     print('-----------------------------------------------------------------')
#     bew = bewerbung
