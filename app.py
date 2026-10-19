import random
import streamlit as st

st.set_page_config(page_title="Trộm Xoài Bị Rượt!", page_icon="🥭", layout="centered")

st.title("🥭 HÀNH TRÌNH TRỘM XOÀI BỊ CHỦ NHÀ RƯỢT 🐕")
st.caption("Game nhập vai hài hước dựng bằng Streamlit")

# Khởi tạo trạng thái Game
if "game_started" not in st.session_state:
  st.session_state.game_started = False
if "xoai_count" not in st.session_state:
  st.session_state.xoai_count = 0
if "stamina" not in st.session_state:
  st.session_state.stamina = 100
if "distance" not in st.session_state:
  st.session_state.distance = 20
if "game_over" not in st.session_state:
  st.session_state.game_over = False
if "win" not in st.session_state:
  st.session_state.win = False
if "log" not in st.session_state:
  st.session_state.log = []


def reset_game():
  st.session_state.game_started = True
  st.session_state.xoai_count = 0
  st.session_state.stamina = 100
  st.session_state.distance = 20
  st.session_state.game_over = False
  st.session_state.win = False
  st.session_state.log = [
      "🔥 Bạn đã leo lên cây xoài nhà ông Bảy. Xoài trĩu quả vàng ươm!"
  ]


# Màn hình bắt đầu
if not st.session_state.game_started:
  st.write(
      "**Mục tiêu:** Trộm càng nhiều xoài càng tốt và tẩu thoát an toàn về"
      " nhà!"
  )
  st.write(
      "**Cảnh báo:** Ông Bảy có cầm chổi lông gà và thả cả chó Becgie đuổi theo"
      " đấy!"
  )
  if st.button("🚀 Bắt đầu trộm xoài!", type="primary"):
    reset_game()
    st.rerun()

# Màn hình chơi game
else:
  st.subheader("📜 Diễn biến:")
  for msg in st.session_state.log[-4:]:
    st.write(f"- {msg}")

  st.divider()

  col1, col2, col3 = st.columns(3)
  col1.metric("🥭 Số xoài hái được", f"{st.session_state.xoai_count} quả")
  col2.metric("⚡ Thể lực", f"{st.session_state.stamina}%")
  col3.metric(
      "🏃 Cự ly với chủ nhà",
      f"{st.session_state.distance} m",
      delta_color="inverse",
  )

  if st.session_state.distance < 10:
    st.error("🚨 CHỦ NHÀ ĐÃ Ở NGAY SAU LƯNG BẠN! CHẠY MAU!")
  elif st.session_state.distance < 20:
    st.warning("⚠️ Đang nghe tiếng chó sủi 'Gâu gâu' rất gần!")

  st.divider()

  if st.session_state.game_over:
    if st.session_state.win:
      st.balloons()
      st.success(
          "🎉 **BẠN ĐÃ TẨU THOÁT THÀNH CÔNG!**\n\n"
          f"Bạn đã mang về **{st.session_state.xoai_count} quả xoài** ngon lành!"
      )
    else:
      st.error(
          "💥 **BẠN ĐÃ BỊ BẮT!**\n\n"
          "Ông Bảy đã gõ chổi vô mông bạn và tịch thu toàn bộ số xoài!"
      )

    if st.button("🔄 Chơi lại trận khác"):
      reset_game()
      st.rerun()

  else:
    st.subheader("🎯 Bạn sẽ làm gì tiếp theo?")
    c1, c2, c3, c4 = st.columns(4)

    if c1.button("🥭 Hái xoài"):
      hái = random.randint(1, 3)
      st.session_state.xoai_count += hái
      bị_đuổi = random.randint(3, 6)
      st.session_state.distance -= bị_đuổi
      st.session_state.log.append(
          f"Bạn hái được {hái} quả xoài! Nhưng chủ nhà áp sát thêm {bị_đuổi}m."
      )

      if st.session_state.distance <= 0:
        st.session_state.game_over = True
      st.rerun()

    if c2.button("🏃 Chạy thục mạng"):
      if st.session_state.stamina >= 15:
        st.session_state.stamina -= 15
        tiến = random.randint(5, 9)
        st.session_state.distance += tiến
        st.session_state.log.append(
            f"Bạn chạy thục mạng, tạo khoảng cách thêm {tiến}m!"
        )

        if st.session_state.distance >= 40:
          st.session_state.win = True
          st.session_state.game_over = True
      else:
        st.session_state.log.append("❌ Bạn đã quá mệt!")
      st.rerun()

    if c3.button("💥 Ném xoài dụ chó"):
      if st.session_state.xoai_count > 0:
        st.session_state.xoai_count -= 1
        st.session_state.distance += 6
        st.session_state.log.append(
            "Bạn ném 1 quả xoài ra xa dụ con chó, chạy xa thêm 6m!"
        )
      else:
        st.session_state.log.append("❌ Bạn không còn xoài để ném!")
      st.rerun()

    if c4.button("😮‍💨 Nghỉ lấy sức"):
      st.session_state.stamina = min(100, st.session_state.stamina + 25)
      bị_đuổi = random.randint(4, 7)
      st.session_state.distance -= bị_đuổi
      st.session_state.log.append(
          f"Bạn nghỉ lấy sức (+25%). Chủ nhà tiến lại thêm {bị_đuổi}m!"
      )

      if st.session_state.distance <= 0:
        st.session_state.game_over = True
      st.rerun()