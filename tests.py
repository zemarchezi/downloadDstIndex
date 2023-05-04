#%%
import numpy as np
import pandas as pd
import pytz
from pysatdata.loaders.load import *
from pysatdata.utils.interpolate_flux_rbsp import *
from pysatdata.utils.plotFunc.plot_funtions import *
import datetime
import gc
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from scipy import interpolate as interp
from pysatdata.utils.library_functions import *
#%%

#
# for n, dd in enumerate(dataT.index):
tranges = [[f'2021-05-26', f'2021-05-27'],[f'2022-02-01', f'2022-02-02'],
           [f'2022-03-21', f'2022-03-22'],[f'2022-06-15', f'2022-06-16'],
        [f'2022-07-23', f'2022-07-24'], [f'2022-03-31', f'2022-04-01']]

stringInstant = '2017-03-07'

# stringInstant = dataT.index[0].split(" ")[0]
instDate = datetime.datetime.strptime(stringInstant, '%Y-%m-%d')


# inidate = datetime.datetime(2017,9,5)
# enddate = datetime.datetime(2017,9,12)
inidate = datetime.datetime.strptime(tranges[5][0], '%Y-%m-%d')
enddate = datetime.datetime.strptime(tranges[5][1], '%Y-%m-%d')
dts = (enddate - inidate).days
timedays = [inidate +datetime.timedelta(days = i) for i in range(dts)]
trange0 = [inidate.strftime('%Y-%m-%d'), enddate.strftime('%Y-%m-%d')]
trange= [(inidate - datetime.timedelta(days = 1)).strftime('%Y-%m-%d'),
         (enddate + datetime.timedelta(days = 1)).strftime('%Y-%m-%d')]

config_file_sat = 'C:/Users/josem/python_projects/pySatData/pysatdata/resources/config_file.json'



lshellOrlStar = 'L-Star'
probe = 'a'

paramLoadEfw = {"satellite": 'rbsp', "probe": 'a', "level": '2', "rel": "rel03",
                "instrument": 'efw', "datatype": 'esvy_despun',
                "varnames" : ['efield_mgse', 'lshell']}
paramLoadEm = {"satellite": 'rbsp', "probe": 'a', "level": '3', "rel": "rel03",
                "instrument": 'emfisis', "datatype": "magnetometer", "coord": "gse",
                "cadence": "1sec", "varnames": []}


#%%
pytplot.del_data()
varss_aceSwe = load_sat(trange=trange, satellite='omni',
                    probe=['omni'], rel='rel03',
                    instrument='omni_cdaweb',datatype='hro_1min',
                    config_file=config_file_sat, downloadonly=False,
                    usePandas=True, usePyTplot=False)
#%%
quants_Swe = pytplot.data_quants['proton_density']
time_swe = pd.to_datetime(quants_Swe.coords['time'].values)
# time_dt_swe = [datetime.datetime.fromtimestamp(i, pytz.timezone("UTC")) for i in time_swe]
nP = pytplot.data_quants['proton_density'].values
bgse_x = pytplot.data_quants['BX_GSE'].values
bgse_y = pytplot.data_quants['BY_GSE'].values
bgse_z = pytplot.data_quants['BZ_GSE'].values
b_total = pytplot.data_quants['F'].values
flow_speed = pytplot.data_quants['flow_speed'].values
temperature = pytplot.data_quants['T'].values
pressure = pytplot.data_quants['Pressure'].values
imf = pytplot.data_quants['IMF'].values
ae_index = pytplot.data_quants['AE_INDEX'].values
symH_index = pytplot.data_quants['SYM_H'].values
asyH_index = pytplot.data_quants['ASY_H'].values

varss_aceSwe.index = time_swe

#%%

