from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
import random

from .models import Student, Course, Grade

def generate_dummy_data():
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026] 
    majors = [
        {"ar": "علوم الحاسب", "en": "Computer Science"},
        {"ar": "الهندسة الكهربائية", "en": "Electrical Engineering"},
        {"ar": "الرياضيات", "en": "Mathematics"},
        {"ar": "إدارة الأعمال", "en": "Business Administration"},
        {"ar": "الهندسة الميكانيكية", "en": "Mechanical Engineering"},
        {"ar": "الفيزياء", "en": "Physics"},
        {"ar": "الكيمياء", "en": "Chemistry"}
    ]
    names = [
        {"ar": "محمد العتيبي", "en": "Mohammed Al-Otaibi"},
        {"ar": "أحمد السعيد", "en": "Ahmed Al-Saeed"},
        {"ar": "فاطمة الزهراء", "en": "Fatima Al-Zahra"},
        {"ar": "خالد الدوسري", "en": "Khaled Al-Dosari"},
        {"ar": "سارة المطيري", "en": "Sara Al-Mutairi"},
        {"ar": "عبدالله الشمري", "en": "Abdullah Al-Shammari"},
        {"ar": "نورة العبدالله", "en": "Noura Al-Abdullah"},
        {"ar": "علي الحربي", "en": "Ali Al-Harbi"},
        {"ar": "ريم العتيبي", "en": "Reem Al-Otaibi"}
    ]
    courses = [
        {"ar": "برمجة 1", "en": "Programming 1", "category": "Programming", "credits": 3},
        {"ar": "برمجة 2", "en": "Programming 2", "category": "Programming", "credits": 3},
        {"ar": "هياكل بيانات", "en": "Data Structures", "category": "Programming", "credits": 3},
        {"ar": "شبكات الحاسوب", "en": "Computer Networks", "category": "Networking", "credits": 2},
        {"ar": "إدارة قواعد البيانات", "en": "Database Management", "category": "Databases", "credits": 3},
        {"ar": "أدب عربي", "en": "Arabic Literature", "category": "Arabic", "credits": 2},
        {"ar": "قواعد اللغة العربية", "en": "Arabic Grammar", "category": "Arabic", "credits": 2},
        {"ar": "الذكاء الاصطناعي", "en": "Artificial Intelligence", "category": "AI", "credits": 3},
        {"ar": "تعلم الآلة", "en": "Machine Learning", "category": "AI", "credits": 3},
        {"ar": "الفيزياء العامة", "en": "General Physics", "category": "Physics", "credits": 3},
        {"ar": "الكيمياء العضوية", "en": "Organic Chemistry", "category": "Chemistry", "credits": 3},
        {"ar": "الهندسة الحرارية", "en": "Thermal Engineering", "category": "Mechanical Engineering", "credits": 3},
        {"ar": "إدارة المشاريع", "en": "Project Management", "category": "Business", "credits": 3}
    ]
    
    for _ in range(10):
        student_id = f"{random.choice(years)}{random.randint(10, 99)}{random.randint(100, 999)}"
        name = random.choice(names)
        major = random.choice(majors)
        student = Student.objects.create(
            student_id=student_id, 
            name_ar=name["ar"],
            name_en=name["en"],
            program_ar=major["ar"],
            program_en=major["en"]
        )
        
        taken_courses = random.sample(courses, k=random.randint(2, len(courses)-1))
        for course in taken_courses:
            course_obj, _ = Course.objects.get_or_create(
                name_ar=course["ar"],
                name_en=course["en"],
                category=course["category"],
                credits=course["credits"]
            )
            Grade.objects.create(student=student, course=course_obj, score=random.uniform(60, 100))

def calculate_recommendations(student):
    taken_courses = {grade.course.name_en: (grade.score, grade.course.category) for grade in student.grades.all()}
    all_courses = Course.objects.all()
    recommended = []

    # Group taken courses by category
    category_scores = {}
    for course_name, (score, category) in taken_courses.items():
        if category not in category_scores:
            category_scores[category] = []
        category_scores[category].append(score)

    # Calculate average score per category
    category_avg = {category: sum(scores) / len(scores) for category, scores in category_scores.items()}

    # Recommend courses in categories where the student is performing well
    for course in all_courses:
        if course.name_en not in taken_courses:
            if course.category in category_avg and category_avg[course.category] >= 80:  # Adjust threshold as needed
                recommended.append({
                    "name_ar": course.name_ar,
                    "name_en": course.name_en,
                    "category": course.category,
                    "credits": course.credits,
                    "estimatedScore": round(category_avg[course.category], 2)
                })

    return recommended


@csrf_exempt
def get_student_recommendations(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    recommendations = calculate_recommendations(student)
    current_gpa = calculate_gpa(student)

    response_data = {
        "student_id": student.student_id,
        "name_ar": student.name_ar,
        "name_en": student.name_en,
        "program_ar": student.program_ar,
        "program_en": student.program_en,
        "current_gpa": current_gpa,
        "recommendedCourses": recommendations,
    }

    return JsonResponse(response_data)

def calculate_gpa(student):
    grades = student.grades.all()
    total_credits = 0
    total_points = 0

    for grade in grades:
        credits = grade.course.credits
        total_credits += credits

        # Convert score to grade points
        if grade.score >= 95:
            grade_points = 5.0
        elif grade.score >= 90:
            grade_points = 4.75
        elif grade.score >= 85:
            grade_points = 4.5
        elif grade.score >= 80:
            grade_points = 4.0
        elif grade.score >= 75:
            grade_points = 3.5
        elif grade.score >= 70:
            grade_points = 3.0
        elif grade.score >= 65:
            grade_points = 2.5
        elif grade.score >= 60:
            grade_points = 2.0
        else:
            grade_points = 0.0

        total_points += grade_points * credits

    return round(total_points / total_credits, 2) if total_credits > 0 else 0

def estimate_gpa_change(student, course_name, selected_grade):
    grade_to_score = {
        "A+": 95, "A": 90, "B+": 85, "B": 80, "C+": 75, "C": 70, "D+": 65, "D": 60, "F": 50
    }
    selected_score = grade_to_score.get(selected_grade, 0)

    # Add the selected course and grade to the student's grades temporarily
    course = Course.objects.get(name_en=course_name)
    Grade.objects.create(student=student, course=course, score=selected_score)

    # Calculate new GPA
    new_gpa = calculate_gpa(student)

    # Remove the temporary grade
    Grade.objects.filter(student=student, course=course).delete()

    return new_gpa

@csrf_exempt
def generate_and_return_dummy_data(request):
    generate_dummy_data()
    return JsonResponse({"message": "Dummy data generated successfully!"})
