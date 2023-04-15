class proximity_zone:
    def __init__(self, name, vessel, vessel_size, zone_size):
        self.name = name
        self.vessel = vessel
        self.vessel_size = vessel_size
        self.zone_size = zone_size

    def get_name(self):
        return self.name

    def check_violations(self, vessels):
        violators = []
        colliders = []

        for v in vessels:
            if not v == self.vessel:
                dist = self.vessel.get_dist_to(v)
                if dist < self.zone_size:
                    violators.append(v)

                if dist < self.vessel_size:
                    colliders.append(v)

        return violators, colliders
