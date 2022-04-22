
class Eqpment():

    eqtypes = [
        'Micrvac',
        'Irradtr',
        'PlymExt',
        'HiVelCr',
        'LiHrvst'
        ]

    def __init__(self,eq_id:str, eq_type:str, eq_name:str) -> None:
        self.eq_id = eq_id
        self.eq_name = eq_name
        self.eq_type = eq_type # should be one of above types

    def __repr__(self) -> str:
        self.eq_name
        self.eq_id
        self.eq_type
        return "<equipment: id= {}, name= {}, type= {}>".format(self.eq_id,self.eq_name,self.eq_type)