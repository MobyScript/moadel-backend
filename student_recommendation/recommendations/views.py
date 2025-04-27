from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json
import random

from .models import Student, Course, Grade

# 202011015 - Fahad
# سعد-  202011016 
# 202211007 - خالد الحربي

def generate_dummy_data():

    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]

    majors = [
        {"ar": "علوم الحاسب", "en": "Computer Science"},
        {"ar": "الهندسة الكهربائية", "en": "Electrical Engineering"},
        {"ar": "الرياضيات", "en": "Mathematics"},
        {"ar": "إدارة الأعمال", "en": "Business Administration"},
        {"ar": "الهندسة الميكانيكية", "en": "Mechanical Engineering"},
        {"ar": "الفيزياء", "en": "Physics"},
        {"ar": "الكيمياء", "en": "Chemistry"},
        {"ar": "الهندسة المدنية", "en": "Civil Engineering"},
        {"ar": "الهندسة البيئية", "en": "Environmental Engineering"},
        {"ar": "الاقتصاد", "en": "Economics"},
        {"ar": "الذكاء الاصطناعي", "en": "Artificial Intelligence"},
        {"ar": "الأمن السيبراني", "en": "Cybersecurity"},
        {"ar": "علوم البيانات", "en": "Data Science"},
        {"ar": "الهندسة الصناعية", "en": "Industrial Engineering"},
        {"ar": "التسويق", "en": "Marketing"},
        {"ar": "التمويل", "en": "Finance"},
        {"ar": "الهندسة المعمارية", "en": "Architecture"},
        {"ar": "علم الأحياء", "en": "Biology"},
        {"ar": "الطب", "en": "Medicine"},
        {"ar": "الصيدلة", "en": "Pharmacy"}
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
        {"ar": "ريم العتيبي", "en": "Reem Al-Otaibi"},
        {"ar": "يوسف القحطاني", "en": "Yousef Al-Qahtani"},
        {"ar": "منى الغامدي", "en": "Mona Al-Ghamdi"},
        {"ar": "عبدالعزيز السبيعي", "en": "Abdulaziz Al-Subaie"},
        {"ar": "هدى العبدالكريم", "en": "Huda Al-Abdulkarim"},
        {"ar": "ماجد الزهراني", "en": "Majed Al-Zahrani"},
        {"ar": "لطيفة السالم", "en": "Latifa Al-Salem"},
        {"ar": "سلمان العتيبي", "en": "Salman Al-Otaibi"},
        {"ar": "أمل الحربي", "en": "Amal Al-Harbi"},
        {"ar": "راشد المطيري", "en": "Rashed Al-Mutairi"},
        {"ar": "نوف الشمري", "en": "Nouf Al-Shammari"},
        {"ar": "بدر العبدالله", "en": "Badr Al-Abdullah"},
    ]
    students = [
        {"student_id": "202011015", "ar": "فهد الحربي", "en": "Fahad Al-Harbi"},
        {"student_id": "202011016", "ar": "سعد الحربي", "en": "Saad Al-Harbi"},
        {"student_id": "202211007", "ar": "خالد الحربي", "en": "Khaled Al-Harbi"},
    ]
    courses = [
        {"id": "CSC201", "ar": "برمجة 1", "en": "Programming 1", "category": "Programming", "credits": 3},
        {"id": "CSC202", "ar": "برمجة 2", "en": "Programming 2", "category": "Programming", "credits": 3},
        {"id": "CSC203", "ar": "هياكل بيانات", "en": "Data Structures", "category": "Programming", "credits": 3},
        {"id": "CSC204", "ar": "شبكات الحاسوب", "en": "Computer Networks", "category": "Networking", "credits": 2},
        {"id": "CSC205", "ar": "إدارة قواعد البيانات", "en": "Database Management", "category": "Databases", "credits": 3},
        {"id": "ARB101", "ar": "أدب عربي", "en": "Arabic Literature", "category": "Arabic", "credits": 2},
        {"id": "ARB102", "ar": "قواعد اللغة العربية", "en": "Arabic Grammar", "category": "Arabic", "credits": 2},
        {"id": "CSC301", "ar": "الذكاء الاصطناعي", "en": "Artificial Intelligence", "category": "AI", "credits": 3},
        {"id": "CSC302", "ar": "تعلم الآلة", "en": "Machine Learning", "category": "AI", "credits": 3},
        {"id": "PHY101", "ar": "الفيزياء العامة", "en": "General Physics", "category": "Physics", "credits": 3},
        {"id": "CHE101", "ar": "الكيمياء العضوية", "en": "Organic Chemistry", "category": "Chemistry", "credits": 3},
        {"id": "MEC201", "ar": "الهندسة الحرارية", "en": "Thermal Engineering", "category": "Mechanical Engineering", "credits": 3},
        {"id": "BUS301", "ar": "إدارة المشاريع", "en": "Project Management", "category": "Business", "credits": 3},
        {"id": "CSC303", "ar": "تصميم وتحليل الخوارزميات", "en": "Algorithm Design & Analysis", "category": "Programming", "credits": 3},
        {"id": "CSC304", "ar": "تطوير تطبيقات الويب", "en": "Web Application Development", "category": "Programming", "credits": 3},
        {"id": "CSC305", "ar": "هندسة البرمجيات", "en": "Software Engineering", "category": "Programming", "credits": 3},
        {"id": "CYB201", "ar": "أمن المعلومات", "en": "Information Security", "category": "Cybersecurity", "credits": 3},
        {"id": "BUS302", "ar": "إدارة نظم المعلومات", "en": "Information Systems Management", "category": "Business", "credits": 3},
        {"id": "DS301", "ar": "تحليل البيانات الضخمة", "en": "Big Data Analytics", "category": "Data Science", "credits": 3},
        {"id": "CSC306", "ar": "إدارة الشبكات", "en": "Network Management", "category": "Networking", "credits": 3},
        {"id": "CSC307", "ar": "أساسيات الروبوتات", "en": "Introduction to Robotics", "category": "AI", "credits": 3},
        {"id": "ELE201", "ar": "الإلكترونيات الرقمية", "en": "Digital Electronics", "category": "Electrical Engineering", "credits": 3},
        {"id": "ELE202", "ar": "التصميم المنطقي", "en": "Logic Design", "category": "Electrical Engineering", "credits": 3},
        {"id": "MAT201", "ar": "الرياضيات المتقدمة", "en": "Advanced Mathematics", "category": "Mathematics", "credits": 3},
        {"id": "MAT202", "ar": "الإحصاء التطبيقي", "en": "Applied Statistics", "category": "Mathematics", "credits": 3},
        {"id": "MAT203", "ar": "التحليل العددي", "en": "Numerical Analysis", "category": "Mathematics", "credits": 3},
        {"id": "PHY201", "ar": "الفيزياء النووية", "en": "Nuclear Physics", "category": "Physics", "credits": 3},
        {"id": "CHE201", "ar": "الكيمياء التحليلية", "en": "Analytical Chemistry", "category": "Chemistry", "credits": 3},
        {"id": "CIV201", "ar": "الهندسة المدنية", "en": "Civil Engineering", "category": "Civil Engineering", "credits": 3},
        {"id": "CIV202", "ar": "الهندسة البيئية", "en": "Environmental Engineering", "category": "Civil Engineering", "credits": 3},
        {"id": "BUS303", "ar": "إدارة الموارد البشرية", "en": "Human Resource Management", "category": "Business", "credits": 3},
        {"id": "BUS304", "ar": "التسويق الرقمي", "en": "Digital Marketing", "category": "Business", "credits": 3},
        {"id": "ECO201", "ar": "الاقتصاد الجزئي", "en": "Microeconomics", "category": "Economics", "credits": 3},
        {"id": "ECO202", "ar": "الاقتصاد الكلي", "en": "Macroeconomics", "category": "Economics", "credits": 3},
        {"id": "FIN201", "ar": "التحليل المالي", "en": "Financial Analysis", "category": "Finance", "credits": 3},
        {"id": "FIN202", "ar": "إدارة المخاطر", "en": "Risk Management", "category": "Finance", "credits": 3},
        {"id": "CSC308", "ar": "أنظمة التشغيل", "en": "Operating Systems", "category": "Programming", "credits": 3},
        {"id": "CSC309", "ar": "الحوسبة السحابية", "en": "Cloud Computing", "category": "Programming", "credits": 3},
        {"id": "DS302", "ar": "التصور البياني للبيانات", "en": "Data Visualization", "category": "Data Science", "credits": 3},
        {"id": "AI301", "ar": "معالجة اللغة الطبيعية", "en": "Natural Language Processing", "category": "AI", "credits": 3},
        {"id": "AI302", "ar": "رؤية الحاسوب", "en": "Computer Vision", "category": "AI", "credits": 3},
        {"id": "CYB202", "ar": "اختبار الاختراق", "en": "Penetration Testing", "category": "Cybersecurity", "credits": 3},
        {"id": "CYB203", "ar": "التشفير", "en": "Cryptography", "category": "Cybersecurity", "credits": 3},
        {"id": "PHY202", "ar": "فيزياء الكم", "en": "Quantum Physics", "category": "Physics", "credits": 3},
        {"id": "CHE202", "ar": "الكيمياء الفيزيائية", "en": "Physical Chemistry", "category": "Chemistry", "credits": 3},
        {"id": "BUS305", "ar": "إدارة العمليات", "en": "Operations Management", "category": "Business", "credits": 3}
    ]


    for student_data in students:
        student, created = Student.objects.get_or_create(
            student_id=student_data["student_id"],
            defaults={"name_ar": student_data["ar"], "name_en": student_data["en"], "program_ar": "علوم الحاسب", "program_en": "Computer Science"}
        )
        
        if created:  # Only assign courses if student was newly created
            # Filter courses based on the student's major
            major_courses = [course for course in courses if course["category"] == "Programming"]
            other_courses = [course for course in courses if course["category"] != "Programming"]
            
            # Select courses: prioritize major courses, then fill with other courses
            taken_courses = random.sample(major_courses, k=min(len(major_courses), 7))  # 7 major courses
            taken_courses += random.sample(other_courses, k=min(len(other_courses), 3))  # 3 courses from other categories
            
            for course in taken_courses:
                course_obj, _ = Course.objects.get_or_create(
                    name_ar=course["ar"],
                    name_en=course["en"],
                    category=course["category"],
                    credits=course["credits"]
                )
                Grade.objects.create(student=student, course=course_obj, score=random.uniform(60, 100))


    for _ in range(50):
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
        
        major_courses = [course for course in courses if course["category"] == major["en"]]
        taken_courses = random.sample(major_courses, k=min(len(major_courses), random.randint(2, max(2, len(major_courses)))))
        for course in taken_courses:
            course_obj, _ = Course.objects.get_or_create(
            name_ar=course["ar"],
            name_en=course["en"],
            category=course["category"],
            credits=course["credits"]
            )
            Grade.objects.create(student=student, course=course_obj, score=random.uniform(60, 100))

    return "All students added successfully!"

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

    # Determine course recommendations
    for course in all_courses:
        if course.name_en not in taken_courses:
            category = course.category
            estimated_score = 70  # Default estimated score

            # Prioritize courses based on previous category performance
            if category in category_avg:
                avg_score = category_avg[category]
                estimated_score = round(avg_score * 1.1 if avg_score >= 80 else avg_score * 0.9, 2)

                # Recommend advanced courses if the student is performing well
                if avg_score >= 80:
                    recommended.append({
                        "name_ar": course.name_ar,
                        "name_en": course.name_en,
                        "category": category,
                        "credits": course.credits,
                        "estimatedScore": estimated_score,
                        "type": "Advanced"
                    })

                # Recommend reinforcement courses if the student is struggling
                elif avg_score < 60:
                    recommended.append({
                        "name_ar": course.name_ar,
                        "name_en": course.name_en,
                        "category": category,
                        "credits": course.credits,
                        "estimatedScore": estimated_score,
                        "type": "Reinforcement"
                    })

    # Sort recommendations by lowest estimated score first (harder courses first)
    recommended.sort(key=lambda x: x["estimatedScore"])

    return recommended[:5]  # Return top 5 recommendations



@csrf_exempt
def get_student_recommendations(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    recommendations = calculate_recommendations(student)
    current_gpa = calculate_gpa(student)

    # Get courses taken with scores
    taken_courses = [
        {
            "course_name_ar": grade.course.name_ar,
            "course_name_en": grade.course.name_en,
            "category": grade.course.category,
            "credits": grade.course.credits,
            "score": grade.score,
        }
        for grade in student.grades.all()
    ]

    response_data = {
        "student_id": student.student_id,
        "name_ar": student.name_ar,
        "name_en": student.name_en,
        "program_ar": student.program_ar,
        "program_en": student.program_en,
        "current_gpa": current_gpa,
        "takenCourses": taken_courses,
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


def get_all_courses(request):
    courses = Course.objects.all()
    course_list = [
        {
            "name_ar": course.name_ar,
            "name_en": course.name_en,
            "category": course.category,
            "credits": course.credits,
        }
        for course in courses
    ]
    return JsonResponse(course_list, safe=False)

@csrf_exempt
def generate_and_return_dummy_data(request):
    generate_dummy_data()
    return JsonResponse({"message": "Dummy data generated successfully!"})
