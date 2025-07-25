# app.py
import streamlit as st

st.set_page_config(
    page_title="آلة حساب الضرائب المغربية",
    page_icon="🇲🇦",
    layout="wide"
)

st.markdown("""
    <h1 style="text-align:center; color:#b30000;">🇲🇦 آلة حساب الضرائب والتعويضات الاجتماعية المغربية - 2025</h1>
    <p style="text-align:center; font-size:16px;">حسب قانون المالية المغربي لسنة 2025</p>
    <hr>
""", unsafe_allow_html=True)

def calculate_ir(annual_income, retirement=False, loan=False):
    exemption = 0
    if retirement:
        exemption += 5000
    if loan:
        exemption += 5000
    annual_income -= exemption

    tax = 0
    if annual_income <= 30000:
        tax = 0
    elif annual_income <= 50000:
        tax = (annual_income - 30000) * 0.1
    elif annual_income <= 60000:
        tax = 2000 + (annual_income - 50000) * 0.2
    else:
        tax = 4000 + (annual_income - 60000) * 0.3
    return max(tax, 0)

def calculate_cnss(gross_salary):
    employee_share = gross_salary * 0.044
    employer_share = gross_salary * 0.1995
    return employee_share, employer_share

def net_salary(gross_salary, retirement=False, loan=False):
    employee_cnss, _ = calculate_cnss(gross_salary)
    annual_salary = gross_salary * 12
    annual_tax = calculate_ir(annual_salary, retirement, loan)
    monthly_tax = annual_tax / 12
    return gross_salary - employee_cnss - monthly_tax

def calculate_tva(invoice_amount, tva_rate):
    tva_value = invoice_amount * (tva_rate / 100)
    total = invoice_amount + tva_value
    return tva_value, total

tabs = st.tabs(["📊 ضريبة الدخل IR", "🏥 CNSS", "💰 صافي الراتب", "🧾 ضريبة القيمة المضافة TVA"])

with tabs[0]:
    st.subheader("📊 حساب ضريبة الدخل (IR)")
    col1, col2 = st.columns(2)
    with col1:
        annual_income = st.number_input("✅ الدخل السنوي (درهم)", min_value=0.0, step=100.0)
        retirement = st.checkbox("📦 هل لديك تأمين تقاعد بنكي؟")
        loan = st.checkbox("🏠 هل لديك قرض عقاري؟")
    if st.button("🔍 احسب ضريبة الدخل", key="calc_ir"):
        ir_value = calculate_ir(annual_income, retirement, loan)
        st.success(f"💸 الضريبة السنوية المستحقة: **{ir_value:.2f} درهم**")

with tabs[1]:
    st.subheader("🏥 حساب اشتراكات CNSS")
    gross_salary = st.number_input("💵 الراتب الشهري الإجمالي", min_value=0.0, step=100.0)
    if st.button("🔍 احسب اشتراكات CNSS", key="calc_cnss"):
        emp, employer = calculate_cnss(gross_salary)
        st.info(f"👤 مساهمة الموظف: **{emp:.2f} درهم** (4.4%)")
        st.info(f"🏢 مساهمة المشغل: **{employer:.2f} درهم** (19.95%)")

with tabs[2]:
    st.subheader("💰 حساب صافي الراتب الشهري")
    gross_salary_net = st.number_input("💼 الراتب الإجمالي الشهري", min_value=0.0, step=100.0)
    retirement_net = st.checkbox("📦 لديك تأمين تقاعد؟", key="ret_net")
    loan_net = st.checkbox("🏠 لديك قرض؟", key="loan_net")
    if st.button("🔍 احسب الصافي", key="calc_net"):
        net = net_salary(gross_salary_net, retirement_net, loan_net)
        st.success(f"📉 الصافي الشهري: **{net:.2f} درهم**")

with tabs[3]:
    st.subheader("🧾 حساب ضريبة القيمة المضافة (TVA)")
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("🏢 اسم الشركة")
        tax_id = st.text_input("🧾 التعريف الضريبي")
        invoice_number = st.text_input("🔢 رقم الفاتورة")
        invoice_amount = st.number_input("💵 مبلغ الفاتورة بدون ضريبة", min_value=0.0)
    with col2:
        tva_rate = st.selectbox("📌 نسبة TVA", [7, 10, 14, 20])
    if st.button("🔍 احسب TVA", key="calc_tva"):
        tva_value, total = calculate_tva(invoice_amount, tva_rate)
        st.write(f"📄 الشركة: **{company_name}**")
        st.write(f"🧾 التعريف الضريبي: **{tax_id}**, رقم الفاتورة: **{invoice_number}**")
        st.info(f"📌 قيمة TVA: **{tva_value:.2f} درهم**")
        st.success(f"💰 المبلغ الإجمالي مع TVA: **{total:.2f} درهم**")

st.markdown("""
<hr>
<p style="text-align:center; font-size:14px;">
  تم إنشاء هذه الأداة لمساعدتك على حساب الضرائب وفقًا لقانون المالية المغربي لسنة 2025. يرجى مراجعة مستشار ضريبي لتأكيد النتائج.
</p>
""", unsafe_allow_html=True)
