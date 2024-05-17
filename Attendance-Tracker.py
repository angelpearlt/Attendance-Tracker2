import csv
import os
from datetime import datetime

# Base class for common attributes and methods
class Person:
    def __init__(self, name):
        self.name = name  # String to store the name

    def get_info(self):
        return f"Name: {self.name}"  # Returns name information

# Student class inheriting from Person
class Student(Person):
    def __init__(self, student_id, name):
        super().__init__(name)  # Inheriting from Person class
        self.student_id = student_id  # String to store student ID

    def get_info(self):
        return f"Student ID: {self.student_id}, {super().get_info()}"  # Polymorphic method to return student info

# School class to manage students
class School:
    def __init__(self, school_name):
        self.school_name = school_name  # String to store school name
        self.students = {}  # Dictionary to store students with student_id as key

    def add_student(self, student):
        if student.student_id not in self.students:  # Check if student ID is unique
            self.students[student.student_id] = student  # Add student to dictionary
            print(f"Student {student.name} added.")
        else:
            print(f"Student ID {student.student_id} already exists.")

    def get_student(self, student_id):
        return self.students.get(student_id, None)  # Retrieve student from dictionary

# Attendance class to represent attendance records
class Attendance:
    def __init__(self, student_id, date, present):
        self.student_id = student_id  # String to store student ID
        self.date = date  # String to store the date
        self.present = present  # Boolean to store attendance status

    def get_info(self):
        return (self.student_id, self.date, self.present)  # Tuple to return attendance info

# AttendanceTracker class to handle attendance tracking, inherits from School
class AttendanceTracker(School):
    def __init__(self, school_name, student_file='students.csv', attendance_file='attendance.csv'):
        super().__init__(school_name)  # Inheriting from School class
        self.student_file = student_file
        self.attendance_file = attendance_file
        self.attendance_records = []  # List to store attendance records
        self.student_fields = ['Student ID', 'Name']
        self.attendance_fields = ['Student ID', 'Name', 'Date', 'Present']

        # Create the student file with headers if it doesn't exist
        if not os.path.exists(self.student_file):
            with open(self.student_file, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.student_fields)
                writer.writeheader()

        # Create the attendance file with headers if it doesn't exist
        if not os.path.exists(self.attendance_file):
            with open(self.attendance_file, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.attendance_fields)
                writer.writeheader()

    # Method to add a student
    def add_student(self, student):
        super().add_student(student)  # Call the parent class method to add the student
        with open(self.student_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.student_fields)
            writer.writerow({'Student ID': student.student_id, 'Name': student.name})

    # Method to mark attendance for a student
    def mark_attendance(self, student_id, present=True):
        student = self.get_student(student_id)  # Retrieve student from the dictionary
        if not student:
            print(f"No student found with ID {student_id}.")
            return
        
        date_str = datetime.now().strftime('%Y-%m-%d')  # Get the current date
        attendance = Attendance(student_id, date_str, present)  # Create attendance record (object)
        self.attendance_records.append(attendance)  # Add to attendance records list
        
        with open(self.attendance_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.attendance_fields)
            writer.writerow({'Student ID': student_id, 'Name': student.name, 'Date': date_str, 'Present': 'Yes' if present else 'No'})
        print(f"Attendance marked for student ID {student_id} ({student.name}) on {date_str}.")

    # Method to display header
    def display_header(self):
        # ANSI escape codes for light pink background and black text
        pink_background = "\033[48;5;217m"
        black_text = "\033[30m"
        reset_style = "\033[0m"

        # Print school name and column headers with styles
        print(f"{pink_background}{black_text}School: {self.school_name}{reset_style}")
        print(f"{pink_background}{black_text}{'Student ID':<12}{'Name':<20}{'Date':<12}{'Present':<10}{reset_style}")

    # Method to view attendance
    def view_attendance(self):
        self.display_header()  # Display the header first
        with open(self.attendance_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Print each attendance record
                print(f"{row['Student ID']:<12}{row['Name']:<20}{row['Date']:<12}{row['Present']:<10}")

# Example usage
if __name__=='__main__':
    tracker = AttendanceTracker("Ramon Teves Pastor Dumaguete Science High School")
    
    students = [
        Student('1', 'Cylon'),  # Creating Student objects using tuples (student_id, name)
        Student('2', 'Jarey'),
        Student('3', 'Margaret'),
        Student('4', 'Nautica'),
        Student('5', 'Angel'),
    ]
    
    for student in students:
        tracker.add_student(student)  # Adding Student objects to tracker
    
    attendance_records = [
        ('1', True),  # Tuple representing attendance record (student_id, present)
        ('2', False),
        ('3', True), 
        ('4', False),
        ('5', True),
    ]
    
    for student_id, present in attendance_records:
        tracker.mark_attendance(student_id, present)  # Marking attendance using tuples and booleans
    
    tracker.view_attendance()