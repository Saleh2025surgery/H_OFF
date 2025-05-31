
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Compact Handoff Report", layout="centered")
st.title("🔄 Surgical Handoff Submission")

if "patients" not in st.session_state:
    st.session_state.patients = []

def format_patient(data):
    lines = []
    def add(label, value): 
        if value.strip():
            lines.append(f"{label}: {value}")
    def add_line(value): 
        if value.strip():
            lines.append(value)

    add("Name", data["name"])
    add("Room", data["room"])
    add("Specialist", data["specialist"])
    add("Age", data["age"])
    add("Allergy", data["allergy"])
    add("PM Hx", data["pmhx"])
    add("PS Hx", data["pshx"])
    add("Diagnosis", data["diagnosis"])
    add("Operation", data["operation"])
    add("Diet", data["diet"])
    add("IVF", data["ivf"])
    vitals = ", ".join(filter(None, [
        f"BP: {data['bp']}" if data["bp"].strip() else "",
        f"HR: {data['hr']}" if data["hr"].strip() else "",
        f"RR: {data['rr']}" if data["rr"].strip() else "",
        f"Temp: {data['temp']}" if data["temp"].strip() else ""
    ]))
    if vitals:
        lines.append(f"V/S: {vitals}")
    checklist = []
    if data["amb"]: checklist.append("Amb")
    if data["uri"]: checklist.append("Urination")
    if data["eat"]: checklist.append("Diet")
    if data["dress"]: checklist.append("Dress")
    if checklist:
        lines.append("✔️ " + ", ".join(checklist))
    add("Foley", data["foley"])
    add("NGT", data["ngt"])
    add("Drain", data["drain"])
    add("Chest Tube", data["chest_tube"])
    add("Stoma", data["stoma"])
    meds = [m for m in data["meds"] if m.strip()]
    if meds:
        lines.append("Medications: " + "; ".join(meds))
    add("DVT Prophylaxis", data["dvt"])
    add("Analgesia", data["analgesia"])
    add("Notes", data["notes"])
    add("Consult", data["consult"])
    return " | ".join(lines)

st.markdown("Fill in one or more patients. Add each patient below:")

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
    add_patient = st.form_submit_button("➕ Add Patient")

    if add_patient:
        patient = {
            "name": name, "room": room, "specialist": specialist,
            "age": age, "allergy": allergy, "pmhx": pmhx, "pshx": pshx,
            "diagnosis": diagnosis, "operation": operation, "diet": diet,
            "ivf": ivf, "bp": bp, "hr": hr, "rr": rr, "temp": temp,
            "amb": amb, "uri": uri, "eat": eat, "dress": dress,
            "foley": foley, "ngt": ngt, "drain": drain, "chest_tube": chest_tube,
            "stoma": stoma, "meds": meds, "dvt": dvt, "analgesia": analgesia,
            "notes": notes, "consult": consult
        }
        st.session_state.patients.append(patient)
        st.success(f"Added: {name}")

if st.session_state.patients:
    st.subheader("📋 Preview Full Compact Report")
    report_lines = [format_patient(p) for p in st.session_state.patients]
    full_report = "\n".join(report_lines)
    st.text_area("Compact Handoff Summary", full_report, height=400)
    st.download_button("📥 Download as .txt", data=full_report, file_name="handoff_compact.txt", mime="text/plain")
