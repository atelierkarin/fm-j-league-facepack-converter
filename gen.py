from config import fm_data_path, facepack_path, facepack_id_list
from pathlib import Path

import shutil
import distutils
from distutils import dir_util
import pandas as pd

# フェイスパックのIDリストを読み込み
df_original = pd.read_csv(facepack_path + facepack_id_list)
df_original = df_original.filter(['UID','名前'], axis=1)

# 転換のIDリストを読み込み
df_target = pd.read_csv("fmse/data.csv", header=None)
df_target.columns = ['新UID','名前']

# リストをマージ
df_transform = pd.merge(df_original, df_target, on='名前')

# フォルダをチェック
target_path = fm_data_path + "/Graphics/j-league/001_New Players"
Path(target_path).mkdir(parents=True, exist_ok=True)

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