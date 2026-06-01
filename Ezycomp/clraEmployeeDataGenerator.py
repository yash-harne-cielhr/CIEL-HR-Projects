import os
import random
import datetime
import calendar
import pandas as pd

# ========================
# CONFIG
# ========================
PARENT_COMPANY = "QA Parent Company"
ASSOCIATE_COMPANY = "QA Associate test 3"
Establishment_type = "CLRA"
NUM_EMPLOYEES = 10

LOCATION_GROUPS = [
    # {"STATE": "Andhra Pradesh", "LOCATION": "AP-EL", "SUB_CODE": "CLRA_EMP_AP"},
    # {"STATE": "Andhra Pradesh", "LOCATION": "AP-EL", "SUB_CODE": "CLRA_SUB_AP"},
    # {"STATE": "Assam", "LOCATION": "AS-GU", "SUB_CODE": "AS-ASE"},
    # {"STATE": "Assam", "LOCATION": "AS-GU", "SUB_CODE": "AS-ASS"},
]

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BASE_PATH = r"C:\Users\Yash Harne\OneDrive\Desktop\Ezycomp\CLRA"
OUTPUT_FOLDER = os.path.join(BASE_PATH, f"{ASSOCIATE_COMPANY}_{timestamp}")

# Define all periods you want here (year, month_name)
PERIODS = [
    (2024, "January"),
    (2024, "February"),
    (2024, "March"),
    (2024, "April"),
    (2024, "May"),
    (2024, "June"),
    (2024, "July"),
    (2024, "August"),
    (2024, "September"),
    (2024, "October"),
    (2024, "November"),
    (2024, "December"),
    
    (2025, "January"),
    (2025, "February"),
    (2025, "March"),
    (2025, "April"),
    (2025, "May"),
    (2025, "June"),
    (2025, "July"),
    (2025, "August"),
    (2025, "September"),
    (2025, "October"),
    (2025, "November"),
    (2025, "December"),
    
    (2026, "January"),
    (2026, "February")
]


# ========================
# Sample Data
# ========================
male_firstnames = ["Aarav","Vivaan","Aditya","Arjun","Krishna","Rohan","Karthik","Manav","Ishaan","Sai","Harsh","Pranav","Rahul","Dhanush","Omkar"]
female_firstnames = ["Ananya","Saanvi","Diya","Ira","Aadhya","Meera","Kavya","Riya","Pooja","Shruti","Naina","Anushka","Tanya","Ishita","Madhuri"]
surnames = ["Sharma","Verma","Patel","Reddy","Nair","Gupta","Kulkarni","Joshi","Iyer","Singh","Khare","Choudhary","Mehta","Deshmukh","Yadav", ""]

# ========================
# Helpers
# ========================
def random_leave_type():
    return random.choice(["PL", "EL", "SL", "CL", "ML", "AL", "LOP", "HFD"])

def random_date_in_month(year, month_num):
    days_in_month = calendar.monthrange(year, month_num)[1]
    day = random.randint(1, days_in_month)
    return datetime.date(year, month_num, day)

def assign_location_groups(num_employees):
    num_groups = len(LOCATION_GROUPS)
    per_group = num_employees // num_groups
    assigned = []

    for i in range(num_employees):
        idx = i // per_group
        if idx >= num_groups:
            idx = num_groups - 1
        assigned.append(LOCATION_GROUPS[idx])

    return assigned

