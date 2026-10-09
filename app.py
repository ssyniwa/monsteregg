import os
import random
from PIL import Image
import streamlit as st

# ページ設定
st.set_page_config(
    page_title="神葬アトリエ：本格戦闘＆育成工房", page_icon="⚔️", layout="wide"
)

# 定数データ
BIOMES = ["ドラゴン型", "獣型", "昆虫型", "飛行型", "水棲型"]
ELEM1 = ["炎", "氷", "雷"]
ELEM2 = ["植物", "血", "結晶"]
WEAPONS = ["ロングソード", "大鎌", "銃", "弓"]

# 戦闘ステージの定義（敵情報や難易度）
BATTLE_STAGES = {
    "初級：魔石の林": {
        "desc": "魔力を帯びた植物と小型モンスターがうろつく森。",
        "enemy_name": "フォレスト・キメラ",
        "enemy_image": "enemy_forest.jpg",
        "enemy_hp": 150,
        "enemy_atk": 20,
        "reward_gold": 300,
        "reward_exp": 30,
    },
    "中級：機械神殿の遺跡": {
        "desc": "古代の防衛機構が目覚めた危険な遺跡。",
        "enemy_name": "ガーディアン・ゴーレム",
        "enemy_image": "enemy_ruins.jpg",
        "enemy_hp": 300,
        "enemy_atk": 45,
        "reward_gold": 700,
        "reward_exp": 50,
    },
    "上級：神葬の塔": {
        "desc": "神話の兵器が眠る、過酷な試練の塔。",
        "enemy_name": "ファントム・ナイト",
        "enemy_image": "enemy_tower.jpg",
        "enemy_hp": 550,
        "enemy_atk": 80,
        "reward_gold": 1500,
        "reward_exp": 80,
    },
    "最上級：アルカディアの王座": {
        "desc": "すべての頂点に君臨する、神話級の守護者との決戦。",
        "enemy_name": "神葬の主・ゼニス",
        "enemy_image": "enemy_god.jpg",
        "enemy_hp": 900,
        "enemy_atk": 120,
        "reward_gold": 3000,
        "reward_exp": 150,
    },
}

# 初期セッション状態の定義
if "gold" not in st.session_state:
  st.session_state.gold = 1000
if "unlocked_encyclopedia" not in st.session_state:
  st.session_state.unlocked_encyclopedia = []
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
# 画像読み込み関数（フォールバック付き）
# ==========================================
def get_smart_creature_image(c):
  stage = c["stage"]
  biome = c["biome"]
  elem1 = c["elem1"]
  elem2 = c["elem2"]
  weapon = c["weapon"]

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


def load_enemy_image(filename):
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
st.title("⚔️ 神葬アトリエ：本格戦闘＆育成工房")
st.sidebar.markdown(f"### 💰 所持金: {st.session_state.gold} G")

menu = st.sidebar.selectbox(
    "メニュー", ["育成ルーム", "素材調合・エサやり", "戦闘ステージ出撃", "図鑑"]
)

# 1. 育成ルーム
if menu == "育成ルーム":
  st.header("🧪 育成槽（3匹の管理）")
  cols = st.columns(3)

  for i, c in enumerate(st.session_state.creatures):
    with cols[i]:
      st.subheader(f"{c['name']} (Stage {c['stage']})")
      img, used_file = get_smart_creature_image(c)
      if img:
        st.image(img, use_container_width=True)
      else:
        st.warning("🖼️ 画像が見つかりません")

      st.info(
          f"**生物種**: {c['biome']}\n\n"
          f"**主属性**: {c['elem1']} | **副属性**: {c['elem2']}\n\n"
          f"**武器種**: {c['weapon']}"
      )
      st.write(f"成長度 (EXP): {c['exp']}/100")
      st.progress(c["exp"] / 100.0)

      if c["stage"] >= 4:
        key = f"{c['biome']}_{c['elem1']}_{c['elem2']}_{c['weapon']}"
        if key not in st.session_state.unlocked_encyclopedia:
          st.session_state.unlocked_encyclopedia.append(key)

