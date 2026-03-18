-- KAKI Care Mock Data: Marcus (CHF Demo Patient)
-- Run this AFTER creating the schema
-- Safe to rerun - clears all data first

-- Clear all tables (order matters due to foreign keys)
TRUNCATE TABLE wearables, personal_info, medications, documents, metrics, users RESTART IDENTITY CASCADE;

-- 1. Insert Marcus into users table
INSERT INTO users (name, age, disease_profile) VALUES (
  'Marcus',
  67,
  '{
    "diseases": [
      {
        "name": "CHF",
        "nyha_class": "II",
        "ejection_fraction": "40%",
        "comorbidities": ["hypertension", "type 2 diabetes"],
        "metrics": ["daily_weight", "heart_rate", "spo2", "bp_systolic", "bp_diastolic"],
        "thresholds": {
          "daily_weight": "gain >2kg in 2 days",
          "spo2": "below 94%",
          "heart_rate": "resting HR >100 bpm or >20% above baseline",
          "bp_systolic": "above 180 or below 90",
          "bp_diastolic": "above 120 or below 60"
        },
        "symptom_options": [
          "shortness_of_breath",
          "ankle_swelling",
          "fatigue",
          "chest_discomfort",
          "dizziness",
          "night_coughing",
          "difficulty_lying_flat"
        ],
        "mood_options": ["great", "good", "okay", "bad", "struggling"]
      }
    ],
    "medications": [
      {"name": "Lisinopril", "dosage": "10mg", "times": ["08:00"]},
      {"name": "Carvedilol", "dosage": "25mg", "times": ["08:00"]},
      {"name": "Furosemide", "dosage": "40mg", "times": ["08:00", "14:00", "20:00"]}
    ]
  }'::jsonb
);

-- 2. Insert 14 days of metrics (daily vitals)
-- Note: Includes anomaly on Mar 15-16 (weight spike from 75.5 to 77.8kg)
INSERT INTO metrics (user_id, date, readings) VALUES
(1, '2026-03-05', '{"weight": 75.2, "bp_systolic": 128, "bp_diastolic": 82, "mood": "good", "symptoms": []}'::jsonb),
(1, '2026-03-06', '{"weight": 75.3, "bp_systolic": 130, "bp_diastolic": 80, "mood": "good", "symptoms": []}'::jsonb),
(1, '2026-03-07', '{"weight": 75.1, "bp_systolic": 126, "bp_diastolic": 78, "mood": "great", "symptoms": []}'::jsonb),
(1, '2026-03-08', '{"weight": 75.4, "bp_systolic": 132, "bp_diastolic": 84, "mood": "okay", "symptoms": ["fatigue"]}'::jsonb),
(1, '2026-03-09', '{"weight": 75.2, "bp_systolic": 129, "bp_diastolic": 81, "mood": "good", "symptoms": []}'::jsonb),
(1, '2026-03-10', '{"weight": 75.5, "bp_systolic": 131, "bp_diastolic": 80, "mood": "good", "symptoms": []}'::jsonb),
(1, '2026-03-11', '{"weight": 75.3, "bp_systolic": 127, "bp_diastolic": 79, "mood": "good", "symptoms": []}'::jsonb),
(1, '2026-03-12', '{"weight": 75.6, "bp_systolic": 133, "bp_diastolic": 82, "mood": "okay", "symptoms": []}'::jsonb),
(1, '2026-03-13', '{"weight": 75.8, "bp_systolic": 135, "bp_diastolic": 85, "mood": "okay", "symptoms": ["fatigue"]}'::jsonb),
(1, '2026-03-14', '{"weight": 76.2, "bp_systolic": 138, "bp_diastolic": 86, "mood": "bad", "symptoms": ["fatigue", "ankle_swelling"]}'::jsonb),
(1, '2026-03-15', '{"weight": 77.0, "bp_systolic": 142, "bp_diastolic": 88, "mood": "bad", "symptoms": ["fatigue", "ankle_swelling", "shortness_of_breath"]}'::jsonb),
(1, '2026-03-16', '{"weight": 77.8, "bp_systolic": 145, "bp_diastolic": 90, "mood": "struggling", "symptoms": ["fatigue", "ankle_swelling", "shortness_of_breath", "difficulty_lying_flat"]}'::jsonb),
(1, '2026-03-17', '{"weight": 76.5, "bp_systolic": 136, "bp_diastolic": 84, "mood": "okay", "symptoms": ["fatigue", "ankle_swelling"]}'::jsonb),
(1, '2026-03-18', '{"weight": 75.8, "bp_systolic": 132, "bp_diastolic": 82, "mood": "okay", "symptoms": ["fatigue"]}'::jsonb);

