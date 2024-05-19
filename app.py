from flask import Flask, render_template, request, redirect, url_for
import pyodbc
import csv

app = Flask(__name__)

# SQL Server database setup
conn = pyodbc.connect(
    'DRIVER={SQL Server};'   
    'SERVER=144.76.195.231\MSSQLSERVER2016;'
    'DATABASE=FinalYearProject;' 
    'UID=admin;'   
    'PWD=Faisal_Awan'  
)
cursor = conn.cursor()

# Create a table for test items
cursor.execute(''' 
    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'test_items')
    BEGIN
        CREATE TABLE test_items (
            id INT IDENTITY(1,1) PRIMARY KEY,
            course NVARCHAR(255),
            topic NVARCHAR(255),
            question_stem NVARCHAR(MAX),
            option_a NVARCHAR(MAX),
            option_b NVARCHAR(MAX),
            option_c NVARCHAR(MAX),
            option_d NVARCHAR(MAX),
            key_answer NVARCHAR(MAX),
            cognitive_level NVARCHAR(255)
        )
    END
''')

# Create a table for student responses
cursor.execute('''
    IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'student_responses')
    BEGIN
        CREATE TABLE student_responses (
            id INT IDENTITY(1,1) PRIMARY KEY,
            student_id INT,
            question_id INT,
            selected_option NVARCHAR(255)
        )
    END
''')

# Data Structures questions
data_structures_questions = [
    ('Computer Science', 'Data Structures', 'What is the primary purpose of a linked list?', 'A. To store data in a sequential manner', 'B. To provide quick random access to elements', 'C. To represent hierarchical relationships', 'D. To efficiently insert and delete elements', 'D', 'Understanding'),
    ('Computer Science', 'Data Structures', 'How would you implement a stack using an array?', 'A. Enqueue operation', 'B. Dequeue operation', 'C. Push operation', 'D. Pop operation', 'C', 'Applying'),
    ('Computer Science', 'Data Structures', 'Which of the following best describes recursion in the context of data structures?', 'A. Repeating a process', 'B. Storing data in a sequential manner', 'C. Managing hierarchical relationships', 'D. Efficiently inserting and deleting elements', 'A', 'Understanding'),
    ('Computer Science', 'Data Structures', 'What is a key difference between a binary search tree and a hash table?', 'A. Search efficiency', 'B. Memory usage', 'C. Insertion speed', 'D. Deletion performance', 'A', 'Analyzing'),
    ('Computer Science', 'Data Structures', 'If you were to design a data structure for employee records, which would be the most suitable?', 'A. Linked List', 'B. Stack', 'C. Queue', 'D. Hash Table', 'D', 'Creating'),
    ('Computer Science', 'Data Structures', 'What is the time complexity of the bubble sort algorithm?', 'A. O(n)', 'B. O(n log n)', 'C. O(n^2)', 'D. O(log n)', 'C', 'Evaluating'),
]

# Data Warehouse questions
data_warehouse_questions = [
    ('Computer Science', 'Data Warehouse', 'What is the purpose of a data warehouse in business intelligence?', 'A. Real-time data processing', 'B. Data storage for web applications', 'C. Analyzing historical data for decision-making', 'D. File management', 'C', 'Understanding'),
    ('Computer Science', 'Data Warehouse', 'In designing a star schema for a data warehouse to analyze sales data, which dimension would you likely include?', 'A. Time', 'B. Color', 'C. Size', 'D. Shape', 'A', 'Applying'),
    ('Computer Science', 'Data Warehouse', 'How would you differentiate between OLAP and OLTP in the context of data warehousing?', 'A. OLAP focuses on real-time transactions', 'B. OLTP is designed for analytical processing', 'C. OLAP handles historical data', 'D. OLTP supports decision-making', 'C', 'Understanding'),
    ('Computer Science', 'Data Warehouse', 'Considering the impact of data quality on a data warehouse, which factor is crucial for effective analysis?', 'A. Data volume', 'B. Data diversity', 'C. Data velocity', 'D. Data quality', 'D', 'Analyzing'),
    ('Computer Science', 'Data Warehouse', 'What strategy would you propose for extracting data from multiple sources into a data warehouse?', 'A. Direct extraction without transformation', 'B. Transforming data during extraction', 'C. Loading raw data into the warehouse', 'D. Extracting only summary data', 'B', 'Creating'),
    ('Computer Science', 'Data Warehouse', 'When evaluating the role of data governance in maintaining data quality, what aspect would be a key consideration?', 'A. Speed of data processing', 'B. Accuracy and reliability of data', 'C. Cost-effectiveness of data storage', 'D. Scalability of data warehouse', 'B', 'Evaluating'),
]

