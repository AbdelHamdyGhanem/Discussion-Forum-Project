-- Allows a user to vote (upvote/downvote) on an answer
DELIMITER //

CREATE PROCEDURE VoteOnAnswer(
    IN p_user_id INT,
    IN p_answer_id INT,
    IN p_vote INT
)
BEGIN
    IF p_vote = 1 THEN
        UPDATE answers SET upvotes = upvotes + 1 WHERE id = p_answer_id;
    ELSEIF p_vote = -1 THEN
        UPDATE answers SET downvotes = downvotes + 1 WHERE id = p_answer_id;
    END IF;
END //

DELIMITER ;