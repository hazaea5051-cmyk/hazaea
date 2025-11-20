import streamlit as st
import altair as alt
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import os

# =========================
#     إعدادات الصفحة
# =========================
st.set_page_config(
    page_title="هزاع للخدمات الحسابية",
    page_icon="📊",
    layout="wide"
)

# =========================
#        تصميم A
# =========================
st.markdown("""
    <style>
    body {
        direction: rtl;
        text-align: right;
    }
    .title {
        color: #003366;
        font-size: 38px;
        font-weight: 800;
        text-align: center;
        margin-bottom: -10px;
    }
    .subtitle {
        color: #666666;
        font-size: 18px;
        text-align: center;
        margin-bottom: 40px;
    }
    .metric-box {
        padding: 15px;
        background-color: #f7f9fc;
        border-radius: 12px;
        border: 1px solid #dfe3eb;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
#       العنوان
# =========================
st.markdown('<div class="title">📊 هزاع للخدمات الحسابية</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">حاسبة العائد العقاري بدون قرض + تصدير تقرير PDF</div>', unsafe_allow_html=True)

# =========================
#       المدخلات
# =========================
st.markdown("## 1) بيانات العقار")

col1, col2 = st.columns(2)

with col1:
    property_price = st.number_input("سعر العقار الكلي (درهم)", min_value=0.0, value=2000000.0, step=50000.0)
    area_sqft = st.number_input("مساحة العقار (قدم²)", min_value=0.0, value=1700.0, step=50.0)

with col2:
    monthly_rent = st.number_input("الإيجار الشهري (درهم)", min_value=0.0, value=8500.0, step=500.0)
    annual_rent_input = st.number_input("الإيجار السنوي (إذا 0 → يستخدم الشهري × 12)", min_value=0.0, value=0.0)

st.markdown("## 2) المصاريف السنوية")

col3, col4 = st.columns(2)

with col3:
    service_fee_per_sqft = st.number_input("رسوم الخدمات لكل قدم² (درهم)", min_value=0.0, value=20.0)
    maintenance_cost = st.number_input("تكلفة الصيانة السنوية (درهم)", min_value=0.0, value=10000.0)

with col4:
    management_fee_percent = st.number_input("نسبة إدارة العقار (%)", min_value=0.0, value=5.0)


# =========================
#      الحسابات
# =========================
if st.button("احسب العائد العقاري 🔍"):

    # الإيجار السنوي
    if annual_rent_input > 0:
        annual_rent = annual_rent_input
    else:
        annual_rent = monthly_rent * 12

    # رسوم الخدمات
    service_fee_total = area_sqft * service_fee_per_sqft

    # رسوم إدارة العقار
    management_fee = annual_rent * (management_fee_percent / 100)

    # صافي الدخل الحقيقي
    net_income = annual_rent - service_fee_total - maintenance_cost - management_fee

    # ROI
    if property_price > 0:
        roi = (net_income / property_price) * 100
    else:
        roi = 0

    # =========================
    #       عرض النتائج
    # =========================
    st.markdown("## 3) النتائج")

    r1, r2, r3 = st.columns(3)

    with r1:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("الإيجار السنوي", f"{annual_rent:,.0f} درهم")
        st.metric("رسوم الخدمات", f"{service_fee_total:,.0f} درهم")
        st.markdown('</div>', unsafe_allow_html=True)

    with r2:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("مصاريف الصيانة", f"{maintenance_cost:,.0f} درهم")
        st.metric("رسوم الإدارة", f"{management_fee:,.0f} درهم")
        st.markdown('</div>', unsafe_allow_html=True)

    with r3:
        st.markdown('<div class="metric-box">', unsafe_allow_html=True)
        st.metric("صافي الدخل السنوي", f"{net_income:,.0f} درهم")
        st.metric("العائد على رأس المال ROI", f"{roi:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    #       تقييم العقار
    # =========================
    st.markdown("## 4) تقييم العقار")

    if roi < 3:
        st.error("❌ العائد منخفض وغير مجدٍ استثمارياً.")
    elif roi < 6:
        st.warning("⚠️ العائد متوسط وقد يكون مقبول.")
    elif roi < 10:
        st.info("ℹ️ العائد جيد مقارنة بالسوق.")
    else:
        st.success("🔥 العائد ممتاز ويعتبر فرصة استثمارية قوية.")

    # =========================
    #      إنشاء PDF
    # =========================

    def generate_pdf():
        filename = "hazza_report.pdf"
        c = canvas.Canvas(filename, pagesize=letter)

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "هزاع للخدمات الحسابية - تقرير العائد العقاري")

        c.setFont("Helvetica", 12)
        c.drawString(50, 720, f"تاريخ التقرير: {datetime.datetime.now().strftime('%Y-%m-%d')}")

        c.drawString(50, 690, f"سعر العقار: {property_price:,.0f} درهم")
        c.drawString(50, 670, f"المساحة: {area_sqft:,.0f} قدم²")
        c.drawString(50, 650, f"الإيجار السنوي: {annual_rent:,.0f} درهم")
        c.drawString(50, 630, f"رسوم الخدمات: {service_fee_total:,.0f} درهم")
        c.drawString(50, 610, f"تكلفة الصيانة: {maintenance_cost:,.0f} درهم")
        c.drawString(50, 590, f"رسوم الإدارة: {management_fee:,.0f} درهم")
        c.drawString(50, 570, f"صافي الدخل السنوي: {net_income:,.0f} درهم")
        c.drawString(50, 550, f"العائد على رأس المال ROI: {roi:.2f}%")

        c.setFont("Helvetica-Bold", 13)
        c.drawString(50, 515, "تقييم العقار:")
        c.setFont("Helvetica", 12)

        if roi < 3:
            c.drawString(50, 495, "❌ العائد منخفض وغير مجدٍ استثمارياً.")
        elif roi < 6:
            c.drawString(50, 495, "⚠️ العائد متوسط وقد يكون مقبول.")
        elif roi < 10:
            c.drawString(50, 495, "ℹ️ العائد جيد مقارنة بالسوق.")
        else:
            c.drawString(50, 495, "🔥 العائد ممتاز ويعتبر فرصة استثمارية قوية.")

        c.save()
        return filename

    # =========================
    #     زر تحميل PDF
    # =========================
    st.markdown("## 5) تصدير النتائج إلى PDF")

    if st.button("📄 تحميل تقرير PDF"):
        pdf_file = generate_pdf()
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📥 اضغط لتنزيل التقرير",
                data=f,
                file_name="Hazza_Property_Report.pdf",
                mime="application/pdf"
            )