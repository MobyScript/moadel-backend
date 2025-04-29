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
        {"ar": "الهندسة الكهربائية", "en": "Electrical Engineering", "total_credits": 130},
        {"ar": "الرياضيات", "en": "Mathematics", "total_credits": 110},
        {"ar": "إدارة الأعمال", "en": "Business Administration", "total_credits": 115},
        {"ar": "الهندسة الميكانيكية", "en": "Mechanical Engineering", "total_credits": 125},
        {"ar": "الفيزياء", "en": "Physics", "total_credits": 110},
        {"ar": "الكيمياء", "en": "Chemistry", "total_credits": 110},
        {"ar": "الهندسة المدنية", "en": "Civil Engineering", "total_credits": 130},
        {"ar": "الهندسة البيئية", "en": "Environmental Engineering", "total_credits": 120},
        {"ar": "الاقتصاد", "en": "Economics", "total_credits": 115},
        {"ar": "الذكاء الاصطناعي", "en": "Artificial Intelligence", "total_credits": 120},
        {"ar": "الأمن السيبراني", "en": "Cybersecurity", "total_credits": 120},
        {"ar": "علوم البيانات", "en": "Data Science", "total_credits": 120},
        {"ar": "الهندسة الصناعية", "en": "Industrial Engineering", "total_credits": 125},
        {"ar": "التسويق", "en": "Marketing", "total_credits": 115},
        {"ar": "التمويل", "en": "Finance", "total_credits": 115},
        {"ar": "الهندسة المعمارية", "en": "Architecture", "total_credits": 135},
        {"ar": "علم الأحياء", "en": "Biology", "total_credits": 110},
        {"ar": "الطب", "en": "Medicine", "total_credits": 180},
        {"ar": "الصيدلة", "en": "Pharmacy", "total_credits": 160}
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
        {"id": "BUS305", "ar": "إدارة العمليات", "en": "Operations Management", "category": "Business", "credits": 3},
        {"id": "CSC310", "ar": "أمن التطبيقات", "en": "Application Security", "category": "Cybersecurity", "credits": 3},
        {"id": "CSC311", "ar": "تحليل البرمجيات", "en": "Software Analysis", "category": "Programming", "credits": 3},
        {"id": "DS303", "ar": "التعلم العميق", "en": "Deep Learning", "category": "Data Science", "credits": 3},
        {"id": "AI303", "ar": "الروبوتات المتقدمة", "en": "Advanced Robotics", "category": "AI", "credits": 3},
        {"id": "ELE203", "ar": "أنظمة التحكم", "en": "Control Systems", "category": "Electrical Engineering", "credits": 3},
        {"id": "MAT204", "ar": "الجبر الخطي", "en": "Linear Algebra", "category": "Mathematics", "credits": 3},
        {"id": "PHY203", "ar": "فيزياء المواد", "en": "Material Physics", "category": "Physics", "credits": 3},
        {"id": "CHE203", "ar": "الكيمياء الحيوية", "en": "Biochemistry", "category": "Chemistry", "credits": 3},
        {"id": "BUS306", "ar": "إدارة الابتكار", "en": "Innovation Management", "category": "Business", "credits": 3},
        {"id": "ECO203", "ar": "الاقتصاد الدولي", "en": "International Economics", "category": "Economics", "credits": 3},
        {"id": "BIO101", "ar": "علم الأحياء العام", "en": "General Biology", "category": "Biology", "credits": 3},
        {"id": "BIO102", "ar": "علم الوراثة", "en": "Genetics", "category": "Biology", "credits": 3},
        {"id": "MED101", "ar": "تشريح الإنسان", "en": "Human Anatomy", "category": "Medicine", "credits": 4},
        {"id": "MED102", "ar": "علم وظائف الأعضاء", "en": "Physiology", "category": "Medicine", "credits": 4},
        {"id": "PHR101", "ar": "الكيمياء الصيدلانية", "en": "Pharmaceutical Chemistry", "category": "Pharmacy", "credits": 3},
        {"id": "PHR102", "ar": "علم الأدوية", "en": "Pharmacology", "category": "Pharmacy", "credits": 3},
        {"id": "ARC101", "ar": "أساسيات التصميم المعماري", "en": "Architectural Design Basics", "category": "Architecture", "credits": 3},
        {"id": "ARC102", "ar": "تاريخ العمارة", "en": "History of Architecture", "category": "Architecture", "credits": 3},
        {"id": "ENV101", "ar": "مقدمة في الهندسة البيئية", "en": "Introduction to Environmental Engineering", "category": "Environmental Engineering", "credits": 3},
        {"id": "ENV102", "ar": "إدارة النفايات", "en": "Waste Management", "category": "Environmental Engineering", "credits": 3},
        {"id": "BIO103", "ar": "علم الأحياء الدقيقة", "en": "Microbiology", "category": "Biology", "credits": 3},
        {"id": "MED103", "ar": "علم الأمراض", "en": "Pathology", "category": "Medicine", "credits": 4},
        {"id": "PHR103", "ar": "الصيدلة السريرية", "en": "Clinical Pharmacy", "category": "Pharmacy", "credits": 3},
        {"id": "ARC103", "ar": "تصميم المباني الخضراء", "en": "Green Building Design", "category": "Architecture", "credits": 3},
        {"id": "ENV103", "ar": "التغير المناخي", "en": "Climate Change", "category": "Environmental Engineering", "credits": 3},
        {"id": "ELE204", "ar": "أنظمة الطاقة المتجددة", "en": "Renewable Energy Systems", "category": "Electrical Engineering", "credits": 3},
        {"id": "MAT205", "ar": "نظرية الأعداد", "en": "Number Theory", "category": "Mathematics", "credits": 3},
        {"id": "PHY204", "ar": "فيزياء البلازما", "en": "Plasma Physics", "category": "Physics", "credits": 3},
        {"id": "CHE204", "ar": "الكيمياء الصناعية", "en": "Industrial Chemistry", "category": "Chemistry", "credits": 3},
        {"id": "BUS307", "ar": "ريادة الأعمال", "en": "Entrepreneurship", "category": "Business", "credits": 3},
        {"id": "BIO104", "ar": "علم المناعة", "en": "Immunology", "category": "Biology", "credits": 3},
        {"id": "MED104", "ar": "علم الأنسجة", "en": "Histology", "category": "Medicine", "credits": 4},
        {"id": "PHR104", "ar": "الصيدلة الحيوية", "en": "Biopharmaceutics", "category": "Pharmacy", "credits": 3},
        {"id": "ARC104", "ar": "تصميم المباني الذكية", "en": "Smart Building Design", "category": "Architecture", "credits": 3},
        {"id": "ENV104", "ar": "إدارة الموارد المائية", "en": "Water Resource Management", "category": "Environmental Engineering", "credits": 3},
        {"id": "ELE205", "ar": "أنظمة الاتصالات", "en": "Communication Systems", "category": "Electrical Engineering", "credits": 3},
        {"id": "MAT206", "ar": "التحليل الحقيقي", "en": "Real Analysis", "category": "Mathematics", "credits": 3},
        {"id": "PHY205", "ar": "فيزياء الليزر", "en": "Laser Physics", "category": "Physics", "credits": 3},
        {"id": "CHE205", "ar": "الكيمياء البيئية", "en": "Environmental Chemistry", "category": "Chemistry", "credits": 3},
        {"id": "BUS308", "ar": "إدارة الجودة", "en": "Quality Management", "category": "Business", "credits": 3},
        {"id": "ECO204", "ar": "اقتصاديات التنمية", "en": "Development Economics", "category": "Economics", "credits": 3},
        {"id": "FIN203", "ar": "التمويل الدولي", "en": "International Finance", "category": "Finance", "credits": 3},
        {"id": "CSC312", "ar": "أنظمة الزمن الحقيقي", "en": "Real-Time Systems", "category": "Programming", "credits": 3},
        {"id": "DS304", "ar": "تحليل البيانات التنبؤية", "en": "Predictive Data Analytics", "category": "Data Science", "credits": 3},
        {"id": "AI304", "ar": "الذكاء الاصطناعي التوضيحي", "en": "Explainable AI", "category": "AI", "credits": 3},
        {"id": "CYB204", "ar": "إدارة الحوادث الأمنية", "en": "Incident Management", "category": "Cybersecurity", "credits": 3},
        {"id": "BIO105", "ar": "علم البيئة", "en": "Ecology", "category": "Biology", "credits": 3},
        {"id": "MED105", "ar": "علم الأوبئة", "en": "Epidemiology", "category": "Medicine", "credits": 4},
        {"id": "PHR105", "ar": "التكنولوجيا الصيدلانية", "en": "Pharmaceutical Technology", "category": "Pharmacy", "credits": 3},
        {"id": "ARC105", "ar": "تصميم المساحات الحضرية", "en": "Urban Space Design", "category": "Architecture", "credits": 3},
        {"id": "ENV105", "ar": "الطاقة المستدامة", "en": "Sustainable Energy", "category": "Environmental Engineering", "credits": 3},
        {"id": "ELE206", "ar": "أنظمة الطاقة الذكية", "en": "Smart Power Systems", "category": "Electrical Engineering", "credits": 3},
        {"id": "MAT207", "ar": "الرياضيات الحاسوبية", "en": "Computational Mathematics", "category": "Mathematics", "credits": 3},
        {"id": "PHY206", "ar": "فيزياء المواد المتقدمة", "en": "Advanced Material Physics", "category": "Physics", "credits": 3},
        {"id": "CHE206", "ar": "الكيمياء الحيوية المتقدمة", "en": "Advanced Biochemistry", "category": "Chemistry", "credits": 3},
        {"id": "BUS309", "ar": "إدارة التغيير", "en": "Change Management", "category": "Business", "credits": 3},
        {"id": "ECO205", "ar": "الاقتصاد البيئي", "en": "Environmental Economics", "category": "Economics", "credits": 3},
        {"id": "FIN204", "ar": "إدارة المحافظ الاستثمارية", "en": "Portfolio Management", "category": "Finance", "credits": 3},
        {"id": "CSC313", "ar": "الحوسبة المتنقلة", "en": "Mobile Computing", "category": "Programming", "credits": 3},
        {"id": "DS305", "ar": "تحليل البيانات النصية", "en": "Text Data Analytics", "category": "Data Science", "credits": 3},
        {"id": "CSC314", "ar": "برمجة التطبيقات المتنقلة", "en": "Mobile Application Programming", "category": "Programming", "credits": 3},
        {"id": "CSC315", "ar": "البرمجة المتوازية", "en": "Parallel Programming", "category": "Programming", "credits": 3},
        {"id": "CSC316", "ar": "برمجة الألعاب", "en": "Game Programming", "category": "Programming", "credits": 3},
        {"id": "CSC317", "ar": "برمجة الأنظمة المدمجة", "en": "Embedded Systems Programming", "category": "Programming", "credits": 3},
        {"id": "CSC318", "ar": "برمجة التطبيقات السحابية", "en": "Cloud Application Programming", "category": "Programming", "credits": 3},
        {"id": "CSC319", "ar": "برمجة واجهات المستخدم", "en": "User Interface Programming", "category": "Programming", "credits": 3},
        {"id": "CSC320", "ar": "برمجة الذكاء الاصطناعي", "en": "AI Programming", "category": "Programming", "credits": 3},
        {"id": "CSC321", "ar": "برمجة قواعد البيانات", "en": "Database Programming", "category": "Programming", "credits": 3},
        {"id": "CSC322", "ar": "برمجة التطبيقات التفاعلية", "en": "Interactive Application Programming", "category": "Programming", "credits": 3},
        {"id": "CSC323", "ar": "برمجة الأنظمة الموزعة", "en": "Distributed Systems Programming", "category": "Programming", "credits": 3}
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

        # Assign 8 major courses and 2 electives to predefined students
        major_courses = [c for c in courses if c["category"] == "Programming"]
        other_courses = [c for c in courses if c["category"] != "Programming"]

        major_taken = major_courses[:8]
        electives = random.sample(other_courses, k=min(len(other_courses), 2))

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
