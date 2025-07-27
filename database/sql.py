from .models import *

create_table_sql = f"""\
CREATE TABLE singleton (
    last_open_date DATE
);
CREATE TABLE {Patient.__tablename__} (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    gender GENDER NOT NULL,
    birthdate DATE NOT NULL,
    address TEXT,
    phone TEXT,
    past_history TEXT
);
CREATE TABLE {Visit.__tablename__} (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    exam_datetime TIMESTAMP DEFAULT (datetime('now', 'localtime')),
    diagnosis TEXT NOT NULL,
    weight INTEGER NOT NULL CHECK( weight > 0 ), -- real weight *10
    days INTEGER NOT NULL CHECK( days >=0 ),
    check_after_n_days INTEGER NOT NULL ( check_after_n_days >= 0 ),
    price INTEGER NOT NULL,
    vnote TEXT,
    follow_note TEXT,
    misc_data TEXT,
    CONSTRAINT ref_patient FOREIGN KEY (patient_id) REFERENCES {Patient.__tablename__} (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
);
CREATE TABLE {Queue.__tablename__} (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER UNIQUE NOT NULL,
    added_datetime TIMESTAMP DEFAULT (datetime('now', 'localtime')),
    CONSTRAINT ref_patient FOREIGN KEY (patient_id) REFERENCES {Patient.__tablename__} (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
CREATE TABLE {Warehouse.__tablename__} (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    element TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK( quantity >= 0 ),
    usage TEXT NOT NULL,
    usage_unit TEXT NOT NULL,
    purchase_price INTEGER NOT NULL CHECK( purchase_price > 0 ),
    sale_price INTEGER NOT NULL CHECK( sale_price > 0 ),
    sale_unit TEXT,
    expire_date DATE,
    note TEXT,
    CONSTRAINT price_check CHECK( sale_price >= purchase_price )
);
CREATE TABLE {LineDrug.__tablename__} (
    id INTEGER PRIMARY KEY,
    warehouse_id INTEGER NOT NULL,
    times INTEGER NOT NULL CHECK( times > 0 ),
    dose TEXT NOT NULL CHECK( dose != '' ),
    quantity INTEGER NOT NULL CHECK( quantity > 0 ),
    visit_id INTEGER NOT NULL,
    usage_note TEXT,
    CONSTRAINT ref_visit FOREIGN KEY (visit_id) REFERENCES {Visit.__tablename__} (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT ref_warehouse FOREIGN KEY (warehouse_id) REFERENCES {Warehouse.__tablename__} (id)
        ON DELETE RESTRICT
        ON UPDATE NO ACTION,
);
CREATE TABLE {Procedure.__tablename__} (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price INTEGER NOT NULL CHECK( price > 0 ),
);
CREATE TABLE {LineProcedure.__tablename__} (
    id INTEGER PRIMARY KEY,
    procedure_id INTEGER NOT NULL,
    visit_id INTEGER NOT NULL,
    CONSTRAINT ref_visit FOREIGN KEY (visit_id) REFERENCES {Visit.__tablename__} (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT ref_procedure FOREIGN KEY (procedure_id) REFERENCES {Procedure.__tablename__} (id)
        ON DELETE RESTRICT
        ON UPDATE NO ACTION
);
"""

create_index_sql = f"""
CREATE INDEX patient_name ON {Patient.__tablename__} (name);
CREATE INDEX procedure_name ON {Procedure.__tablename__} (name);
CREATE INDEX drug_name ON {Warehouse.__tablename__} (name);
CREATE INDEX drug_element ON {Warehouse.__tablename__} (element);
"""

create_view_sql = f"""
CREATE VIEW {Queue.__tablename__}_view AS
    SELECT
        p.id AS pid,
        p.name,
        p.gender,
        p.birthdate,
        date(q.added_datetime, 'localtime')
    FROM {Queue.__tablename__} AS q
    JOIN {Patient.__tablename__} AS p
    ON q.patient_id = p.id
    ORDER BY q.added_datetime ASC
;
CREATE VIEW seentoday_view AS
    SELECT
        p.id AS pid,
        p.name,
        p.gender,
        p.birthdate,
        v.id as vid,
        date(v.exam_datetime, 'localtime')
    FROM {Patient.__tablename__} AS p
    JOIN {Visit.__tablename__} as v
    ON v.patient_id = p.id
    WHERE date(v.exam_datetime) = date('now', 'localtime')
    ORDER BY v.exam_datetime DESC
;
"""

create_trigger_sql = f"""
CREATE TRIGGER last_open_date_update
BEFORE UPDATE OF last_open_date ON singleton 
WHEN unixepoch(OLD.last_open_date) < unixepoch(NEW.last_open_date)
BEGIN
DELETE FROM {Queue.__tablename__};
END;

CREATE TRIGGER linedrug_insert 
BEFORE INSERT ON {LineDrug.__tablename__}
BEGIN
UPDATE {Warehouse.__tablename__} SET quantity = quantity - NEW.quantity
    WHERE id = NEW.warehouse_id;
END;

CREATE TRIGGER linedrug_delete
BEFORE DELETE ON {LineDrug.__tablename__}
BEGIN
UPDATE {Warehouse.__tablename__} SET quantity = quantity + OLD.quantity
    WHERE id = OLD.warehouse_id;
END;
"""

finalized_sql = """
INSERT OR IGNORE INTO singleton (last_open_date) VALUES (date('now', 'localtime'));
"""