dstData = pd.read_csv(f'dstIndex{inidate.year}.csv', index_col=0)
dstData.index = pd.to_datetime(dstData.index)
# mask = (dstData.index > pd.Timestamp(time_dt_swe[0].strftime('%Y-%m-%d'))+datetime.timedelta(hours=13)) & (dstData.index < pd.Timestamp(time_dt_swe[-1].strftime('%Y-%m-%d'))+datetime.timedelta(hours=13))
# mask = (dstData.index > pd.Timestamp(time_dt_swe[0].strftime('%Y-%m-%d'))+datetime.timedelta(hours=4)) & (dstData.index < pd.Timestamp(time_dt_swe[-1].strftime('%Y-%m-%d'))+datetime.timedelta(hours=4))
mask = (dstData.index > pd.Timestamp(time_swe[0].strftime('%Y-%m-%d'))) & (dstData.index < pd.Timestamp(time_swe[-1].strftime('%Y-%m-%d')))
dstData = dstData[mask]
#%%
time_dst = dstData.index
dst_index = dstData['dst'].values
#%%
fls = interp.interp1d((np.arange(0, len(dst_index))), dst_index, bounds_error=False)
lsnewy = np.linspace(0, len(dst_index), len(time_swe))
n_dstIndex = fls(lsnewy)

#%%
plotParamsDict = {      'trangeXlim': trange0,
                      'time_dt_swe': time_swe,
                      'nP': nP,
                      'bgse_x': bgse_x,
                      'bgse_y': bgse_y,
                      'bgse_z': bgse_z,
                      'b_total': b_total,
                      'flow_speed': flow_speed,
                      'temperature':temperature,
                      'pressure':pressure,
                      'imf': imf,
                      'asyH_index': asyH_index,
                      'dst_index': dst_index,
                      'time_dst': time_dst,
                      'symH_index': symH_index,
                      'ae_index': ae_index,
                      'fontsize': 16,
                      'probe': 'A',
                      'level': 2,
                      'plotDir': 'rbsp/rept/'
                     }


#%%
def plot_classicSWparams(**kwargs):
    matplotlib.rc('font', family='serif')
    def format_func(value, tick_number):
        hora = pd.to_datetime(mdates.num2date(value)).replace(tzinfo=None)

        return ('{:d}'.format(hora.hour))

    for key, val in kwargs.items():
        globals()[key] = val


    out_figDir = str(Path.home().joinpath('Pictures', plotDir))

    if not os.path.exists(out_figDir) and os.path.dirname(out_figDir) != '':
        os.makedirs(out_figDir)

    xLim=[datetime.datetime.strptime(trangeXlim[0], '%Y-%m-%d'), datetime.datetime.strptime(trangeXlim[1], '%Y-%m-%d')]
 
    matplotlib.rc('font', size=fontsize)
    plt.close('all')
    plt.ioff()
    figprops = dict(figsize=(16,12), dpi=120)
    fig = plt.figure(**figprops)


    if level == 2:
        om = ' -- OMNI directional'
    else:
        om = ''

    figureFilename = f'SolarWind_GeomIndex' \
                     f'_{trangeXlim[0]}_{trangeXlim[1]}.png'
    # Dst Sym-h
    bx = plt.axes([0.063, 0.78, 0.892, 0.17])

#     bx.plot(time_dst, dst_index, '-', color='g')
    bx.plot(time_dt_swe, symH_index, '-', color='g')
    bx.get_xaxis().set_ticks_position('both')
    bx.get_yaxis().set_ticks_position('both')
    for gs in range(0,len(timedays)):
        bx.text(((gs)*(1/(len(timedays)))+(1/(2*len(timedays)))), 1.08, 
                f'{timedays[gs].day:d}-{timedays[gs].strftime("%b").capitalize()}', horizontalalignment='center', verticalalignment='center',
                fontsize=18, transform=bx.transAxes)
    bx.text(1.02, 0.5, 'a.', horizontalalignment='center', verticalalignment='center',
            fontsize=18, transform=bx.transAxes, weight='bold')
    
