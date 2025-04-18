import streamlit as st
import pandas as pd
import os
from datetime import datetime
import unicodedata

EXCEL_FILE = "新さがすん.xlsx"

# 全角・半角、カタカナ・ひらがなを統一
def normalize_text(text):
    if pd.isna(text):
        return ""
    text = str(text)
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(str.maketrans("ァィゥェォッャュョヮヵヶ", "アイウエオツヤユヨワカケ"))
    text = "".join(["あ" if "ぁ" <= ch <= "お" else
                    "か" if "か" <= ch <= "ご" else
                    "さ" if "さ" <= ch <= "ぞ" else
                    "た" if "た" <= ch <= "ど" else
                    "な" if "な" <= ch <= "の" else
                    "は" if "は" <= ch <= "ぽ" else
                    "ま" if "ま" <= ch <= "も" else
                    "や" if "や" <= ch <= "よ" else
                    "ら" if "ら" <= ch <= "ろ" else
                    "わ" if "わ" <= ch <= "ん" else ch
                    for ch in text])
    return text

@st.cache_data
def load_data():
    return pd.read_excel(EXCEL_FILE)

# 最終更新日
if os.path.exists(EXCEL_FILE):
    last_updated = os.path.getmtime(EXCEL_FILE)
    dt = datetime.fromtimestamp(last_updated)
    st.markdown(f"<p style='text-align:right;font-size:0.9em;color:gray;'>🗓️ 最終更新日: {dt.strftime('%Y-%m-%d %H:%M')}</p>", unsafe_allow_html=True)

# タイトル
st.markdown("<h2 style='text-align: center;'>🎵 新さがすん</h2>", unsafe_allow_html=True)

df = load_data()

# 検索用に正規化列を作成
for col in ["頭文字", "アーティスト名", "アルバム名", "曲名", "所在"]:
    if col in df.columns:
        df[f"検索用_{col}"] = df[col].apply(normalize_text)

# 検索ボックス
search = st.text_input("🔍 キーワードで検索", "")

# フィルタリング
if search:
    search_normalized = normalize_text(search)
    mask = pd.Series(False, index=df.index)
    for col in ["頭文字", "アーティスト名", "アルバム名", "曲名", "所在"]:
        mask |= df[f"検索用_{col_}
        
