import streamlit as st
import pandas as pd
import unicodedata
import jaconv
import requests
import io
# テキスト正規化（全角→半角、ひらがな⇄カタカナも統一、アルファベット小文字化など）
def normalize_text(text):
    if pd.isna(text):
        return ''
    text = str(text)
    text = unicodedata.normalize('NFKC', text)  # ← これが正しい
  # 全角・半角を統一
    text = jaconv.kata2hira(text)           # カタカナ→ひらがな に変換
    return text.lower()                     # 小文字化

# スプレッドシートのApps Script公開URL
url = "https://script.google.com/macros/s/AKfycbx6yH3M8l_eQPhx8aTUn3DUEebIUM9GM02IYuSBUwtnZNdXbnB0lzh0TDCeqUbls6wU/exec"

# データ取得
response = requests.get(url)
print(response.text)
df = pd.read_json(io.StringIO(response.text), orient='records')







# 検索対象の列（存在する列のみ使う）
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

# データフレームの表示（検索用の列は非表示）
st.write("データ件数:", len(df_filtered))
st.dataframe(df_filtered[search_columns])