# 2. 素材調合・エサやり
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
    new_biome = st.selectbox(
        "生物種（ベースボディ）", BIOMES, index=BIOMES.index(c["biome"])
    )
    new_elem1 = st.selectbox("主属性", ELEM1, index=ELEM1.index(c["elem1"]))
  with col2:
    new_elem2 = st.selectbox("副属性", ELEM2, index=ELEM2.index(c["elem2"]))
    new_weapon = st.selectbox(
        "武器種", WEAPONS, index=WEAPONS.index(c["weapon"])
    )

  if st.button("🌟 特製エサを与えて育成する (-100G)"):
    if st.session_state.gold >= 100:
      st.session_state.gold -= 100
      c["biome"] = new_biome
      c["elem1"] = new_elem1
      c["elem2"] = new_elem2
      c["weapon"] = new_weapon
      c["exp"] += 40

      if c["exp"] >= 100 and c["stage"] < 4:
        c["stage"] += 1
        c["exp"] = 0
        st.success(
            f"✨ {c['name']} が ステージ {c['stage']} に進化しました！"
        )
      elif c["stage"] >= 4:
        c["exp"] = 100
        st.success(f"✨ {c['name']} のステータスが更新されました！")
      else:
        st.success(f"{c['name']} にエサを与えました！")
      st.rerun()
    else:
      st.error("❌ ゴールドが足りません！")

# 3. 戦闘ステージ出撃（本格ターン制バトル）
elif menu == "戦闘ステージ出撃":
  st.header("⚔️ 本格バトル・ダンジョン探索")
  st.write(
      "育てた3匹のチームで強敵に挑みます。各個体の進化ステージや装備が戦闘力を大きく左右します。"
  )

  selected_stage_name = st.selectbox(
      "挑戦するステージを選択", list(BATTLE_STAGES.keys())
  )
  stage_info = BATTLE_STAGES[selected_stage_name]

  # 敵情報の表示
  col_enemy_info, col_enemy_img = st.columns([2, 1])
  with col_enemy_info:
    st.subheader(f"🛡️ 遭遇エネミー: {stage_info['enemy_name']}")
    st.markdown(f"*{stage_info['desc']}*")
    st.metric(label="敵HP", value=stage_info["enemy_hp"])
    st.metric(label="敵攻撃力", value=stage_info["enemy_atk"])
    st.write(
        f"🎁 勝利報酬: 💰 **{stage_info['reward_gold']} G** / 🌟 経験値"
        f" **{stage_info['reward_exp']}**"
    )

  with col_enemy_img:
    enemy_img = load_enemy_image(stage_info["enemy_image"])
    if enemy_img:
      st.image(
          enemy_img,
          use_container_width=True,
          caption=stage_info["enemy_name"],
      )

  st.divider()

  if st.button("🚀 チーム出撃！ ターン制バトル開始"):
    # チームの総合戦闘力計算（ステージが高いほど有利、武器種や進化段階が影響）
    total_party_power = sum(
        [
            (c["stage"] * 40)
            + (50 if c["stage"] == 4 else 0)
            + random.randint(10, 30)
            for c in st.session_state.creatures
        ]
    )
    enemy_hp = stage_info["enemy_hp"]
    enemy_atk = stage_info["enemy_atk"]

    # 簡易ターンシミュレーション
    battle_logs = []
    turn = 1
    victory = False

    while turn <= 5:
      # プレイヤーチームの攻撃
      party_damage = total_party_power + random.randint(-10, 20)
      enemy_hp -= party_damage
      battle_logs.append(
          f"ターン {turn}: チームの総攻撃！ 敵に **{party_damage}** のダメージ！"
          f" (残り敵HP: {max(0, enemy_hp)})"
      )

      if enemy_hp <= 0:
        victory = True
        break

      # 敵の反撃
      battle_logs.append(
          f"ターン {turn}: 敵の反撃！ チームに **{enemy_atk}** のダメージ！"
      )
      turn += 1

    # 結果判定
    st.subheader("📜 戦闘ログ")
    for log in battle_logs:
      st.write(log)

    if victory or enemy_hp <= 0:
      reward_g = stage_info["reward_gold"]
      reward_e = stage_info["reward_exp"]
      st.session_state.gold += reward_g

      for c in st.session_state.creatures:
        c["exp"] += reward_e
        if c["exp"] >= 100 and c["stage"] < 4:
          c["stage"] += 1
          c["exp"] = 0

      st.success(
          f"🎉 討伐成功！ 報酬として **{reward_g} G** を獲得し、3匹全員が強くなりました！"
      )
    else:
      st.error(
          "⚠️ 敵の圧倒的な力の前に敗北しました…。育成ルームでさらに特訓・進化させてから挑みましょう！"
      )

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
