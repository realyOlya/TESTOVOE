from dataclasses import dataclass
from typing import Optional
#from datetime import datetime


@dataclass
class Pet:
    #имя, вид, id_tg, др, id_op
    name: str
    type_animal: str
    owner_id: int
    birth_date: Optional[str] = None
    id: Optional[int] = None


    def get_display_name(self):
        if self.birth_date:
            return f"{self.name} ({self.type_animal}, {self.birth_date})"
        return f"{self.name} ({self.type_animal})"

    """def is_adult(self):
        if not self.BIRTH_DATE:
            return True  
        try:
            birth = datetime.strptime(self.BIRTH_DATE, "%d.%m.%Y")
            age = (datetime.now() - birth).days / 365.25
            return age >= 1
        except:
            return True""" # в разработке, на данный момент лишнее