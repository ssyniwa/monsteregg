import random
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="神葬アトリエ：3匹の育成工房", page_icon="⚔️", layout="wide"
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
  # 3匹の初期データ
  st.session_state.creatures = [
    {
      "name": "実験体A",
      "stage": 1,  # 1: 幼体, 2: 成長期, 3: 半神人型, 4: 神葬解放
      "biome": "ドラゴン型",
      "elem1": "炎",
      "elem2": "結晶",
      "weapon": "ロングソード",
      "exp": 0,
    },
    {
      "name": "実験体B",
      "stage": 1,
      "biome": "獣型",
      "elem1": "雷",
      "elem2": "血",
      "weapon": "大鎌",
      "exp": 0,
    },
    {
      "name": "実験体C",
      "stage": 1,
      "biome": "昆虫型",
      "elem1": "氷",
      "elem2": "植物",
      "weapon": "弓",
      "exp": 0,
    },
  ]


# プロンプト生成関数（Gemini画像生成用などに応用可能）
def generate_prompt(c):
  if c["stage"] < 4:
    return (
        f"A fantasy monster, base species is {c['biome']}, infused with"
        f" element {c['elem1']} and secondary element {c['elem2']}, cute"
        f" growing stage {c['stage']}, digital art"
    )
  else:
    return (
        f"A masterclass fantasy humanoid divine warrior holding a divine weapon"
        f" [{c['weapon']}], base creature was {c['biome']}, infused with"
        f" {c['elem1']} and {c['elem2']}, epic masterpiece, dark fantasy, 8k"
        f" resolution"
    )


# タイトル
st.title("⚔️ 神葬アトリエ：3匹の育成＆戦闘工房")
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
      st.subheader(f"{c['name']} (Lv.{c['stage']})")
      # ビジュアルプレースホルダー（実際のアプリではGemini画像を表示）
      st.info(
          f"**生物種**: {c['biome']}\n\n**主属性**: {c['elem1']} |"
          f" **副属性**: {c['elem2']}\n\n**武器種**: {c['weapon']}"
      )
      st.write(f"成長度 (EXP): {c['exp']}/100")
      st.progress(c["exp"])

      prompt_preview = generate_prompt(c)
      st.caption(f"生成プロンプト案:\n`{prompt_preview}`")

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

  if st.button("エサを与えて育成する (-100G)"):
    if st.session_state.gold >= 100:
      st.session_state.gold -= 100
      c["biome"] = new_biome
      c["elem1"] = new_elem1
      c["elem2"] = new_elem2
      c["weapon"] = new_weapon
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
    # 簡易戦闘シミュレーション
    success = random.choice([True, True, False])  # 2/3の確率で勝利
    if success:
      reward_gold = 400
      st.session_state.gold += reward_gold
      for c in st.session_state.creatures:
        c["exp"] += 20
      st.success(
          f"🎉 勝利！ 報酬として {reward_gold}G を獲得し、3匹の経験値がアップしました！"
      )
    else:
      st.warning("⚠️ 敵の反撃により敗退…特訓し直して再挑戦しよう。")

elif menu == "図鑑":
  st.header("📖 神葬アルカディア図鑑")
  st.write(
      "これまでに到達した究極の「神葬武器持ち人型形態」の記録を残します。"
  )
  for b in BIOMES:
    for w in WEAPONS:
      st.markdown(
          f"- **[未解放]** 生物種: `{b}` × 武器種: `{w}` （最終形態未到達）"
      )
