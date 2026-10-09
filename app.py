import os
import random
from PIL import Image
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="神葬アトリエ：アルカディアの箱庭", page_icon="⚔️", layout="wide"
)

# 定数データ
BIOMES = ["ドラゴン型", "獣型", "昆虫型", "飛行型", "水棲型"]
ELEM1 = ["炎", "氷", "雷"]
ELEM2 = ["植物", "血", "結晶"]
WEAPONS = ["ロングソード", "大鎌", "銃", "弓"]

# 初期セッション状態の定義
if "gold" not in st.session_state:
  st.session_state.gold = 1000
if "unlocked_encyclopedia" not in st.session_state:
  st.session_state.unlocked_encyclopedia = []
if "creatures" not in st.session_state:
  st.session_state.creatures = [
      {
          "name": "実験体α",
          "stage": 1,  # 1: 幼体, 2: 成長期, 3: 半神人型, 4: 神葬解放（最終）
          "biome": "ドラゴン型",
          "elem1": "炎",
          "elem2": "結晶",
          "weapon": "ロングソード",
          "exp": 0,
      },
      {
          "name": "実験体β",
          "stage": 1,
          "biome": "獣型",
          "elem1": "雷",
          "elem2": "血",
          "weapon": "大鎌",
          "exp": 0,
      },
      {
          "name": "実験体γ",
          "stage": 1,
          "biome": "昆虫型",
          "elem1": "氷",
          "elem2": "植物",
          "weapon": "弓",
          "exp": 0,
      },
  ]


# ==========================================
# 賢いフォールバック付き画像読み込み関数
# ==========================================
def get_smart_creature_image(c):
  stage = c["stage"]
  biome = c["biome"]
  elem1 = c["elem1"]
  elem2 = c["elem2"]
  weapon = c["weapon"]

  candidate_filenames = []

  # ステージごとの詳細度に応じたファイル名候補の優先リストを生成
  if stage == 1:
    candidate_filenames = [f"stage1_{biome}.jpg"]
  elif stage == 2:
    candidate_filenames = [
        f"stage2_{biome}_{elem1}.jpg",
        f"stage1_{biome}.jpg",
    ]
  elif stage == 3:
    candidate_filenames = [
        f"stage3_{biome}_{elem1}_{elem2}.jpg",
        f"stage2_{biome}_{elem1}.jpg",
        f"stage1_{biome}.jpg",
    ]
  elif stage >= 4:
    candidate_filenames = [
        f"final_{biome}_{elem1}_{elem2}_{weapon}.jpg",
        f"stage3_{biome}_{elem1}_{elem2}.jpg",
        f"stage2_{biome}_{elem1}.jpg",
        f"stage1_{biome}.jpg",
    ]

  # フォルダ内を上から順に探し、最初に見つかった画像を採用
  for filename in candidate_filenames:
    image_path = os.path.join("assets", filename)
    if os.path.exists(image_path):
      return Image.open(image_path), filename

  # 全て見つからない場合のフォールバック（default.png）
  default_path = os.path.join("assets", "default.jpg")
  if os.path.exists(default_path):
    return Image.open(default_path), "default.jpg"

  return None, None


# ==========================================
# UIデザイン & ナビゲーション
# ==========================================
st.title("⚔️ 神葬アトリエ：3匹の育成＆戦闘工房")
st.sidebar.markdown(f"### 💰 所持金: {st.session_state.gold} G")

menu = st.sidebar.selectbox(
    "メニュー", ["育成ルーム", "素材調合・エサやり", "戦闘ステージ出撃", "図鑑"]
)

# 1. 育成ルーム
if menu == "育成ルーム":
  st.header("🧪 育成槽（3匹の管理）")
  st.write(
      "現在育成中の3匹の個体ステータスと、進捗状況を確認できます。段階に応じて最適な画像が自動で反映されます。"
  )
  cols = st.columns(3)

  for i, c in enumerate(st.session_state.creatures):
    with cols[i]:
      st.subheader(f"{c['name']} (Stage {c['stage']})")

      # 画像の表示とフォールバック情報の取得
      img, used_file = get_smart_creature_image(c)
      if img:
        st.image(img, use_container_width=True)
        st.caption(f"📁 読込画像: `{used_file}`")
      else:
        st.warning(
            "🖼️ 画像がありません\n`assets/` フォルダに画像を追加してください"
        )

      # ステータス表示
      st.info(
          f"**生物種**: {c['biome']}\n\n"
          f"**主属性**: {c['elem1']} | **副属性**: {c['elem2']}\n\n"
          f"**武器種**: {c['weapon']}"
      )
      st.write(f"成長度 (EXP): {c['exp']}/100")
      st.progress(c["exp"] / 100.0)

      # 最終形態に到達している場合、図鑑に登録
      if c["stage"] >= 4:
        encyclopedia_key = (
            f"{c['biome']}_{c['elem1']}_{c['elem2']}_{c['weapon']}"
        )
        if encyclopedia_key not in st.session_state.unlocked_encyclopedia:
          st.session_state.unlocked_encyclopedia.append(encyclopedia_key)