#     bx.text(0.66, 1.13, 'MP', horizontalalignment='center', verticalalignment='center',
#             fontsize=18, transform=bx.transAxes, rotation=45)
#     bx.text(0.78, 1.13, 'RP', horizontalalignment='center', verticalalignment='center',
#             fontsize=18, transform=bx.transAxes, rotation=45)
    bx.set_ylabel('SYM-H $[nT]$')
    bx.axvline(x=datetime.datetime(2018,3,17,20), color='k')
    bx.axvline(x=datetime.datetime(2018,3,18,22), color='k')
    bx.yaxis.set_minor_locator(AutoMinorLocator())
    bx.xaxis.set_minor_locator(mdates.HourLocator(interval=3))
    bx.xaxis.set_major_locator(mdates.HourLocator(interval=12))
    bx.tick_params(direction='in', length=15, width=0.7, colors='k',
                   grid_color='k', grid_alpha=0.5, which='major')
    bx.tick_params(direction='in', length=10, width=0.7, colors='k',
                   grid_color='k', grid_alpha=0.5, which='minor')
    bx.set_xlim(xLim[0], xLim[1])
    bx.set_xticklabels([])
    bx.grid(linestyle=':', alpha=0.3)


   
    #
    # # flowSpeed
    cx = plt.axes([0.063, 0.60, 0.892, 0.17])
    cx.plot(time_dt_swe, flow_speed, '-', color='orange')
    cx.axvline(x=datetime.datetime(2018,3,17,20), color='k')
    cx.axvline(x=datetime.datetime(2018,3,18,22), color='k')
    cx.set_xlim(xLim[0], xLim[1])
    cx.set_ylim(np.nanmin(flow_speed)-5, np.nanmax(flow_speed)+5)
    cx.text(1.02, 0.5, 'b.', horizontalalignment='center', verticalalignment='center',
            fontsize=18, transform=cx.transAxes, weight='bold')
    cx.tick_params(direction='in', length=15, width=0.7, colors='k',
                   grid_color='k', grid_alpha=0.5, which='major')
    cx.tick_params(direction='in', length=10, width=0.7, colors='k',
                   grid_color='k', grid_alpha=0.5, which='minor')
    cx.get_xaxis().set_ticks_position('both')
    cx.get_yaxis().set_ticks_position('both')
    cx.set_xticklabels([])
    cx.set_ylabel('$V_R$ $[Km~s^{-1}]$')
    cx.yaxis.set_minor_locator(AutoMinorLocator())
    cx.xaxis.set_minor_locator(mdates.HourLocator(interval=3))
    cx.xaxis.set_major_locator(mdates.HourLocator(interval=12))
    cx.grid(linestyle=':', alpha=0.3)

    
    #
    # ## IMF
    dx = plt.axes([0.063, 0.42, 0.892, 0.17])
    dx.plot(time_dt_swe, nP, '-', color='m')
    dx.axvline(x=datetime.datetime(2018,3,17,20), color='k')
    dx.axvline(x=datetime.datetime(2018,3,18,22), color='k')
    dx.get_xaxis().set_ticks_position('both')
    dx.get_yaxis().set_ticks_position('both')
    dx.text(1.02, 0.5, 'c.', horizontalalignment='center', verticalalignment='center',
            fontsize=18, transform=dx.transAxes, weight='bold')
    dx.set_ylabel('N$_p$ $[cm^{-3}]$')
    dx.yaxis.set_minor_locator(AutoMinorLocator())
    dx.xaxis.set_minor_locator(mdates.HourLocator(interval=3))
    dx.xaxis.set_major_locator(mdates.HourLocator(interval=12))
    dx.set_xticklabels([])
    dx.tick_params(direction='in', length=15, width=0.7, colors='k',
                   grid_color='k', grid_alpha=0.5, which='major')
    dx.tick_params(direction='in', length=10, width=0.7, colors='k',
                   grid_color='k', grid_alpha=0.5, which='minor')
    dx.set_xlim(xLim[0], xLim[1])
