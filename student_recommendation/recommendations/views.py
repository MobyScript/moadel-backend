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
        {"ar": "علوم الحاسب", "en": "Computer Science", "total_credits": 120},
        {"ar": "الذكاء الاصطناعي", "en": "Artificial Intelligence", "total_credits": 120},
        {"ar": "الأمن السيبراني", "en": "Cybersecurity", "total_credits": 120},
        {"ar": "علوم البيانات", "en": "Data Science", "total_credits": 120},
        {"ar": "هندسة البرمجيات", "en": "Software Engineering", "total_credits": 120}
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
    
    predefined_students = [
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
        {"id": "CSC301", "ar": "الذكاء الاصطناعي", "en": "Artificial Intelligence", "category": "AI", "credits": 3},
        {"id": "CSC302", "ar": "تعلم الآلة", "en": "Machine Learning", "category": "AI", "credits": 3},
        {"id": "CSC303", "ar": "تصميم وتحليل الخوارزميات", "en": "Algorithm Design & Analysis", "category": "Programming", "credits": 3},
        {"id": "CSC304", "ar": "تطوير تطبيقات الويب", "en": "Web Application Development", "category": "Programming", "credits": 3},
        {"id": "CSC305", "ar": "هندسة البرمجيات", "en": "Software Engineering", "category": "Programming", "credits": 3},
        {"id": "CSC306", "ar": "إدارة الشبكات", "en": "Network Management", "category": "Networking", "credits": 3},
        {"id": "CSC307", "ar": "أساسيات الروبوتات", "en": "Introduction to Robotics", "category": "AI", "credits": 3},
        {"id": "CSC308", "ar": "أنظمة التشغيل", "en": "Operating Systems", "category": "Programming", "credits": 3},
        {"id": "CSC309", "ar": "الحوسبة السحابية", "en": "Cloud Computing", "category": "Programming", "credits": 3},
        {"id": "CSC310", "ar": "أمن التطبيقات", "en": "Application Security", "category": "Cybersecurity", "credits": 3},
        {"id": "CSC311", "ar": "تحليل البرمجيات", "en": "Software Analysis", "category": "Programming", "credits": 3},
        {"id": "CSC312", "ar": "أنظمة الزمن الحقيقي", "en": "Real-Time Systems", "category": "Programming", "credits": 3},
        {"id": "CSC313", "ar": "الحوسبة المتنقلة", "en": "Mobile Computing", "category": "Programming", "credits": 3},
        {"id": "CSC314", "ar": "برمجة التطبيقات المتنقلة", "en": "Mobile Application Programming", "category": "Programming", "credits": 3},
        {"id": "CSC315", "ar": "البرمجة المتوازية", "en": "Parallel Programming", "category": "Programming", "credits": 3},
        {"id": "CSC316", "ar": "برمجة الألعاب", "en": "Game Programming", "category": "Programming", "credits": 3},
        {"id": "CSC317", "ar": "برمجة الأنظمة المدمجة", "en": "Embedded Systems Programming", "category": "Programming", "credits": 3},
        {"id": "CSC318", "ar": "برمجة التطبيقات السحابية", "en": "Cloud Application Programming", "category": "Programming", "credits": 3},
        {"id": "CSC319", "ar": "برمجة واجهات المستخدم", "en": "User Interface Programming", "category": "Programming", "credits": 3},
        {"id": "CSC320", "ar": "برمجة الذكاء الاصطناعي", "en": "AI Programming", "category": "Programming", "credits": 3},
        {"id": "CSC321", "ar": "برمجة قواعد البيانات", "en": "Database Programming", "category": "Programming", "credits": 3},
        {"id": "CSC322", "ar": "برمجة التطبيقات التفاعلية", "en": "Interactive Application Programming", "category": "Programming", "credits": 3},
        {"id": "CSC323", "ar": "برمجة الأنظمة الموزعة", "en": "Distributed Systems Programming", "category": "Programming", "credits": 3},
        {"id": "LAB101", "ar": "مختبر البرمجة 1", "en": "Programming Lab 1", "category": "Lab", "credits": 1},
        {"id": "LAB102", "ar": "مختبر البرمجة 2", "en": "Programming Lab 2", "category": "Lab", "credits": 1},
        {"id": "LAB201", "ar": "مختبر الشبكات", "en": "Networking Lab", "category": "Lab", "credits": 1},
        {"id": "LAB202", "ar": "مختبر قواعد البيانات", "en": "Database Lab", "category": "Lab", "credits": 1},
        {"id": "LAB301", "ar": "مختبر الذكاء الاصطناعي", "en": "AI Lab", "category": "Lab", "credits": 1},
        {"id": "LAB302", "ar": "مختبر تعلم الآلة", "en": "Machine Learning Lab", "category": "Lab", "credits": 1},
        {"id": "LAB303", "ar": "مختبر الروبوتات", "en": "Robotics Lab", "category": "Lab", "credits": 1},
        {"id": "LAB304", "ar": "مختبر التطبيقات السحابية", "en": "Cloud Applications Lab", "category": "Lab", "credits": 1},
        {"id": "LAB305", "ar": "مختبر أمن التطبيقات", "en": "Application Security Lab", "category": "Lab", "credits": 1},
        {"id": "LAB306", "ar": "مختبر البرمجة المتوازية", "en": "Parallel Programming Lab", "category": "Lab", "credits": 1},
    ]

    all_students = []
    # Step 1: Create predefined students with Computer Science major
    for data in predefined_students:
        student = Student.objects.create(
            student_id=data["student_id"],
            name_ar=data["ar"],
            name_en=data["en"],
            program_ar="علوم الحاسب",
            program_en="Computer Science"
        )
        all_students.append(student)

        # Assign random major courses and electives to predefined students
        major_courses = [c for c in courses if c["category"] == "Programming"]
        other_courses = [c for c in courses if c["category"] != "Programming"]

        num_major_courses = random.randint(5, 8)
        num_electives = random.randint(1, 3)
        major_taken = random.sample(major_courses, k=min(len(major_courses), num_major_courses))
        electives = random.sample(other_courses, k=min(len(other_courses), num_electives))

        taken_courses = major_taken + electives

        for course in taken_courses:
            course_obj, _ = Course.objects.get_or_create(
                name_ar=course["ar"],
                name_en=course["en"],
                category=course["category"],
                credits=course["credits"]
            )
            score = random.uniform(60, 100)
            Grade.objects.create(
                student=student,
                course=course_obj,
                score=score
            )

        # Add remaining courses as courses to take
        remaining_courses = [c for c in courses if c not in taken_courses]
        for course in remaining_courses:
            Course.objects.get_or_create(
                name_ar=course["ar"],
                name_en=course["en"],
                category=course["category"],
                credits=course["credits"]
            )

    # Step 2: Create random students with random majors
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
        all_students.append(student)

        # Assign 5 to 10 courses to random students
        major_courses = [c for c in courses if c["category"] == major["en"]]
        other_courses = [c for c in courses if c["category"] != major["en"]]

        num_major_courses = random.randint(3, 8)
        num_electives = random.randint(2, 5)
        major_taken = random.sample(major_courses, k=min(len(major_courses), num_major_courses))
        electives = random.sample(other_courses, k=min(len(other_courses), num_electives))

        taken_courses = major_taken + electives

        for course in taken_courses:
            course_obj, _ = Course.objects.get_or_create(
                name_ar=course["ar"],
                name_en=course["en"],
                category=course["category"],
                credits=course["credits"]
            )
            score = random.uniform(60, 100)
            Grade.objects.create(
                student=student,
                course=course_obj,
                score=score
            )

        # Add remaining courses as courses to take
        remaining_courses = [c for c in courses if c not in taken_courses]
        for course in remaining_courses:
            Course.objects.get_or_create(
                name_ar=course["ar"],
                name_en=course["en"],
                category=course["category"],
                credits=course["credits"]
            )

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
    taken_grades = student.grades.all()
    taken_courses_ids = taken_grades.values_list('course_id', flat=True)
    current_gpa = calculate_gpa(student)

    # Total credits earned
    total_credits = sum(grade.course.credits for grade in taken_grades)

    # Define credit limits based on major
    credit_limits = {
        "Computer Science": 136,
        "Software Engineering": 132,
        "Information Systems": 128,
    }

    # Get credit limit based on student's major
    credit_limit = credit_limits.get(student.program_en, 120)  # Default to 120 if major not found

    # Calculate remaining credits needed
    remaining_credits = max(0, credit_limit - total_credits)

    # Get courses left that the student has not taken yet
    all_courses = Course.objects.exclude(id__in=taken_courses_ids)
    random_courses_left = random.sample(
        list(all_courses), 
        k=min(len(all_courses), remaining_credits // 3)  # Assuming average course credits are 3
    )

    courses_left = [
        {
            "name_ar": course.name_ar,
            "name_en": course.name_en,
            "category": course.category,
            "credits": course.credits,
        }
        for course in random_courses_left
    ]

    # Courses the student has taken
    taken_courses = [
        {
            "course_name_ar": grade.course.name_ar,
            "course_name_en": grade.course.name_en,
            "category": grade.course.category,
            "credits": grade.course.credits,
            "score": grade.score,
        }
        for grade in taken_grades
    ]

    # Total number of courses taken
    total_courses_taken = taken_grades.count()

    response_data = {
        "student_id": student.student_id,
        "name_ar": student.name_ar,
        "name_en": student.name_en,
        "program_ar": student.program_ar,
        "program_en": student.program_en,
        "current_gpa": current_gpa,
        "total_courses_taken": total_courses_taken,
        "total_credits": total_credits,
        "credit_limit": credit_limit,
        "remaining_credits": remaining_credits,
        "takenCourses": taken_courses,
        "recommendedCourses": recommendations,
        "coursesLeft": courses_left,
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

def get_all_students(request):
    students = Student.objects.all()
    student_list = [
        {
            "student_id": student.student_id,
            "name_ar": student.name_ar,
            "name_en": student.name_en,
            "GPA": calculate_gpa(student),
            "Major": student.program_en,
        }
        for student in students
    ]
    return JsonResponse(student_list, safe=False)


def create_new_dummy_data(request):
    # Clear existing data
    Student.objects.all().delete()
    Course.objects.all().delete()
    Grade.objects.all().delete()

    # Generate new dummy data
    generate_dummy_data()

    return JsonResponse({"message": "Dummy data created successfully!"})

@csrf_exempt
def generate_and_return_dummy_data(request):
    generate_dummy_data()
    return JsonResponse({"message": "Dummy data generated successfully!"})
