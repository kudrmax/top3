class EqualableByAttributes:
    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False

        self_attrs = self.__dict__
        other_attrs = other.__dict__

        return self_attrs == other_attrs
