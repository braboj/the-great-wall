from django.db import models


class WallProfile(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class WallSection(models.Model):
    profile = models.ForeignKey(WallProfile, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=255)
    start_height = models.IntegerField()

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class WorkLog(models.Model):
    section = models.ForeignKey(WallSection, on_delete=models.CASCADE, related_name='work_logs')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='work_logs')
    current_height = models.IntegerField(default=0)
    day = models.IntegerField()
    ice = models.IntegerField()
    cost = models.IntegerField()

    def __str__(self):
        return f"Day {self.day} Log for Section {self.section.name} by Team {self.team.name}"

    def calculate(self):
        # Assuming ice and cost are calculated per day and per foot added
        ice_per_foot = 195  # cubic yards
        cost_per_cubic_yard = 1900  # Gold Dragon coins

        added_height = self.current_height - self.section.start_height
        self.ice = added_height * ice_per_foot
        self.cost = self.ice * cost_per_cubic_yard

        # Return values for any additional handling if needed
        return self.ice, self.cost
