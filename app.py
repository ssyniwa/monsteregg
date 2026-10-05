import os
import random
from PIL import Image
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="神葬アトリエ：画像インポート版", page_icon="⚔️", layout="wide"
)

# 定数データ
BIOMES = ["ドラゴン型", "獣型", "昆虫型", "飛行型", "水棲型"]
ELEM1 = ["炎", "氷", "雷"]
ELEM2 = ["植物", "血", "結晶"]
WEAPONS = ["ロングソード", "大鎌", "銃", "弓"]

# 初期セッション状態の定義
if "gold" not in st.session_state:
  st.session_state.gold = 1000
if "creatures" not in st.session_state:
  st.session_state.creatures = [
    {
      "name": "実験体A",
      "stage": 1,  # 1: 幼体, 2: 成長期, 3: 半神人型, 4: 神葬解放（最終）
      "biome": "ドラゴン型",
      "elem1": "炎",
      "elem2": "結晶",
      "weapon": "ロングソード",
      "exp": 0,
      "image_filename": "stage1_dragon.png",  # 紐付ける画像ファイル名
    },
    {
      "name": "実験体B",
      "stage": 1,
      "biome": "獣型",
      "elem1": "雷",
      "elem2": "血",
      "weapon": "大鎌",
      "exp": 0,
      "image_filename": "stage1_beast.png",
    },
    {
      "name": "実験体C",
      "stage": 1,
      "biome": "昆虫型",
      "elem1": "氷",
      "elem2": "植物",
      "weapon": "弓",
      "exp": 0,
      "image_filename": "stage1_insect.png",
    },
  ]


# 画像を安全に読み込む関数
def load_creature_image(filename):
  image_path = os.path.join("assets", filename)
  if os.path.exists(image_path):
    return Image.open(image_path)
  else:
    # 画像ファイルがない場合のダミー生成（またはデフォルト画像）
    # ここでは見つからない旨のプレースホルダーを返す代わりにNoneにする
    return None


# タイトル
st.title("⚔️ 神葬アトリエ：画像読込＆育成工房")
st.sidebar.markdown(f"### 所持金: 💰 {st.session_state.gold} G")

# メインメニュー
menu = st.sidebar.selectbox(
    "メニュー", ["育成ルーム", "素材調合・エサやり", "戦闘ステージ出撃", "図鑑"]
)

if menu == "育成ルーム":
  st.header("🧪 育成槽（3匹の管理）")
  cols = st.columns(3)

  for i, c in enumerate(st.session_state.creatures):
    with cols[i]:
      st.subheader(f"{c['name']} (Stage {c['stage']})")

      # 画像の表示
      img = load_creature_image(c["image_filename"])
      if img:
        st.image(img, use_container_width=True)
      else:
        st.warning(
            f"🖼️ 画像が見つかりません\n`assets/{c['image_filename']}` を配置してください"
        )

      st.info(
          f"**生物種**: {c['biome']}\n\n**主属性**: {c['elem1']} |"
          f" **副属性**: {c['elem2']}\n\n**武器種**: {c['weapon']}"
      )
      st.write(f"成長度 (EXP): {c['exp']}/100")
      st.progress(c["exp"])

elif menu == "素材調合・エサやり":
  st.header("🥣 育成・エサやりカスタム")
  target_idx = st.selectbox(
      "育成する個体を選択",
      [0, 1, 2],
      format_func=lambda x: st.session_state.creatures[x]["name"],
  )
  c = st.session_state.creatures[target_idx]

  col1, col2 = st.columns(2)
  with col1:
    new_biome = st.selectbox("生物種を変更・調整", BIOMES, index=BIOMES.index(c["biome"]))
    new_elem1 = st.selectbox("主属性を変更", ELEM1, index=ELEM1.index(c["elem1"]))
  with col2:
    new_elem2 = st.selectbox(
        "副属性を変更", ELEM2, index=ELEM2.index(c["elem2"])
    )
    new_weapon = st.selectbox(
        "武器種を設定（変異トリガー）",
        WEAPONS,
        index=WEAPONS.index(c["weapon"]),
    )

  # 画像ファイルの切り替え設定（簡易的ルール）
  new_img_filename = st.text_input(
      "表示する画像ファイル名 (assets/ フォルダ内)", value=c["image_filename"]
  )

  if st.button("エサを与えて育成する (-100G)"):
    if st.session_state.gold >= 100:
      st.session_state.gold -= 100
      c["biome"] = new_biome
      c["elem1"] = new_elem1
      c["elem2"] = new_elem2
      c["weapon"] = new_weapon
      c["image_filename"] = new_img_filename
      c["exp"] += 35

      if c["exp"] >= 100 and c["stage"] < 4:
        c["stage"] += 1
        c["exp"] = 0
        st.success(
            f"✨ {c['name']} がステージ {c['stage']} に進化・変異しました！"
        )
      else:
        st.success(f"{c['name']} にエサを与えました！ステータスが変動しました。")
      st.rerun()
    else:
      st.error("ゴールドが足りません！")

elif menu == "戦闘ステージ出撃":
  st.header("⚔️ バトル・ダンジョン探索")
  st.write(
      "育てた3匹のチームでダンジョンに挑み、素材とゴールドを稼ぎます。"
  )

  stage_level = st.selectbox(
      "出撃ステージ選択", ["初級：魔石の林", "中級：機械神殿の遺跡", "上級：神葬の塔"]
  )

  if st.button("バトル開始！"):
    success = random.choice([True, True, False])
    if success:
      reward_gold = 400
      st.session_state.gold += reward_gold
      for c in st.session_state.creatures:
        c["exp"] += 20
      st.success(
          f"🎉 勝利！ 報酬として {reward_gold}G を獲得し、3匹の経験値がアップしました！"
      )
    else:
      st.warning("⚠️ 敗退…育成ルームでステータスや画像を調整して再挑戦しよう。")

elif menu == "図鑑":
  st.header("📖 神葬アルカディア図鑑")
  st.write("これまでに用意した画像と到達した形態の記録。")
  for b in BIOMES:
    for w in WEAPONS:
      st.markdown(f"- 生物種: `{b}` × 武器種: `{w}` （登録スロット）")
