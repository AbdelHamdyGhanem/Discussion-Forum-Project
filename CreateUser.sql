-- create a new user and add the user to the system
DELIMITER //

CREATE PROCEDURE CreateUser(
    IN p_username VARCHAR(50),
    IN p_email VARCHAR(100),
    IN p_password VARCHAR(50)
)
BEGIN
    INSERT INTO users (username, email, password)
    VALUES (p_username, p_email, p_password);
END //

DELIMITER ;