# 2. 素材調合・エサやり
elif menu == "素材調合・エサやり":
  st.header("🥣 育成・エサやりカスタム")
  st.write(
      "素材や触媒を投与して、個体の生物種や属性、武器適性を変化させます（費用: 100G）。"
  )

  target_idx = st.selectbox(
      "育成する個体を選択",
      [0, 1, 2],
      format_func=lambda x: st.session_state.creatures[x]["name"],
  )
  c = st.session_state.creatures[target_idx]

  col1, col2 = st.columns(2)
  with col1:
    new_biome = st.selectbox(
        "生物種（ベースボディ）", BIOMES, index=BIOMES.index(c["biome"])
    )
    new_elem1 = st.selectbox("主属性 (属性1)", ELEM1, index=ELEM1.index(c["elem1"]))
  with col2:
    new_elem2 = st.selectbox(
        "副属性 (属性2)", ELEM2, index=ELEM2.index(c["elem2"])
    )
    new_weapon = st.selectbox(
        "武器種（変異トリガー）",
        WEAPONS,
        index=WEAPONS.index(c["weapon"]),
    )

  if st.button("🌟 特製エサを与えて育成する (-100G)"):
    if st.session_state.gold >= 100:
      st.session_state.gold -= 100
      c["biome"] = new_biome
      c["elem1"] = new_elem1
      c["elem2"] = new_elem2
      c["weapon"] = new_weapon
      c["exp"] += 40  # 経験値加算

      # 経験値が100を超えたら次のステージへ進化
      if c["exp"] >= 100 and c["stage"] < 4:
        c["stage"] += 1
        c["exp"] = 0
        st.success(
            f"✨ 素晴らしい！ {c['name']} が ステージ {c['stage']}"
            " に進化しました！"
        )
      elif c["stage"] >= 4:
        c["exp"] = 100
        st.success(
            f"✨ {c['name']}"
            " はすでに神話級の最終形態に到達しています！ステータスが更新されました。"
        )
      else:
        st.success(f"{c['name']} にエサを与えました！ 成長が進んでいます。")
      st.rerun()
    else:
      st.error("❌ ゴールドが足りません！「戦闘ステージ出撃」で稼ぎましょう。")

# 3. 戦闘ステージ出撃
elif menu == "戦闘ステージ出撃":
  st.header("⚔️ バトル・ダンジョン探索")
  st.write(
      "育てた3匹のチームでダンジョンに挑み、勝利報酬としてゴールドと経験値を獲得します。"
  )

  stage_level = st.selectbox(
      "出撃ステージ選択",
      [
          "初級：魔石の林 (難易度低・報酬少)",
          "中級：機械神殿の遺跡 (難易度中・報酬中)",
          "上級：神葬の塔 (難易度高・報酬高)",
      ],
  )

  if st.button("🚀 チーム出撃！ バトル開始"):
    # 難易度に応じた勝率と報酬設定
    if "初級" in stage_level:
      win_prob, reward = 0.85, 300
    elif "中級" in stage_level:
      win_prob, reward = 0.65, 600
    else:
      win_prob, reward = 0.45, 1200

    if random.random() < win_prob:
      st.session_state.gold += reward
      for c in st.session_state.creatures:
        c["exp"] += 25
        if c["exp"] >= 100 and c["stage"] < 4:
          c["stage"] += 1
          c["exp"] = 0
      st.success(
          f"🎉 討伐成功！ 報酬として **{reward} G** を獲得し、3匹の経験値が上昇しました！"
      )
    else:
      st.warning(
          "⚠️ 敵の反撃に遭い、撤退しました…。育成ルームでエサを与えて強化し直しましょう。"
      )

# 4. 図鑑
elif menu == "図鑑":
  st.header("📖 神葬アルカディア図鑑")
  st.write(
      "これまでに到達した「神葬武器持ちの最終人型形態」のコレクション記録です。"
  )

  unlocked_count = len(st.session_state.unlocked_encyclopedia)
  st.metric(
      label="図鑑コンプリート状況",
      value=f"{unlocked_count} / {len(BIOMES) * len(ELEM1) * len(ELEM2) * len(WEAPONS)}",
  )

  st.divider()

  # 全組み合わせの図鑑グリッド表示
  for b in BIOMES:
    with st.expander(f"📌 生物種ベース: {b}"):
      for w in WEAPONS:
        st.markdown(f"**【 武器種: {w} 】**")
        cols = st.columns(3)
        for i, e1 in enumerate(ELEM1):
          with cols[i]:
            st.caption(f"主属性: {e1}")
            for e2 in ELEM2:
              key = f"{b}_{e1}_{e2}_{w}"
              if key in st.session_state.unlocked_encyclopedia:
                st.success(f"解放済\n`{e1}×{e2}`")
              else:
                st.code(f"未解放\n({e1}×{e2})", language="text")
