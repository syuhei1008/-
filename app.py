import streamlit as st
import pandas as pd
import unicodedata
import os
import datetime

st.set_page_config(page_title="新さがすん", layout="centered")

EXCEL_FILE = "新さがすん.xlsx"

@st.cache_data
def load_data():
    return pd.read_excel(EXCEL_FILE)

def normalize_text(text):
    if pd.isna(text):
        return ""
    text = unicodedata.normalize("NFKC", str(text)).lower()
    return text.translate(str.maketrans(
        "ぁあぃいぅうぇえぉおかがきぎくぐけげこご"
        "さざしじすずせぜそぞただちぢっつづてでとど"
        "なにぬねのはばぱひびぴふぶぷへべぺほぼぽ"
        "まみむめもやゃゆゅよょらりるれろわをんゔゕゖ",
        "ァアィイゥウェエォオカガキギクグケゲコゴ"
        "サザシジスズセゼソゾタダチヂッツヅテデトド"
        "ナニヌネノハバパヒビピフブプヘベペホボポ"
        "マミムメモヤャユュヨョラリルレロワヲンヴヵヶ"
    ))

# 最終更新日の表示
if os.path.exists(EXCEL_FILE):
    last_updated = os.path.getmtime(EXCEL_FILE)
    dt = datetime.datetime.fromtimestamp(last_updated)
    st.markdown(f"<p style='text-align:right;font-size:0.9em;color:gray;'>📅 最終更新日: {dt.strftime('%Y-%m-%d %H:%M')}</p>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>🎵 新さがすん</h2>", unsafe_allow_html=True)

df = load_data()

# 検索用に正規化列を作成
for col in ['頭文字', 'アーティスト名', 'アルバム名', '曲名', '所在']:
    df[f"検索用_{col}"] = df[col].apply(normalize_text)

search = st.text_input("🔍 キーワードで検索", "")

if search:
    search_normalized = normalize_text(search)
    mask = pd.Series(False, index=df.index)
    for col in ['頭文字', 'アーティスト名', 'アルバム名', '曲名', '所在']:
        mask |= df[f"検索用_{col}"].str.contains(search_normalized, na=False)
    df = df[mask]

# あ〜おなどのグループで折りたたみ
head_groups = {
    "あ行": list("アイウエオ"),
    "か行": list("カキクケコ"),
    "さ行": list("サシスセソ"),
    "た行": list("タチツテト"),
    "な行": list("ナニヌネノ"),
    "は行": list("ハヒフヘホ"),
    "ま行": list("マミムメモ"),
    "や行": list("ヤユヨ"),
    "ら行": list("ラリルレロ"),
    "わ行": list("ワヲン"),
    "その他": []
}

for group, initials in head_groups.items():
    group_df = df[df["頭文字"].isin(initials)] if initials else df[~df["頭文字"].isin(sum(head_groups.values(), []))]
    if not group_df.empty:
        with st.expander(f"{group} ({len(group_df)})", expanded=(search != "")):
            st.dataframe(group_df[["頭文字", "アーティスト名", "アルバム名", "曲名", "所在"]], use_container_width=True)
