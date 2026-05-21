import streamlit as st
import time

# ページ設定
st.set_page_config(page_title="券売機シミュレーター", layout="centered")

# セッション状態の初期化
if "step" not in st.session_state:
    st.session_state.step = 1  # 1: 左の画面（自動遷移待機）, 2: 右の画面（確定ボタン待ち）, 3: 完了画面
if "inserted_amount" not in st.session_state:
    st.session_state.inserted_amount = 0

PRICE = 200  # 購入金額

# タイトル
st.title("券売機シミュレーター")

# --- STEP 1: 左の画像（お金を入れる・自動遷移システム） ---
if st.session_state.step == 1:
    st.subheader("【画面1】お金を投入してください")
    
    # 左の画像を表示
    st.image("IMG_2339.jpg", caption="元の画面", use_container_width=True)
    
    # 現在のステータス表示
    shortage = max(0, PRICE - st.session_state.inserted_amount)
    st.metric(label="購入金額", value=f"{PRICE} 円")
    st.metric(label="投入金額", value=f"{st.session_state.inserted_amount} 円")
    st.metric(label="不足金額", value=f"{shortage} 円")
    
    # お金を入れるボタン（モック）
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("100円硬貨を入れる"):
            st.session_state.inserted_amount += 100
            st.rerun()
    with col2:
        if st.button("500円硬貨を入れる"):
            st.session_state.inserted_amount += 500
            st.rerun()
    with col3:
        if st.button("クリア"):
            st.session_state.inserted_amount = 0
            st.rerun()

    # 金額が条件を満たした場合の2秒待機処理
    if st.session_state.inserted_amount >= PRICE:
        st.success("金額が満たされました。2秒後に次の画面へ遷移します...")
        time.sleep(2)  # 2秒間操作を止める（待機）
        st.session_state.step = 2
        st.rerun()

# --- STEP 2: 右の画像（お支払い確定ボタンの画面） ---
elif st.session_state.step == 2:
    st.subheader("【画面2】お支払い確定画面")
    
    # 右の画像を表示
    st.image("Gemini_Generated_Image_yout0uyout0uyout.png", caption="確定ボタン付き画面", use_container_width=True)
    
    st.metric(label="投入金額（確定待ち）", value=f"{st.session_state.inserted_amount} 円")
    
    # お支払い確定ボタン
    # ※Streamlitの標準ボタンは画像の上に重ねられないため、画像の下に配置しています。
    if st.button("お支払い確定", type="primary", use_container_width=True):
        st.session_state.step = 3
        st.rerun()
        
    if st.button("最初に戻る"):
        st.session_state.step = 1
        st.session_state.inserted_amount = 0
        st.rerun()

# --- STEP 3: 購入完了画面 ---
elif st.session_state.step == 3:
    st.subheader("【完了】ありがとうございました！")
    
    change = st.session_state.inserted_amount - PRICE
    st.balloons()
    
    st.success("切符と領収書をお受け取りください。")
    if change > 0:
        st.info(f"お釣り: {change} 円")
        
    if st.button("続けて購入する"):
        st.session_state.step = 1
        st.session_state.inserted_amount = 0
        st.rerun()
