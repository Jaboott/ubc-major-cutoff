class MajorStats:
    def __init__(self, name, id, type, year, max_grade, min_grade, initial_reject, final_admit, domestic, note=""):
        self.name = name
        self.id = id
        self.type = type
        self.year = year
        self.max_grade = max_grade
        self.min_grade = min_grade
        self.initial_reject = initial_reject
        self.final_admit = final_admit
        self.domestic = domestic
        self.note = note

    def __str__(self):
        return (f"Major Name: {self.name}\n"
                f"Major ID: {self.id}\n"
                f"Major Type: {self.type}\n"
                f"Year: {self.year}\n"
                f"Max Grade: {self.max_grade}\n"
                f"Min Grade: {self.min_grade}\n"
                f"Initial Reject: {self.initial_reject}\n"
                f"Final Admit: {self.final_admit}\n"
                f"Domestic: {self.domestic}\n"
                f"Note: {self.note}\n"
                f"----------------------------------------")