-- 3. Insert documents (EHR + Transcript)
INSERT INTO documents (user_id, document_name, content) VALUES
(1, 'EHR - Discharge Summary (Jan 2024)', 
'DISCHARGE SUMMARY

Patient: Marcus Chen
DOB: 1959-05-12
Age: 67 years
MRN: 2847561

ADMISSION DATE: 2024-01-15
DISCHARGE DATE: 2024-01-22

PRIMARY DIAGNOSIS:
Congestive Heart Failure (CHF) - NYHA Class II
ICD-10: I50.9

SECONDARY DIAGNOSES:
- Essential Hypertension (I10)
- Type 2 Diabetes Mellitus without complications (E11.9)

CLINICAL FINDINGS:
- Ejection Fraction: 40% (mild to moderate reduction)
- BNP on admission: 850 pg/mL (elevated)
- Chest X-ray: Mild cardiomegaly, no acute infiltrates
- ECG: Normal sinus rhythm, no acute changes

HOSPITAL COURSE:
Patient admitted with shortness of breath and bilateral lower extremity edema. Responded well to IV diuretics. Transitioned to oral medications with good response. Weight decreased from 79kg to 75kg during admission.

DISCHARGE MEDICATIONS:
1. Lisinopril 10mg - once daily in the morning
2. Carvedilol 25mg - once daily in the morning
3. Furosemide 40mg - three times daily (8AM, 2PM, 8PM)
4. Metformin 500mg - twice daily with meals (for diabetes)

DISCHARGE INSTRUCTIONS:
- Daily weight monitoring - report gain >2kg in 2 days
- Low sodium diet (<2000mg/day)
- Fluid restriction 1.5-2L/day
- Monitor for warning signs: increased shortness of breath, leg swelling, difficulty lying flat, rapid weight gain
- Follow up with cardiology in 2 weeks

FOLLOW-UP APPOINTMENTS:
- Dr. Sarah Chen, Cardiology - Mount Sinai - 2024-02-05 at 10:00 AM

Attending Physician: Dr. James Wong, MD
Cardiology Department
Mount Sinai Medical Center'),

(1, 'Transcript - Cardiology Follow-up (Feb 2024)',
'APPOINTMENT TRANSCRIPT

Date: 2024-02-05
Patient: Marcus Chen
Provider: Dr. Sarah Chen, Cardiologist

---

Dr. Chen: Hi Marcus, how have you been feeling since your discharge?

Marcus: Much better overall. The swelling in my legs has gone down a lot. I have been checking my weight every morning like you asked.

Dr. Chen: Great to hear. What has your weight been?

Marcus: It has been pretty steady around 75 to 75.5 kg. One day it went up to 76 but came back down the next day.

Dr. Chen: That is good. A small fluctuation like that is normal. We worry when it goes up more than 2 kg in just a couple of days. How about your breathing?

Marcus: Better than before I was admitted. I can walk around the house without getting too winded. Going up stairs is still a bit hard though.

Dr. Chen: That is expected for NYHA Class II. You should be comfortable at rest and with light activity, but moderate exertion like stairs may cause some symptoms. Are you taking all your medications?

Marcus: Yes, the Lisinopril and Carvedilol in the morning, and the Furosemide three times a day. Sometimes I forget the afternoon dose if I am out.

Dr. Chen: Try to be consistent with the Furosemide especially. It helps keep fluid from building up. Missing doses can lead to the swelling coming back. Maybe set a phone alarm?

Marcus: Good idea, I will do that.

Dr. Chen: Any dizziness, chest pain, or palpitations?

Marcus: No chest pain. Sometimes I feel a bit lightheaded when I stand up too fast.

Dr. Chen: That can happen with your blood pressure medications. Try standing up slowly. If it gets worse or you feel faint, let me know.

Dr. Chen: Overall you are doing well. Keep monitoring your weight daily. If you gain more than 2 kg in 2 days, or if you notice your ankles swelling again, shortness of breath getting worse, or you cannot lie flat at night, call us right away or go to the ER.

Marcus: Understood.

Dr. Chen: I will see you again in 3 months unless anything comes up. Take care Marcus.

Marcus: Thank you Dr. Chen.');

-- 4. Insert personal_info (AI-extracted notable events from chat)
INSERT INTO personal_info (user_id, timestamp, extracted_info) VALUES
(1, '2026-03-08 22:30:00+00', 'Patient reported feeling more tired than usual after walking to the mailbox'),
(1, '2026-03-13 03:15:00+00', 'Patient woke up at 3AM feeling bloated and had difficulty falling back asleep'),
(1, '2026-03-14 19:45:00+00', 'Patient noticed shoes feeling tighter, mentioned ankle swelling'),
(1, '2026-03-15 08:20:00+00', 'Patient reported needing extra pillow to sleep comfortably'),
(1, '2026-03-16 10:30:00+00', 'Patient expressed concern about rapid weight gain, feeling anxious about condition');

-- 5. Insert 14 days of medication adherence
-- Note: Missed PM doses on Mar 13 and Mar 14
INSERT INTO medications (user_id, date, taken) VALUES
(1, '2026-03-05', '{"Lisinopril": {"08:00": true}, "Carvedilol": {"08:00": true}, "Furosemide": {"08:00": true, "14:00": true, "20:00": true}}'::jsonb),
(1, '2026-03-06', '{"Lisinopril": {"08:00": true}, "Carvedilol": {"08:00": true}, "Furosemide": {"08:00": true, "14:00": true, "20:00": true}}'::jsonb),
(1, '2026-03-07', '{"Lisinopril": {"08:00": true}, "Carvedilol": {"08:00": true}, "Furosemide": {"08:00": true, "14:00": true, "20:00": true}}'::jsonb),
(1, '2026-03-08', '{"Lisinopril": {"08:00": true}, "Carvedilol": {"08:00": true}, "Furosemide": {"08:00": true, "14:00": true, "20:00": true}}'::jsonb),
(1, '2026-03-09', '{"Lisinopril": {"08:00": true}, "Carvedilol": {"08:00": true}, "Furosemide": {"08:00": true, "14:00": true, "20:00": true}}'::jsonb),
(1, '2026-03-10', '{"Lisinopril": {"08:00": true}, "Carvedilol": {"08:00": true}, "Furosemide": {"08:00": true, "14:00": true, "20:00": true}}'::jsonb),
(1, '2026-03-11', '{"Lisinopril": {"08:00": true}, "Carvedilol": {"08:00": true}, "Furosemide": {"08:00": true, "14:00": true, "20:00": true}}'::jsonb),
(1, '2026-03-12', '{"Lisinopril": {"08:00": true}, "Carvedilol": {"08:00": true}, "Furosemide": {"08:00": true, "14:00": true, "20:00": true}}'::jsonb),
(1, '2026-03-13', '{"Lisinopril": {"08:00": true}, "Carvedilol": {"08:00": true}, "Furosemide": {"08:00": true, "14:00": true, "20:00": false}}'::jsonb),
(1, '2026-03-14', '{"Lisinopril": {"08:00": true}, "Carvedilol": {"08:00": true}, "Furosemide": {"08:00": true, "14:00": false, "20:00": false}}'::jsonb),
(1, '2026-03-15', '{"Lisinopril": {"08:00": true}, "Carvedilol": {"08:00": true}, "Furosemide": {"08:00": true, "14:00": true, "20:00": true}}'::jsonb),
(1, '2026-03-16', '{"Lisinopril": {"08:00": true}, "Carvedilol": {"08:00": true}, "Furosemide": {"08:00": true, "14:00": true, "20:00": true}}'::jsonb),
(1, '2026-03-17', '{"Lisinopril": {"08:00": true}, "Carvedilol": {"08:00": true}, "Furosemide": {"08:00": true, "14:00": true, "20:00": true}}'::jsonb),
(1, '2026-03-18', '{"Lisinopril": {"08:00": true}, "Carvedilol": {"08:00": true}, "Furosemide": {"08:00": true, "14:00": true, "20:00": true}}'::jsonb);

-- 6. Insert wearables data (last 7 days, multiple entries per day)
-- Note: Elevated HR and low SpO2 on Mar 15-16 (correlates with decompensation)
INSERT INTO wearables (user_id, raw_data, created_at) VALUES
-- Mar 12
(1, '{"heart_rate": {"value": 68, "unit": "bpm"}, "spo2": {"value": 97, "unit": "%"}, "steps": {"value": 4200}, "sleep_hours": {"value": 7.2}}'::jsonb, '2026-03-12 08:00:00+00'),
(1, '{"heart_rate": {"value": 72, "unit": "bpm"}, "spo2": {"value": 96, "unit": "%"}}'::jsonb, '2026-03-12 14:00:00+00'),
(1, '{"heart_rate": {"value": 70, "unit": "bpm"}, "spo2": {"value": 97, "unit": "%"}}'::jsonb, '2026-03-12 20:00:00+00'),
-- Mar 13
(1, '{"heart_rate": {"value": 74, "unit": "bpm"}, "spo2": {"value": 96, "unit": "%"}, "steps": {"value": 3800}, "sleep_hours": {"value": 5.5}}'::jsonb, '2026-03-13 08:00:00+00'),
(1, '{"heart_rate": {"value": 78, "unit": "bpm"}, "spo2": {"value": 95, "unit": "%"}}'::jsonb, '2026-03-13 14:00:00+00'),
(1, '{"heart_rate": {"value": 76, "unit": "bpm"}, "spo2": {"value": 95, "unit": "%"}}'::jsonb, '2026-03-13 20:00:00+00'),
-- Mar 14
(1, '{"heart_rate": {"value": 80, "unit": "bpm"}, "spo2": {"value": 95, "unit": "%"}, "steps": {"value": 2900}, "sleep_hours": {"value": 5.0}}'::jsonb, '2026-03-14 08:00:00+00'),
(1, '{"heart_rate": {"value": 84, "unit": "bpm"}, "spo2": {"value": 94, "unit": "%"}}'::jsonb, '2026-03-14 14:00:00+00'),
(1, '{"heart_rate": {"value": 82, "unit": "bpm"}, "spo2": {"value": 94, "unit": "%"}}'::jsonb, '2026-03-14 20:00:00+00'),
-- Mar 15 (decompensation worsening)
(1, '{"heart_rate": {"value": 88, "unit": "bpm"}, "spo2": {"value": 93, "unit": "%"}, "steps": {"value": 1800}, "sleep_hours": {"value": 4.5}}'::jsonb, '2026-03-15 08:00:00+00'),
(1, '{"heart_rate": {"value": 92, "unit": "bpm"}, "spo2": {"value": 92, "unit": "%"}}'::jsonb, '2026-03-15 14:00:00+00'),
(1, '{"heart_rate": {"value": 90, "unit": "bpm"}, "spo2": {"value": 93, "unit": "%"}}'::jsonb, '2026-03-15 20:00:00+00'),
-- Mar 16 (peak decompensation)
(1, '{"heart_rate": {"value": 94, "unit": "bpm"}, "spo2": {"value": 92, "unit": "%"}, "steps": {"value": 1200}, "sleep_hours": {"value": 4.0}}'::jsonb, '2026-03-16 08:00:00+00'),
(1, '{"heart_rate": {"value": 96, "unit": "bpm"}, "spo2": {"value": 91, "unit": "%"}}'::jsonb, '2026-03-16 14:00:00+00'),
(1, '{"heart_rate": {"value": 92, "unit": "bpm"}, "spo2": {"value": 92, "unit": "%"}}'::jsonb, '2026-03-16 20:00:00+00'),
-- Mar 17 (improving after resuming meds)
(1, '{"heart_rate": {"value": 82, "unit": "bpm"}, "spo2": {"value": 94, "unit": "%"}, "steps": {"value": 2500}, "sleep_hours": {"value": 5.5}}'::jsonb, '2026-03-17 08:00:00+00'),
(1, '{"heart_rate": {"value": 80, "unit": "bpm"}, "spo2": {"value": 95, "unit": "%"}}'::jsonb, '2026-03-17 14:00:00+00'),
(1, '{"heart_rate": {"value": 78, "unit": "bpm"}, "spo2": {"value": 95, "unit": "%"}}'::jsonb, '2026-03-17 20:00:00+00'),
-- Mar 18 (continuing to improve)
(1, '{"heart_rate": {"value": 74, "unit": "bpm"}, "spo2": {"value": 96, "unit": "%"}, "steps": {"value": 3200}, "sleep_hours": {"value": 6.5}}'::jsonb, '2026-03-18 08:00:00+00'),
(1, '{"heart_rate": {"value": 72, "unit": "bpm"}, "spo2": {"value": 96, "unit": "%"}}'::jsonb, '2026-03-18 14:00:00+00');
