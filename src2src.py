import os, os.path, glob, requests, zipfile
from os import path
from guietta import Gui, _, G, ___, QPlainTextEdit

def dl(url):
    return requests.get(url, allow_redirects=True).content

def append(output):
    console.QPlainTextEdit.appendPlainText(output)

if os.name != "nt":
    print("This script requires that you run it on windows.")
else:
    if path.exists('utils/source2utils/qc_to_vmdl.py') == False:
        open('utils/crowbarcmd/crowbarcmd.exe', 'wb').write(dl('https://github.com/UltraTechX/Crowbar-Command-Line/releases/download/0.68-v1/CrowbarCommandLineDecomp.exe'))
        
    gui = Gui( [ 'Content Directory:',  '__dir__',    ['Convert'] ],
               [ G('output'),           ___,                   ___] )
    
    console = Gui( [ QPlainTextEdit, ___, ___] )
    
    gui.output = console
    
    with gui.Convert:
        if gui.is_running:
            mdlpaths = glob.glob(gui.dir + '/**/*.mdl', recursive=True)
            for mdl in mdlpaths:
                append(mdl)
        
    console.QPlainTextEdit.setReadOnly(True)
    
    gui.run()