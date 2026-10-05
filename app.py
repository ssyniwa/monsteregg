import os
import random
from PIL import Image
import streamlit as st



def get_smart_creature_image(c):
  """個体のステージと現在の要素から、

  最も適した画像を段階的に探して返す（フォールバック機能付き）
  """
  stage = c["stage"]
  biome = c["biome"]
  elem1 = c.get("elem1", "")
  elem2 = c.get("elem2", "")
  weapon = c.get("weapon", "")

  candidate_filenames = []

  # ステージに応じた候補ファイルを「詳細度が高い順」にリストアップ
  if stage == 1:
    # ステージ1: 生物種のみ
    candidate_filenames = [f"stage1_{biome}.png"]
  elif stage == 2:
    # ステージ2: 生物種 + 主属性
    candidate_filenames = [
        f"stage2_{biome}_{elem1}.png",
        f"stage1_{biome}.png",  # なければステージ1へフォールバック
    ]
  elif stage == 3:
    # ステージ3: 生物種 + 主属性 + 副属性
    candidate_filenames = [
        f"stage3_{biome}_{elem1}_{elem2}.png",
        f"stage2_{biome}_{elem1}.png",
        f"stage1_{biome}.png",
    ]
  elif stage >= 4:
    # ステージ4（最終神葬解放）: 全要素
    candidate_filenames = [
        f"final_{biome}_{elem1}_{elem2}_{weapon}.png",
        f"stage3_{biome}_{elem1}_{elem2}.png",
        f"stage1_{biome}.png",
    ]

  # フォルダ内を上から順に探し、最初に見つかった画像を採用する
  for filename in candidate_filenames:
    image_path = os.path.join("assets", filename)
    if os.path.exists(image_path):
      return Image.open(image_path), filename  # 読み込んだ画像と、使ったファイル名を返す

  # 全て見つからない場合のデフォルト画像
  default_path = os.path.join("assets", "default.png")
  if os.path.exists(default_path):
    return Image.open(default_path), "default.png"

  return None, "画像なし"
