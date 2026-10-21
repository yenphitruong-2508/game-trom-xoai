import streamlit as st
import random
import time

st.set_page_config(page_title="Trộm Xoài Bị Rượt", page_icon="🥭", layout="centered")

# CSS tạo giao diện sống động
st.markdown("""
<style>
    .main-title { text-align: center; color: #FF4B4B; font-weight: bold; }
    .status-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 15px; }
    .story-box { background-color: #fff3cd; border-left: 5px solid #ffeba2; padding: 15px; border-radius: 5px; font-size: 18px; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# Khởi tạo trạng thái Game (Session State)
if 'state' not in st.session_state:
    st.session_state.state = 'START' # START, STEAL, CHASE, GAMEOVER, WIN
    st.session_state.xoai = 0
    st.session_state.distance = 0 # Quãng đường đã chạy (Mục tiêu 100m)
    st.session_state.gap = 15 # Khoảng cách với chủ nhà/chó (mét)
    st.session_state.boost = 2 # Số lần bấm Tăng tốc
    st.session_state.log = []
    st.session_state.obstacle = None

def add_log(msg):
    st.session_state.log.insert(0, msg)

st.markdown("<h1 class='main-title'>🥭 TRỘM XOÀI: CUỘC RƯỢT ĐUỔI NGHẸT THỞ 🐕💨</h1>", unsafe_allow_html=True)

# ================= 1. BẮT ĐẦU: LEO RÀO =================
if st.session_state.state == 'START':
    st.markdown("""
    ### 🏡 Bên ngoài bờ rào nhà Ông Bảy
    Cây xoài keo trĩu quả vàng ươm đang tỏa hương thơm phức qua hàng rào.
    Bạn đang đứng nhìn thèm rỏ nước miếng...
    """)
    if st.button("🧗 Leo rào chui vào vườn xoài", use_container_width=True):
        st.session_state.state = 'STEAL'
        st.rerun()

# ================= 2. MỞ ĐẦU: HÁI XOÀI & BỊ PHÁT HIỆN =================
elif st.session_state.state == 'STEAL':
    st.markdown("""
    ### 🌳 Đang ở dưới gốc cây xoài!
    Bạn nhẹ nhàng với tay hái từng quả xoài mọng nước...
    """)
    st.metric("🥭 Số xoài đang ôm trên tay", f"{st.session_state.xoai} quả")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🥭 Hái thêm 1 quả nữa", use_container_width=True):
            st.session_state.xoai += random.randint(2, 4)
            st.rerun()
    with col2:
        if st.button("🚨 Ôm đống xoài chuồn thôi!", use_container_width=True) or st.session_state.xoai >= 5:
            st.session_state.state = 'CHASE'
            st.session_state.gap = 15
            st.session_state.distance = 0
            st.session_state.obstacle = random.choice(["Hòn đá to", "Hàng rào thấp", "Vũng bùn trơn"])
            add_log("🐕 **GÂU GÂU GÂU!** Con chó Vàng cất tiếng sủa inh ỏi!")
            add_log("👴 **Ông Bảy vung chổi:** 'Thằng kia! Đứng lại mauuu!'")
            add_log("🏃 Bạn vội ôm chặt đống xoài vắt chân lên cổ chạy!")
            st.rerun()

# ================= 3. RƯỢT ĐUỔI (GAMEPLAY CHÍNH) =================
elif st.session_state.state == 'CHASE':
    # Hiển thị thông số
    col1, col2, col3 = st.columns(3)
    col1.metric("🥭 Xoài ôm trên tay", f"{st.session_state.xoai} quả")
    col2.metric("🏃 Đã chạy được", f"{st.session_state.distance} / 100 m")
    col3.metric("🐕 Khoảng cách chó & chủ nhà", f"{st.session_state.gap} m", delta_color="normal")
    
    # Thanh năng lượng Tăng tốc
    st.progress(min(st.session_state.distance / 100, 1.0), text="Quãng đường thoát hiểm")

    # Nhật ký diễn biến
    if st.session_state.log:
        st.markdown(f"<div class='story-box'>{st.session_state.log[0]}</div>", unsafe_allow_html=True)
    
    st.warning(f"⚠️ **CẢNH BÁO:** Phía trước có **{st.session_state.obstacle}**!")

    # Các nút xử lý hành động
    c1, c2, c3 = st.columns(3)
    action = None
    
    with c1:
        if st.button("🦘 Nhảy cao qua", use_container_width=True):
            action = "NHAY"
    with c2:
        if st.button("🔄 Lách né sang bên", use_container_width=True):
            action = "LACK"
    with c3:
        boost_label = f"⚡ TĂNG TỐC! ({st.session_state.boost} lần)"
        if st.button(boost_label, use_container_width=True, disabled=(st.session_state.boost <= 0)):
            action = "BOOST"

    if action:
        # Xử lý logic
        if action == "BOOST":
            st.session_state.boost -= 1
            st.session_state.distance += 25
            st.session_state.gap += 8
            add_log("🚀 **BẮT TỐC ĐỘ!** Bạn ôm đống xoài bứt tốc xé gió, bỏ xa chó và chủ nhà!")
        else:
            # Tỷ lệ né chướng ngại vật thành công
            correct_action = "NHAY" if st.session_state.obstacle in ["Hòn đá to", "Vũng bùn trơn"] else "LACK"
            
            if action == correct_action:
                st.session_state.distance += 15
                st.session_state.gap += 2
                add_log(f"✨ Bạn xử lý cực nhanh: {action} thành công qua {st.session_state.obstacle}!")
            else:
                st.session_state.distance += 5
                st.session_state.gap -= 6
                st.session_state.xoai = max(0, st.session_state.xoai - 1)
                add_log(f"💥 **RẦM!** Bạn vấp phải {st.session_state.obstacle}, rơi mất 1 quả xoài và bị đuổi sát đít!")

        # Tạo chướng ngại vật mới
        st.session_state.obstacle = random.choice(["Hòn đá to", "Hàng rào thấp", "Vũng bùn trơn", "Bụi rậm Gai"])

        # Kiểm tra thắng / thua
        if st.session_state.gap <= 0:
            st.session_state.state = 'GAMEOVER'
        elif st.session_state.distance >= 100:
            st.session_state.state = 'WIN'
            
        st.rerun()

# ================= 4. KẾT THÚC: THUA =================
elif st.session_state.state == 'GAMEOVER':
    st.error("😭 **BỊ BẮT RỒI!**")
    st.markdown("""
    Con chó Vàng đớp trúng gấu quần, Ông Bảy chạy tới xách tai bạn lên!
    
    * **Thiệt hại:** Mất toàn bộ xoài + Ăn 3 chổi vào mông.
    """)
    if st.button("🔄 Thử lại trận khác!", use_container_width=True):
        st.session_state.state = 'START'
        st.session_state.xoai = 0
        st.session_state.log = []
        st.rerun()

# ================= 5. KẾT THÚC: THẮNG =================
elif st.session_state.state == 'WIN':
    st.balloons()
    st.success("🎉 **TẨU THOÁT THÀNH CÔNG!**")
    st.markdown(f"""
    Bạn đã chạy thoát khỏi tầm mắt của Ông Bảy và con chó Vàng!
    
    🏆 **Thành quả:** Bắt trọn **{st.session_state.xoai} quả xoài keo** chín ngon lành!
    """)
    if st.button("🎮 Chơi lại màn mới", use_container_width=True):
        st.session_state.state = 'START'
        st.session_state.xoai = 0
        st.session_state.log = []
        st.rerun()
