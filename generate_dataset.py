import os
import csv

DOCUMENTS = [
    # Shared Documents (Academic, Exams, Policies)
    {
        "id": "DOC-SHARED-001",
        "title": "Academic Calendar 2026-2027",
        "category": "Academic",
        "subject": "General",
        "audience": "All",
        "access_level": "shared",
        "description": "The official academic calendar for Future Scholars International School for 2026-2027.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/shared/academic/academic_calendar.md",
        "content": """# Academic Calendar 2026-2027

Welcome to the Future Scholars International School academic year 2026-2027. This calendar outlines all major dates, holidays, and examination periods.

## Fall Semester
- **Start of Term**: September 1, 2026
- **Mid-Term Break**: October 26 - October 30, 2026
- **Winter Break**: December 18, 2026 - January 3, 2027

## Spring Semester
- **Start of Term**: January 4, 2027
- **Spring Break**: March 29 - April 9, 2027
- **End of Term**: June 25, 2027

## Examination Periods
- **Mid-Year Exams**: January 11 - January 22, 2027
- **Final Exams**: June 7 - June 18, 2027

Please note that dates are subject to change. Any modifications will be communicated via the school's official newsletter.
"""
    },
    {
        "id": "DOC-SHARED-002",
        "title": "General School Rules",
        "category": "Policies",
        "subject": "General",
        "audience": "All",
        "access_level": "shared",
        "description": "General rules and expectations for all students and staff.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/shared/school_policies/general_rules.md",
        "content": """# General School Rules

Future Scholars International School expects all members of its community to uphold the highest standards of behavior, respect, and integrity.

## Code of Conduct
1. **Respect**: All students and staff must treat each other with respect. Bullying, harassment, and discrimination are strictly prohibited.
2. **Punctuality**: Students must arrive at school by 8:15 AM. Classes begin promptly at 8:30 AM.
3. **Dress Code**: Students are required to wear the official school uniform at all times, unless otherwise specified for special events.
4. **Technology Use**: Mobile phones must be turned off and kept in lockers during school hours. Laptops and tablets may only be used for educational purposes under teacher supervision.

## Disciplinary Actions
Violations of the Code of Conduct may result in disciplinary actions, including warnings, detention, suspension, or expulsion, depending on the severity of the infraction.
"""
    },
    {
        "id": "DOC-SHARED-003",
        "title": "Exam Schedule 2026-2027",
        "category": "Exams",
        "subject": "General",
        "audience": "All",
        "access_level": "shared",
        "description": "Detailed schedule for the mid-year and final examinations.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/shared/exams/exam_schedule.md",
        "content": """# Exam Schedule 2026-2027

This document provides the examination schedule for the 2026-2027 academic year at Future Scholars International School.

## Mid-Year Examinations (January 2027)
- **January 11**: Mathematics (9:00 AM - 11:00 AM)
- **January 12**: English Language and Literature (9:00 AM - 11:30 AM)
- **January 13**: Sciences (Biology, Chemistry, Physics) (9:00 AM - 11:00 AM)
- **January 14**: History and Geography (9:00 AM - 11:00 AM)
- **January 15**: Modern Foreign Languages (9:00 AM - 10:30 AM)

## Final Examinations (June 2027)
- **June 7**: Mathematics (9:00 AM - 11:00 AM)
- **June 8**: English Language and Literature (9:00 AM - 11:30 AM)
- **June 9**: Sciences (Biology, Chemistry, Physics) (9:00 AM - 11:00 AM)
- **June 10**: History and Geography (9:00 AM - 11:00 AM)
- **June 11**: Modern Foreign Languages (9:00 AM - 10:30 AM)

Students must arrive at the examination hall at least 15 minutes before the start time.
"""
    },
    {
        "id": "DOC-SHARED-004",
        "title": "Homework Policy",
        "category": "Policies",
        "subject": "General",
        "audience": "All",
        "access_level": "shared",
        "description": "Guidelines regarding homework expectations and deadlines.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/shared/school_policies/homework_policy.md",
        "content": """# Homework Policy

Future Scholars International School believes that homework is an essential part of the learning process. It reinforces classroom learning and helps students develop independent study skills.

## Expectations by Grade Level
- **Grades 1-3**: 30-45 minutes per day
- **Grades 4-6**: 45-60 minutes per day
- **Grades 7-9**: 60-90 minutes per day
- **Grades 10-12**: 90-120 minutes per day

## Deadlines and Late Submissions
Homework must be submitted on the specified due date. Late submissions will incur a penalty of 10% deduction per day, up to a maximum of 3 days. After 3 days, the assignment will receive a zero. Exceptions may be granted in cases of illness or family emergencies, provided a valid excuse note is provided.
"""
    },
    {
        "id": "DOC-SHARED-005",
        "title": "Academic Integrity Policy",
        "category": "Policies",
        "subject": "General",
        "audience": "All",
        "access_level": "shared",
        "description": "Policy defining and prohibiting academic dishonesty.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/shared/school_policies/academic_integrity.md",
        "content": """# Academic Integrity Policy

Academic integrity is a core value at Future Scholars International School. We expect all students to produce authentic and original work.

## Definitions of Academic Dishonesty
1. **Plagiarism**: Using another person's words, ideas, or work without proper citation or acknowledgment.
2. **Cheating**: Using unauthorized materials, information, or study aids during an examination or assignment.
3. **Fabrication**: Inventing or falsifying information, data, or citations.
4. **Collusion**: Assisting another student in an act of academic dishonesty.

## Consequences
First offenses will result in a zero for the assignment and a meeting with the parents. Subsequent offenses may lead to suspension and a permanent record of academic misconduct on the student's transcript.
"""
    },
    {
        "id": "DOC-SHARED-006",
        "title": "Student Support Guidelines",
        "category": "Academic",
        "subject": "General",
        "audience": "All",
        "access_level": "shared",
        "description": "Information on support services available to students.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/shared/academic/student_support.md",
        "content": """# Student Support Guidelines

Future Scholars International School is committed to supporting the academic, emotional, and social well-being of all our students.

## Academic Support
Students struggling academically can access free tutoring services provided by peer mentors and teachers. Tutoring sessions are held in the library every Tuesday and Thursday from 3:30 PM to 4:30 PM.

## Counseling Services
The school employs full-time counselors who are available to assist students with personal, social, and emotional issues. Appointments can be scheduled through the main office or by emailing the counseling department directly. Counseling sessions are strictly confidential.
"""
    },
    {
        "id": "DOC-SHARED-007",
        "title": "Mathematics Curriculum Overview",
        "category": "Academic",
        "subject": "Mathematics",
        "audience": "All",
        "access_level": "shared",
        "description": "Overview of the mathematics curriculum for the school year.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/shared/academic/math_curriculum.md",
        "content": """# Mathematics Curriculum Overview

The mathematics curriculum at Future Scholars International School is designed to foster critical thinking, problem-solving skills, and numerical fluency.

## Core Topics
- **Algebra**: Linear equations, quadratic equations, polynomials, and functions.
- **Geometry**: Properties of shapes, theorems, trigonometry, and coordinate geometry.
- **Statistics and Probability**: Data analysis, probability distributions, and statistical inference.
- **Calculus**: Limits, derivatives, integrals, and applications of calculus (introduced in senior years).

## Learning Objectives
Students will develop the ability to apply mathematical concepts to real-world scenarios, construct logical arguments, and communicate mathematical ideas effectively.
"""
    },
    {
        "id": "DOC-SHARED-008",
        "title": "Science Curriculum Overview",
        "category": "Academic",
        "subject": "Science",
        "audience": "All",
        "access_level": "shared",
        "description": "Overview of the science curriculum for the school year.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/shared/academic/science_curriculum.md",
        "content": """# Science Curriculum Overview

Our science curriculum is designed to inspire curiosity and an understanding of the natural world through inquiry-based learning and experimentation.

## Core Subjects
- **Biology**: Cell biology, genetics, evolution, ecology, and human anatomy.
- **Chemistry**: Atomic structure, chemical bonding, reactions, stoichiometry, and organic chemistry.
- **Physics**: Mechanics, thermodynamics, waves, electromagnetism, and modern physics.

## Laboratory Work
Practical laboratory work is a fundamental component of the science curriculum. Students are required to participate in experiments, record observations, and write comprehensive lab reports. Safety goggles and lab coats must be worn at all times during practical sessions.
"""
    },

    # Student Documents (Study Guides, Activities)
    {
        "id": "DOC-STU-MATH-001",
        "title": "Grade 10 Mathematics Study Guide",
        "category": "Study Guide",
        "subject": "Mathematics",
        "audience": "Students",
        "access_level": "student",
        "description": "A comprehensive study guide for Grade 10 mathematics students.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/student/mathematics/grade10_math_guide.md",
        "content": """# Grade 10 Mathematics Study Guide

Welcome to Grade 10 Mathematics! This guide covers key concepts you need to master this year.

## 1. Linear Equations and Inequalities
You will learn to solve systems of linear equations using graphing, substitution, and elimination methods. Remember that an inequality represents a range of possible solutions rather than a single point.

## 2. Quadratic Functions
A quadratic function takes the form f(x) = ax^2 + bx + c. The graph of a quadratic function is a parabola. You must be able to find the vertex, axis of symmetry, and roots (x-intercepts) using factoring or the quadratic formula.

## 3. Trigonometry
Trigonometry focuses on the relationships between the angles and sides of triangles. Key concepts include SOH CAH TOA (Sine, Cosine, Tangent) and applying the Sine and Cosine rules to non-right-angled triangles.

## Study Tips
- Practice daily: Math requires consistent practice. Complete all homework assignments.
- Show your work: Always write down the steps you took to arrive at your answer.
- Ask for help: If you are struggling with a concept, attend the after-school tutoring sessions.
"""
    },
    {
        "id": "DOC-STU-SCI-001",
        "title": "Physics Fundamentals",
        "category": "Study Guide",
        "subject": "Science",
        "audience": "Students",
        "access_level": "student",
        "description": "Basic principles of physics for middle and high school students.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/student/science/physics_fundamentals.md",
        "content": """# Physics Fundamentals

Physics is the study of matter, energy, and the fundamental forces of nature.

## Newton's Laws of Motion
1. **First Law (Inertia)**: An object at rest stays at rest, and an object in motion stays in motion with the same speed and in the same direction unless acted upon by an unbalanced force.
2. **Second Law (F=ma)**: The acceleration of an object depends on the mass of the object and the amount of force applied. Force equals mass times acceleration.
3. **Third Law**: For every action, there is an equal and opposite reaction.

## Energy
Energy cannot be created or destroyed, only transformed from one form to another (Law of Conservation of Energy). Important forms include kinetic energy (energy of motion) and potential energy (stored energy).

## Waves and Sound
A wave is a disturbance that transfers energy through space or a medium. Sound is a longitudinal wave that requires a medium (like air or water) to travel.
"""
    },
    {
        "id": "DOC-STU-ENG-001",
        "title": "Essay Writing Guide",
        "category": "Study Guide",
        "subject": "English",
        "audience": "Students",
        "access_level": "student",
        "description": "A student guide to structuring and writing effective essays.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/student/english/essay_writing_guide.md",
        "content": """# Essay Writing Guide

Writing a strong essay is a crucial skill for your academic success at Future Scholars International School. Follow these structural guidelines.

## 1. Introduction
The introduction should hook the reader, provide necessary background information, and present a clear thesis statement. The thesis statement is the main argument of your essay and usually appears at the end of the introductory paragraph.

## 2. Body Paragraphs
Each body paragraph should focus on a single main idea that supports your thesis. Use the PEEL structure:
- **Point**: A topic sentence stating the main idea.
- **Evidence**: Examples, quotes, or data to support your point.
- **Explanation**: An analysis of how the evidence supports your point and thesis.
- **Link**: A concluding sentence that links back to the thesis and transitions to the next paragraph.

## 3. Conclusion
The conclusion should restate your thesis (in different words), summarize the main points of your body paragraphs, and provide a final thought or call to action. Do not introduce new information in the conclusion.
"""
    },
    {
        "id": "DOC-STU-GEN-001",
        "title": "Exam Preparation Guide",
        "category": "Guide",
        "subject": "General",
        "audience": "Students",
        "access_level": "student",
        "description": "Tips and strategies for preparing for school examinations.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/student/general/exam_prep_guide.md",
        "content": """# Exam Preparation Guide

Effective exam preparation begins weeks before the actual test. Use these strategies to maximize your performance.

## Create a Study Schedule
Plan your study time well in advance. Allocate more time to challenging subjects and break your study sessions into manageable chunks (e.g., the Pomodoro Technique: 25 minutes of studying followed by a 5-minute break).

## Active Recall and Spaced Repetition
Instead of just re-reading notes, use active recall by testing yourself on the material. Use flashcards for key terms and concepts. Review the material at increasing intervals (spaced repetition) to move information into long-term memory.

## Past Papers
Practicing with past examination papers is one of the best ways to prepare. It helps you familiarize yourself with the format of the questions and manage your time effectively during the exam.

## Healthy Habits
Ensure you get at least 8 hours of sleep per night, especially before the exam. Eat a healthy breakfast and stay hydrated.
"""
    },
    {
        "id": "DOC-STU-ACT-001",
        "title": "Student Activities Guide",
        "category": "Activities",
        "subject": "Extracurricular",
        "audience": "Students",
        "access_level": "student",
        "description": "Information on clubs, sports, and extracurricular activities.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/student/activities/activities_guide.md",
        "content": """# Student Activities Guide

Future Scholars International School offers a wide range of extracurricular activities to enrich your educational experience.

## Sports Teams
Tryouts for the following sports teams take place in the first week of September:
- Soccer (Boys and Girls)
- Basketball (Boys and Girls)
- Swimming
- Track and Field

## Clubs and Societies
- **Debate Club**: Meets Wednesdays at 3:45 PM in Room 102.
- **Robotics Club**: Meets Thursdays at 4:00 PM in the Science Lab.
- **Drama Society**: Prepares for the annual school play. Auditions will be held in October.
- **Environmental Club**: Focuses on sustainability initiatives around the school campus.

Students are encouraged to participate in at least one extracurricular activity per semester.
"""
    },
    {
        "id": "DOC-STU-SCI-002",
        "title": "Biology Fundamentals",
        "category": "Study Guide",
        "subject": "Science",
        "audience": "Students",
        "access_level": "student",
        "description": "Basic principles of biology for students.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/student/science/biology_fundamentals.md",
        "content": """# Biology Fundamentals

Biology is the study of life and living organisms.

## Cell Theory
All living things are composed of cells. The cell is the basic unit of life, and all new cells arise from existing cells. Key organelles include the nucleus (contains DNA), mitochondria (produces energy), and ribosomes (synthesize proteins).

## Genetics
Genetics is the study of heredity. Traits are passed from parents to offspring through genes, which are segments of DNA. Humans have 23 pairs of chromosomes.

## Evolution
Evolution explains how species change over time through the process of natural selection, where organisms best suited to their environment are more likely to survive and reproduce.
"""
    },
    {
        "id": "DOC-STU-SCI-003",
        "title": "Chemistry Basics",
        "category": "Study Guide",
        "subject": "Science",
        "audience": "Students",
        "access_level": "student",
        "description": "Basic principles of chemistry for students.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/student/science/chemistry_basics.md",
        "content": """# Chemistry Basics

Chemistry is the study of matter and the changes it undergoes.

## Atomic Structure
Atoms consist of a nucleus containing protons (positive charge) and neutrons (no charge), surrounded by electrons (negative charge) in specific energy levels or shells.

## Periodic Table
The Periodic Table organizes elements based on their atomic number and chemical properties. Elements in the same column (group) have similar properties.

## Chemical Bonding
Atoms form bonds to achieve a stable electron configuration.
- **Ionic Bonds**: Formed when electrons are transferred from one atom to another.
- **Covalent Bonds**: Formed when atoms share electrons.
"""
    },
    {
        "id": "DOC-STU-MATH-002",
        "title": "Geometry Fundamentals",
        "category": "Study Guide",
        "subject": "Mathematics",
        "audience": "Students",
        "access_level": "student",
        "description": "Basic principles of geometry for students.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/student/mathematics/geometry_fundamentals.md",
        "content": """# Geometry Fundamentals

Geometry deals with the properties and relations of points, lines, surfaces, and solids.

## Triangles
- The sum of the interior angles of a triangle is always 180 degrees.
- **Pythagorean Theorem**: In a right-angled triangle, the square of the hypotenuse is equal to the sum of the squares of the other two sides (a^2 + b^2 = c^2).

## Circles
- **Circumference**: The distance around the circle (C = 2πr).
- **Area**: The space enclosed by the circle (A = πr^2).

## Volume
Volume is the amount of space occupied by a 3D object.
- **Cube**: V = s^3
- **Cylinder**: V = πr^2h
"""
    },
    {
        "id": "DOC-STU-MATH-003",
        "title": "Algebra Fundamentals",
        "category": "Study Guide",
        "subject": "Mathematics",
        "audience": "Students",
        "access_level": "student",
        "description": "Basic principles of algebra for students.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/student/mathematics/algebra_fundamentals.md",
        "content": """# Algebra Fundamentals

Algebra uses letters (variables) to represent numbers in equations and formulas.

## Variables and Expressions
A variable represents an unknown value. An expression is a combination of variables, numbers, and operations (e.g., 3x + 5).

## Solving Equations
The goal is to isolate the variable on one side of the equation. What you do to one side, you must do to the other to maintain balance.
Example: 
2x - 4 = 10
2x = 14
x = 7

## Factoring
Factoring involves breaking down an expression into a product of simpler expressions. Common techniques include factoring out the greatest common factor (GCF) and factoring quadratics (x^2 + bx + c).
"""
    },
    {
        "id": "DOC-STU-ENG-002",
        "title": "English Grammar Guide",
        "category": "Study Guide",
        "subject": "English",
        "audience": "Students",
        "access_level": "student",
        "description": "A quick reference guide for English grammar rules.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/student/english/grammar_guide.md",
        "content": """# English Grammar Guide

Mastering grammar is essential for clear and effective communication.

## Parts of Speech
- **Noun**: A person, place, thing, or idea.
- **Verb**: An action or state of being.
- **Adjective**: Modifies a noun or pronoun.
- **Adverb**: Modifies a verb, adjective, or another adverb.

## Subject-Verb Agreement
The subject and verb must agree in number (singular or plural).
- *Incorrect*: The dogs barks.
- *Correct*: The dogs bark.

## Punctuation
- **Comma**: Used to separate items in a list, join independent clauses (with a conjunction), and set off introductory phrases.
- **Semicolon**: Used to link closely related independent clauses without a conjunction.
"""
    },
    {
        "id": "DOC-STU-GEN-002",
        "title": "Student Study Skills",
        "category": "Guide",
        "subject": "General",
        "audience": "Students",
        "access_level": "student",
        "description": "Strategies for effective studying and time management.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/student/general/study_skills.md",
        "content": """# Student Study Skills

Developing strong study skills will benefit you throughout your academic career.

## Time Management
Use a planner or digital calendar to track assignments, tests, and extracurricular activities. Prioritize tasks based on urgency and importance. Avoid procrastination by breaking large tasks into smaller, manageable steps.

## Note-Taking
During class, focus on capturing key concepts and main ideas rather than writing down every word the teacher says. Consider using the Cornell Method: divide your page into a cue column (for keywords/questions), a notes column, and a summary section at the bottom.

## Reading Strategies
When reading textbook chapters, use the SQ3R method: Survey (skim the headings), Question (turn headings into questions), Read (to find the answers), Recite (say the answers aloud), and Review (summarize what you read).
"""
    },
    {
        "id": "DOC-STU-GEN-003",
        "title": "Student FAQ",
        "category": "FAQ",
        "subject": "General",
        "audience": "Students",
        "access_level": "student",
        "description": "Frequently asked questions by students.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/student/general/student_faq.md",
        "content": """# Student FAQ

**Q: What should I do if I am absent from school?**
A: Your parents must email the attendance office before 9:00 AM on the day of your absence. Upon returning, you are responsible for checking the online portal for missed assignments and speaking with your teachers to catch up on missed work.

**Q: How do I access the school Wi-Fi?**
A: Use your student ID number as the username and your portal password to connect to the 'FSIS-Student' network.

**Q: Where can I get a replacement ID card?**
A: Replacement ID cards can be requested at the main office. There is a $10 fee for lost cards.
"""
    },


    # Teacher Documents (Grading, Assessments, Admin)
    {
        "id": "DOC-TCH-GEN-001",
        "title": "Teacher Grading Policy",
        "category": "Policy",
        "subject": "General",
        "audience": "Teachers",
        "access_level": "teacher",
        "description": "Internal grading percentages and procedures for staff.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/teacher/general/grading_policy.md",
        "content": """# Teacher Grading Policy

This document outlines the internal grading policy for Future Scholars International School. **This information is strictly for teaching staff and must not be shared with students or parents.**

## Grade Weighting Configuration
All gradebooks must be configured in the internal system with the following specific weights:
- **Formative Assessments (Quizzes, Classwork)**: 35%
- **Summative Assessments (Unit Tests, Projects)**: 45%
- **Homework and Participation**: 20%

## Late Work Policy (Internal Guidance)
While the student handbook states a strict 10% penalty per day for late work, teachers are granted internal discretion to waive this penalty for students with documented IEPs (Individualized Education Programs) or under direction from the counseling department. Ensure you check the internal flags in the Student Information System before applying penalties.

## Grade Submission Deadlines
Quarterly grades must be submitted to the registrar's office no later than 4:00 PM on the Wednesday following the end of the quarter.
"""
    },
    {
        "id": "DOC-TCH-GEN-002",
        "title": "Assessment Design Guidelines",
        "category": "Guidelines",
        "subject": "General",
        "audience": "Teachers",
        "access_level": "teacher",
        "description": "Guidelines for creating fair and rigorous assessments.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/teacher/general/assessment_design.md",
        "content": """# Assessment Design Guidelines

Assessments must be designed to accurately measure student mastery of learning objectives.

## Cognitive Rigor
Use Bloom's Taxonomy to ensure assessments evaluate a range of cognitive skills.
- **Knowledge/Comprehension**: 30% of assessment items.
- **Application/Analysis**: 40% of assessment items.
- **Synthesis/Evaluation**: 30% of assessment items.

## Test Security
- All summative assessment drafts must be stored on the secure teacher shared drive (`T:\\Assessments`). Do not save them on local hard drives.
- Printed copies of exams must be kept in the locked cabinet in the departmental office until the day of the exam.
- Any suspected breach of test security must be reported immediately to the Academic Coordinator.
"""
    },
    {
        "id": "DOC-TCH-MATH-001",
        "title": "Mathematics Teacher Guide",
        "category": "Teacher Guide",
        "subject": "Mathematics",
        "audience": "Teachers",
        "access_level": "teacher",
        "description": "Instructional strategies and pacing for mathematics courses.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/teacher/mathematics/math_teacher_guide.md",
        "content": """# Mathematics Teacher Guide

## Pacing Guide for Grade 10
- **Quarter 1**: Linear Equations, Inequalities, and Systems (Weeks 1-9)
- **Quarter 2**: Polynomials and Quadratic Functions (Weeks 10-18)
- **Quarter 3**: Exponential and Logarithmic Functions (Weeks 19-27)
- **Quarter 4**: Trigonometry and Statistics (Weeks 28-36)

## Addressing Common Misconceptions
When teaching quadratic functions, a common student error is failing to recognize that taking the square root of a number yields both a positive and a negative result. Emphasize this repeatedly during instruction.

## Approved Resources
Only use approved textbooks and the supplementary materials listed on the departmental intranet page. Use of external online worksheets must be vetted by the Head of Department to ensure alignment with our curriculum standards.
"""
    },
    {
        "id": "DOC-TCH-SCI-001",
        "title": "Science Teacher Guide",
        "category": "Teacher Guide",
        "subject": "Science",
        "audience": "Teachers",
        "access_level": "teacher",
        "description": "Lab safety and equipment procedures for science teachers.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/teacher/science/science_teacher_guide.md",
        "content": """# Science Teacher Guide

## Laboratory Safety Protocols (Internal)
Teachers are legally responsible for student safety during laboratory sessions.
- **Inventory**: The chemical inventory key is kept in the lockbox in the prep room. The code is 8421. Do not share this code with students.
- **Disposal**: Hazardous waste must be segregated according to the protocol on page 42 of the internal safety manual. Never dispose of organic solvents in the sink.
- **Incident Reporting**: If a student is injured, administer first aid immediately, notify the school nurse, and complete an Incident Report Form (available on the staff portal) within 24 hours.

## Standardized Lab Rubric
When grading lab reports, allocate 40% of the grade to Data Analysis and Evaluation, 30% to Method and Procedure, 20% to Conclusion, and 10% to formatting and safety compliance.
"""
    },
    {
        "id": "DOC-TCH-ENG-001",
        "title": "English Teacher Guide",
        "category": "Teacher Guide",
        "subject": "English",
        "audience": "Teachers",
        "access_level": "teacher",
        "description": "Guidelines for grading essays and selecting literature.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/teacher/english/english_teacher_guide.md",
        "content": """# English Teacher Guide

## Essay Grading Standardization
To ensure consistency across the English department, all teachers must use the departmental analytic rubric for grading major essays.
- Focus heavily on thesis development and evidence integration.
- For grammar and mechanics, deduct a maximum of 15% of the total essay grade, unless the errors significantly impede comprehension.

## Plagiarism Detection
All final drafts of major papers must be submitted through the Turnitin integration in the LMS. Any paper with a similarity index above 25% requires a manual review. If plagiarism is confirmed, follow the procedure outlined in the Academic Integrity Policy and notify the Dean of Students.

## Approved Literature List
Any text not on the pre-approved literature list requires a Curriculum Review Request form to be submitted 30 days prior to the start of the unit.
"""
    },
    {
        "id": "DOC-TCH-GEN-003",
        "title": "Lesson Planning Standards",
        "category": "Standards",
        "subject": "General",
        "audience": "Teachers",
        "access_level": "teacher",
        "description": "Requirements for teacher lesson plans.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/teacher/general/lesson_planning.md",
        "content": """# Lesson Planning Standards

All teaching staff are required to maintain detailed lesson plans.

## Required Components
Every lesson plan must include the following components:
1. **Learning Objective**: Clearly stated using measurable action verbs (e.g., 'Students will be able to evaluate...').
2. **Standard Alignment**: Reference the specific curriculum standard addressed.
3. **Differentiation Strategy**: How the lesson will be adapted for English Language Learners (ELL) and students with special educational needs.
4. **Formative Assessment Check**: The specific method used to check for understanding during the lesson (e.g., exit ticket, Think-Pair-Share).

## Submission
Lesson plans for the upcoming week must be uploaded to the principal's shared folder by 5:00 PM every Friday. Random audits will be conducted monthly.
"""
    },
    {
        "id": "DOC-TCH-GEN-004",
        "title": "Classroom Management Guidelines",
        "category": "Guidelines",
        "subject": "General",
        "audience": "Teachers",
        "access_level": "teacher",
        "description": "Internal procedures for handling classroom behavior.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/teacher/general/classroom_management.md",
        "content": """# Classroom Management Guidelines

Effective classroom management is essential for a productive learning environment.

## The Three-Strike Intervention Model
1. **Strike 1 (Verbal Warning)**: Privately redirect the student's behavior. Do not embarrass them in front of the class.
2. **Strike 2 (Seat Change/Detention)**: Move the student or assign a teacher-led detention. Log this intervention in the Student Behavior System (SBS).
3. **Strike 3 (Office Referral)**: Send the student to the Dean of Students with an accompanying referral slip. 

## De-escalation Techniques
If a student becomes aggressive or highly agitated, remain calm, lower your voice, and avoid power struggles. If the situation presents a safety risk to other students, press the emergency call button located near the classroom door to summon administration immediately.
"""
    },
    {
        "id": "DOC-TCH-STAFF-001",
        "title": "Teacher Attendance Procedures",
        "category": "Procedures",
        "subject": "Staff",
        "audience": "Teachers",
        "access_level": "teacher",
        "description": "Procedures for reporting teacher absences and arranging coverage.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/teacher/staff/attendance_procedures.md",
        "content": """# Teacher Attendance Procedures

## Reporting an Absence
If you are unable to report to work due to illness or an emergency, you must log the absence in the AES (Automated Absence System) before 6:00 AM on the day of the absence. You must also text the Cover Manager at 555-0199 to ensure a substitute is secured.

## Sub Plans
Emergency sub plans (covering at least three days of generic instruction) must be kept in the bright red folder on your desk at all times. Update these plans at the beginning of each semester.

## Personal Days
Requests for personal leave must be submitted via the HR portal at least two weeks in advance. Personal days will not be approved during standardized testing weeks or the week immediately preceding winter or spring break.
"""
    },
    {
        "id": "DOC-TCH-STAFF-002",
        "title": "Academic Performance Review Procedures",
        "category": "Procedures",
        "subject": "Staff",
        "audience": "Teachers",
        "access_level": "teacher",
        "description": "Procedures for annual teacher performance reviews.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/teacher/staff/performance_review.md",
        "content": """# Academic Performance Review Procedures

This outlines the annual performance evaluation process for instructional staff.

## The Evaluation Cycle
1. **Goal Setting (September)**: Teachers submit two professional growth goals to their department head.
2. **Formal Observation (November - February)**: The principal or department head will conduct one scheduled and one unannounced observation.
3. **Mid-Year Check-in (January)**: A brief meeting to review progress toward goals.
4. **Summative Evaluation (May)**: A final meeting to review the overall performance rating, which is based on observations, student growth metrics, and professional contributions.

## Rating Scale
Teachers are rated on a four-point scale: Highly Effective, Effective, Developing, and Ineffective. Two consecutive years of an 'Ineffective' rating will result in non-renewal of contract.
"""
    },
    {
        "id": "DOC-TCH-STAFF-003",
        "title": "Teacher Responsibilities Handbook",
        "category": "Handbook",
        "subject": "Staff",
        "audience": "Teachers",
        "access_level": "teacher",
        "description": "Overview of duties outside of classroom instruction.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/teacher/staff/responsibilities.md",
        "content": """# Teacher Responsibilities Handbook

Beyond instructional duties, teachers are expected to fulfill various operational roles.

## Duty Roster
All teachers are assigned weekly supervision duties (e.g., cafeteria monitoring, hallway duty, or bus duty). Ensure you arrive at your duty station on time. The duty roster is posted on the staff room bulletin board.

## Parent-Teacher Conferences
Parent-Teacher conferences are held twice a year (November and April). Teachers must be available from 4:00 PM to 8:00 PM on conference days. Maintain detailed records of student progress to share with parents. Ensure interactions remain professional; if a parent becomes hostile, immediately request the presence of an administrator.
"""
    },
    {
        "id": "DOC-TCH-STAFF-004",
        "title": "Exam Administration Procedures",
        "category": "Procedures",
        "subject": "Staff",
        "audience": "Teachers",
        "access_level": "teacher",
        "description": "Secure procedures for proctoring exams.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/teacher/staff/exam_administration.md",
        "content": """# Exam Administration Procedures

To maintain the integrity of our assessment system, teachers must strictly adhere to these proctoring rules.

## Prior to the Exam
- Ensure desks are spaced appropriately.
- Write the start and end times clearly on the whiteboard.
- Instruct students to place all bags, phones, and smartwatches at the front of the room.

## During the Exam
- Active invigilation is required. Do not grade papers or use your phone while proctoring. Continually circulate the room.
- If you suspect a student is cheating, confiscate their paper immediately, note the time and circumstances on the paper, provide them with a fresh exam booklet to continue, and file an incident report immediately after the exam concludes.

## After the Exam
- Count all exam booklets before allowing students to leave the room. No materials may leave the testing environment.
"""
    },
    {
        "id": "DOC-TCH-STAFF-005",
        "title": "Teacher Feedback Guidelines",
        "category": "Guidelines",
        "subject": "Staff",
        "audience": "Teachers",
        "access_level": "teacher",
        "description": "Guidelines on providing effective feedback to students.",
        "path": "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/raw/teacher/staff/feedback_guidelines.md",
        "content": """# Teacher Feedback Guidelines

Providing timely and actionable feedback is critical for student growth.

## Actionable and Specific
Feedback should clearly identify what the student did well and specific steps for improvement. Avoid vague comments like 'Good job' or 'Needs work'. Instead, state: 'Your thesis statement is clear, but your second paragraph needs more statistical evidence to support your claim.'

## Timeliness
Assignments must be graded and returned with feedback within one week of submission. Major projects and essays must be returned within two weeks.

## The Feedback Sandwich
When providing constructive criticism, utilize the feedback sandwich approach internally: start with a positive observation, provide the critical feedback, and end with an encouraging remark or a specific action step.
"""
    }
]

