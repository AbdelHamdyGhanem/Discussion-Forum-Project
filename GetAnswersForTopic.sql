-- Retrieves all answers for a specific topic/question
DELIMITER //

CREATE PROCEDURE GetAnswersForTopic(
    IN p_question_id INT
)
BEGIN
    SELECT * FROM answers WHERE question_id = p_question_id;
END //

DELIMITER ;