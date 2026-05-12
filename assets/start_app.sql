PRAGMA foreign_keys = ON;
UPDATE singleton SET last_open_date = DATE('now', 'localtime');

CREATE TRIGGER IF NOT EXISTS last_open_date_update
AFTER UPDATE OF last_open_date ON singleton
WHEN OLD.last_open_date < NEW.last_open_date
BEGIN
    DELETE FROM seentoday;
END;

CREATE TRIGGER IF NOT EXISTS medicine_insert 
BEFORE INSERT ON medicines
BEGIN
    UPDATE medicine_store SET quantity = quantity - NEW.quantity
        WHERE id = NEW.medicine_id;
END;

CREATE TRIGGER IF NOT EXISTS medicine_delete
BEFORE DELETE ON medicines
BEGIN
    UPDATE medicine_store SET quantity = quantity + OLD.quantity
        WHERE id = OLD.medicine_id;
END;

CREATE TRIGGER IF NOT EXISTS visit_insert
AFTER INSERT ON visits
BEGIN
    INSERT INTO seentoday (visit_id) VALUES (NEW.id);
END;

