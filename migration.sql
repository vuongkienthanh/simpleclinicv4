-- old my_database.db
-- new simpleclinic.db

INSERT INTO simpleclinic.patients (id, name, gender, birthdate)
SELECT MAX(id), name, gender, birthdate
FROM patients
GROUP BY name;

INSERT INTO simpleclinic.visits (id, patient_id, exam_datetime, weight, days, medical_history, diagnosis, note, price)
SELECT id, patient_id, exam_datetime, weight, days, IFNULL(vnote, ''), diagnosis, IFNULL(follow, ''), price
FROM visits;

UPDATE simpleclinic.visits SET exam_datetime = strftime('%Y-%m-%dT%H:%M:%S', DATETIME(exam_datetime));

TODO
insert into simpleclinic.medicine_store (id, name, element,

INSERT OR REPLACE INTO simpleclinic.medicines(visit_id, medicine_id, times, dose,quantity, usage_note)
SELECT visit_id, warehouse_id, times, dose, quantity, IFNULL(usage_note, '') from linedrugs

