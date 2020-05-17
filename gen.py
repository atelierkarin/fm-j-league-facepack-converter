import os
import shutil
import distutils
import pandas as pd

from distutils import dir_util
from pathlib import Path
from tools import calc_age

from config import fm_data_path, facepack_path, facepack_id_list, with_delete, with_club_info, fmse_data_date

# フェイスパックのIDリストを読み込み
df_original = pd.read_csv(facepack_path + facepack_id_list)
df_original = df_original.filter(['UID','名前','クラブ','誕生日'], axis=1)

# 年齢を計算
df_original['年齢'] = df_original.apply(lambda row: calc_age(row['誕生日'], fmse_data_date), axis=1)

# 転換のIDリストを読み込み
df_target = pd.read_csv("fmse/data.csv", header=None)
df_target.columns = ['新UID','名前','クラブ','年齢']

# リストをマージ
df_transform = pd.merge(df_original, df_target, on=['名前','クラブ','年齢'])

# フォルダをチェック
target_path = fm_data_path + "/Graphics/j-league/001_New Players"
Path(target_path).mkdir(parents=True, exist_ok=True)

# 古いファイルを削除
if with_delete:
  for file in os.listdir(target_path):
    if file.endswith('.png'):
      os.remove(file)
  os.remove(target_path + "/config.xml")

# 既存プレイヤーのアイコンをコピー
distutils.dir_util.copy_tree(facepack_path + '/001_Original Players', fm_data_path + '/Graphics/j-league/001_Original Players')

xml_new_players = "<record>\n"
xml_new_players += "\t<boolean id=\"preload\" value=\"false\"/>\n"
xml_new_players += "\t<boolean id=\"amap\" value=\"false\"/>\n"
xml_new_players += "\t<list id=\"maps\">\n"
for index, row in df_transform.iterrows():
  old_id, new_id = row["UID"], row["新UID"]
  try:
    shutil.copy(facepack_path + '/001_New Players/{}.png'.format(old_id), target_path + '/{}.png'.format(new_id))
    xml_new_players += "\t\t<record from=\"{}\" to=\"graphics/pictures/person/{}/portrait\"/>\n".format(new_id, new_id)
  except FileNotFoundError:
    print(facepack_path + '/001_New Players/{}.png'.format(old_id) + 'が見つかりません')
  
xml_new_players += "\t</list>\n"
xml_new_players += "</record>"

with open(target_path + "/config.xml", mode='w') as f:
  f.write(xml_new_players)