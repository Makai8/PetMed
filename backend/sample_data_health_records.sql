-- PetMed Sprint Cycle III
-- Section 4: Meaningful Sample Data
-- Sample pet allergies, conditions, and medications

USE petmed;

-- 1. PET ALLERGIES
-- Each allergy belongs to an existing pet.

INSERT INTO pet_allergy (pet_id, allergen, reaction, noted_at)
VALUES
(7380000, 'Chicken protein', 'Itchy skin and redness', '2026-09-10 10:30:00'),
(7380001, 'Dust mites', 'Sneezing and watery eyes', '2026-09-15 14:00:00'),
(7380002, 'Grass pollen', 'Skin irritation after outdoor activity', '2026-09-20 09:15:00'),
(7380003, 'Beef protein', 'Digestive discomfort', '2026-10-02 11:45:00');

-- 2. PET MEDICAL CONDITIONS
-- Each condition is linked to an existing pet.

INSERT INTO pet_condition (pet_id, condition_name, diagnosed_at, status)
VALUES
(7380000, 'Atopic dermatitis', '2026-09-12', 'active'),
(7380002, 'Hip dysplasia', '2026-08-05', 'active'),
(7380003, 'Seasonal allergies', '2026-09-18', 'managed'),
(7380004, 'Dental gingivitis', '2026-10-10', 'active');

-- 3. PET MEDICATIONS
-- Each medication belongs to an existing pet.
-- Medication reference is optional in this schema.
-- All examples are fictional demonstration records.

INSERT INTO pet_medication
(pet_id, medication_ref_id, name, dosage, frequency, start_date, end_date)
VALUES
(7380000, NULL, 'Cetirizine', 'Veterinarian-prescribed dose', 'Once daily', '2026-09-12', '2026-11-12'),
(7380002, NULL, 'Carprofen', 'Veterinarian-prescribed dose', 'As directed by veterinarian', '2026-08-06', '2026-12-06'),
(7380003, NULL, 'Apoquel', 'Veterinarian-prescribed dose', 'Once daily', '2026-09-19', '2026-11-19');

-- 4. VERIFY SAMPLE DATA

SELECT * FROM pet_allergy;
SELECT * FROM pet_condition;
SELECT * FROM pet_medication;
