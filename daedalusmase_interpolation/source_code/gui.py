import sys
import glob
from ipywidgets import *
import ipywidgets as widgets
import interpolationmase_mainfunc as inter
# window creation
def loadgui(filepath,orbitpath):
    '''
    This function used create GUI to interact with daedalusmase_errorPropagation module
    Args:
        filepath (String): directory of TIE-GCM files
        orbitpath (String): directory of orbit files
    
    '''
   
    layout1 = {'width':'850px'}
    style1 = {'description_width':'150px'}
    
    tiegcm_file=widgets.Dropdown(options=sorted(glob.glob(filepath)), description='TIE-GCM files: ', style=style1, layout=layout1)

    orbit_file=widgets.Dropdown(options=sorted(glob.glob(orbitpath)), description='Orbit files: ', style=style1, layout=layout1)
    global linearInter,TricubicInter,saveOption
    saveOption= widgets.Checkbox(value=False,  description="Save Output",style=style1, layout=layout1)
    # linearInter= widgets.Checkbox(value=True,  description="Linear Interpolation",style=style1, layout=layout1)
    # TricubicInter= widgets.Checkbox(value=True,  description="Tricubic Interpolation",style=style1, layout=layout1)
    InterScheme=widgets.Dropdown(
            options=['Trilinear','Tricubic','IDW'],
            value='Trilinear',
            description='Interpolation Scheme:',
            disabled=False,
            style=style1, 
            layout=layout1
            )
    TGvar=widgets.Dropdown(
            options=['All','XNMBAR','TI','TN','OP','DEN','HALL','HE','PEDERSEN','POTEN','TE',
                    'O2_CM3', 'EEX', 'EEY', 'EEZ', 'ELECDEN', 'N2_CM3', 'NOP_LAM', 'NPLUS', '02P', 'O_CM3'
                    'UN', 'VN', 'WN_lev', 'HALL', 'N2D', 'N4S', 'NO', 'Ui_lev', 'Vi_lev', 'WI_LEV','ZGMID'],
            value='TN',
            description='TIEGCM Variable:',
            disabled=False,
            style=style1, 
            layout=layout1
            )
    def Exec_Btn_Clicked( b ):
        
        print( "Interpolation started..." )
        inter.runinterpolator(tiegcm_file.value,orbit_file.value,tgvar=TGvar.value,interpolation=InterScheme.value,Save=saveOption.value,outfilename="InterResults.nc")
        
        
  

    def createGUI():
        MainPanel = widgets.VBox() 
        MainTab = widgets.Tab() 
        VerticalPanel = widgets.VBox()
        InterpolationPanel=widgets.HBox()
        MainTab.children = [ VerticalPanel ]
        MainTab.set_title(0, 'Interpolator')
        MainPanel.children = [MainTab ]
        Exec_Btn = widgets.Button (description='Run',tooltip="Click here to Interpolate",)
        Exec_Btn.style.button_color = 'Red'
        Exec_Btn.on_click( Exec_Btn_Clicked )
        VerticalPanel.children = [tiegcm_file,orbit_file,TGvar,InterScheme,saveOption,Exec_Btn]
    
        return MainPanel
    display( createGUI() )