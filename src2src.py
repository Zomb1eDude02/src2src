import os, os.path, glob, requests, json
from os import path
from guietta import Gui, _, G, ___, QPlainTextEdit, QFileDialog, QCheckBox

def append(output): # too lazy to write this out everytime, setting it as a variable didn't work?
    console.QPlainTextEdit.appendPlainText(output)

if os.name != "nt":
    print("This script requires that you run it on windows.")
else:
    gui = Gui( [ 'Content Directory:',      '__dir__',    ['Browse']  ],
               [ QCheckBox('convert mdls directly'), ___, ['Convert'] ],
               [ G('output'),           ___,                   ___    ] )
    
    console = Gui( [ QPlainTextEdit, ___, ___] )
    
    gui.output = console # defines content for group
    
    # ---- folder gui ---- #
    with gui.Browse:
        if gui.is_running:
            folderpath = QFileDialog.getExistingDirectory()
            gui.dir = folderpath

    # ---- Read content directory from input, then list found mdl files. ---- #
    with gui.Convert:
        if gui.is_running:
            mdlpaths = glob.glob(gui.dir + '/**/*.mdl', recursive=True)
            if str(gui.convertmdlsdirectly.checkState()) == 'PySide2.QtCore.Qt.CheckState.Unchecked':
                for mdl in mdlpaths:
                        append('Decompiling ' + mdl)
                        os.system('data\crowbarcmd\crowbarcmd.exe -p "' + mdl + '"')
                append('Decompilation complete (or errored)')
            else:
                append('todo')

    console.QPlainTextEdit.setReadOnly(True) # Make output readonly

    # ---- Check for required utilities, if not found download them. ---- #
    utils = open('data/utils.json')
    utilsdata = json.load(utils)
    for utilpath, utillink in utilsdata.items():
        if path.exists(utilpath) == False:
            append(str(utilpath) + 'not found! Downloading...')
            open(str(utilpath), 'wb').write(requests.get(utillink, allow_redirects=True).content)
        elif path.exists(utilpath) == True:
            append('Found ' + str(utilpath) + '! Skipping Download')
    utils.close()   

    gui.run() # runs gui