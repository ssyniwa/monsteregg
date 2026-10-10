import os
import random
from PIL import Image
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="神葬アトリエ：交代制バトル＆育成工房", page_icon="⚔️", layout="wide"
)

# 定数データ
BIOMES = ["ドラゴン型", "獣型", "昆虫型", "飛行型", "水棲型"]
ELEM1 = ["炎", "氷", "雷"]
ELEM2 = ["植物", "血", "結晶"]
WEAPONS = ["ロングソード", "大鎌", "銃", "弓"]

# 種族ごとの基本ステータス補正係数 (HP, 攻撃力, 防御力, 素早さ)
BIOME_STATS = {
    "ドラゴン型": {"hp": 170, "atk": 25, "def": 10, "spd": 10},
    "獣型": {"hp": 150, "atk": 20, "def": 5, "spd": 18},
    "昆虫型": {"hp": 120, "atk": 22, "def": 3, "spd": 25},
    "飛行型": {"hp": 130, "atk": 18, "def": 2, "spd": 30},
    "水棲型": {"hp": 190, "atk": 15, "def": 15, "spd": 8},
}

# 各難易度のステージ（初級1、中級3、上級3、最上級1の計8ステージ）
BATTLE_STAGES = {
    "初級：魔石の林": {
        "desc": "魔力を帯びた植物と小型モンスターがうろつく森。",
        "boss": {
            "name": "フォレスト・キメラ (ボス)",
            "image": "enemy_forest_boss.jpg",
            "hp": 200,
            "atk": 25,
            "def": 10,
        },
        "minions": [
            {
                "name": "魔樹の苗木",
                "image": "enemy_forest_minion1.jpg",
                "hp": 50,
                "atk": 12,
                "def": 5,
            },
            {
                "name": "毒スライム",
                "image": "enemy_forest_minion2.jpg",
                "hp": 60,
                "atk": 15,
                "def": 5,
            },
            {
                "name": "キラービー",
                "image": "enemy_forest_minion3.jpg",
                "hp": 40,
                "atk": 18,
                "def": 3,
            },
            {
                "name": "フォレストウルフ",
                "image": "enemy_forest_minion4.jpg",
                "hp": 70,
                "atk": 16,
                "def": 8,
            },
        ],
        "reward_gold": 250,
        "reward_exp": 30,
    },
    "中級①：機械神殿の遺跡": {
        "desc": "古代の防衛機構が目覚めた危険な遺跡。",
        "boss": {
            "name": "ガーディアン・ゴーレム (ボス)",
            "image": "enemy_ruins_boss.jpg",
            "hp": 350,
            "atk": 40,
            "def": 20,
        },
        "minions": [
            {
                "name": "ブロークン・ドローン",
                "image": "enemy_ruins_minion1.jpg",
                "hp": 70,
                "atk": 18,
                "def": 8,
            },
            {
                "name": "セントリータレット",
                "image": "enemy_ruins_minion2.jpg",
                "hp": 80,
                "atk": 22,
                "def": 10,
            },
            {
                "name": "ガード・スフィア",
                "image": "enemy_ruins_minion3.jpg",
                "hp": 60,
                "atk": 20,
                "def": 12,
            },
            {
                "name": "プロト・ナイト",
                "image": "enemy_ruins_minion4.jpg",
                "hp": 100,
                "atk": 25,
                "def": 15,
            },
        ],
        "reward_gold": 450,
        "reward_exp": 45,
    },
    "中級②：水晶の鉱山": {
        "desc": "硬質な結晶に覆われた魔力あふれる鉱山地帯。",
        "boss": {
            "name": "クリスタル・ガーディアン (ボス)",
            "image": "enemy_crystal_boss.jpg",
            "hp": 380,
            "atk": 42,
            "def": 25,
        },
        "minions": [
            {
                "name": "鉱石ビースト",
                "image": "enemy_crystal_minion1.jpg",
                "hp": 75,
                "atk": 19,
                "def": 10,
            },
            {
                "name": "水晶コウモリ",
                "image": "enemy_crystal_minion2.jpg",
                "hp": 65,
                "atk": 21,
                "def": 8,
            },
            {
                "name": "ゴーレム・カケラ",
                "image": "enemy_crystal_minion3.jpg",
                "hp": 90,
                "atk": 20,
                "def": 15,
            },
            {
                "name": "ジェム・スライム",
                "image": "enemy_crystal_minion4.jpg",
                "hp": 85,
                "atk": 24,
                "def": 10,
            },
        ],
        "reward_gold": 500,
        "reward_exp": 50,
    },
    "中級③：沈黙の回廊": {
        "desc": "不気味な静寂に包まれた魔術師たちの廃墟。",
        "boss": {
            "name": "サイレント・スペクター (ボス)",
            "image": "enemy_silent_boss.jpg",
            "hp": 400,
            "atk": 48,
            "def": 18,
        },
        "minions": [
            {
                "name": "リビング・アーマー",
                "image": "enemy_silent_minion1.jpg",
                "hp": 95,
                "atk": 22,
                "def": 18,
            },
            {
                "name": "シャドウ・クリープ",
                "image": "enemy_silent_minion2.jpg",
                "hp": 70,
                "atk": 26,
                "def": 6,
            },
            {
                "name": "ファントム・アイ",
                "image": "enemy_silent_minion3.jpg",
                "hp": 60,
                "atk": 28,
                "def": 5,
            },
            {
                "name": "呪われた彫像",
                "image": "enemy_silent_minion4.jpg",
                "hp": 110,
                "atk": 23,
                "def": 20,
            },
        ],
        "reward_gold": 550,
        "reward_exp": 55,
    },
    "上級①：神葬の塔": {
        "desc": "神話の兵器が眠る、過酷な試練の塔。",
        "boss": {
            "name": "ファントム・ナイト (ボス)",
            "image": "enemy_tower_boss.jpg",
            "hp": 600,
            "atk": 70,
            "def": 35,
        },
        "minions": [
            {
                "name": "ソウル・ファントム",
                "image": "enemy_tower_minion1.jpg",
                "hp": 130,
                "atk": 35,
                "def": 15,
            },
            {
                "name": "カース・アーマー",
                "image": "enemy_tower_minion2.jpg",
                "hp": 160,
                "atk": 40,
                "def": 25,
            },
            {
                "name": "ブラッド・ガーゴイル",
                "image": "enemy_tower_minion3.jpg",
                "hp": 140,
                "atk": 45,
                "def": 18,
            },
            {
                "name": "ダーク・メイジ",
                "image": "enemy_tower_minion4.jpg",
                "hp": 120,
                "atk": 50,
                "def": 12,
            },
        ],
        "reward_gold": 800,
        "reward_exp": 75,
    },
    "上級②：業火の溶岩洞": {
        "desc": "マグマが煮えたぎる過酷な地底ダンジョン。",
        "boss": {
            "name": "マグマ・ドラゴン (ボス)",
            "image": "enemy_lava_boss.jpg",
            "hp": 650,
            "atk": 75,
            "def": 30,
        },
        "minions": [
            {
                "name": "フレイム・リザード",
                "image": "enemy_lava_minion1.jpg",
                "hp": 140,
                "atk": 38,
                "def": 16,
            },
            {
                "name": "マグマ・スライム",
                "image": "enemy_lava_minion2.jpg",
                "hp": 150,
                "atk": 36,
                "def": 20,
            },
            {
                "name": "インプ・ウォーリア",
                "image": "enemy_lava_minion3.jpg",
                "hp": 125,
                "atk": 44,
                "def": 12,
            },
            {
                "name": "ヘルハウンド",
                "image": "enemy_lava_minion4.jpg",
                "hp": 155,
                "atk": 42,
                "def": 18,
            },
        ],
        "reward_gold": 900,
        "reward_exp": 85,
    },
    "上級③：虚空の聖堂": {
        "desc": "歪んだ時空と異界の気配が漂う聖堂跡。",
        "boss": {
            "name": "ヴォイド・マスター (ボス)",
            "image": "enemy_void_boss.jpg",
            "hp": 720,
            "atk": 82,
            "def": 38,
        },
        "minions": [
            {
                "name": "アビス・ウォーカー",
                "image": "enemy_void_minion1.jpg",
                "hp": 150,
                "atk": 42,
                "def": 18,
            },
            {
                "name": "カオス・ウィスプ",
                "image": "enemy_void_minion2.jpg",
                "hp": 130,
                "atk": 48,
                "def": 14,
            },
            {
                "name": "スター・キメラ",
                "image": "enemy_void_minion3.jpg",
                "hp": 170,
                "atk": 45,
                "def": 22,
            },
            {
                "name": "虚空の番犬",
                "image": "enemy_void_minion4.jpg",
                "hp": 160,
                "atk": 50,
                "def": 20,
            },
        ],
        "reward_gold": 1050,
        "reward_exp": 95,
    },
    "最上級：アルカディアの王座": {
        "desc": "すべての頂点に君臨する、神話級の守護者との決戦。",
        "boss": {
            "name": "神葬の主・ゼニス (ボス)",
            "image": "enemy_god_boss.jpg",
            "hp": 1000,
            "atk": 100,
            "def": 50,
        },
        "minions": [
            {
                "name": "天界の使徒・アルファ",
                "image": "enemy_god_minion1.jpg",
                "hp": 200,
                "atk": 55,
                "def": 30,
            },
            {
                "name": "天界の使徒・ベータ",
                "image": "enemy_god_minion2.jpg",
                "hp": 200,
                "atk": 55,
                "def": 30,
            },
            {
                "name": "審判の翼竜",
                "image": "enemy_god_minion3.jpg",
                "hp": 250,
                "atk": 65,
                "def": 35,
            },
            {
                "name": "神域の番人",
                "image": "enemy_god_minion4.jpg",
                "hp": 300,
                "atk": 70,
                "def": 40,
            },
        ],
        "reward_gold": 1500,
        "reward_exp": 130,
    },
}

