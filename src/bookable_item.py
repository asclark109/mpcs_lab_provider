"""bookable_item.py, a module for an abstract type representing a thing
that can be 'booked' by a client in this program."""

from abc import ABC, abstractmethod
 
class BookableItem(ABC):
 
    # @abstractmethod
    # def total_units(self) -> int:
    #     pass

    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def cost_per_hour(self) -> float:
        pass

    @abstractmethod
    def downpayment_fraction(self) -> float:
        pass