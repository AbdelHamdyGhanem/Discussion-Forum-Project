DELIMITER //

CREATE PROCEDURE DeleteAnswer(
    IN p_answer_id INT
)
BEGIN
    DELETE FROM answers WHERE answer_id = p_answer_id;
END //

DELIMITER ;