# ========================
# Employee Master (full-year randoms allowed)
# ========================
def generate_employee_master():
    employees = []
    group_assignments = assign_location_groups(NUM_EMPLOYEES)

    for i in range(NUM_EMPLOYEES):
        group = group_assignments[i]

        gender = random.choices(["Male", "Female"], weights=[60, 40], k=1)[0]
        surname = random.choice(surnames)

        # -------------------------
        # NAME LOGIC
        # -------------------------
        if gender == "Male":
            first_name = random.choice(male_firstnames)
            employee_name = f"{first_name} {surname}"
            father_name = f"{random.choice(male_firstnames)} {surname}"
            husband_name = None
        else:
            first_name = random.choice(female_firstnames)
            employee_name = f"{first_name} {surname}"
            father_name = f"{random.choice(male_firstnames)} {surname}"
            husband_name = f"{random.choice(male_firstnames)} {random.choice(surnames)}"

        # -------------------------
        # DOB (1989–2003)
        # -------------------------
        dob_date = datetime.date(
            random.randint(1989, 2003),
            random.randint(1, 12),
            random.randint(1, 28)
        )

        # -------------------------
        # DOJ (>= DOB + 18 AND between 2024–2025)
        # -------------------------
        min_doj_year = max(dob_date.year + 18, 2024)

        if min_doj_year > 2025:
            min_doj_year = 2025

        doj_date = datetime.date(
            random.randint(min_doj_year, 2025),
            random.randint(10, 12),
            random.randint(1, 28)
        )

        # -------------------------
        # DOL (80% probability, > DOJ)
        # -------------------------
        if random.random() < 0.7:
            min_dol_year = max(doj_date.year, 2024)

            dol_date = datetime.date(
                random.randint(min_dol_year, 2025),
                random.randint(10, 12),
                random.randint(1, 28)
            )

            if dol_date <= doj_date:
                dol_date = doj_date + datetime.timedelta(days=random.randint(1, 365))

            dol_value = dol_date.strftime("%d-%m-%Y")
        else:
            dol_value = ""

        # -------------------------
        # EMPLOYEE RECORD
        # -------------------------
        emp = {
            "PARENT COMPANY": PARENT_COMPANY,
            "ASSOCIATE COMPANY": ASSOCIATE_COMPANY,
            "STATE": group["STATE"],
            "LOCATION": group["LOCATION"],
            "Company Employer Sub Contractor Code":group["SUB_CODE"] if Establishment_type == "CLRA" else "",
            "Employee Code": f"CLRAE{i+1:03d}",
            "Employee name": employee_name,
            "Gender": gender,
            "Date of Birth": dob_date.strftime("%d-%m-%Y"),
            "Date of Joining": doj_date.strftime("%d-%m-%Y"),
            "Date of Exit": dol_value if dol_value != "" else "",
            "Father Name": father_name,
            "Husband Name": random.choice([husband_name, ""]) if husband_name else "",
            "Department": random.choice(["HR", "Marketing", "IT", "Finance", ""]),
            "Designation": random.choice(["Manager", "Associate SE", "QA", "Product Manager"]),
            "Establishment Type": Establishment_type,
            "Vendor Nature Of Work": random.choice(["Security Services", "HR", "DBS", "Facility Services", ""]),
            "Identification Marks": random.choice(["Mole on cheek", "Scar on forehead", "Birthmark on arm", "Tattoo on wrist", ""]),
            "Aadhar Number": str(random.randint(10**11, 10**12 - 1)) if random.random() < 0.8 else "",
            "PAN Number": ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=5)) + str(random.randint(1000,9999)) + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") if random.random() < 0.8 else "",
            "PF No": "PF" + str(random.randint(1000000, 99999999)) if random.random() < 0.8 else "",
            "PF UAN No": str(random.randint(100000000000, 999999999999)) if random.random() < 0.8 else "",
            "ESI Number": "ESI" + str(random.randint(100000, 9999999)) if random.random() < 0.8 else "",
            "Bank Name": random.choice(["Axis Bank", "ICICI Bank", "Bank of Maharashtra", "Bank of India", ""]),
            "Bank Account Number": str(random.randint(10**5, 10**14)) if random.random() < 0.8 else "",
            "Permanent Address": f"{random.randint(1,999)} {random.choice(['MG Road','Park Street','1st Avenue','Lake View','Station Road'])}, {random.choice(['Mumbai','Delhi','Bangalore','Chennai','Kolkata'])}, {random.choice(['Maharashtra','Delhi','Karnataka','Tamil Nadu','West Bengal'])} - {random.randint(100000,999999)}" if random.random() < 0.5 else "",
            "Temporary Address": f"{random.randint(1,999)} {random.choice(['MG Road','Park Street','1st Avenue','Lake View','Station Road'])}, {random.choice(['Mumbai','Delhi','Bangalore','Chennai','Kolkata'])}, {random.choice(['Maharashtra','Delhi','Karnataka','Tamil Nadu','West Bengal'])} - {random.randint(100000,999999)}" if random.random() < 0.5 else "",
            "Reason of exit": random.choice(["Resigned", "Terminated", "Retired", ""]) if dol_value != "" else "",
            "Tenure of Employment": random.randint(0, 5) if random.random() < 0.8 else "",
            "Mobile": str(random.randint(6000000000, 9999999999)) if random.random() < 0.8 else "",
            "Email": (employee_name.lower().replace(" ", ".").replace("..", ".")+ str(random.randint(1, 999))+ "@gmail.com") if random.random() < 0.8 else "",
        }

        employees.append(emp)

    df = pd.DataFrame(employees)

    return df, employees