# 初期セッション状態の定義（初期資金を600に変更）
if "gold" not in st.session_state:
  st.session_state.gold = 600
if "unlocked_encyclopedia" not in st.session_state:
  st.session_state.unlocked_encyclopedia = []
if "battle_state" not in st.session_state:
  st.session_state.battle_state = None
if "creatures" not in st.session_state:
  st.session_state.creatures = [
      {
          "name": "実験体α",
          "stage": 1,
          "biome": "ドラゴン型",
          "elem1": "炎",
          "elem2": "結晶",
          "weapon": "ロングソード",
          "exp": 0,
          "bonus_hp": 0,
          "bonus_atk": 0,
          "bonus_def": 0,
      },
      {
          "name": "実験体β",
          "stage": 1,
          "biome": "獣型",
          "elem1": "雷",
          "elem2": "血",
          "weapon": "大鎌",
          "exp": 0,
          "bonus_hp": 0,
          "bonus_atk": 0,
          "bonus_def": 0,
      },
      {
          "name": "実験体γ",
          "stage": 1,
          "biome": "昆虫型",
          "elem1": "氷",
          "elem2": "植物",
          "weapon": "弓",
          "exp": 0,
          "bonus_hp": 0,
          "bonus_atk": 0,
          "bonus_def": 0,
      },
  ]