def generate_dataset():
    # Ensure directories exist
    for doc in DOCUMENTS:
        os.makedirs(os.path.dirname(doc['path']), exist_ok=True)
        
        # Write Markdown file
        with open(doc['path'], 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write(f"Document ID: {doc['id']}\n")
            f.write(f"Title: {doc['title']}\n")
            f.write(f"Category: {doc['category']}\n")
            f.write(f"Subject: {doc['subject']}\n")
            f.write(f"Audience: {doc['audience']}\n")
            f.write(f"Access Level: {doc['access_level']}\n")
            f.write(f"Description: {doc['description']}\n")
            f.write("---\n\n")
            f.write(doc['content'])

    # Write CSV manifest
    csv_path = "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/dataset_manifest.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['document_id', 'title', 'category', 'subject', 'audience', 'access_level', 'file_path', 'description'])
        for doc in DOCUMENTS:
            # save relative path in manifest for portability
            rel_path = doc['path'].split('school-rag-assistant/')[1]
            writer.writerow([doc['id'], doc['title'], doc['category'], doc['subject'], doc['audience'], doc['access_level'], rel_path, doc['description']])

    # Write Markdown manifest
    md_path = "c:/Users/acer/Downloads/PROJECT-ITI-RAG-SYS/school-rag-assistant/data/dataset_manifest.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# Dataset Manifest\n\n")
        f.write("| Document ID | Title | Category | Subject | Audience | Access Level | File Path | Description |\n")
        f.write("|-------------|-------|----------|---------|----------|--------------|-----------|-------------|\n")
        for doc in DOCUMENTS:
            rel_path = doc['path'].split('school-rag-assistant/')[1]
            f.write(f"| {doc['id']} | {doc['title']} | {doc['category']} | {doc['subject']} | {doc['audience']} | {doc['access_level']} | `{rel_path}` | {doc['description']} |\n")

    print(f"Generated {len(DOCUMENTS)} documents successfully.")

if __name__ == "__main__":
    generate_dataset()
