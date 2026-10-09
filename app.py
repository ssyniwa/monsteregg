import os
import random
from PIL import Image
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="神葬アトリエ：本格交代バトル＆育成工房", page_icon="⚔️", layout="wide"
)

# 定数データ
BIOMES = ["ドラゴン型", "獣型", "昆虫型", "飛行型", "水棲型"]
ELEM1 = ["炎", "氷", "雷"]
ELEM2 = ["植物", "血", "結晶"]
WEAPONS = ["ロングソード", "大鎌", "銃", "弓"]

# 種族ごとの基本ステータス補正係数 (HP, 攻撃力, 防御力, 素早さ)
BIOME_STATS = {
    "ドラゴン型": {"hp": 180, "atk": 35, "def": 20, "spd": 10},
    "獣型": {"hp": 140, "atk": 28, "def": 15, "spd": 18},
    "昆虫型": {"hp": 100, "atk": 32, "def": 10, "spd": 25},
    "飛行型": {"hp": 110, "atk": 25, "def": 12, "spd": 30},
    "水棲型": {"hp": 200, "atk": 22, "def": 25, "spd": 8},
}

# 各難易度のステージ（ボス1体 ＋ 配下4体の構成）
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
        "reward_gold": 500,
        "reward_exp": 40,
    },
    "中級：機械神殿の遺跡": {
        "desc": "古代の防衛機構が目覚めた危険な遺跡。",
        "boss": {
            "name": "ガーディアン・ゴーレム (ボス)",
            "image": "enemy_ruins_boss.jpg",
            "hp": 380,
            "atk": 45,
            "def": 25,
        },
        "minions": [
            {
                "name": "ブロークン・ドローン",
                "image": "enemy_ruins_minion1.jpg",
                "hp": 80,
                "atk": 20,
                "def": 10,
            },
            {
                "name": "セントリータレット",
                "image": "enemy_ruins_minion2.jpg",
                "hp": 90,
                "atk": 25,
                "def": 12,
            },
            {
                "name": "ガード・スフィア",
                "image": "enemy_ruins_minion3.jpg",
                "hp": 70,
                "atk": 22,
                "def": 15,
            },
            {
                "name": "プロト・ナイト",
                "image": "enemy_ruins_minion4.jpg",
                "hp": 110,
                "atk": 28,
                "def": 18,
            },
        ],
        "reward_gold": 1200,
        "reward_exp": 70,
    },
    "上級：神葬の塔": {
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
        "reward_gold": 2500,
        "reward_exp": 110,
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
        "reward_gold": 5000,
        "reward_exp": 200,
    },
}

# 初期セッション状態の定義
if "gold" not in st.session_state:
  st.session_state.gold = 1500
if "unlocked_encyclopedia" not in st.session_state:
  st.session_state.unlocked_encyclopedia = []
if "battle_state" not in st.session_state:
  st.session_state.battle_state = None  # バトル中のデータを保持
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

# 1. 育成ルーム
if menu == "育成ルーム":
  st.header("🧪 育成槽（3匹の管理 & 種族特性）")
  st.markdown(
      "種族ごとに**体力・攻撃・防御・素早さ**の特性が異なります。資金を使った育成でさらにステータスを強化できます。"
  )
  cols = st.columns(3)

  for i, c in enumerate(st.session_state.creatures):
    with cols[i]:
      st.subheader(f"{c['name']} (Stage {c['stage']})")
      img, used_file = get_smart_creature_image(c)
      if img:
        st.image(img, use_container_width=True)

      stats = calculate_stats(c)
      st.info(
          f"**生物種**: {c['biome']}\n\n"
          f"**主属性**: {c['elem1']} | **副属性**: {c['elem2']}\n\n"
          f"**武器種**: {c['weapon']}"
      )
      st.markdown(
          f"❤️ **最大HP**: {stats['hp']} | ⚔️ **攻撃**: {stats['atk']} | 🛡️"
          f" **防御**: {stats['def']} | ⚡ **素早さ**: {stats['spd']}"
      )
      st.write(f"成長度 (EXP): {c['exp']}/100")
      st.progress(c["exp"] / 100.0)

      if c["stage"] >= 4:
        key = f"{c['biome']}_{c['elem1']}_{c['elem2']}_{c['weapon']}"
        if key not in st.session_state.unlocked_encyclopedia:
          st.session_state.unlocked_encyclopedia.append(key)

# 2. 素材調合・エサやり (ステータス強化対応)
elif menu == "素材調合・エサやり":
  st.header("🥣 育成・エサやり & ステータス強化カスタム")
  st.markdown(
      "素材と資金(200G)を投資して、生物種や属性の変更だけでなく、個体の**HP・攻撃力・防御力**を直接強化できます。"
  )

  target_idx = st.selectbox(
      "育成・強化する個体を選択",
      [0, 1, 2],
      format_func=lambda x: st.session_state.creatures[x]["name"],
  )
  c = st.session_state.creatures[target_idx]

  col1, col2 = st.columns(2)
  with col1:
    new_biome = st.selectbox(
        "生物種（ベースボディ）", BIOMES, index=BIOMES.index(c["biome"])
    )
    new_elem1 = st.selectbox("主属性", ELEM1, index=ELEM1.index(c["elem1"]))
  with col2:
    new_elem2 = st.selectbox("副属性", ELEM2, index=ELEM2.index(c["elem2"]))
    new_weapon = st.selectbox(
        "武器種", WEAPONS, index=WEAPONS.index(c["weapon"])
    )

  st.divider()
  st.subheader("💪 追加ステータス強化 (費用: 200G)")
  inc_hp = st.number_input("HP強化 (+)", min_value=0, max_value=100, step=10, value=20)
  inc_atk = st.number_input(
      "攻撃力強化 (+)", min_value=0, max_value=50, step=5, value=10
  )
  inc_def = st.number_input(
      "防御力強化 (+)", min_value=0, max_value=50, step=5, value=5
  )

  if st.button("🌟 特製エサを与えて育成・強化する (-200G)"):
    cost = 200
    if st.session_state.gold >= cost:
      st.session_state.gold -= cost
      c["biome"] = new_biome
      c["elem1"] = new_elem1
      c["elem2"] = new_elem2
      c["weapon"] = new_weapon
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
        st.success(
            f"✨ {c['name']} の育成とステータス強化が完了しました！"
        )
      st.rerun()
    else:
      st.error("❌ ゴールドが足りません！バトルステージで稼ぎましょう。")

