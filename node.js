const mysql = require('mysql');

// Create a connection to the MySQL server
const connection = mysql.createConnection({
  host: 'localhost', // Change to your MySQL host
  user: 'root',      // Change to your MySQL username
  password: 'password',  // Change to your MySQL password
});

// Connect to the MySQL server
connection.connect((err) => {
  if (err) throw err;
  console.log('Connected to MySQL server');
  
  // Create the database if it doesn't exist
  connection.query('CREATE DATABASE IF NOT EXISTS student', (err) => {
    if (err) throw err;
    console.log('Database "student" created or already exists');

    // Switch to the "student" database
    connection.query('USE student', (err) => {
      if (err) throw err;

      // Create the table "student_details" if it doesn't exist
      const createTableQuery = `
        CREATE TABLE IF NOT EXISTS student_details (
          stu_id INT AUTO_INCREMENT PRIMARY KEY,
          stu_name VARCHAR(255),
          stu_marks INT,
          emp_cgpa FLOAT
        )
      `;
      connection.query(createTableQuery, (err) => {
        if (err) throw err;
        console.log('Table "student_details" created or already exists');

        // Insert records into the table
        const insertQuery = `
          INSERT INTO student_details (stu_name, stu_marks, emp_cgpa) VALUES
            ('John Doe', 85, 3.5),
            ('Jane Smith', 92, 3.8),
            ('Michael Johnson', 78, 3.2)
        `;
        connection.query(insertQuery, (err) => {
          if (err) throw err;
          console.log('Inserted 3 records into "student_details"');

          // Display records from the table
          connection.query('SELECT * FROM student_details', (err, results) => {
            if (err) throw err;
            console.log('Student Records:');
            console.log(results);
          });

          // Close the connection
          connection.end();
        });
      });
    });
  });
});