# ステータス計算ヘルパー
def calculate_stats(c):
  base = BIOME_STATS[c["biome"]]
  stage_mult = 1.0 + (c["stage"] - 1) * 0.4
  max_hp = int((base["hp"] + c["bonus_hp"]) * stage_mult)
  atk = int((base["atk"] + c["bonus_atk"]) * stage_mult)
  defense = int((base["def"] + c["bonus_def"]) * stage_mult)
  spd = int(base["spd"] * stage_mult)
  return {"hp": max_hp, "atk": atk, "def": defense, "spd": spd}


# 画像読み込み関数
def get_smart_creature_image(c):
  stage, biome, elem1, elem2, weapon = (
      c["stage"],
      c["biome"],
      c["elem1"],
      c["elem2"],
      c["weapon"],
  )
  if stage == 1:
    candidates = [f"stage1_{biome}.jpg"]
  elif stage == 2:
    candidates = [f"stage2_{biome}_{elem1}.jpg", f"stage1_{biome}.jpg"]
  elif stage == 3:
    candidates = [
        f"stage3_{biome}_{elem1}_{elem2}.jpg",
        f"stage2_{biome}_{elem1}.jpg",
        f"stage1_{biome}.jpg",
    ]
  else:
    candidates = [
        f"final_{biome}_{elem1}_{elem2}_{weapon}.jpg",
        f"stage3_{biome}_{elem1}_{elem2}.jpg",
        f"stage1_{biome}.jpg",
    ]

  for filename in candidates:
    path = os.path.join("assets", filename)
    if os.path.exists(path):
      return Image.open(path), filename

  default_path = os.path.join("assets", "default.jpg")
  if os.path.exists(default_path):
    return Image.open(default_path), "default.jpg"
  return None, None


