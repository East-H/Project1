import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import matplotlib.font_manager as fm
font_path = "C:/Windows/Fonts/H2GTRM.TTF"
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font',family = font_name)

conf_data = pd.read_csv('UcdpPrioConflict_v24_1 - 복사본.csv')

#conflict_id에 대하여 시작연도만 추출
min_yr_idx = conf_data.groupby('conflict_id')["year"].idxmin()

df_min_yr = conf_data.loc[min_yr_idx]

df_min_yr = df_min_yr.sort_values(by="year").reset_index(drop=False)
df_min_yr['recurrence'] = False
side_a_counts = {}
#recurrence 값 입력
for idx,row in df_min_yr.iterrows():
    side_a = row['side_a']
    if side_a in side_a_counts:
        side_a_counts[side_a]+=1
        df_min_yr.at[idx,"recurrence"] = True
    else:
        side_a_counts[side_a] = 1
df_min_yr = df_min_yr.sort_values(by="index").reset_index(drop=True)

#conf_data에 reccurence붙이기
recur_data = df_min_yr[['index','conflict_id','recurrence']]
recur_data = recur_data.set_index('index')

#분쟁기간 시각화 (days)
date = pd.DataFrame()
date['conflict_id'] = conf_data['conflict_id']
conf_data['start_date2'] = pd.to_datetime(conf_data['start_date2'])
conf_data['ep_end_date'] = pd.to_datetime(conf_data['ep_end_date'],errors='coerce')
date['end_state'] = conf_data['ep_end']
date['duration'] = (conf_data['ep_end_date']-conf_data['start_date2']).dt.days

df_no_na = conf_data.dropna(subset=['ep_end_date'])

latest_end_date_idx = df_no_na.groupby('conflict_id')['ep_end_date'].idxmax()
latest_end_dates = conf_data.loc[latest_end_date_idx]

duration = date.groupby('conflict_id')['duration'].max()
#duration = date.loc[last_duration_idx]
#plt.hist(duration)



#새로운 데이터 프레임 new_conf_data
new_conf_data = latest_end_dates.reset_index(drop=True)
new_conf_data = new_conf_data.set_index('conflict_id')

recur_data2 = recur_data.reset_index(drop=True)
recur_data2 = recur_data2.set_index('conflict_id')
recur_data2 = recur_data2.sort_values(by='conflict_id')

new_conf_data['recurrence'] = recur_data2['recurrence']
new_conf_data['duration'] = duration
new_conf_data = new_conf_data.reset_index(drop=False)
new_conf_data
