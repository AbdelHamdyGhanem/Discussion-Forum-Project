-- Allows a user to create a new question
DELIMITER //

CREATE PROCEDURE CreateTopic(
    IN p_title VARCHAR(255)
)
BEGIN
    INSERT INTO questions (title, content)
    VALUES (p_title, '');
END //

DELIMITER ;