def load_image(filename):
  path = os.path.join("assets", filename)
  if os.path.exists(path):
    return Image.open(path)
  default_path = os.path.join("assets", "default.jpg")
  if os.path.exists(default_path):
    return Image.open(default_path)
  return None


# ==========================================
# UI & ナビゲーション
# ==========================================
st.title("⚔️ 神葬アトリエ：交代制バトル＆育成工房")
st.sidebar.markdown(f"### 💰 所持金: {st.session_state.gold} G")

menu = st.sidebar.selectbox(
    "メニュー", ["育成ルーム", "素材調合・エサやり", "戦闘ステージ出撃", "図鑑"]
)

# 1. 育成ルーム (特徴の選択と確定機能を統合)[cite: 4]
if menu == "育成ルーム":
  st.header("🧪 育成槽（3匹の特徴設定 & ステータス管理）")
  st.markdown(
      "ここでは各実験体の**特徴（生物種・属性・武器種）の選択と確定**、および現在のステータス確認ができます。"
  )
  cols = st.columns(3)

  for i, c in enumerate(st.session_state.creatures):
    with cols[i]:
      st.subheader(f"{c['name']} (Stage {c['stage']})")
      img, used_file = get_smart_creature_image(c)
      if img:
        st.image(img, use_container_width=True)

      # 育成ルーム内での特徴選択と確定フォーム
      with st.form(key=f"config_form_{i}"):
        st.markdown(f"**【 {c['name']} の特徴設定】**")
        new_biome = st.selectbox(
            "生物種", BIOMES, index=BIOMES.index(c["biome"]), key=f"biome_{i}"
        )
        new_elem1 = st.selectbox(
            "主属性", ELEM1, index=ELEM1.index(c["elem1"]), key=f"elem1_{i}"
        )
        new_elem2 = st.selectbox(
            "副属性", ELEM2, index=ELEM2.index(c["elem2"]), key=f"elem2_{i}"
        )
        new_weapon = st.selectbox(
            "武器種",
            WEAPONS,
            index=WEAPONS.index(c["weapon"]),
            key=f"weapon_{i}",
        )

        submitted = st.form_submit_button("特徴を確定する")
        if submitted:
          c["biome"] = new_biome
          c["elem1"] = new_elem1
          c["elem2"] = new_elem2
          c["weapon"] = new_weapon
          st.success(f"{c['name']} の特徴を更新・確定しました！")
          st.rerun()

      stats = calculate_stats(c)
      st.info(
          f"**確定中ステータス**\n\n"
          f"- 生物種: {c['biome']}\n"
          f"- 主属性: {c['elem1']} | 副属性: {c['elem2']}\n"
          f"- 武器種: {c['weapon']}"
      )
      st.markdown(
          f"❤️ **HP**: {stats['hp']} | ⚔️ **攻撃**: {stats['atk']} | 🛡️"
          f" **防御**: {stats['def']} | ⚡ **素早さ**: {stats['spd']}"
      )
      st.write(f"成長度 (EXP): {c['exp']}/100")
      st.progress(c["exp"] / 100.0)

      if c["stage"] >= 4:
        key = f"{c['biome']}_{c['elem1']}_{c['elem2']}_{c['weapon']}"
        if key not in st.session_state.unlocked_encyclopedia:
          st.session_state.unlocked_encyclopedia.append(key)

