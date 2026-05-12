CREATE TABLE IF NOT EXISTS singleton (
    id INTEGER PRIMARY KEY,
    last_open_date INTEGER
);

CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL CHECK (name <> ''),
    gender GENDER NOT NULL,
    birthdate DATE NOT NULL,
    past_history TEXT NOT NULL,
    misc TEXT
);

CREATE TABLE IF NOT EXISTS visits (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    exam_datetime TIMESTAMP DEFAULT (datetime('now', 'localtime')),
    weight INTEGER NOT NULL CHECK (weight > 0), -- real weight /10
    medical_history TEXT NOT NULL,
    diagnosis TEXT NOT NULL CHECK (diagnosis <> ''),
    days INTEGER NOT NULL CHECK (days >= 0),
    note TEXT NOT NULL,
    price INTEGER NOT NULL,
    misc TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS seentoday (
    id INTEGER PRIMARY KEY,
    visit_id INTEGER,
    misc TEXT,
    FOREIGN KEY (visit_id) REFERENCES visits (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS medicine_store (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL CHECK (name <> ''),
    element TEXT NOT NULL CHECK (element <> ''),
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    route TEXT NOT NULL CHECK (route <> ''),
    usage_unit TEXT NOT NULL CHECK (usage_unit <> ''),
    selling_unit TEXT NOT NULL CHECK (selling_unit <> ''),
    cost_price INTEGER NOT NULL CHECK (cost_price >= 0),
    selling_price INTEGER NOT NULL CHECK (selling_price >=0),
    misc TEXT,
    CHECK (selling_price >= cost_price)
);

CREATE TABLE IF NOT EXISTS medicines (
    medicine_id INTEGER,
    visit_id INTEGER,
    times INTEGER NOT NULL CHECK (times > 0),
    dose TEXT NOT NULL CHECK (dose <> ''),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    usage_note TEXT NOT NULL,
    misc TEXT,
    PRIMARY KEY (medicine_id, visit_id),
    FOREIGN KEY (visit_id) REFERENCES visits (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (medicine_id) REFERENCES medicine_store (id)
        ON DELETE RESTRICT
        ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS service_store (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price INTEGER NOT NULL CHECK (price >= 0),
    misc TEXT
);

CREATE TABLE IF NOT EXISTS services (
    service_id INTEGER,
    visit_id INTEGER,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    misc TEXT,
    PRIMARY KEY (service_id, visit_id),
    FOREIGN KEY (visit_id) REFERENCES visits (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (service_id) REFERENCES service_store (id)
        ON DELETE RESTRICT
        ON UPDATE NO ACTION
);

CREATE INDEX IF NOT EXISTS patient_name ON patients (name);
-- CREATE INDEX IF NOT EXISTS medicine_name ON medicine_store (name);
-- CREATE INDEX IF NOT EXISTS medicine_element ON medicine_store (element);
-- CREATE INDEX IF NOT EXISTS service_name ON service_store (name);

INSERT OR IGNORE INTO singleton (id, last_open_date) VALUES ( 1, DATE('now', 'localtime'));