# ========================
# Monthly Generators
# ========================
def generate_leave_credit(employees, year, month):
    rows = []
    for emp in employees:
        rows.append({
            "PARENT COMPANY": PARENT_COMPANY,
            "ASSOCIATE COMPANY": ASSOCIATE_COMPANY,
            "STATE": emp["STATE"],
            "LOCATION": emp["LOCATION"],
            "Month": month,
            "Year": year,
            "Company Employer Sub Contractor Code": emp["Company Employer Sub Contractor Code"],
            "Employee code": emp["Employee Code"],
            "PL,EL,AL Monthly credit": random.randint(0, 2),
            "PL,EL,AL Opening balance": random.randint(0, 2),
            "PL,EL,AL Closing balance": random.randint(0, 8),
            "SL Monthly credit": random.randint(0, 2),
            "SL Opening balance": random.randint(0, 3),
            "SL Closing balance": random.randint(0, 9),
            "CL Monthly credit": random.randint(0, 3),
            "CL Opening balance": random.randint(0, 2),
            "CL Closing balance": random.randint(0, 7),
            "ML Opening balance": 0 if emp["Gender"] == "Male" else random.randint(0, 2),
            "ML Closing balance": 0 if emp["Gender"] == "Male" else random.randint(0, 2),
        })
    return pd.DataFrame(rows)

def generate_leave_availed(employees, year, month):
    rows = []
    month_num = datetime.datetime.strptime(month, "%B").month
    days_in_month = calendar.monthrange(year, month_num)[1]

    for emp in employees:
        start_date = random_date_in_month(year, month_num)
        end_day = min(days_in_month, start_date.day + random.randint(0, 3))
        end_date = datetime.date(year, month_num, end_day)

        leave_type = random_leave_type()

        # ✅ If Half Day Leave
        if leave_type == "HFD":
            no_of_days = 0.5
            end_date = start_date  # optional: keep same date for half day
        else:
            no_of_days = (end_date - start_date).days + 1

        rows.append({
            "PARENT COMPANY": PARENT_COMPANY,
            "ASSOCIATE COMPANY": ASSOCIATE_COMPANY,
            "STATE": emp["STATE"],
            "LOCATION": emp["LOCATION"],
            "Month": month,
            "Year": year,
            "Company Employer Sub Contractor Code": emp["Company Employer Sub Contractor Code"],
            "EMPLOYEE CODE": emp["Employee Code"],
            "START DATE": start_date.strftime("%d-%m-%Y"),
            "END DATE": end_date.strftime("%d-%m-%Y"),
            "LEAVE TYPE": leave_type,
            "NO OF DAYS": no_of_days,
        })

    return pd.DataFrame(rows)

def generate_attendance(employees, year, month):
    days = [str(d) for d in range(1, 32)]
    columns = [
        "PARENT COMPANY", "ASSOCIATE COMPANY", "STATE", "LOCATION",
        "Company Employer Sub Contractor Code", 
        "Month", "Year",
        "Employee Code", "Office In Time", "Office Out Time",
        "Interval In Time", "Interval Out Time"
    ] + days + ["Present Days"]

    rows = []
    month_num = datetime.datetime.strptime(month, "%B").month
    days_in_month = calendar.monthrange(year, month_num)[1]

    for emp in employees:
        row = {
            "PARENT COMPANY": PARENT_COMPANY,
            "ASSOCIATE COMPANY": ASSOCIATE_COMPANY,
            "STATE": emp["STATE"],
            "LOCATION": emp["LOCATION"],
            "Month": month,
            "Year": year,
            "Company Employer Sub Contractor Code": emp["Company Employer Sub Contractor Code"],
            "Employee Code": emp["Employee Code"],
            "Office In Time": random.choice(["09:00am", "09:10am", "07:10am", "08:15am", ""]),
            "Office Out Time": random.choice(["06:00pm", "07:10pm", "06:10pm", "07:15pm", ""]),
            "Interval In Time": random.choice(["13:00", "13:10", "14:10", "14:15", ""]),
            "Interval Out Time": random.choice(["13:30", "14:25", "14:20", "15:00", ""]),
        }
        present_count = 0

        for d in days:
            day_num = int(d)
            if day_num > days_in_month:
                mark = ""
            else:
                weekday = datetime.date(year, month_num, day_num).weekday()
                if weekday in (5, 6):
                    mark = "WO"
                else:
                    mark = random.choices(
                        ["P", "PL", "EL", "SL", "CL", "ML", "AL", "LOP", "HFD", ""],
                        [70, 5, 5, 5, 5, 2, 2, 2, 2, 2]
                    )[0]
                    if mark == "P":
                        present_count += 1
            row[d] = mark

        row["Present Days"] = present_count
        rows.append(row)
    return pd.DataFrame(rows, columns=columns)

