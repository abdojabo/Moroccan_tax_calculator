import streamlit as st
import pandas as pd

st.set_page_config(page_title="🇲🇦 Moroccan Tax Calculator", layout="wide")

# Language selector
lang = st.sidebar.selectbox("Language / اللغة", ["Français", "العربية"])

# Translator function
def tr(fr, ar):
    return fr if lang == "Français" else ar

st.title(tr("Calculateur Fiscal Marocain 🇲🇦", "🇲🇦 آلة حساب الضرائب المغربية"))

st.markdown("### " + tr("Choisissez un type de calcul :", "اختر نوع الحساب:"))

tabs = st.tabs([
    tr("IR - Impôt sur le Revenu", "ضريبة الدخل IR"),
    tr("CNSS - Cotisations Sociales", "الضمان الاجتماعي CNSS"),
    tr("IS - Impôt sur les Sociétés", "الضريبة على الشركات IS"),
    tr("TVA - Taxe sur la Valeur Ajoutée", "الضريبة على القيمة المضافة TVA"),
])

# IR Calculation
with tabs[0]:
    st.header(tr("Calcul de l'IR", "حساب ضريبة الدخل"))
    annual_income = st.number_input(tr("Revenu Annuel (MAD)", "الدخل السنوي بالدرهم"), min_value=0.0)
    if annual_income:
        tax = 0
        if annual_income <= 30000:
            tax = 0
        elif annual_income <= 50000:
            tax = (annual_income - 30000) * 0.1
        elif annual_income <= 60000:
            tax = 2000 + (annual_income - 50000) * 0.2
        else:
            tax = 4000 + (annual_income - 60000) * 0.3
        st.metric(tr("IR à Payer", "مبلغ الضريبة"), f"{tax:.2f} MAD")

# CNSS Calculation
with tabs[1]:
    st.header(tr("Cotisations CNSS", "اشتراكات CNSS"))
    salary = st.number_input(tr("Salaire Mensuel (MAD)", "الراتب الشهري بالدرهم"), min_value=0.0)
    if salary:
        employee = salary * 0.044
        employer = salary * 0.1995
        total = employee + employer
        st.info(f"✅ {tr('Part salarié', 'نصيب الموظف')}: {employee:.2f} MAD (4.4%)")
        st.info(f"✅ {tr('Part employeur', 'نصيب المشغل')}: {employer:.2f} MAD (19.95%)")
        st.success(f"{tr('Total CNSS', 'المجموع')}: {total:.2f} MAD")
        # Retard
        st.subheader(tr("Pénalités de Retard", "غرامات التأخير"))
        months_delay = st.slider(tr("Mois de retard", "عدد أشهر التأخير"), 0, 12, 0)
        if months_delay > 0:
            penalty_rate = 0.1  # 10% mensuel (exemple)
            penalty = total * penalty_rate * months_delay
            st.warning(f"📌 {tr('Pénalité estimée', 'مبلغ التأخير التقريبي')}: {penalty:.2f} MAD")

# IS Calculation
with tabs[2]:
    st.header(tr("Impôt sur les Sociétés (IS)", "الضريبة على الشركات (IS)"))
    net_profit = st.number_input(tr("Bénéfice Net Annuel (MAD)", "الربح الصافي السنوي بالدرهم"), min_value=0.0)
    if net_profit:
        is_tax = 0
        if net_profit <= 300000:
            is_tax = net_profit * 0.10
        elif net_profit <= 1000000:
            is_tax = net_profit * 0.20
        else:
            is_tax = net_profit * 0.31
        st.metric(tr("IS à payer", "الضريبة المستحقة"), f"{is_tax:.2f} MAD")

# TVA Calculation
with tabs[3]:
    st.header(tr("Calcul de la TVA", "حساب الضريبة على القيمة المضافة"))
    company = st.text_input(tr("Nom de l'entreprise", "اسم الشركة"))
    tax_id = st.text_input(tr("Identifiant Fiscal", "التعريف الضريبي"))
    invoice_number = st.text_input(tr("Numéro de Facture", "رقم الفاتورة"))
    price = st.number_input(tr("Montant HT (MAD)", "ثمن الفاتورة دون احتساب الضريبة"), min_value=0.0)
    tva_rate = st.selectbox(tr("Taux de TVA", "نسبة الضريبة"), [7, 10, 14, 20])
    if price:
        tva_amount = price * tva_rate / 100
        total_price = price + tva_amount
        st.write(f"✅ {tr('Montant TVA', 'مبلغ الضريبة')}: {tva_amount:.2f} MAD")
        st.write(f"✅ {tr('Montant TTC', 'الثمن الإجمالي')}: {total_price:.2f} MAD")

        # Multiple Entries
        if "tva_data" not in st.session_state:
            st.session_state.tva_data = []
        if st.button(tr("Ajouter cette TVA", "أضف هذه الضريبة")):
            st.session_state.tva_data.append({
                "Entreprise": company,
                "Facture": invoice_number,
                "Montant HT": price,
                "Taux TVA": f"{tva_rate}%",
                "TVA": tva_amount,
                "TTC": total_price,
            })

        if st.session_state.tva_data:
            df = pd.DataFrame(st.session_state.tva_data)
            st.dataframe(df)
            st.write(f"📊 {tr('TVA Totale', 'مجموع الضريبة')} = {df['TVA'].sum():.2f} MAD")
            st.download_button("📥 Télécharger Excel", data=df.to_csv(index=False).encode('utf-8'),
                               file_name="tva_details.csv", mime="text/csv")

# Footer
st.markdown("---")
st.info(tr("📞 Pour toute consultation financière ou comptable, contactez : BOUTAHER Abdeljalil - Expert Comptable",
           "📞 للاستشارة المالية أو المحاسبية، اتصل بـ بوطاهر عبد الجليل - محاسب ومستشار مالي"))
