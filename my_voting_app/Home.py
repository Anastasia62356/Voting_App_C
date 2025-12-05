#%%writefile app.py
import streamlit as st
import pandas as pd
import mysql.connector

# ---------------------------------------------------------
# 1. 設定 & 定数
# ---------------------------------------------------------
PAGE_TITLE = "投票アプリ"
APP_HEADER = "🗳️ 議題一覧"
APP_DESCRIPTION = "みんなで意見を集めよう！気になる議題に投票できます。"

# ---------------------------------------------------------
# 2. ページ設定
# ---------------------------------------------------------
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="🗳️",
    layout="centered"
)

# ---------------------------------------------------------
# 3. DB接続関数（RDS）
# ---------------------------------------------------------
def get_connection():
    return mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASS"],
        database=st.secrets["DB_NAME"],
        port=3306
    )



# ---------------------------------------------------------
# 5. ヘッダー
# ---------------------------------------------------------
st.title(APP_HEADER)
st.caption(APP_DESCRIPTION)
st.divider()

# ---------------------------------------------------------
# 6. 議題取得（DBから）
# ---------------------------------------------------------
conn = get_connection()
cursor = conn.cursor(dictionary=True)

cursor.execute("SELECT * FROM topics")
topics = cursor.fetchall()

# ---------------------------------------------------------
# 7. 議題表示（カード風・DB連動）
# ---------------------------------------------------------
for topic in topics:
    with st.container(border=True):
        st.subheader(topic["title"])

        col1, col2 = st.columns([1, 2])

        with col1:
            if st.button("👍 投票する", key=f"vote_{topic['id']}"):
                cursor.execute(
                    "UPDATE topics SET votes = votes + 1 WHERE id = %s",
                    (topic["id"],)
                )
                conn.commit()
                st.success("投票しました！")
                st.rerun()  # 即時画面更新

        with col2:
            st.write(f"現在の投票数：{topic['votes']} 票")

cursor.close()
conn.close()

