import sys
import glob
from ipywidgets import *
import ipywidgets as widgets
import factors
import productderivation as pD
import supportfunctions
import plots as pl
import errorprogation as EP
# window creation
style = {'description_width': '150px'}
layout1stcolumn = {'width': '300px'}
layout2ndcolumn = {'width': '250px'}
layout3rdcolumn = {'width': '100px'}
button_layout = {'width': '150px'}
style1 = {'description_width': '150px'}
layout1 = {'width': '850px'}
style2 = {'description_width': '95px'}
layout2 = {'width': '160px'}
layout3 = {'width': '350px'}
style3 = {'description_width': '60px'}
layout4 = {'width': '215px'}


def loadgui():
    '''
    This function used create GUI to interact with daedalusmase_errorPropagation module

    '''
    tiegcm_file=widgets.Dropdown(options=sorted(glob.glob("*.nc")), description='TIE-GCM files: ', style=style1, layout=layout1)

    lat_value = widgets.Dropdown(
        options=[('-88.75', 0), ('-86.25', 1), ('-83.75', 2), ('-81.25', 3), ('-78.75', 4), ('-76.25', 5), ('-73.75', 6),('-71.25', 7),
                ('-68.75', 8), ('-66.25', 9), ('-63.75', 10), ('-61.25', 11), ('-58.75', 12), ('-56.25', 13),
                ('-53.75', 14), ('-51.25', 15),
                ('-48.75', 16), ('-46.25', 17), ('-43.75', 18), ('-41.25', 19), ('-38.75', 20), ('-36.25', 21),
                ('-33.75', 22), ('-31.25', 23),
                ('-28.75', 24), ('-26.25', 25), ('-23.75', 26), ('-21.25', 27), ('-18.75', 28), ('-16.25', 29),
                ('-13.75', 30), ('-11.25', 31),
                ('-8.75', 32), ('-6.25', 33), ('-3.75', 34), ('-1.25', 35), ('1.25', 36), ('3.75', 37), ('6.25', 38),
                ('8.75', 39),
                ('11.25', 40), ('13.75', 41), ('16.25', 42), ('18.75', 43), ('21.25', 44), ('23.75', 45), ('26.25', 46),
                ('28.75', 47),
                ('31.25', 48), ('33.75', 49), ('36.25', 50), ('38.75', 51), ('41.25', 52), ('43.75', 53),
                ('46.25', 54), ('48.75', 55), ('51.25', 56), ('53.75', 57), ('56.25', 58), ('58.75', 59),
                ('61.25', 60), ('63.75', 61), ('66.25', 62), ('68.75', 63), ('71.25', 64), ('73.75', 65),
                ('76.25', 66), ('78.75', 67), ('81.25', 68), ('83.75', 69), ('84.25', 70), ('87.75', 71)],
        value=61,
        description='Latitude (deg):',
        layout=layout1stcolumn,
        style=style
    )
    lon_value = widgets.Dropdown(
        options=[('-180.0', 0),
                ('-177.5', 1), ('-175.0', 2), ('-172.5', 3), ('-170.0', 4), ('-167.5', 5), ('-165.0', 6), ('-162.5', 7),
                ('-160.0', 8),
                ('-157.5', 9), ('-155.0', 10), ('-152.5', 11), ('-150.0', 12), ('-147.5', 13), ('-145.0', 14),
                ('-142.5', 15), ('-140.0', 16),
                ('-137.5', 17), ('-135.0', 18), ('-132.5', 19), ('-130.0', 20), ('-127.5', 21), ('-125.0', 22),
                ('-122.5', 23), ('-120.0', 24),
                ('-117.5', 25), ('-115.0', 26), ('-112.5', 27), ('-110.0', 28), ('-107.5', 29), ('-105.0', 30),
                ('-102.5', 31), ('-100.0', 32),
                ('-97.5', 33), ('-95.0', 34), ('-92.5', 35), ('-90.0', 36), ('-87.5', 37), ('-85.0', 38), ('-82.5', 39),
                ('-80.0', 40),
                ('-77.5', 41), ('-75.0', 42), ('-72.5', 43), ('-70.0', 44), ('-67.5', 45), ('-65.0', 46), ('-62.5', 47),
                ('-60.0', 48),
                ('-57.5', 49), ('-55.0', 50), ('-52.5', 51), ('-50.0', 52), ('-47.5', 53), ('-45.0', 54), ('-42.5', 55),
                ('-40.0', 56),
                ('-37.5', 57), ('-35.0', 58), ('-32.5', 59), ('-30.0', 60), ('-27.5', 61), ('-25.0', 62), ('-22.5', 63),
                ('-20.0', 64),
                ('-17.5', 65), ('-15.0', 66), ('-12.5', 67), ('-10.0', 68), ('-7.5', 69), ('-5.0', 70), ('-2.5', 71),
                ('0.0', 72),
                ('2.5', 73), ('5.0', 74), ('7.5', 75), ('10.0', 76), ('12.5', 77), ('15.0', 78), ('17.5', 79),
                ('20.0', 80), ('22.5', 81),
                ('25.0', 82), ('27.5', 83), ('30.0', 84), ('32.5', 85), ('35.0', 86), ('37.5', 87), ('40.0', 88),
                ('42.5', 89), ('45.0', 90),
                ('47.5', 91), ('50.0', 92), ('52.5', 93), ('55.0', 94), ('57.5', 95), ('60.0', 96), ('62.5', 97),
                ('65.0', 98),
                ('67.5', 99), ('70.0', 100), ('72.5', 101), ('75.0', 102), ('77.5', 103), ('80.0', 104), ('82.5', 105),
                ('85.0', 106),
                ('87.5', 107), ('90.0', 108), ('92.5', 109), ('95.0', 110), ('97.5', 111), ('100.0', 112), ('102.5', 113),
                ('105.0', 114),
                ('107.5', 115), ('110.0', 116), ('112.5', 117), ('115.0', 118), ('117.5', 119), ('120.0', 120),
                ('122.5', 121), ('125.0', 122), ('127.5', 123), ('130.0', 124), ('132.5', 125), ('135.0', 126),
                ('137.5', 127), ('140.0', 128), ('142.5', 129), ('145.0', 130), ('147.5', 131), ('150.0', 132),
                ('152.5', 133), ('155.0', 134), ('157.5', 135), ('160.0', 136), ('162.5', 137), ('165.0', 138),
                ('167.5', 139), ('170.0', 140), ('172.5', 141), ('175.0', 142), ('177.5', 143),
                ],
        value=49,
        description='Longitude (deg):',
        layout=layout1stcolumn,
        style=style
    )
    min_height_plot = widgets.Dropdown(value=110, options=range(100, 601, 10), description='min plotting altitude', style=style,
        layout=layout1stcolumn)
    max_height_plot = widgets.Dropdown(value=150, options=range(100, 601, 10), description='max plotting altitude', style=style,
        layout=layout1stcolumn)

    timer_value = widgets.Dropdown(value=9, options=range(0, 60), description='TimeStep:', style=style,
        layout=layout1stcolumn)
    pressure_level = widgets.Dropdown(value=0, options=range(0, 57), description='Pressure Level:', style=style,
        layout=layout1stcolumn)
    COLL_Freq_plot_checkbox = widgets.Checkbox(value=False, description="Plot Collision Frequencies", style=style1,
        layout=layout1)
    COND_plot_checkbox = widgets.Checkbox(value=False, description="Plot Conductivities", style=style1, layout=layout1)
    HR_plot_checkbox = widgets.Checkbox(value=False, description="Plot Heating Rates", style=style1, layout=layout1)
    CS_plot_checkbox = widgets.Checkbox(value=False, description="Cross Section", style=style1, layout=layout1)
    Currents_plot_checkbox = widgets.Checkbox(value=False, description="Currents", style=style1, layout=layout1)

    Error_COLL_Freq_plot_checkbox = widgets.Checkbox(value=False, description="Plot Collision Frequencies Error Propagation",
        style=style1, layout=layout1)
    Error_COND_plot_checkbox = widgets.Checkbox(value=False, description="Plot Conductivities Error Propagation",
        style=style1, layout=layout1)
    Error_HR_plot_checkbox = widgets.Checkbox(value=False, description="Plot Heating Rates Error Propagation", style=style1,
        layout=layout1)
    Error_CS_plot_checkbox = widgets.Checkbox(value=False, description="Cross Section Error Propagation", style=style1,
        layout=layout1)
    Error_Currents_plot_checkbox = widgets.Checkbox(value=False, description="Currents Error Propagation", style=style1,
        layout=layout1)

    night_checkbox = widgets.Checkbox(value=True,  description="Add Nightshade",style=style1, layout=layout1)

    Error_Source = widgets.ToggleButton(
        value=False,
        description='Source of Errors',
        disabled=False,
        button_style='',  # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Select (dark grey) to use Errors from Daedalus Science Study',
        icon=''  # (FontAwesome names without the `fa-` prefix)
    )
    # B_error widget
    B_error = widgets.BoundedFloatText(
        value=5,
        min=0,
        max=1000,
        step=1,
        description='Absolute Error Of $B(nT)$:',
        description_tooltip='Insert the absolute error of Magnetic Field(nT) ',
        disabled=False,
        layout=layout1stcolumn,
        style=style,
    )

    # Ti_error widget
    Ti_error = widgets.BoundedFloatText(
        value=5,
        min=0,
        max=100,
        step=0.01,
        description='Error Of ($T_i$) %:',
        description_tooltip='Insert the % percentage of Ion Temperature ($T_i$)',
        disabled=False,
        layout=layout1stcolumn,
        style=style,
    )

    # Te_error widget
    Te_error = widgets.BoundedFloatText(
        value=5,
        min=0,
        max=100,
        step=0.01,
        description='Error Of ($T_e$) %:',
        description_tooltip='Insert the % percentage of Electron Temperature ($T_e$)',
        disabled=False,
        layout=layout1stcolumn,
        style=style,
    )

    # Tn_error widget
    Tn_error = widgets.BoundedFloatText(
        value=5,
        min=0,
        max=100,
        step=0.01,
        description='Error Of ($T_n$) %:',
        description_tooltip='Insert the % percentage of Neutral Temperature ($T_n$)',
        disabled=False,
        layout=layout1stcolumn,
        style=style,
    )

    # Ne_error widget
    Ne_error = widgets.BoundedFloatText(
        value=5,
        min=0,
        max=100,
        step=0.01,
        description='Error Of Density ($N_e$) %:',
        description_tooltip='Insert the % percentage of Electron Density ($N_e$)',
        disabled=False,
        layout=layout1stcolumn,
        style=style,
    )

    # O_error widget
    O_error = widgets.BoundedFloatText(
        value=5,
        min=0,
        max=100,
        step=0.01,
        description='Error Of Density ($O$) %:',
        description_tooltip='Insert the % percentage of Atomic Oxygen Density ($O$)',
        disabled=False,
        layout=layout1stcolumn,
        style=style,
    )

    # O2_error widget
    O2_error = widgets.BoundedFloatText(
        value=5,
        min=0,
        max=100,
        step=0.01,
        description='Error Of Density ($O_2$) %:',
        description_tooltip='Insert the % percentage of Molecule Oxygen Density ($O_2$)',
        disabled=False,
        layout=layout1stcolumn,
        style=style,
    )

    # N2_error widget
    N2_error = widgets.BoundedFloatText(
        value=5,
        min=0,
        max=100,
        step=0.01,
        description='Error Of Density ($N_2$) %:',
        description_tooltip='Insert the % percentage of Nitrogen Density ($N_2$)',
        disabled=False,
        layout=layout1stcolumn,
        style=style,
    )

    # O2p_error widget
    O2p_error = widgets.BoundedFloatText(
        value=5,
        min=0,
        max=100,
        step=0.01,
        description='Error Of Density ($O^{+}_{2}$) %:',
        description_tooltip='Insert the % percentage of Density ($O^{+}_{2}$)',
        disabled=False,
        layout=layout1stcolumn,
        style=style,
    )

    # Op_error widget
    Op_error = widgets.BoundedFloatText(
        value=5,
        min=0,
        max=100,
        step=0.01,
        description='Error Of Density ($O^{+}$) %:',
        description_tooltip='Insert the % percentage of Density ($O^{+}$)',
        disabled=False,
        layout=layout1stcolumn,
        style=style,
    )

    # NOp_error widget
    NOp_error = widgets.BoundedFloatText(
        value=5,
        min=0,
        max=100,
        step=0.01,
        description='Error Of Density ($NO^{+}$) %:',
        description_tooltip='Insert the % percentage of Density ($NO^{+}$)',
        disabled=False,
        layout=layout1stcolumn,
        style=style,
    )

    # E_error widget
    E_error = widgets.BoundedFloatText(
        value=2,
        min=0,
        max=100,
        step=0.01,
        description='Error of ($E$) mV/m:',
        description_tooltip='Insert the absolute error of ($E$)',
        disabled=False,
        layout=layout1stcolumn,
        style=style,
    )

    # Un_error widget
    Un_error = widgets.BoundedFloatText(
        value=5,
        min=0,
        max=100,
        step=0.01,
        description='Error of ($Un$) %:',
        description_tooltip='Insert the % percentage of ($Un$)',
        disabled=False,
        layout=layout1stcolumn,
        style=style,
    )

    # Ui_error widget
    Ui_error = widgets.BoundedFloatText(
        value=5,
        min=0,
        max=100,
        step=0.01,
        description='Error of ($Ui$) %:',
        description_tooltip='Insert the % percentage of ($Un$)',
        disabled=False,
        layout=layout1stcolumn,
        style=style,
    )

    run_error_button = widgets.Button(
        value=False,
        description='Error Calculation',
        disabled=False,
        button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Press to start Error Propagation Calculations, First you must hit "Calculate Products Button"',
        icon='check',
        layout=button_layout,
        style=style,

    )

    run_Map_error_button = widgets.Button(
        value=False,
        description='Error Calculation',
        disabled=False,
        button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Press to start Error Propagation Calculations, First you must hit "Calculate Products Button"',
        icon='check',
        layout=button_layout,
        style=style,

    )


    def Error_Btn_Clicked(b):
        print("Error Calculation started...")


        EP.error(error_flag=Error_Source.value, B_error=B_error.value, E_error=E_error.value, 
                NO_error=O_error.value, NO2_error=O2_error.value, NN2_error=N2_error.value, 
                NOp_error=Op_error.value, NO2p_error=O2p_error.value, NNOp_error=NOp_error.value,
                Ne_error=Ne_error.value, Te_error=Te_error.value, Ti_error=Ti_error.value, Tn_error=Tn_error.value, 
                Un_error=Un_error.value, Vi_error=Ui_error.value, lat_value=lat_value.value, lon_value=lon_value.value,
                pressure_level=-1)


        if Error_COND_plot_checkbox.value == True:   
            pl.plot_conductivities_contr(lat_value.value, lon_value.value,min_HP,max_HP)# plot Conductivities Error Calculations
            pl.plot_conductivities_error(lat_value.value, lon_value.value,min_HP,max_HP)
            pl.plot_conductivities_plus_error(lat_value.value, lon_value.value,min_HP,max_HP)
            pl.plot_conductivities_rel_error(lat_value.value, lon_value.value,min_HP,max_HP)

        if Error_COLL_Freq_plot_checkbox.value == True:
            pl.plot_collisions_contr(lat_value.value, lon_value.value,min_HP,max_HP)  # plot Collision Frequencies Error Calculations
            pl.plot_collisions_error(lat_value.value, lon_value.value,min_HP,max_HP)
            pl.plot_collisions_plus_error(lat_value.value, lon_value.value,min_HP,max_HP)
            pl.plot_collisions_rel_error(lat_value.value, lon_value.value,min_HP,max_HP)

        if Error_HR_plot_checkbox.value == True:
            pl.plot_heating_rates_contr(lat_value.value, lon_value.value,min_HP,max_HP)# call function to plot Heating Rates Errors
            pl.plot_heating_rates_error(lat_value.value, lon_value.value,min_HP,max_HP)
            pl.plot_heating_rates_plus_error(lat_value.value, lon_value.value,min_HP,max_HP)
            pl.plot_heating_rates_rel_error(lat_value.value, lon_value.value,min_HP,max_HP)

            
        if Error_CS_plot_checkbox.value == True:
            pl.plot_csections_error(lat_value.value, lon_value.value,min_HP,max_HP)# plot Cross Section Error Calculations
            pl.plot_csections_plus_error(lat_value.value, lon_value.value,min_HP,max_HP)
            pl.plot_csections_rel_error(lat_value.value, lon_value.value,min_HP,max_HP)

        if Error_Currents_plot_checkbox.value == True:
            pl.plot_currents_error(lat_value.value, lon_value.value,min_HP,max_HP)     # plot Currents Error Calculations
            pl.plot_currents_plus_error(lat_value.value, lon_value.value,min_HP,max_HP)
            pl.plot_currents_rel_error(lat_value.value, lon_value.value,min_HP,max_HP)




    def Exec_Btn_Clicked(b):
        print("Calculation started...")
        global min_HP,max_HP
        min_HP=min_height_plot.value
        max_HP=max_height_plot.value
        print(tiegcm_file.value, timer_value.value)
        pD.models_input(tiegcm_file.value, timer_value.value, lat_value.value, lon_value.value)
        pD.products(lat_value.value, lon_value.value)

        # run(tiegcm_file.value, timer_value.value, lat_value=lat_value.value, lon_value=lon_value.value)
        if COND_plot_checkbox.value == True:
            pl.plot_conductivities(lat_value.value, lon_value.value,min_HP,max_HP)  # call function to plot conductivities
        if COLL_Freq_plot_checkbox.value == True:
            pl.plot_collisions(lat_value.value, lon_value.value,min_HP,max_HP)     # call function to plot Collision Frequencies
        if HR_plot_checkbox.value == True:
            pl.plot_heating_rates(lat_value.value, lon_value.value,min_HP,max_HP)   # call function to plot Heating Rates
        if CS_plot_checkbox.value == True:
            pl.plot_cross_sections(lat_value.value, lon_value.value,min_HP,max_HP)      # call function to plot Cross Sections
        if Currents_plot_checkbox.value == True:
            pl.plot_currents()            # call function to plot currents


    def Error_Map_Btn_Clicked(b):
        print("Error Map Calculation started...")
        error_flag=True
        EP.error(error_flag=error_flag, B_error=B_error.value, E_error=E_error.value, 
                NO_error=O_error.value, NO2_error=O2_error.value, NN2_error=N2_error.value, 
                NOp_error=Op_error.value, NO2p_error=O2p_error.value, NNOp_error=NOp_error.value,
                Ne_error=Ne_error.value, Te_error=Te_error.value, Ti_error=Ti_error.value, Tn_error=Tn_error.value, 
                Un_error=Un_error.value, Vi_error=Ui_error.value, 
                pressure_level=pressure_level.value)
    

        if Error_COND_plot_checkbox.value == True:
            pl.mapla_conductivities_rel_error_plot(pressure_level.value,night_checkbox.value)
            pl.mapll_conductivities_rel_error_plot(pressure_level.value,night_checkbox.value)

        if Error_COLL_Freq_plot_checkbox.value == True: 
            pl.mapll_collisions_rel_error_plot(pressure_level.value,night_checkbox.value)# plot Collision Frequencies Error Calculations
            pl.mapll_conductivities_rel_error_plot(pressure_level.value,night_checkbox.value)

        if Error_HR_plot_checkbox.value == True:     
            pl.mapla_heating_rates_rel_error_plot(pressure_level.value,night_checkbox.value)# call function to plot Heating Rates Errors
            pl.mapll_heating_rates_rel_error_plot(pressure_level.value,night_checkbox.value)
           
        if Error_CS_plot_checkbox.value == True:
            pl.mapla_cross_section_rel_error_plot(pressure_level.value,night_checkbox.value)# plot Cross Section Error Calculations
            pl.mapll_csection_rel_error_plot(pressure_level.value,night_checkbox.value)

        if Error_Currents_plot_checkbox.value == True:
            pl.mapla_currents_rel_error_plot(pressure_level.value,night_checkbox.value)# plot Currents Error Calculations
            pl.mapll_currents_rel_error_plot(pressure_level.value,night_checkbox.value)




    def Exec_Map_Btn_Clicked(b):
        print("Calculation Map started...")

        global min_HP,max_HP
        min_HP=min_height_plot.value
        max_HP=max_height_plot.value
        print(tiegcm_file.value, timer_value.value)
        pD.models_input(tiegcm_file.value, timer_value.value,  pressure_level=pressure_level.value)
        pD.products( pressure_level=pressure_level.value)

        # run(tiegcm_file.value, timer_value.value, lat_value=lat_value.value, lon_value=lon_value.value)
        if COND_plot_checkbox.value == True:
            pl.mapla_conductivities_plot(pressure_level.value,night_checkbox.value)# call function to plot conductivities
            pl.mapll_conductivities_plot(pressure_level.value,night_checkbox.value)
        if COLL_Freq_plot_checkbox.value == True:
            pl.mapll_conductivities_plot(pressure_level.value,night_checkbox.value)# call function to plot Collision Frequencies
            pl.mapla_collisions_rel_error_plot(pressure_level.value,night_checkbox.value)      
        if HR_plot_checkbox.value == True:
            pl.mapla_heating_rates_plot(pressure_level.value,night_checkbox.value)# call function to plot Heating Rates
            pl.mapll_heating_rates_plot(pressure_level.value,night_checkbox.value)
        if CS_plot_checkbox.value == True:
            pl.mapla_cross_section_plot(pressure_level.value,night_checkbox.value)# call function to plot Cross Sections
            pl.mapll_csection_plot(pressure_level.value,night_checkbox.value)
        if Currents_plot_checkbox.value == True:
            pl.mapla_currents_plot(pressure_level.value,night_checkbox.value)# call function to plot Currents
            pl.mapll_currents_plot(pressure_level.value,night_checkbox.value)


    def createGUI():
        ## the top level visual elements
        print("GUI creating...")
        MainPanel = widgets.VBox()
        MainTab = widgets.Tab()
        # ############################################################################
        VerticalPanel = widgets.VBox()
        BasicVerticalPanel = widgets.VBox()
        BasicVerticalPanel.children = [lat_value, lon_value, timer_value]
        PlottingHeight=widgets.HBox()
        PlottingHeight.children=[min_height_plot,max_height_plot]
        ErrorPanel1 = widgets.VBox()
        ErrorPanel1.children = [O_error, O2_error, N2_error, Op_error, O2p_error, NOp_error]
        ErrorPanel2 = widgets.VBox()
        ErrorPanel2.children = [B_error, Ti_error, Te_error, Tn_error, Ne_error]
        ErrorPanel3 = widgets.VBox()
        ErrorPanel3.children = [E_error, Un_error, Ui_error]
        ErrorPanel = widgets.HBox()
        ErrorPanel.children = [ErrorPanel1, ErrorPanel2, ErrorPanel3]
        PlotSelectPanel1 = widgets.HBox()
        PlotSelectPanel1.children = [COLL_Freq_plot_checkbox, COND_plot_checkbox]
        PlotSelectPanel2 = widgets.HBox()
        PlotSelectPanel2.children = [HR_plot_checkbox, CS_plot_checkbox, Currents_plot_checkbox]
        PlotSelectPanel = widgets.VBox()
        PlotSelectPanel.children = [PlotSelectPanel1, PlotSelectPanel2]
        PlotErrorSelectPanel1 = widgets.HBox()
        PlotErrorSelectPanel1.children = [Error_COLL_Freq_plot_checkbox, Error_COND_plot_checkbox]
        PlotErrorSelectPanel2 = widgets.HBox()
        PlotErrorSelectPanel2.children = [Error_HR_plot_checkbox, Error_CS_plot_checkbox, Error_Currents_plot_checkbox]
        PlotErrorSelectPanel = widgets.VBox()
        PlotErrorSelectPanel.children = [PlotErrorSelectPanel1, PlotErrorSelectPanel2]
        Btn_panel = widgets.HBox()
        # ###############################################################################
        MapPanel = widgets.VBox()
        BasicMapPanel = widgets.VBox()
        BasicMapPanel.children = [pressure_level, timer_value]
        MapErrorPanel1 = widgets.VBox()
        MapErrorPanel1.children = [O_error, O2_error, N2_error, Op_error, O2p_error]
        MapErrorPanel2 = widgets.VBox()
        MapErrorPanel2.children = [B_error, Ti_error, Te_error, Tn_error, Ne_error]
        MapErrorPanel3 = widgets.VBox()
        MapErrorPanel3.children = [E_error, Un_error]
        MapErrorPanel = widgets.HBox()
        MapErrorPanel.children = [MapErrorPanel1, MapErrorPanel2, MapErrorPanel3]
        Btn_Map_panel = widgets.HBox()
        # #################################################################################
        MainTab.children = [VerticalPanel, MapPanel]
        MainTab.set_title(0, 'Vertical Profiles')
        MainTab.set_title(1, 'Maps')
        MainPanel.children = [MainTab]
        # #################################################################################
        Exec_Btn = widgets.Button(description='Calculate Products', tooltip="Click here to calculate Daedalus products", )
        Exec_Btn.style.button_color = 'MediumTurquoise'
        Exec_Btn.on_click(Exec_Btn_Clicked)
        run_error_button.on_click(Error_Btn_Clicked)
        Btn_panel.children = [Exec_Btn, run_error_button]
        VerticalPanel.children = [tiegcm_file, BasicVerticalPanel,PlottingHeight, PlotSelectPanel, ErrorPanel, PlotErrorSelectPanel,
                                Error_Source, Btn_panel]

        Exec_Map_Btn = widgets.Button(description='Calculate Products',
                                    tooltip="Click here to calculate Daedalus products", )
        Exec_Map_Btn.style.button_color = 'MediumTurquoise'
        Exec_Map_Btn.on_click(Exec_Map_Btn_Clicked)
        run_Map_error_button.on_click(Error_Map_Btn_Clicked)
        Btn_Map_panel.children = [Exec_Map_Btn, run_Map_error_button]
        MapPanel.children = [tiegcm_file, BasicMapPanel, MapErrorPanel, night_checkbox, Btn_Map_panel]

        return MainPanel

    display(createGUI())
