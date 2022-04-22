"""module holding Equipment class and subclasses of Equipment."""

# external
from abc import abstractmethod

# local
from bookable_item import BookableItem

class Equipment(BookableItem):

    DOWN_PAYMENT_FRAC = 0.5

    eqtypes = [
        'Micrvac',
        'Irradtr',
        'PlymExt',
        'HiVelCr',
        'LiHrvst'
        ]

    def __init__(self, eq_id:str, eq_name:str) -> None:
        self.eq_name = eq_name
        self.eq_id = eq_id
        # self.eq_type

    def get_id(self) -> str:
        return self.eq_id

    def get_name(self) -> str:
        return self.eq_name

    @abstractmethod
    def cost_per_hour(self) -> float:
        pass

    def downpayment_fraction(self) -> float:
        return self.DOWN_PAYMENT_FRAC

class Microvac(Equipment):

    COST_PER_HOUR = 1000

    def __init__(self,eq_id:str, eq_name:str) -> None:
        super().__init__(eq_id,eq_name)
        self.eq_type = "Micrvac"

    def cost_per_hour(self) -> float:
        return self.COST_PER_HOUR

    def downpayment_fraction(self) -> float:
        return self.DOWN_PAYMENT_FRAC

    def __repr__(self) -> str:
        self.eq_name
        self.eq_id
        self.eq_type
        return "<equipment: id= {}, name= {}, type= {}>".format(self.eq_id,self.eq_name,self.eq_type)
    

class Irradiator(Equipment,BookableItem):

    COST_PER_HOUR = 2220

    def __init__(self,eq_id:str, eq_name:str) -> None:
        super().__init__(eq_id,eq_name)
        self.eq_type = "Irradtr"

    def cost_per_hour(self) -> float:
        return self.COST_PER_HOUR

    def downpayment_fraction(self) -> float:
        return self.DOWN_PAYMENT_FRAC

    def __repr__(self) -> str:
        self.eq_name
        self.eq_id
        self.eq_type
        return "<equipment: id= {}, name= {}, type= {}>".format(self.eq_id,self.eq_name,self.eq_type)

class PolymerExtruder(Equipment,BookableItem):

    COST_PER_HOUR = 600

    def __init__(self,eq_id:str, eq_name:str) -> None:
        super().__init__(eq_id,eq_name)
        self.eq_type = "PlymExt"

    def cost_per_hour(self) -> float:
        return self.COST_PER_HOUR

    def downpayment_fraction(self) -> float:
        return self.DOWN_PAYMENT_FRAC

    def __repr__(self) -> str:
        self.eq_name
        self.eq_id
        self.eq_type
        return "<equipment: id= {}, name= {}, type= {}>".format(self.eq_id,self.eq_name,self.eq_type)

class HighVelocityCrusher(Equipment,BookableItem):

    COST_PER_HOUR = 10000*2 # 10,000 USD / half hour

    def __init__(self,eq_id:str, eq_name:str) -> None:
        super().__init__(eq_id,eq_name)
        self.eq_type = "HiVelCr"

    def cost_per_hour(self) -> float:
        return self.COST_PER_HOUR

    def downpayment_fraction(self) -> float:
        return self.DOWN_PAYMENT_FRAC

    def __repr__(self) -> str:
        self.eq_name
        self.eq_id
        self.eq_type
        return "<equipment: id= {}, name= {}, type= {}>".format(self.eq_id,self.eq_name,self.eq_type)

class LightningHarvester(Equipment,BookableItem):

    COST_PER_HOUR = 8800


    def __init__(self,eq_id:str, eq_name:str) -> None:
        super().__init__(eq_id,eq_name)
        self.eq_type = "LiHrvst"

    def cost_per_hour(self) -> float:
        return self.COST_PER_HOUR

    def downpayment_fraction(self) -> float:
        return self.DOWN_PAYMENT_FRAC

    def __repr__(self) -> str:
        self.eq_name
        self.eq_id
        self.eq_type
        return "<equipment: id= {}, name= {}, type= {}>".format(self.eq_id,self.eq_name,self.eq_type)

