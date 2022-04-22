from bookable_item import BookableItem
from equipment_factory import EquipmentFactory
from workshop import Workshop

class BookableItemFactory():

    bookable_types = [
        'Wrkshop',
        'Micrvac',
        'Irradtr',
        'PlymExt',
        'HiVelCr',
        'LiHrvst'
        ]

    @staticmethod
    def create_bookable_item(bookable_item_id:str, bookable_item_type:str, name:str)->BookableItem:
        if bookable_item_type == "Wrkshop":
            return Workshop(bookable_item_id,name)
        if bookable_item_type in BookableItemFactory.bookable_types[1:]:
            return EquipmentFactory.create_equipment(eq_id=bookable_item_id,eq_type=bookable_item_type,eq_name=name)
        else:
            raise ValueError("did not understand bookable item type provided. must be one of {}".format(",".join(BookableItemFactory.bookable_types)))