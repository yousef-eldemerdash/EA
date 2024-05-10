import Classes

# Data preparation

# Faculty Creation
computer_science = Classes.Faculty("Computer Science And Artificial Intelligence")

# Professors Creation
Dr_AmanyMostafa = Classes.FacultyMember("Dr. Amany Mostafa", computer_science, availability=[])
Dr_HanyMohamed = Classes.FacultyMember("Dr. Hany Mohamed", computer_science, availability=[])
Dr_LailaAbdelhamed = Classes.FacultyMember("Dr. Laila Abdelhamed", computer_science, availability=[])
Dr_AzzaMohamed = Classes.FacultyMember("Dr. Azza Mohamed", computer_science, availability=[])
Dr_AliGhandor = Classes.FacultyMember("Dr. Ali Ghandor", computer_science, availability=[])
Dr_AmrGhoneim = Classes.FacultyMember("Dr. Amr Ghoneim", computer_science, availability=[])
Dr_MohamedElSaid = Classes.FacultyMember("Dr. Mohamed El-Said", computer_science, availability=[])
Dr_HossamShamrdan = Classes.FacultyMember("Dr. Hossam shamrdan", computer_science, availability=[])
Dr_WessamElBehaidy = Classes.FacultyMember("Dr. Wessam El-Behaidy", computer_science, availability=[])
Dr_HananFahmy = Classes.FacultyMember("Dr. Hanan Fahmy", computer_science, availability=[])
Dr_IslamGamal = Classes.FacultyMember("Dr. Islam Gamal", computer_science, availability=[])
Dr_YasserFahmy = Classes.FacultyMember("Dr. Yasser Fahmy", computer_science, availability=[])
Dr_WaelAbbas = Classes.FacultyMember("Dr. Wael Abbas", computer_science, availability=[])
Dr_MohamedMarri = Classes.FacultyMember("Dr. Mohamed Marri", computer_science, availability=[])
Dr_AhmedHesham = Classes.FacultyMember("Dr. Ahmed Hesham", computer_science, availability=[])
Dr_AhmedElSaed = Classes.FacultyMember("Dr. Ahmed EL-Saed", computer_science, availability=[])



# Course Creation
Mathematics1 = Classes.Course("MA 111", "Mathematics-1", 2, computer_science, "general", instructor=Dr_AmanyMostafa)
Physics = Classes.Course("PH 111", "Physics", 2, computer_science, "general", instructor=Dr_HanyMohamed)
Electronics = Classes.Course("IT 111", "Electronics-1", 2, computer_science, "general", instructor=Dr_AzzaMohamed)
ComputerScience = Classes.Course("CS-111", "Introduction to computer science", 2, computer_science, "general", instructor=Dr_AmrGhoneim)
InformationSystem = Classes.Course("IS-231", "Fundamentals of information system", 2, computer_science, "general", instructor=Dr_LailaAbdelhamed)
DataCommunication = Classes.Course("IT 221", "Data Communication", 2, computer_science, "general", instructor=Dr_HossamShamrdan)
PL2 = Classes.Course("CS 213", "Programming-2", 2, computer_science, "general", instructor=Dr_MohamedElSaid)
DataStructure = Classes.Course("CS 214", "Data Structure", 2, computer_science, "general", instructor=Dr_MohamedElSaid)
LogicDesign = Classes.Course("CS 221", "Logic Design", 2, computer_science, "general", instructor=Dr_WessamElBehaidy)
OperationResearch = Classes.Course("IS 240", "Operation Research", 2, computer_science, "general", instructor=Dr_LailaAbdelhamed)
DataBase1 = Classes.Course("IS 211", "Database system-1", 2, computer_science, "general", instructor=Dr_HananFahmy)
ArtificialIntelligence= Classes.Course("AI 310", "Artificial Intelligence", 2, computer_science, "AI", instructor=Dr_AmrGhoneim)
BigDataTech= Classes.Course("IS 365", "Big data technology", 2, computer_science, "IS", instructor=Dr_WaelAbbas)
DataBase2= Classes.Course("IS 312", "Database system-2", 2, computer_science, "IS", instructor=Dr_LailaAbdelhamed)
MachineLearning= Classes.Course("AI 330", "Machine Learning", 2, computer_science, "AI", instructor=Dr_WessamElBehaidy)
DigitalSignalProcessing= Classes.Course("IT 341", "Digital signal processing", 2, computer_science, "IT", instructor=Dr_YasserFahmy)
ConvexOptimization= Classes.Course("AI 320", "Convex optimization theory", 2, computer_science, "AI", instructor=Dr_IslamGamal)
ParallelProcessing= Classes.Course("CS 471", "Parallel processing and high performance computing", 2, computer_science, "CS", instructor=Dr_AhmedHesham)
InformationSystemSecurity= Classes.Course("IS 414", "Information system security", 2, computer_science, "IS", instructor=Dr_MohamedMarri)
OperatingSystem2= Classes.Course("CS 342", "Operating system-2", 2, computer_science, "CS", instructor=Dr_MohamedElSaid)
Multimedia= Classes.Course("IT 433", "Multimedia", 2, computer_science, "IT", instructor=Dr_HossamShamrdan)
DataStorageAndRetrieval= Classes.Course("IS 313", "Data storage and retrieval", 2, computer_science, "IS", instructor=Dr_AhmedElSaed)





# Classroom Creation
Hall1= Classes.Classroom(1, 50, computer_science)
Hall2= Classes.Classroom(2, 50, computer_science)
Hall3= Classes.Classroom(3, 50, computer_science)
Hall4= Classes.Classroom(4, 50, computer_science)
Hall5= Classes.Classroom(5, 50, computer_science)
Hall6= Classes.Classroom(6, 50, computer_science)
Hall7= Classes.Classroom(7, 50, computer_science)
Hall8= Classes.Classroom(8, 50, computer_science)



# Timeslots Creation
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
start_times = ["8:00 AM", "10:00 AM", "12:00 PM", "2:00 PM", "4:00 PM"]
end_times = ["10:00 AM", "12:00 PM", "2:00 PM", "4:00 PM", "6:00 PM"]
for day in days:
    for start_time, end_time in zip(start_times, end_times):
        Classes.Timeslot(day, start_time, end_time)