# OOP questions
oop_questions = [
    ('Computer Science', 'OOP', 'What is polymorphism in object-oriented programming?', 'A. Inheritance', 'B. Overriding', 'C. Ability to take multiple forms', 'D. Encapsulation', 'C', 'Understanding'),
    ('Computer Science', 'OOP', 'In designing a class hierarchy for a zoo simulation, which concept allows different types of animals to share common behaviors?', 'A. Inheritance', 'B. Polymorphism', 'C. Encapsulation', 'D. Abstraction', 'A', 'Creating'),
    ('Computer Science', 'OOP', 'Implement a simple inheritance example in a programming language of your choice. Consider creating a base class "Vehicle" and a derived class "Car."', 'A. code snippet here', 'B. code snippet here', 'C. code snippet here', 'D. code snippet here', 'A', 'Applying'),
    ('Computer Science', 'OOP', 'Examine the advantages and disadvantages of encapsulation in object-oriented programming.', 'A. Improved security but increased complexity', 'B. Simplicity but reduced security', 'C. Improved security and simplicity', 'D. Reduced security and complexity', 'C', 'Analyzing'),
    ('Computer Science', 'OOP', 'When evaluating the importance of interfaces in achieving abstraction, what role do interfaces play in OOP?', 'A. Providing multiple inheritance', 'B. Defining common behavior without implementation', 'C. Enforcing encapsulation', 'D. Controlling access to class members', 'B', 'Evaluating'),
]

# Computer Network questions
computer_network_questions = [
    ('Computer Science', 'Computer Network', 'Explain the process of subnetting in IP addressing.', 'A. Dividing a large network into smaller sub-networks', 'B. Assigning unique addresses to each device', 'C. Configuring routers for optimal performance', 'D. Enabling DNS resolution', 'A', 'Applying'),
    ('Computer Science', 'Computer Network', 'Assess the advantages and disadvantages of using a wired vs. wireless network.', 'A. Improved mobility but reduced security', 'B. Higher data rates but more susceptible to interference', 'C. Lower cost but limited coverage', 'D. Lower latency but potential for cable clutter', 'B', 'Evaluating'),
    ('Computer Science', 'Computer Network', 'What is a router in a computer network?', 'A. Device that connects multiple networks together', 'B. Manages data traffic within a single network', 'C. Transmits data between computers in a network', 'D. Converts digital signals to analog signals', 'A', 'Understanding'),
    ('Computer Science', 'Computer Network', 'Explain the role of DNS (Domain Name System) in networking.', 'A. Resolving IP addresses to MAC addresses', 'B. Translating domain names to IP addresses', 'C. Filtering malicious network traffic', 'D. Managing network bandwidth', 'B', 'Understanding'),
    ('Computer Science', 'Computer Network', 'Propose a network security plan for a small business.', 'A. Implementing firewalls and intrusion detection systems', 'B. Restricting physical access to networking equipment', 'C. Regularly updating antivirus software', 'D. Configuring secure VPN connections for remote access', 'A', 'Creating'),
    ('Computer Science', 'Computer Network', 'Analyze the impact of network congestion on data transfer speed.', 'A. Increased latency and packet loss', 'B. Improved network performance', 'C. Enhanced data throughput', 'D. Reduced data security', 'A', 'Analyzing'),
        ('Computer Science', 'Computer Network', 'Analyze the impact of network congestion.', 'A. Increased latency and packet loss', 'B. Improved network performance', 'C. Enhanced data throughput', 'D. Reduced data security', 'B', 'Creating'),

]


# Computer Architecture questions
computer_architecture_questions = [
    ('Computer Science', 'Computer Architecture', 'Describe the purpose of the CPU in a computer system.', 
     'A. Manage storage devices', 'B. Execute instructions', 'C. Handle network connections', 'D. Control peripheral devices', 
     'B', 'Understanding'),
    
    ('Computer Science', 'Computer Architecture', 'Compare the performance impact of a single-core vs. multi-core processor for a CPU-intensive task.', 
     'A. Improved multitasking but higher power consumption', 'B. Higher clock speeds but increased heat generation', 
     'C. Parallel processing but potential for synchronization issues', 'D. Lower latency but limited scalability', 
     'C', 'Analyzing'),
    
    ('Computer Science', 'Computer Architecture', 'What is cache memory in a computer?', 
     'A. Volatile storage used for main program execution', 'B. Non-volatile storage for long-term data retention', 
     'C. High-speed memory for temporary data storage', 'D. Memory used for storing application files', 
     'C', 'Remembering'),
    
    ('Computer Science', 'Computer Architecture', 'Implement a pipeline architecture for instruction execution in a CPU.', 
     'A. Code snippet A', 'B. Code snippet B', 'C. Code snippet C', 'D. Code snippet D', 
     'B', 'Applying'),
    
    ('Computer Science', 'Computer Architecture', 'Evaluate the impact of pipelining on CPU performance.', 
     'A. Increased throughput but potential for hazards', 'B. Reduced latency but increased resource contention', 
     'C. Improved parallelism but potential for pipeline stalls', 'D. Lower power consumption but increased complexity', 
     'C', 'Evaluating'),
]


