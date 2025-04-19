import streamlit as st
import pandas as pd
import unicodedata
import jaconv
# テキスト正規化（全角→半角、ひらがな⇄カタカナも統一、アルファベット小文字化など）
def normalize_text(text):
    if pd.isna(text):
        return ''
    text = str(text)
    text = unicodedata.normalize('NFKC', text)  # 全角・半角を統一
    text = jaconv.kata2hira(text)           # カタカナ→ひらがな に変換
    return text.lower()                     # 小文字化

# Excelファイル読み込み
excel_path = "新さがすん.xlsx"
df = pd.read_excel(excel_path, header=4)



# 検索対象の列（存在する列のみ使う）
search_columns = ['頭文字', 'アーティスト名', 'アルバム名', '曲名', '所在']
search_columns = [col for col in search_columns if col in df.columns]

# 正規化用列を追加
for col in search_columns:
    df[f"検索用_{col}"] = df[col].apply(normalize_text)

# Streamlit UI
st.markdown("## 🎵 さがすん")

# 検索入力
# 検索入力＋クリアボタン
col1, col2 = st.columns([5, 1])


# セッションキーを定義（上で使っている "search_input" と合わせる）
search_input_key = "search_input"


# 🔍 検索欄とクリアボタンの並び表示
col1, col2 = st.columns([5, 1])


search_input_key =st.text_input("🔍 キーワードで検索", key=search_input_key)
# もしセッションステートに存在しない場合は初期化
if search_input_key not in st.session_state:
    st.session_state[search_input_key] = ""
search_input = st.session_state[search_input_key]

with col2:
    if st.button("❌ クリア"):
        st.session_state[search_input_key] = ""
        st.rerun()  # ← 入力クリア後にページを再描画！


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
