import streamlit as st
import pandas as pd
import unicodedata
import jaconv
import requests
import io

# テキスト正規化（全角→半角、ひらがな⇔カタカナ統一、アルファベット小文字化）
def normalize_text(text):
    if pd.isna(text):
        return ''
    text = str(text)
    text = unicodedata.normalize('NFKC', text)  # 全角・半角統一
    text = jaconv.kata2hira(text)               # カタカナ→ひらがな
    return text.lower()                         # 小文字化

# スプレッドシートのApps Script公開URL
url = "https://script.google.com/macros/s/AKfycbwbdFEk_z6BYU8lZ-hWKtarlmo3UJACr2oQYOUiJhGQbigiNOxewJ8rsECAHnNDzf_h/exec"

# データ取得
response = requests.get(url)
df = pd.read_json(io.StringIO(response.text), orient='records')

# 曲名が改行で区切られている場合、行を展開する
if '曲名' in df.columns:
    df = df.dropna(subset=['曲名'])
    df['曲名'] = df['曲名'].astype(str)
    df = df.assign(曲名=df['曲名'].str.split('\n')).explode('曲名').reset_index(drop=True)


# 検索対象の列（存在する列のみ使用）
search_columns = ['頭文字', 'アーティスト名', 'アルバム名', '曲名', '所在']
search_columns = [col for col in search_columns if col in df.columns]

# 正規化用列を追加
for col in search_columns:
    df[f"検索用_{col}"] = df[col].apply(normalize_text)

# Streamlit UI
st.markdown("## 🎵 さがすん")

# 検索入力
search_input = st.text_input("🔍 キーワードで検索")

# 検索処理
if search_input:
    search_normalized = normalize_text(search_input)
    mask = pd.Series(False, index=df.index)
    for col in search_columns:
        key = f"検索用_{col}"
        if key in df.columns:
            mask |= df[key].str.contains(search_normalized, na=False)
    df_filtered = df[mask]
else:
    df_filtered = df

# データ表示（検索用列は非表示）
st.write("データ件数:", len(df_filtered))







