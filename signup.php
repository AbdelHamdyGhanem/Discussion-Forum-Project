<?php
// Database connection settings
$servername = "localhost:4306";
$username = "abdelghanem";
$password = "";
$database = "test"; // Change this to your actual database name

try {
    // Create connection
    $conn = new PDO("mysql:host=$servername;dbname=$database", $username, $password);
    // Set the PDO error mode to exception
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Retrieve signup form data
    $email = $_POST['email'];
    $password = $_POST['psw']; // Remember to hash this password before storing it in the database
    
    // Hash the password
    $hashedPassword = password_hash($password, PASSWORD_DEFAULT);

    // Prepare SQL statement to insert user data into the users table
    $stmt = $conn->prepare("INSERT INTO users (email, password) VALUES (:email, :password)");
    $stmt->bindParam(':email', $email);
    $stmt->bindParam(':password', $hashedPassword); // Store the hashed password

    // Execute the SQL statement
    $stmt->execute();

    // Redirect to a success page or display a success message
    // header("Location: success.php");
    // echo "Signup successful!";

} catch(PDOException $e) {
    // Log error to a file
    $errorLog = fopen("error.log", "a") or die("Unable to open file!");
    fwrite($errorLog, "Error: " . $e->getMessage() . "\n");
    fclose($errorLog);
    
    // Output error message to the browser console
    echo "<script>console.error('Error: " . $e->getMessage() . "');</script>";
}

// Close the database connection
$conn = null;
?>
