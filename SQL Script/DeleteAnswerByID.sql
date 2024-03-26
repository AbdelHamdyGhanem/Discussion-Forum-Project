CREATE PROCEDURE DeleteAnswerByID(
    IN answer_id_param INT
    )
    BEGIN
    DELETE FROM Answers WHERE answer_id = answer_id_param;
    END //
