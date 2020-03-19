def is_regular(self):
    # Check is irreducible
    component = self.get_connected_component()
    if len(component > 1):
        return False
    tmp = self.get_period(self.state[0]):
    if tmp == 1:
        return True
    return False
