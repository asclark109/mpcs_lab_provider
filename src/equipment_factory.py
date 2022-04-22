"""module holding EquipmentFactory class. Responsible for making it easy to make subclasses of Equipemnt"""

# local
from equipment import Equipment
from equipment import Microvac,Irradiator,PolymerExtruder,HighVelocityCrusher,LightningHarvester

class EquipmentFactory():

    eqtypes = [
        'Micrvac',
        'Irradtr',
        'PlymExt',
        'HiVelCr',
        'LiHrvst'
        ]

    @staticmethod
    def create_equipment(eq_id:str, eq_type:str, eq_name:str)->Equipment:
        if eq_type == "Micrvac":
            return Microvac(eq_id,eq_name)
        if eq_type == "Irradtr":
            return Irradiator(eq_id,eq_name)
        if eq_type == "PlymExt":
            return PolymerExtruder(eq_id,eq_name)
        if eq_type == "HiVelCr":
            return HighVelocityCrusher(eq_id,eq_name)
        if eq_type == "LiHrvst":
            return LightningHarvester(eq_id,eq_name)
        else:
            raise ValueError("did not understand equipment type provided. must be one of {}".format(",".join(EquipmentFactory.eqtypes)))