-- Retrieves details of a specific user
DELIMITER //

CREATE PROCEDURE GetUserDetails(
    IN p_user_id INT
)
BEGIN
    SELECT * FROM users WHERE id = p_user_id;
END //

DELIMITER ;