# 3. 戦闘ステージ出撃（交代制ターンバトル実装）
elif menu == "戦闘ステージ出撃":
  st.header("⚔️ 交代制ターンバトル・ダンジョン探索")

  # バトルが始まっていない場合はステージ選択画面
  if st.session_state.battle_state is None:
    st.write(
        "挑戦するステージを選択してください。各ステージには**ボス1体と配下4体**が待ち受けています。"
    )
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
      # バトルデータの初期化
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
            "image": get_smart_creature_image(c)[1],
        })

      # 敵リストの構築（配下4体 ＋ ボス1体 = 計5体）
      enemies = []
      # 配下4体
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
      # ボス1体
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
          "active_party_idx": 0,  # 現在戦っている味方のインデックス
          "enemies": enemies,
          "active_enemy_idx": 0,  # 現在戦っている敵のインデックス
          "logs": [
              f"=== {selected_stage_name} 戦闘開始 ===",
              f"敵の群れ（配下4体 ＋ ボス1体）が現れた！",
          ],
          "reward_gold": stage_info["reward_gold"],
          "reward_exp": stage_info["reward_exp"],
      }
      st.rerun()

  else:
    # --- バトル中の画面と処理 ---
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

    # 戦闘フィールドの表示（味方 vs 敵）
    col_ally_field, col_vs, col_enemy_field = st.columns([2, 1, 2])

    with col_ally_field:
      st.markdown(
          f"### 🛡️ 味方前衛: {current_ally['name']} ({current_ally['biome']})"
      )
      ally_img = load_image(current_ally["image"])
      if ally_img:
        st.image(ally_img, width=200)
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
        st.image(enemy_img, width=200)
      st.progress(max(0.0, current_enemy["hp"] / current_enemy["max_hp"]))
      st.write(
          f"HP: **{max(0, current_enemy['hp'])} / {current_enemy['max_hp']}** |"
          f" 攻撃: {current_enemy['atk']}"
      )

    st.divider()

    # バトルアクション操作パネル
    col_act1, col_act2, col_act3 = st.columns(3)

    # 1. 攻撃ボタン
    with col_act1:
      if st.button("⚔️ 通常攻撃", use_container_width=True):
        # プレイヤーの攻撃
        dmg_to_enemy = max(
            5, current_ally["atk"] - int(current_enemy["def"] * 0.5)
        )
        current_enemy["hp"] -= dmg_to_enemy
        b_state["logs"].insert(
            0,
            f"{current_ally['name']} の攻撃！ {current_enemy['name']} に"
            f" **{dmg_to_enemy}** のダメージ！",
        )

        # 敵の生存確認
        if current_enemy["hp"] <= 0:
          b_state["logs"].insert(
              0, f"✨ {current_enemy['name']} を倒した！"
          )
          active_e_idx += 1
          b_state["active_enemy_idx"] = active_e_idx

          # 全ての敵を倒したか判定
          if active_e_idx >= len(enemies):
            # 勝利処理
            st.session_state.gold += b_state["reward_gold"]
            for c in st.session_state.creatures:
              c["exp"] += b_state["reward_exp"]
              if c["exp"] >= 100 and c["stage"] < 4:
                c["stage"] += 1
                c["exp"] = 0
            st.success(
                f"🎉 ダンジョン完全踏破！ 報酬 {b_state['reward_gold']} G"
                " を獲得しました！"
            )
            st.session_state.battle_state = None
            st.rerun()
        else:
          # 敵の反撃
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
            # 生きている味方がいるか確認
            alive_indices = [
                i for i, p in enumerate(party) if p["hp"] > 0
            ]
            if not alive_indices:
              st.error(
                  "💀 パーティ全員が戦闘不能になりました…。作戦負けです。"
              )
              st.session_state.battle_state = None
              st.rerun()
            else:
              # 自動で次の生きてるメンバーへ交代
              b_state["active_party_idx"] = alive_indices[0]
              b_state["logs"].insert(
                  0,
                  f"🔄 控えの {party[alive_indices[0]]['name']}"
                  " が前線に交代した！",
              )
        st.rerun()

    # 2. 味方交代セレクト＆ボタン
    with col_act2:
      # 生きているメンバーのみ選択肢に
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
          # 交代時は敵からの反撃ターンになる
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

    # 3. 撤退ボタン
    with col_act3:
      if st.button("🏳️ 降参して撤退", use_container_width=True):
        st.warning(
            "⚠️ ダンジョンから撤退しました。育成し直して再挑戦しましょう。"
        )
        st.session_state.battle_state = None
        st.rerun()

    st.divider()
    st.subheader("📜 リアルタイム戦闘ログ")
    for log in b_state["logs"][:8]:  # 直近8件を表示
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
