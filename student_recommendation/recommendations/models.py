from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    program_ar = models.CharField(max_length=100)
    program_en = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name_en} ({self.student_id})"

class Course(models.Model):
    name_ar = models.CharField(max_length=100, unique=True)
    name_en = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50)  # e.g., "Arabic", "Programming", etc.
    credits = models.IntegerField(default=1)  # Add credits field

    def __str__(self):
        return self.name_en

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return f"{self.student.name_en} - {self.course.name_en}: {self.score}"