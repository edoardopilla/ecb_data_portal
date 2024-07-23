# import necessary libraries
from ecbdata import ecbdata
import pandas as pd
import functools as ft

# define list of series keys for all euro area countries and euro area (changing composition)
series_key_lst = ['ICP.M.AT.N.000000.4.ANR', 'ICP.M.BE.N.000000.4.ANR', 'ICP.M.CY.N.000000.4.ANR',
                  'ICP.M.DE.N.000000.4.ANR', 'ICP.M.EE.N.000000.4.ANR', 'ICP.M.ES.N.000000.4.ANR',
                  'ICP.M.FI.N.000000.4.ANR', 'ICP.M.FR.N.000000.4.ANR', 'ICP.M.GR.N.000000.4.ANR',
                  'ICP.M.HR.N.000000.4.ANR', 'ICP.M.IE.N.000000.4.ANR', 'ICP.M.IT.N.000000.4.ANR',
                  'ICP.M.LT.N.000000.4.ANR', 'ICP.M.LU.N.000000.4.ANR', 'ICP.M.LV.N.000000.4.ANR',
                  'ICP.M.MT.N.000000.4.ANR', 'ICP.M.NL.N.000000.4.ANR', 'ICP.M.PT.N.000000.4.ANR',
                  'ICP.M.SI.N.000000.4.ANR', 'ICP.M.SK.N.000000.4.ANR', 'ICP.M.U2.N.000000.4.ANR']

# retrieve data from ECB data portal
df_lst = [ecbdata.get_series(series_id, start = '1999-01') for series_id in series_key_lst]

# drop unnecessary columns and rename to allow dynamic naming of plots
df_lst = [df_lst[i][['REF_AREA', 'TIME_PERIOD', 'OBS_VALUE']].rename(
    columns = {'OBS_VALUE': str(df_lst[i].REF_AREA[0])}).drop(
        columns = ['REF_AREA']) for i in range(len(df_lst))]

# merge dataframes to plot jointly
df_merge = ft.reduce(lambda left, right: pd.merge(left, right, on = 'TIME_PERIOD', how = 'left'), df_lst)

#%% plot inflation series jointly
df_merge.plot(kind = 'line', x = 'TIME_PERIOD', title = 'Inflation across Euro area countries',
              legend = False, xlabel = '', ylabel = 'Inflation rate (%)')


#%% plot inflation series individually
for df in df_lst:
    df.plot(kind = 'line', x = 'TIME_PERIOD', color = 'black',
            title = f'Inflation {df.columns[1]}', legend = False, xlabel = '',
            ylabel = 'Inflation rate (%)')

#%% read cpi data
cpi_df = pd.read_excel('cpi_u2_data.xlsx')

# set date as index
cpi_df = cpi_df.set_index(keys = 'date')

# calculate month-on-month inflation
cpi_df['infl_mom'] = cpi_df.cpi.pct_change(periods = 1)

# calculate year-on-year inflation
cpi_df['infl_yoy'] = cpi_df.cpi.pct_change(periods = 12)

# calculate yearly average inflation (mind closed = 'left' allowing correct solution)
cpi_df['infl_yoy_avg'] = cpi_df.infl_yoy.rolling(window = 12, step = 12, closed = 'left').mean()

#%% plot interpolated yearly average inflation
cpi_df.interpolate(method = 'linear').plot(y = 'infl_yoy_avg')
