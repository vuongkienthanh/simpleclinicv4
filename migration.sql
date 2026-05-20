INSERT OR REPLACE INTO simpleclinic.patients (id, name, gender, birthdate, past_history)
SELECT MAX(id), name, gender, strftime('%F',DATETIME(birthdate)), ''
FROM patients
GROUP BY name;

INSERT OR REPLACE INTO simpleclinic.visits (id, patient_id, exam_datetime, weight, days, medical_history, diagnosis, note, price)
SELECT v.id, patient_id, exam_datetime, weight, days, IFNULL(vnote, ''), diagnosis, IFNULL(follow, ''), price
FROM visits as v
JOIN simpleclinic.patients as p 
WHERE v.patient_id = p.id;


UPDATE simpleclinic.visits SET exam_datetime = strftime('%FT%T', DATETIME(exam_datetime));

INSERT OR REPLACE INTO simpleclinic.medicine_store (id, name, element, quantity, route, usage_unit, selling_unit, cost_price, selling_price)
SELECT id, name, element, quantity, usage, usage_unit, IFNULL(sale_unit, usage_unit), purchase_price, IFNULL(sale_price, purchase_price) FROM warehouse;

INSERT OR REPLACE INTO simpleclinic.service_store (id, name, price)
SELECT id, name, price FROM procedures;

INSERT OR REPLACE INTO simpleclinic.medicines(medicine_id, visit_id, times, dose,quantity, usage_note)
SELECT warehouse_id, visit_id, times, dose, quantity, IFNULL(usage_note, '') from linedrugs AS LD
JOIN simpleclinic.visits AS v
WHERE v.id = LD.visit_id;

INSERT OR REPLACE INTO simpleclinic.services(service_id, visit_id, quantity)
SELECT procedure_id, visit_id, 1 from lineprocedures;

UPDATE simpleclinic.visits SET note =''