#     dx.set_ylim(np.nanmin(nP)-2, np.nanmin(nP)+2)
    dx.grid(linestyle=':', alpha=0.3)

    
    #
    #
    # ## imf
    ex = plt.axes([0.063, 0.24, 0.892, 0.17])
    ex.plot(time_dt_swe, bgse_z, '-', color='r')
    ex.axvline(x=datetime.datetime(2018,3,17,20), color='k')
    ex.axvline(x=datetime.datetime(2018,3,18,22), color='k')
    # ex.plot(time_dt_swe, b_total, '-', color='r', label="B total")
    ex.get_xaxis().set_ticks_position('both')
    ex.get_yaxis().set_ticks_position('both')
    ex.text(1.02, 0.5, 'd.', horizontalalignment='center', verticalalignment='center',
            fontsize=18, transform=ex.transAxes, weight='bold')
    # ex.legend(loc='upper right', bbox_to_anchor=(1.14, 1.02))
    ex.set_ylabel('IMF $B_z$ [nT]')
    ex.yaxis.set_minor_locator(AutoMinorLocator())
    ex.xaxis.set_minor_locator(mdates.HourLocator(interval=3))
    ex.xaxis.set_major_locator(mdates.HourLocator(interval=12))
    ex.tick_params(direction='in', length=15, width=0.7, colors='k',
                   grid_color='k', grid_alpha=0.5, which='major')
    ex.tick_params(direction='in', length=10, width=0.7, colors='k',
                   grid_color='k', grid_alpha=0.5, which='minor')
    ex.set_xlim(xLim[0], xLim[1])
    ex.set_xticklabels([])
    ex.grid(linestyle=':', alpha=0.3)
    #
    # ## AsyH index
    fx = plt.axes([0.063, 0.06, 0.892, 0.17])
    fx.plot(time_dt_swe, pressure, '-', color='k')
    fx.axvline(x=datetime.datetime(2018,3,17,20), color='k')
    fx.axvline(x=datetime.datetime(2018,3,18,22), color='k')
    # fx.plot(time_dt_swe, ae_index, '-', color='k')
    fx.get_xaxis().set_ticks_position('both')
    fx.get_yaxis().set_ticks_position('both')
    fx.text(1.02, 0.5, 'e.', horizontalalignment='center', verticalalignment='center',
            fontsize=18, transform=fx.transAxes, weight='bold')
    fx.set_ylabel('Pressure [nPa]')
    # fx.set_ylabel('AE Index [nT]')
    fx.set_xlabel('Universal Time [hour]', fontsize=18)
    fx.yaxis.set_minor_locator(AutoMinorLocator())
    fx.xaxis.set_minor_locator(mdates.HourLocator(interval=3))
    fx.xaxis.set_major_locator(mdates.HourLocator(interval=12))
    fx.tick_params(direction='in', length=15, width=0.7, colors='k',
                   grid_color='k', grid_alpha=0.5, which='major')
    fx.tick_params(direction='in', length=10, width=0.7, colors='k',
                   grid_color='k', grid_alpha=0.5, which='minor')
    fx.set_xlim(xLim[0], xLim[1])
#     fx.set_ylim(0, 2e5)
    fx.xaxis.set_major_formatter(plt.FuncFormatter(format_func))
    fx.grid(linestyle=':', alpha=0.3)
    #
    #


    logging.info(f'saving figure at: {out_figDir}/{figureFilename}')
    plt.savefig(f'{out_figDir}/{figureFilename}', bbox_inches='tight')
    plt.savefig(f"{out_figDir}/{figureFilename.replace('png', 'pdf')}", bbox_inches='tight')
    # plt.show()

plot_classicSWparams(**plotParamsDict)
# %%

# %%
