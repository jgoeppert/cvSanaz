import pandas as pd
import os
import codecs 
import shutil

df = pd.read_excel(r'./Sanaz Bewerbungen.xlsx')
# df = pd.read_csv(r'./SanazBewerbungen.csv')
# df = pd.read_csv('SanazBewerbungen.csv',sep='|')
df = df.fillna('')
# df = df.replace('&','\\&')
# df = df.replace('%','3')


fields=[
    'firma',
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
]


for idx,bewerbung in df.iterrows():
    file = codecs.open(r"sections/stelleNow.tex", "w","utf-8")
    for field in fields:
        # print(bewerbung[field.index(field)])
        # print(bewerbung[field])
        val = str(bewerbung[field])
        val = val.replace('%','\\%')
        val = val.replace('&','\\&')
        writeString = '\def\\' + field + '{%s}\n' % val
        # if val == nan: val = ''
        file.write(writeString)
    # input('waiting')
    file.close()
    # input('after file')
    texString = 'pdflatex.exe .\Z_main.tex'
    # texString = 'pdflatex.exe -jobname=%s -output-dir=outputs .\Z_main.tex' % bewerbung['firma'].replace(' ', '_')
    print(texString)
    os.system(texString)
    name = 'Sanaz_Goeppert_Asadollahpour'
    target = os.path.join(os.getcwd(), 'outputs', '%s_%s_%s.pdf' % (name,bewerbung['firma'],bewerbung['stelleHead']) )
    # target = target.replace(' ', '_')
    # target = target.decode('utf-8','ignore').encode("utf-8")
    # target = target.replace(' ', '_').replace('/','').replace('*','').replace('%','')
    target = target.replace(' ','_')
    target = target.replace('/','')
    target = target.replace('*','')
    target = target.replace('%','')
    target = target.replace(',','')
    source = os.path.join(os.getcwd(), 'Z_main.pdf')
    # input(target)
    shutil.copy2(source,target)
    # input(target)

# for bewerbung in df.iterrows():
#     print(bewerbung)
#     print('-----------------------------------------------------------------')
#     bew = bewerbung