def generate_wages(employees, year, month):
    rows = []
    month_num = datetime.datetime.strptime(month, "%B").month
    for emp in employees:
        present_days = random.randint(17, 20)
        rows.append({
            "PARENT COMPANY": PARENT_COMPANY,
            "ASSOCIATE COMPANY": ASSOCIATE_COMPANY,
            "STATE": emp["STATE"],
            "LOCATION": emp["LOCATION"],
            "Month": month,
            "Year": year,
            "Company Employer Sub Contractor Code": emp["Company Employer Sub Contractor Code"],
            "Employee Code": emp["Employee Code"],
            "Present Days": present_days,
            "LOP Days": 20 - present_days,
            "Fixed Gross": random.randint(10000, 50000) if random.random() < 0.8 else 0,
            "Basic Wages": random.randint(8000, 20000) if random.random() < 0.8 else 0,
            "Basic Arrear": random.randint(100, 500) if random.random() < 0.8 else 0,
            "House Rent Allowance": random.randint(3000, 10000) if random.random() < 0.8 else 0,
            "House Rent Arrear": random.randint(100, 500) if random.random() < 0.8 else 0,
            "Conveyance Allowance": random.randint(1000, 3000) if random.random() < 0.8 else 0,
            "Conveyance Arrear": random.randint(100, 500) if random.random() < 0.8 else 0,
            "Special Allowance": random.randint(2000, 7000) if random.random() < 0.8 else 0,
            "Special Allowance Arrear": random.randint(100, 500) if random.random() < 0.8 else 0,
            "Dearness Allowance": random.randint(2000, 7000) if random.random() < 0.8 else 0,
            "Dearness Arrear": random.randint(100, 500) if random.random() < 0.8 else 0,
            "Misc. Allowances": random.randint(100, 500) if random.random() < 0.8 else 0,
            "Other Earning": random.randint(100, 500) if random.random() < 0.8 else 0,
            "Bonus": random.randint(1000, 4000) if random.random() < 0.8 else 0,
            "Over Time": random.randint(500, 1000) if random.random() < 0.8 else 0,
            "Gratuity": random.randint(2000, 10000) if random.random() < 0.8 else 0,
            "Medical Allowance": random.randint(200, 5000) if random.random() < 0.8 else 0,
            "Holiday Payment": random.randint(100, 300) if random.random() < 0.8 else 0,
            "Gross Earnings": random.randint(20000, 60000) if random.random() < 0.8 else 0,
            "Gross Earnings Arrear": random.randint(100, 300) if random.random() < 0.8 else 0,
            "Provident Fund": 1800,
            "Provident Fund Arrear": random.randint(100, 300) if random.random() < 0.8 else 0,
            "Employer Provident Fund": 900,
            "Professional Tax": 200,
            "Profeessiona Tax Arrear": random.randint(100, 300) if random.random() < 0.8 else 0,
            "Income Tax": random.randint(0, 2000) if random.random() < 0.8 else 0,
            "ESI": (esi := 0 if random.random() < 0.2 else random.randint(10000, 50000)),
            "ESI Arrear": 0 if esi == 0 else random.randint(0, 500) if random.random() < 0.8 else 0,
            "LWF": 25,
            "Other Deduction": random.randint(0, 500) if random.random() < 0.8 else 0,
            "Fines": random.randint(0, 500) if random.random() < 0.8 else 0,
            "Insurance": random.randint(0, 500) if random.random() < 0.8 else 0,
            "Salary Advance": random.randint(0, 500) if random.random() < 0.8 else 0,
            "Gross Deduction": random.randint(0, 500) if random.random() < 0.8 else 0,
            "Gross Deduction Arrear": random.randint(0, 500) if random.random() < 0.8 else 0,
            "Net Payable": random.randint(0, 500) if random.random() < 0.8 else 0,
            "Net Payable Arrear": random.randint(0, 500) if random.random() < 0.8 else 0,
            "Overtime Hours": random.randint(0, 5) if random.random() < 0.8 else 0,
            "Overtime Taken Date": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Advance Paid Date": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "No of Adv Installments to be Recovered": random.randint(0, 5) if random.random() < 0.8 else 0,
            "Date on Adv Recovery Completed": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Nature & Date for Fine": random.choice(["Misconduct & " + random_date_in_month(year, month_num).strftime("%d-%m-%Y"), "Late Submission & " + random_date_in_month(year, month_num).strftime("%d-%m-%Y"), ""]),
            "Relay or Set": random.choice(["Relay", "Set", ""]),
            "Act or Omiss": random.choice(["Act", "Omiss", ""]),
            "Date Of Fines Show Cause": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Date of Fine Recovery Completed": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Damage Loss Amount": random.randint(0, 500) if random.random() < 0.8 else 0,
            "Cause of Damage Or Loss Date": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Date Of Deduction Show Cause": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "No of Deduction Installment to be recovered": random.randint(0, 5),
            "Date on Which Deduction Completed": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "No. Of Installment for FDA": random.randint(0, 5) if random.random() < 0.8 else 0,
            "First InstallMent Date for FDA": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Last InstallMent Date for FDA": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Other Concessions": random.randint(0, 5) if random.random() < 0.8 else 0,
            "Absense from Duty": random.randint(0, 5) if random.random() < 0.8 else 0,
            "Tenure of employment": random.randint(0, 10) if random.random() < 0.8 else 0,
            "Purpose of Advance": random.choice(["Family", "Medical", "Maternity", ""]),
            "Deduction Date of First Installment": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Deduction Date of Last Installment": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Particular of Damage Or Loss": random.choice(["Broken office laptop due to negligence", "Damage to warehouse inventory during handling", "Unauthorized removal of company assets", ""]),
            "Total Contribution Deduction": random.randint(100, 300) if random.random() < 0.8 else 0,
            "Maternity Leave From Date": "" if emp["Gender"] == "Male" else random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Date Of Birth Of child": "" if emp["Gender"] == "Male" else random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Insurance paid date": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Insurance Paid amount": random.randint(100, 300) if random.random() < 0.8 else 0,
            "No.of days Laid Off": random.randint(0, 15) if random.random() < 0.8 else 0,
            "Discharge and Dismissal": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Proof of Illness": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Proof of Death": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Proof of Birth": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Maternity paid Date": "" if emp["Gender"] == "Male" else random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Maternity Advance Paid": "0" if emp["Gender"] == "Male" else random.randint(1000, 1500) if random.random() < 0.8 else 0,
            "Maternity Bonus": "0" if emp["Gender"] == "Male" else random.randint(1000, 1500) if random.random() < 0.8 else 0,
            "Normal Earning": random.randint(10000, 15000) if random.random() < 0.8 else 0,
            "Attendance Bonus": random.randint(1000, 1500) if random.random() < 0.8 else 0,
            "Subsistence Allowance": random.randint(1000, 1500) if random.random() < 0.8 else 0,
            "Society Fund": random.randint(100, 500) if random.random() < 0.8 else 0,
            "Advance Installment Paid Date": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Installment Amount Paid": random.randint(1000, 5000),
            "Whether Workmen showed Cause against Deduction": random.choice(["Yes", "No"]),
            "Employees Explanation Heard By": random.choice(["Mahesh Sagar", "Suresh M."]),
            "Whether Workmen showed Cause against Fine": random.choice(["Yes", "No"]),
            "No of Installments Fixed to Recover Damages": random.randint(0, 3) if random.random() < 0.8 else 0,
            "Wages of Overtime on each Occassion": random.randint(200, 500) if random.random() < 0.8 else 0,
            "Normal Rate of wages": random.randint(500, 600) if random.random() < 0.8 else 0,
            "Normal Hours": random.randint(0, 12) if random.random() < 0.8 else 0,
            "OverTime Rate of Wages": random.randint(0, 15) if random.random() < 0.8 else 0,
            "Leave Wages": random.randint(1000, 1500) if random.random() < 0.8 else 0,
            "Salary Paid Date": random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "Date of Payment": random_date_in_month(year, month_num).strftime("%d-%m-%Y"),
            "ESI Date of Notice": "" if esi == 0 else random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "ESI Time of Notice": "" if esi == 0 else random.choice(["01:00am", "07:10am", "08:40pm", "12:15pm", ""]),
            "ESI Cause": "" if esi == 0 else random.choice(["Illness", "Injury", "Maternity", ""]),
            "ESI Nature": "" if esi == 0 else random.choice(["Temporary", "Permanent", ""]),
            "ESI Date": "" if esi == 0 else random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            "ESI Time": "" if esi == 0 else random.choice(["01:00 AM", "07:10 AM", "08:40 PM", "12:15 PM", ""]),
            "ESI Place": "" if esi == 0 else random.choice(["Mumbai", "Pune", "Nagpur", "Thane", "Bangalore", "Bhopal", ""]),
            "ESI Date Of Payment": "" if esi == 0 else random_date_in_month(year, month_num).strftime("%d-%m-%Y") if random.random() < 0.8 else "",
            # "Work Days": 20,
            "Overtime Paid Date": (random_date_in_month(year, month_num).strftime("%d-%m-%Y")if random.random() < 0.8 else ""),
            "TDS": random.randint(0, 5000) if random.random() < 0.8 else 0,
        })
    return pd.DataFrame(rows)

