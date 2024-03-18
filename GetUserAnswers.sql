-- Retrieves all answers posted by a specific user
DELIMITER //

CREATE PROCEDURE GetUserAnswers(
    IN p_user_id INT
)
BEGIN
    SELECT * FROM answers WHERE user_id = p_user_id;
END //

DELIMITER ;