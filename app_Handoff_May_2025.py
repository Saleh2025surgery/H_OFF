import streamlit as st
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_SENDER = "your_email@gmail.com"  # <-- change this
EMAIL_PASSWORD = "your_app_password"   # <-- paste Gmail app password
EMAIL_RECEIVER = "bashammakh97.2.5@gmail.com"

st.set_page_config(page_title="Multi-Patient Surgical Handoff", layout="centered")
st.title("🔄 Surgical Handoff Submission")

st.markdown("Fill out the handoff data for each patient. Click 'Add Patient' to enter a new record.")

if "patients" not in st.session_state:
    st.session_state.patients = []

def format_patient(data):
    meds = "\n".join([f"   {i+1}. {m}" for i, m in enumerate(data["meds"]) if m])
    return f"""
Patient Medical Record
Name: {data["name"]}        Room: {data["room"]}
Specialist: {data["specialist"]}
Age: {data["age"]}        Allergy: {data["allergy"]}

PM Hx (Past Medical History): {data["pmhx"]}
PS Hx (Past Surgical History): {data["pshx"]}

Diagnosis: {data["diagnosis"]}
Operation: {data["operation"]}

Diet: {data["diet"]}
IVF (Intravenous Fluids): {data["ivf"]}

Vital Signs (V/S):
BP: {data["bp"]}, HR: {data["hr"]}, RR: {data["rr"]}, Temp: {data["temp"]}
Ambulation: {"Yes" if data["amb"] else "No"}
Urination: {"Yes" if data["uri"] else "No"}
Diet: {"Yes" if data["eat"] else "No"}
Dress: {"Yes" if data["dress"] else "No"}

Medical Devices:
- Foley's: {data["foley"]}
- NGT: {data["ngt"]}
- Drain: {data["drain"]}
- Chest Tube: {data["chest_tube"]}
- Stoma: {data["stoma"]}

Medications:
{meds}

DVT Prophylaxis: {data["dvt"]}
Analgesia: {data["analgesia"]}

Important Notes:
{data["notes"]}

Consultation: {data["consult"]}
------------------------------------------------------------
"""

with st.form("patient_form", clear_on_submit=True):
    name = st.text_input("Name")
    room = st.text_input("Room")
    specialist = st.text_input("Specialist")
    age = st.text_input("Age")
    allergy = st.text_input("Allergy")
    pmhx = st.text_area("Past Medical History")
    pshx = st.text_area("Past Surgical History")
    diagnosis = st.text_area("Diagnosis")
    operation = st.text_area("Operation")
    diet = st.text_input("Diet")
    ivf = st.text_input("IV Fluids")
    bp = st.text_input("BP")
    hr = st.text_input("HR")
    rr = st.text_input("RR")
    temp = st.text_input("Temp")
    amb = st.checkbox("Ambulation")
    uri = st.checkbox("Urination")
    eat = st.checkbox("Diet Tolerance")
    dress = st.checkbox("Dressing Change")
    foley = st.text_input("Foley")
    ngt = st.text_input("NGT")
    drain = st.text_input("Drain")
    chest_tube = st.text_input("Chest Tube")
    stoma = st.text_input("Stoma")
    meds = [st.text_input(f"Medication {i+1}") for i in range(7)]
    dvt = st.text_input("DVT Prophylaxis")
    analgesia = st.text_input("Analgesia")
    notes = st.text_area("Important Notes")
    consult = st.text_input("Consultation")

    add_patient = st.form_submit_button("➕ Add Patient to Handoff")

    if add_patient:
        patient_data = {
            "name": name, "room": room, "specialist": specialist,
            "age": age, "allergy": allergy, "pmhx": pmhx, "pshx": pshx,
            "diagnosis": diagnosis, "operation": operation, "diet": diet,
            "ivf": ivf, "bp": bp, "hr": hr, "rr": rr, "temp": temp,
            "amb": amb, "uri": uri, "eat": eat, "dress": dress,
            "foley": foley, "ngt": ngt, "drain": drain, "chest_tube": chest_tube,
            "stoma": stoma, "meds": meds, "dvt": dvt, "analgesia": analgesia,
            "notes": notes, "consult": consult
        }
        st.session_state.patients.append(patient_data)
        st.success(f"✅ Patient '{name}' added to handoff list.")

if st.session_state.patients:
    st.subheader("🧾 Patients to Submit")
    for i, p in enumerate(st.session_state.patients):
        st.markdown(f"**{i+1}. {p['name']} (Room {p['room']})**")

    if st.button("📤 Submit All to Email"):
        handoff_text = "\n".join([format_patient(p) for p in st.session_state.patients])
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = "📝 Full Surgical Handoff"
        msg.attach(MIMEText(handoff_text, "plain"))

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                smtp.send_message(msg)
            st.success("✅ Email sent with full handoff summary.")
            st.session_state.patients = []
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")
