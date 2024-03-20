-- stored procedure for users
DELIMITER //

CREATE PROCEDURE CreateUser(
    IN p_email VARCHAR(255),
    IN p_password VARCHAR(255)
)
BEGIN
    INSERT INTO users (email, password) VALUES (p_email, p_password);
END //

DELIMITER ;

/*
--- table for users ---
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255),
    password VARCHAR(255)
);
*/