# 2. 素材調合・エサやり (ステータス強化・育成専用)[cite: 4]
elif menu == "素材調合・エサやり":
  st.header("🥣 育成・エサやり & ステータス強化カスタム")
  st.markdown(
      "素材と資金(200G)を投資してステータス強化を行います。**1回のエサやりでのHP・攻撃・防御の上昇値の合計は最大35まで**に制限されています。"
  )

  target_idx = st.selectbox(
      "強化する個体を選択",
      [0, 1, 2],
      format_func=lambda x: st.session_state.creatures[x]["name"],
  )
  c = st.session_state.creatures[target_idx]

  st.write(
      f"現在の対象: **{c['name']}** (生物種: {c['biome']} / 武器: {c['weapon']})"
  )
  st.markdown(
      "※特徴の変更や再設定は**「育成ルーム」**で行ってからお越しください。"
  )

  st.divider()
  st.subheader("💪 追加ステータス強化 (費用: 200G / 上昇合計上限: 35)")
  inc_hp = st.number_input("HP強化 (+)", min_value=0, max_value=35, step=5, value=15)
  inc_atk = st.number_input(
      "攻撃力強化 (+)", min_value=0, max_value=35, step=5, value=10
  )
  inc_def = st.number_input(
      "防御力強化 (+)", min_value=0, max_value=35, step=5, value=10
  )

  total_inc = inc_hp + inc_atk + inc_def
  st.write(f"現在のステータス上昇合計値: **{total_inc} / 35**")

  if st.button("🌟 特製エサを与えて育成・強化する (-200G)"):
    if total_inc > 35:
      st.error(
          "❌ 1回のエサやりでの上昇値の合計が35を超えています！配分を調整してください。"
      )
    else:
      cost = 200
      if st.session_state.gold >= cost:
        st.session_state.gold -= cost
        c["bonus_hp"] += inc_hp
        c["bonus_atk"] += inc_atk
        c["bonus_def"] += inc_def
        c["exp"] += 45

        if c["exp"] >= 100 and c["stage"] < 4:
          c["stage"] += 1
          c["exp"] = 0
          st.success(
              f"✨ {c['name']} が ステージ {c['stage']} に進化しました！"
          )
        else:
          st.success(f"✨ {c['name']} のステータス強化が完了しました！")
        st.rerun()
      else:
        st.error(
            "❌ ゴールドが足りません！バトルステージでゴールドを稼ぎましょう。"
        )

