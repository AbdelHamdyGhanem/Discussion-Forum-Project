-- stored procedure for login
DELIMITER //

CREATE PROCEDURE AuthenticateUser(
    IN p_email VARCHAR(255),
    IN p_password VARCHAR(255)
)
BEGIN
    SELECT * FROM users WHERE email = p_email AND password = p_password;
END //

DELIMITER ;