# Assembly Language Programming questions
assembly_language_questions = [
    ('Computer Science', 'Assembly Language', 'Write an assembly language code snippet to add two numbers stored in registers AX and BX.', 
     'A. ADD AX, BX', 'B. SUB AX, BX', 'C. MOV AX, BX', 'D. MUL AX, BX', 'A', 'Applying'),

    ('Computer Science', 'Assembly Language', 'Assess the efficiency of using assembly language compared to high-level languages for programming tasks.', 
     'A. Lower-level control but increased development time', 'B. Faster execution but platform-dependent', 
     'C. Improved readability but limited hardware interaction', 'D. Easier debugging but higher memory usage', 
     'B', 'Evaluating'),

    ('Computer Science', 'Assembly Language', 'What is the role of the assembler in the programming process?', 
     'A. Converts assembly code to machine code', 'B. Executes assembly programs', 'C. Manages memory allocation', 
     'D. Interprets high-level language code', 'A', 'Understanding'),

    ('Computer Science', 'Assembly Language', 'Explain the concept of registers in assembly language.', 
     'A. Storage for high-level variables', 'B. Temporary data storage within the CPU', 
     'C. Manage memory allocation for programs', 'D. Input/output operations in assembly', 
     'B', 'Understanding'),

    ('Computer Science', 'Assembly Language', 'Create an assembly language program to perform matrix multiplication.', 
     'A. MOV AX, BX', 'B. ADD AX, BX', 'C. MUL AX, BX', 'D. Matrix multiplication is not possible in assembly', 
     'D', 'Creating'),

    ('Computer Science', 'Assembly Language', 'Analyze the advantages and disadvantages of using assembly language for system-level programming.', 
     'A. Efficient low-level control but platform-dependent', 'B. Improved readability but slower execution', 
     'C. Easier debugging but limited hardware interaction', 'D. Faster development but higher memory usage', 
     'A', 'Analyzing'),
]



# Sample test items
test_items = (
    data_structures_questions +
    data_warehouse_questions +
    oop_questions +
    computer_network_questions +
    computer_architecture_questions +
    assembly_language_questions
)



cursor.execute('SELECT COUNT(*) FROM test_items')
table_empty = cursor.fetchone()[0] == 0

if table_empty:
    # Insert data into the table
    for item in test_items:
        question = item[4]  # Assuming index 4 contains the question stem information
        print("Question:", question)
        
        # Check if the question already exists in the database
        cursor.execute('SELECT COUNT(*) FROM test_items WHERE question_stem = ?', (question,))
        question_exists = cursor.fetchone()[0] > 0
        
        if not question_exists:
            # If the question doesn't exist, insert the item into the database
            cursor.execute('''
                INSERT INTO test_items (course, topic, question_stem, option_a, option_b, option_c, option_d, key_answer, cognitive_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', item)
            conn.commit()  # Commit the transaction after inserting the item
else:
    print("Table is not empty. No need to insert data.")



# Web page routes

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        selected_course = request.form.get('course')
        return redirect(url_for('select_course', course=selected_course))

    # Display available courses
    courses = set(item[1] for item in test_items)
    return render_template('index.html', courses=courses)
    
    

# @app.route('/select_course', methods=['POST'])
@app.route('/select_course', methods=['GET', 'POST'])
def select_course():
    # Get selected course
    selected_course = request.form.get('course')

    # Get test items for the selected course
    cursor.execute('SELECT * FROM test_items WHERE topic = ?', (selected_course,))
    
    # Fetch the items after executing the query
    items = cursor.fetchall()
    
    
    return render_template('test_page.html', course=selected_course, items=items)

@app.route('/record_response', methods=['POST'])
def record_response():
    # Get selected course and question ID
    selected_course = request.form.get('course')
    
    # Iterate over the submitted form data to find question IDs and selected options
    for key, value in request.form.items():
        if key.startswith('question_id_'):
            try:
                question_id = int(value)
                #student_id = request.form.get('student_id')
                student_id = 1
                selected_option = request.form.get(f'selected_option_{question_id}')

                # Insert student response into the database
                cursor.execute('''
                    INSERT INTO student_responses (student_id, question_id, selected_option)
                    VALUES (?, ?, ?)
                ''', (student_id, question_id, selected_option))
                conn.commit()
            except ValueError:
                # Handle the case where the question_id value cannot be converted to int
                print("Error: Invalid question_id value")

    # Redirect to the test page
    #return redirect(url_for('result.html', course=selected_course))
    return redirect(url_for('result', course=selected_course))


@app.route('/result', methods=['GET'])
def result():
    student_id = 1 
    # Fetch all student responses with associated question details
    cursor.execute('''
        SELECT s.student_id, t.question_stem, s.selected_option, t.key_answer, t.cognitive_level
        FROM student_responses s
        JOIN test_items t ON s.question_id = t.id
        WHERE s.student_id = ?
    ''', (student_id,))

    
    # Fetch all student responses after executing the query
    responses = cursor.fetchall()

    # Calculate total questions and corrected questions
    total_questions = len(responses)
    corrected_questions = sum(1 for response in responses if response[2] == response[3])

    # Render the result template with the obtained data
    return render_template('result.html', responses=responses, total_questions=total_questions, corrected_questions=corrected_questions)


if __name__ == '__main__':
    app.run(debug=True)
