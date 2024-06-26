ROLE_ADMIN = "admin"
ROLE_STAFF = "staff"
ROLE_USER = "user"

USER_ROLE_CHOICES = [
    (ROLE_ADMIN, ROLE_ADMIN),
    (ROLE_STAFF, ROLE_STAFF),
    (ROLE_USER, ROLE_USER),
]

DESIGNATION_DEAN = "dean"
DESIGNATION_CHAIRMAN = "chairman"
DESIGNATION_PROFESSOR = "professor"
DESIGNATION_ASSOCIATE_PROFESSOR = "associate_professor"
DESIGNATION_STUDENT = "student"

DESIGNATION_ROLE_CHOICES = [
    (DESIGNATION_DEAN, DESIGNATION_DEAN),
    (DESIGNATION_CHAIRMAN, DESIGNATION_CHAIRMAN),
    (DESIGNATION_PROFESSOR, DESIGNATION_PROFESSOR),
    (DESIGNATION_ASSOCIATE_PROFESSOR, DESIGNATION_ASSOCIATE_PROFESSOR),
    (DESIGNATION_STUDENT, DESIGNATION_STUDENT),
]

DEPT_FISH = "fisheries"
DEPT_MARINE = "marine"
DEPT_OCEAN = "oceanography"

DEPARTMENT_CHOICES = [
    (DEPT_FISH, DEPT_FISH),
    (DEPT_MARINE, DEPT_MARINE),
    (DEPT_OCEAN, DEPT_OCEAN),
]

YEAR_1ST = "1st year"
YEAR_2ND = "2nd year"
YEAR_3RD = "3rd year"
YEAR_4TH = "4th year"

YEAR_CHOICES = [
    (YEAR_1ST, YEAR_1ST),
    (YEAR_2ND, YEAR_2ND),
    (YEAR_3RD, YEAR_3RD),
    (YEAR_4TH, YEAR_4TH),
]

SEM_1 = "1st semester"
SEM_2 = "2nd semester"
SEM_3 = "3rd semester"
SEM_4 = "4th semester"
SEM_5 = "5th semester"
SEM_6 = "6th semester"
SEM_7 = "7th semester"
SEM_8 = "8th semester"
SEM_9 = "9th semester"
SEM_10 = "10th semester"

SEMESTER_CHOICES = [
    (SEM_1, SEM_1),
    (SEM_2, SEM_2),
    (SEM_3, SEM_3),
    (SEM_4, SEM_4),
    (SEM_5, SEM_5),
    (SEM_6, SEM_6),
    (SEM_7, SEM_7),
    (SEM_8, SEM_8),
    (SEM_9, SEM_9),
    (SEM_10, SEM_10),
]

DEGREE_BSC = "B.Sc"
DEGREE_MSC = "M.Sc"
DEGREE_PHD = "PhD"

DEGREE_CHOICES = [
    (DEGREE_BSC, DEGREE_BSC),
    (DEGREE_MSC, DEGREE_MSC),
    (DEGREE_PHD, DEGREE_PHD),
]

GENDER_MALE = "male"
GENDER_FEMALE = "female"
GENDER_OTHER = "other"

GENDER_CHOICES = [
    (GENDER_MALE, GENDER_MALE),
    (GENDER_FEMALE, GENDER_FEMALE),
    (GENDER_OTHER, GENDER_OTHER),
]

ENROLL_S = "success"
ENROLL_F = "failed"

ENROLL_CHOICES = [
    (ENROLL_S, ENROLL_S),
    (ENROLL_F, ENROLL_F),
]
