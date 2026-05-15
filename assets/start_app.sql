PRAGMA foreign_keys = ON;

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