# ========================
# MAIN
# ========================
def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # =====================================
    # Generate Employee Master (Single File)
    # =====================================
    master_df, employees = generate_employee_master()

    master_df.to_excel(
        os.path.join(OUTPUT_FOLDER, f"Employee_Master_{timestamp}.xlsx"),
        index=False
    )

    # =====================================
    # Group periods year-wise
    # =====================================
    yearwise_periods = {}

    for year, month in PERIODS:
        if year not in yearwise_periods:
            yearwise_periods[year] = []

        yearwise_periods[year].append(month)

    # =====================================
    # Generate Year-wise Files
    # =====================================
    for year, months in yearwise_periods.items():

        print(f"\n📁 Processing Year: {year}")

        # Create year folder
        year_folder = os.path.join(OUTPUT_FOLDER, str(year))
        os.makedirs(year_folder, exist_ok=True)

        # Data collectors
        all_leave_credit = []
        all_leave_availed = []
        all_attendance = []
        all_wages = []

        # ==========================
        # Generate month-wise data
        # ==========================
        for month in months:

            print(f"   ➜ Generating {month} {year}")

            lc = generate_leave_credit(employees, year, month)
            la = generate_leave_availed(employees, year, month)
            att = generate_attendance(employees, year, month)
            wag = generate_wages(employees, year, month)

            all_leave_credit.append(lc)
            all_leave_availed.append(la)
            all_attendance.append(att)
            all_wages.append(wag)

        # ==========================
        # Combine all months
        # ==========================
        final_leave_credit = pd.concat(all_leave_credit, ignore_index=True)
        final_leave_availed = pd.concat(all_leave_availed, ignore_index=True)
        final_attendance = pd.concat(all_attendance, ignore_index=True)
        final_wages = pd.concat(all_wages, ignore_index=True)

        # ==========================
        # Save year-wise files
        # ==========================
        final_leave_credit.to_excel(
            os.path.join(year_folder, f"Leave_Credit_{year}.xlsx"),
            index=False
        )

        final_leave_availed.to_excel(
            os.path.join(year_folder, f"Leave_Availed_{year}.xlsx"),
            index=False
        )

        final_attendance.to_excel(
            os.path.join(year_folder, f"Attendance_{year}.xlsx"),
            index=False
        )

        final_wages.to_excel(
            os.path.join(year_folder, f"Wages_{year}.xlsx"),
            index=False
        )

        print(f"✅ Completed Year {year}")

    print("\n🎉 All year-wise files generated successfully!")

if __name__ == "__main__":
    main()