# 3. 戦闘ステージ出撃（経験値獲得およびスキル攻撃実装）[cite: 4]
elif menu == "戦闘ステージ出撃":
  st.header("⚔️ 交代制ターンバトル・ダンジョン探索")
  st.markdown(
      "⚠️ **注意**: 戦闘に勝利するとゴールドに加えて**経験値が獲得**でき、パーティ全体の育成が進みます[cite: 4]！"
  )

  if st.session_state.battle_state is None:
    selected_stage_name = st.selectbox(
        "出撃ステージ選択", list(BATTLE_STAGES.keys())
    )
    stage_info = BATTLE_STAGES[selected_stage_name]

    col_info, col_img = st.columns([2, 1])
    with col_info:
      st.subheader(f"🛡️ ターゲットボス: {stage_info['boss']['name']}")
      st.markdown(f"*{stage_info['desc']}*")
      st.write(
          f"📦 **配下モンスター**: {len(stage_info['minions'])}体 (最初に迎撃)"
      )
      st.write(
          f"🎁 勝利報酬: 💰 **{stage_info['reward_gold']} G** / 🌟 経験値"
          f" **{stage_info['reward_exp']}**"
      )
    with col_img:
      boss_img = load_image(stage_info["boss"]["image"])
      if boss_img:
        st.image(boss_img, use_container_width=True, caption="ステージボス")

    if st.button("🚀 このステージに出撃する！"):
      party = []
      for idx, c in enumerate(st.session_state.creatures):
        st_data = calculate_stats(c)
        party.append({
            "id": idx,
            "name": c["name"],
            "max_hp": st_data["hp"],
            "hp": st_data["hp"],
            "atk": st_data["atk"],
            "def": st_data["def"],
            "spd": st_data["spd"],
            "biome": c["biome"],
            "elem1": c["elem1"],
            "elem2": c["elem2"],
            "weapon": c["weapon"],
            "stage": c["stage"],
            "image": get_smart_creature_image(c)[1],
        })

      enemies = []
      for m in stage_info["minions"]:
        enemies.append({
            "name": m["name"],
            "hp": m["hp"],
            "max_hp": m["hp"],
            "atk": m["atk"],
            "def": m["def"],
            "image": m["image"],
            "is_boss": False,
        })
      b = stage_info["boss"]
      enemies.append({
          "name": b["name"],
          "hp": b["hp"],
          "max_hp": b["hp"],
          "atk": b["atk"],
          "def": b["def"],
          "image": b["image"],
          "is_boss": True,
      })

      st.session_state.battle_state = {
          "stage_name": selected_stage_name,
          "party": party,
          "active_party_idx": 0,
          "enemies": enemies,
          "active_enemy_idx": 0,
          "logs": [
              f"=== {selected_stage_name} 戦闘開始 ===",
              f"敵の群れ（配下4体 ＋ ボス1体）が現れた！",
          ],
          "reward_gold": stage_info["reward_gold"],
          "reward_exp": stage_info["reward_exp"],
      }
      st.rerun()

  else:
    b_state = st.session_state.battle_state
    party = b_state["party"]
    active_p_idx = b_state["active_party_idx"]
    enemies = b_state["enemies"]
    active_e_idx = b_state["active_enemy_idx"]

    current_ally = party[active_p_idx]
    current_enemy = enemies[active_e_idx]

    st.subheader(
        f"⚔️ バトル進行中: {b_state['stage_name']} (残りの敵: {len(enemies)-active_e_idx}体)"
    )

    col_ally_field, col_vs, col_enemy_field = st.columns([2, 1, 2])

    with col_ally_field:
      st.markdown(
          f"### 🛡️ 味方前衛: {current_ally['name']} (Stage"
          f" {current_ally['stage']})"
      )
      ally_img = load_image(current_ally["image"])
      if ally_img:
        st.image(ally_img, width=300)
      st.progress(max(0.0, current_ally["hp"] / current_ally["max_hp"]))
      st.write(
          f"HP: **{max(0, current_ally['hp'])} / {current_ally['max_hp']}** |"
          f" 攻撃: {current_ally['atk']} | 防御: {current_ally['def']}"
      )

    with col_vs:
      st.markdown(
          "<h1 style='text-align: center; margin-top: 50px;'>VS</h1>",
          unsafe_allow_html=True,
      )

    with col_enemy_field:
      boss_tag = " 🔥【BOSS】" if current_enemy["is_boss"] else ""
      st.markdown(f"### 👹 敵: {current_enemy['name']}{boss_tag}")
      enemy_img = load_image(current_enemy["image"])
      if enemy_img:
        st.image(enemy_img, width=300)
      st.progress(max(0.0, current_enemy["hp"] / current_enemy["max_hp"]))
      st.write(
          f"HP: **{max(0, current_enemy['hp'])} / {current_enemy['max_hp']}** |"
          f" 攻撃: {current_enemy['atk']}"
      )

    st.divider()

    col_act1, col_act2, col_act3 = st.columns(3)

    # ステージに応じたスキル名と倍率の設定
    stage = current_ally["stage"]
    if stage == 1:
      skill_name = "通常攻撃"
      multiplier = 0.4
    elif stage == 2:
      skill_name = f"{current_ally['elem1']}属性の{current_ally['biome']}ブレス"
      multiplier = 0.6
    elif stage == 3:
      skill_name = (
          f"{current_ally['elem2']}を纏う{current_ally['biome']}の咆哮"
      )
      multiplier = 0.8
    else:  # Stage 4
      skill_name = (
          f"神葬解放：{current_ally['elem1']}×{current_ally['elem2']}の"
          f"{current_ally['biome']}・{current_ally['weapon']}"
      )
      multiplier = 1.0

    with col_act1:
      if st.button(
          f"⚔️ {skill_name} ({int(multiplier*100)}%威力)",
          use_container_width=True,
      ):
        dmg_to_enemy = max(
            5, int(current_ally["atk"] * multiplier) - int(current_enemy["def"] * 0.5)
        )
        current_enemy["hp"] -= dmg_to_enemy
        b_state["logs"].insert(
            0,
            f"{current_ally['name']} の **{skill_name}**！"
            f" {current_enemy['name']} に **{dmg_to_enemy}** のダメージ！",
        )

        if current_enemy["hp"] <= 0:
          b_state["logs"].insert(
              0, f"✨ {current_enemy['name']} を倒した！"
          )
          active_e_idx += 1
          b_state["active_enemy_idx"] = active_e_idx

          if active_e_idx >= len(enemies):
            # 勝利処理：ゴールドと経験値を付与
            st.session_state.gold += b_state["reward_gold"]
            exp_gained = b_state["reward_exp"]

            evolution_messages = []
            for c in st.session_state.creatures:
              c["exp"] += exp_gained
              if c["exp"] >= 100 and c["stage"] < 4:
                c["stage"] += 1
                c["exp"] = 0
                evolution_messages.append(
                    f"✨ {c['name']} が ステージ {c['stage']} に進化しました！"
                )

            st.success(
                f"🎉 ダンジョン完全踏破！ 報酬として **{b_state['reward_gold']} G**"
                f" と **EXP +{exp_gained}** を獲得しました！"
            )
            for emsg in evolution_messages:
              st.info(emsg)

            st.session_state.battle_state = None
            st.rerun()
        else:
          dmg_to_ally = max(
              3, current_enemy["atk"] - int(current_ally["def"] * 0.5)
          )
          current_ally["hp"] -= dmg_to_ally
          b_state["logs"].insert(
              0,
              f"{current_enemy['name']} の反撃！ {current_ally['name']} に"
              f" **{dmg_to_ally}** のダメージ！",
          )

          if current_ally["hp"] <= 0:
            b_state["logs"].insert(
                0, f"💥 {current_ally['name']} は戦闘不能になった！"
            )
            alive_indices = [
                i for i, p in enumerate(party) if p["hp"] > 0
            ]
            if not alive_indices:
              st.error(
                  "💀 パーティ全員が戦闘不能になりました…。育成ルームでステータスを強化して再挑戦しましょう。"
              )
              st.session_state.battle_state = None
              st.rerun()
            else:
              b_state["active_party_idx"] = alive_indices[0]
              b_state["logs"].insert(
                  0,
                  f"🔄 控えの {party[alive_indices[0]]['name']}"
                  " が前線に交代した！",
              )
        st.rerun()

    with col_act2:
      alive_party = [
          (i, p) for i, p in enumerate(party) if p["hp"] > 0 and i != active_p_idx
      ]
      if alive_party:
        sub_choice = st.selectbox(
            "交代先選択",
            alive_party,
            format_func=lambda x: f"{x[1]['name']} (HP: {x[1]['hp']})",
            label_visibility="collapsed",
        )
        if st.button("🔄 メンバー交代", use_container_width=True):
          b_state["active_party_idx"] = sub_choice[0]
          b_state["logs"].insert(
              0,
              f"🔄 前線を {party[active_p_idx]['name']} から"
              f" {sub_choice[1]['name']} に交代した！",
          )
          dmg_to_ally = max(
              3, current_enemy["atk"] - int(sub_choice[1]["def"] * 0.5)
          )
          sub_choice[1]["hp"] -= dmg_to_ally
          b_state["logs"].insert(
              0,
              f"敵のスキを突かれ、{sub_choice[1]['name']} に"
              f" **{dmg_to_ally}** のダメージ！",
          )
          if sub_choice[1]["hp"] <= 0:
            b_state["logs"].insert(
                0, f"💥 {sub_choice[1]['name']} は戦闘不能になった！"
            )
            remaining_alive = [
                i for i, p in enumerate(party) if p["hp"] > 0
            ]
            if not remaining_alive:
              st.error("💀 全滅しました…")
              st.session_state.battle_state = None
              st.rerun()
            else:
              b_state["active_party_idx"] = remaining_alive[0]
          st.rerun()
      else:
        st.write("交代できる控えがいません")

    with col_act3:
      if st.button("🏳️ 降参して撤退", use_container_width=True):
        st.warning("⚠️ ダンジョンから撤退しました。")
        st.session_state.battle_state = None
        st.rerun()

    st.divider()
    st.subheader("📜 リアルタイム戦闘ログ")
    for log in b_state["logs"][:8]:
      st.text(log)

# 4. 図鑑
elif menu == "図鑑":
  st.header("📖 神葬アルカディア図鑑")
  unlocked_count = len(st.session_state.unlocked_encyclopedia)
  st.metric(
      label="コンプリート状況",
      value=f"{unlocked_count} / {len(BIOMES) * len(ELEM1) * len(ELEM2) * len(WEAPONS)}",
  )
  st.divider()

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
