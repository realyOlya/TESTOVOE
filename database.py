import sqlite3
from typing import List
from models import Pet


def init_db():
    conn = sqlite3.connect('vet_clinic.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type_animal TEXT NOT NULL,
            birth_date TEXT,
            owner_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def add_pet(pet: Pet):
    conn = sqlite3.connect('vet_clinic.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pets (name, type_animal, birth_date, owner_id) VALUES (?, ?, ?, ?)",
        (pet.name, pet.type_animal, pet.birth_date, pet.owner_id)
    )
    conn.commit()
    pet_id = cursor.lastrowid
    conn.close()
    pet.id = pet_id
    return pet_id


def get_pets_by_owner(owner_id: int) -> List[Pet]:
    conn = sqlite3.connect('vet_clinic.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, type_animal, birth_date, owner_id FROM pets WHERE owner_id = ? ORDER BY created_at DESC",
        (owner_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    return [
        Pet(
            id=row[0],
            name=row[1],
            type_animal=row[2],
            birth_date=row[3],
            owner_id=row[4]
        )
        for row in rows
    ]