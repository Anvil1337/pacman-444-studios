from abc import ABC, abstractmethod
from threading import Timer


class Ability(ABC):

    @abstractmethod
    def __init__(self, pacman, duration):
        self.pacman = pacman
        self.duration = duration

    @property
    def duration_timer(self):
        return Timer(self.duration, self.deactivate)

    @abstractmethod
    def run(self):
        self.activate()
        self.duration_timer.start()

    @abstractmethod
    def deactivate(self):
        pass

    @abstractmethod
    def activate(self):
        pass


class SpeedAbility(Ability):
    """ Speeds pacman up while ability is active """

    def __init__(self, pacman, duration, pacman_vel, pacman_boost):
        self.pacman_velocity = pacman_vel
        self.pacman_boost = pacman_boost
        super().__init__(pacman, duration)

    def run(self):
        super().run()

    def activate(self):
        self.pacman.velocity += self.pacman_boost

    def deactivate(self):
        self.pacman.velocity = self.pacman_velocity


class TransformAbility(Ability):
    """ Lets player freely cycle through forms while ability is active """

    @property
    def duration(self):
        return self.duration

    def __init__(self, pacman, duration, ghosts, ghost_velocity, ghost_slowdown):
        self.ghosts = ghosts
        self.ghost_velocity = ghost_velocity
        self.ghost_slowdown = ghost_slowdown
        self.is_active = False
        super().__init__(pacman, duration)

    def run(self):
        super().run()

    def activate(self):
        self.is_active = True
        for ghost in self.ghosts:
            ghost.velocity -= self.ghost_slowdown

    def deactivate(self):
        self.is_active = False
        for ghost in self.ghosts:
            ghost.velocity = self.ghost_velocity

    def changeForm(self):

        # Hardcoded

        if self.is_active:
            if self.pacman.form == 'red':
                self.pacman.form = 'green'

            elif self.pacman.form == 'green':
                self.pacman.form = 'blue'

            else:
                self.pacman.form = 'red'
