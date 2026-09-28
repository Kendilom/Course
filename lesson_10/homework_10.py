class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

class Manager(Employee):
    def __init__(self, department):
        Employee.__init__(self, 'dima', 200)
        self.department = 16

class Developer(Employee):
    def __init__(self, programming_language):
        Employee.__init__(self, 'taras', 300)
        self.programming_language = programming_language

class TeamLead(Manager, Developer):
    def __init__(self, team_size, name, salary):
        Manager.__init__(self, 16)
        self.team_size = team_size
        self.name = name
        self.salary = salary

lead = TeamLead(40, 'grisha', 7000)
print(hasattr(lead, 'name'))
print(hasattr(lead, 'department'))
print(hasattr(lead, 'programming_language'))
print(hasattr(lead, 'salary'))
print(lead.name)
print(lead.salary)