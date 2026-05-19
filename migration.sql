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

INSERT INTO simpleclinic.medicine_store (id, name, element, quantity, route, usage_unit, selling_unit, cost_price, selling_unit)
SELECT id, name, element, quantity, usage, usage_unit, IFNULL(sale_unit, usage_unit), purchase_price, sale_price FROM warehouse;

INSERT INTO simpleclinic.service_store (id, name, price)
SELECT id, name, price FROM procedures;

INSERT OR REPLACE INTO simpleclinic.medicines(medicine_id, visit_id, times, dose,quantity, usage_note)
SELECT warehouse_id, visit_id, times, dose, quantity, IFNULL(usage_note, '') from linedrugs;

INSERT OR REPLACE INTO simpleclinic.services(service_id, visit_id, quantity)
SELECT procedure_id, visit_id, 1 from lineprocedures;

