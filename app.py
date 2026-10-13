import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==================== PHẦN XỬ LÝ DỮ LIỆU (PANDAS) ====================

# #1. Tạo frame
data = {
    'Họ và tên': ['Nguyễn Văn A', 'Trần Thị B', 'Lê Văn C', 'Nguyễn Thị D', 'Phạm Văn E', 
                  'Hoàng Thị F', 'Vũ Văn G', 'Đặng Thị H', 'Bùi Văn I', 'Đỗ Thị K'],
    'Chuyên cần': [8.5, 9.0, 7.5, 6.0, 8.0, 9.5, 5.0, 10.0, 6.5, 7.0],
    'Giữa kỳ': [7.5, 8.0, 6.5, 5.5, 7.0, 8.5, 4.5, 9.0, 6.0, 6.5],
    'Cuối kỳ': [8.0, 8.5, 7.0, 5.0, 7.5, 9.0, 4.0, 9.5, 5.5, 6.0]
}
df = pd.DataFrame(data)

# #2. Tính điểm tổng kết
df['Tong_ket'] = (0.2 * df['Chuyên cần'] + 0.3 * df['Giữa kỳ'] + 0.5 * df['Cuối kỳ']).round(2)

# #3. Xếp loại sinh viên
def phan_loai(diem):
    if diem >= 8.5: return 'Giỏi'
    elif diem >= 7.0: return 'Khá'
    elif diem >= 5.0: return 'Trung bình'
    else: return 'Yếu'
df['Xep_loai'] = df['Tong_ket'].apply(phan_loai)

# #4. Tính toán số liệu thống kê
dtb_lop = df['Tong_ket'].mean().round(2)
max_sv = df.loc[df['Tong_ket'].idxmax()]
min_sv = df.loc[df['Tong_ket'].idxmin()]
so_sv_dat = (df['Tong_ket'] >= 5.0).sum()


# ==================== PHẦN GIAO DIỆN WEB APP (STREAMLIT) ====================

# Hiển thị tiêu đề bài tập
st.title('QUẢN LÝ ĐIỂM SINH VIÊN')

# Hiển thị bảng điểm của 10 sinh viên
st.subheader('📊 Bảng điểm chi tiết')
st.dataframe(df, use_container_width=True)

# Hiển thị các thông tin thống kê tổng hợp của lớp
st.subheader('📈 Thống kê chung của lớp')
col1, col2 = st.columns(2)
with col1:
    st.metric(label="Điểm trung bình cả lớp", value=dtb_lop)
    st.metric(label="Số sinh viên đạt (Điểm >= 5.0)", value=f"{so_sv_dat} / 10")
with col2:
    st.metric(label="Sinh viên cao điểm nhất", value=f"{max_sv['Họ và tên']} ({max_sv['Tong_ket']})")
    st.metric(label="Sinh viên thấp điểm nhất", value=f"{min_sv['Họ và tên']} ({min_sv['Tong_ket']})")

# Tạo danh sách xổ xuống (Selectbox) để tra cứu sinh viên
st.subheader('🔍 Tra cứu thông tin sinh viên')
sinh_vien_duoc_chon = st.selectbox('Chọn một sinh viên để xem chi tiết:', df['Họ và tên'])

# Hiển thị kết quả tra cứu tương ứng
if sinh_vien_duoc_chon:
    thong_tin = df[df['Họ và tên'] == sinh_vien_duoc_chon].iloc[0]
    
    col_sv1, col_sv2 = st.columns(2)
    with col_sv1:
        st.write(f"**Họ và tên:** {thong_tin['Họ và tên']}")
        st.write(f"**Điểm Chuyên cần:** {thong_tin['Chuyên cần']}")
        st.write(f"**Điểm Giữa kỳ:** {thong_tin['Giữa kỳ']}")
    with col_sv2:
        st.write(f"**Điểm Cuối kỳ:** {thong_tin['Cuối kỳ']}")
        st.write(f"**Điểm Tổng kết:** :red[{thong_tin['Tong_ket']}]")
        st.write(f"**Xếp loại:** :blue[{thong_tin['Xep_loai']}]")

# Hiển thị biểu đồ cột điểm tổng kết
st.subheader('📊 Biểu đồ điểm tổng kết')
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.bar(df['Họ và tên'], df['Tong_ket'], color='skyblue', edgecolor='navy')
ax.set_ylabel('Điểm tổng kết')
plt.xticks(rotation=30, ha='right')
plt.ylim(0, 10)

# Chèn điểm số cụ thể lên đầu cột biểu đồ trên web
for i, v in enumerate(df['Tong_ket']):
    ax.text(i, v + 0.1, str(v), ha='center', fontsize=9, fontweight='bold')

st.pyplot(fig)

# Phần chân trang: Hiển thị họ tên và MSSV người tạo (Chữ nhỏ)
st.markdown("---")
st.markdown('<p style="font-size: 12px; color: gray; text-align: center;">Sinh viên thực hiện: Nguyễn Văn A - MSSV: B21DCCN000</p>', unsafe_allow_html=True)
