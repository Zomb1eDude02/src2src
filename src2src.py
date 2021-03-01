import sys, os, os.path, glob, requests, json, zipfile
from os import path
from guietta import Gui, _, ___, QFileDialog, QCheckBox

sys.path.append('data/source2utils/') # allow importing from data dir

if os.name != "nt":
    print("This script requires that you run it on windows.")
else:
    gui = Gui( [ 'Content Directory:',      '__dir__',    ['Browse']  ],
               [ QCheckBox('outside hlvr_addons folder'), QCheckBox('decompile models'), QCheckBox('no compile') ],
               [ ['Convert'],           ___,                   ___    ] )
    
    # ---- folder gui ---- #
    with gui.Browse:
        if gui.is_running:
            folderpath = QFileDialog.getExistingDirectory()
            gui.dir = folderpath

    with gui.Convert:
        if gui.is_running:
            contentpath = gui.dir # avoid issues if someone decides to change the path during this process
            mdlpaths = glob.glob(contentpath + '/**/*.mdl', recursive=True) # store mdl locations in list
            print('converting VTFs to TGAs...')
            os.system('data\\vtflib\\bin\\x64\\VTFCmd.exe -folder "' + contentpath + '\\materials\\*.vtf" -recurse -exportformat tga') # recursively convert vtf files to tga files
            print('VTF to TGA converion complete')
            print('converting VMTs to VMATs...')
            vmt_to_vmat(contentpath + '\\materials\\') # run the vmt files through source2utils
            print('VMT to VMAT conversion complete')
            if str(gui.decompilemodels.checkState()) == 'PySide2.QtCore.Qt.CheckState.Checked': # check if models should be decompiled first or just straight converted
                print('Beginning decompilation and qc to vmdl conversion, this may take a while')
                for mdl in mdlpaths:
                        print('Decompiling ' + mdl)
                        os.system('data\\crowbarcmd\\crowbarcmd.exe -p "' + mdl + '"') # decompile all found mdl files
                print('Decompilation complete (or errored)')
                print('Converting qc files...')
                qc_to_vmdl(contentpath) # run qc files through source2utils for conversion
                print('qc to vmdl conversion complete')
            else:
                print('Beginning mdl to vmdl conversion, this may take a while')
                mdl_to_vmdl(contentpath) # run mdl files through source2utils for direct conversion
                print('mdl to vmdl conversion complete')
            if str(gui.nocompile.checkState()) == 'PySide2.QtCore.Qt.CheckState.Unchecked': # check if content should be compiled or not
                print('Beginning compilation')
                if str(gui.outsidehlvr_addonsfolder.checkState()) == 'PySide2.QtCore.Qt.CheckState.Checked': # check if content is outside of the hlvr_addons directory
                    resourcecompiler = '"' + contentpath + '\\..\\..\\game\\bin\\win64\\resourcecompiler.exe" -i "' + contentpath + '\\*" -game hlvr -r -nop4 -v -f'
                else:
                    resourcecompiler = '"' + contentpath + '\\..\\..\\..\\game\\bin\\win64\\resourcecompiler.exe" -i "' + contentpath + '\\*" -game hlvr -r -nop4 -v -f'
                os.system('"' + resourcecompiler + '"') # compile all content
                print('Compilation complete!')

    # ---- Check for required utilities, if not found download them. ---- #
    utils = open('data/utils.json')
    utilsdata = json.load(utils)
    for utilpath, utillink in utilsdata.items():
        if path.exists(utilpath) == False:
            print(str(utilpath) + 'not found! Downloading...')
            open(str(utilpath), 'wb').write(requests.get(utillink, allow_redirects=True).content)
        elif path.exists(utilpath) == True:
            print('Found ' + str(utilpath) + '! Skipping Download')
    if path.exists('data/vtflib/bin/x64/GPL.txt') == False:
            with zipfile.ZipFile('data/vtflib/vtflib.zip', 'r') as vtflib_zip:
                vtflib_zip.extractall('data/vtflib/')
    from mdl_to_vmdl import mdl_to_vmdl # import modified source2utils
    from qc_to_vmdl import qc_to_vmdl # import modified source2utils
    from vmt_to_vmat import vmt_to_vmat # import modified source2utils
    utils.close()

    gui.run() # runs gui