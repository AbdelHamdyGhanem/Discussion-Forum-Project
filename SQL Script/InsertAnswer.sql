CREATE PROCEDURE InsertAnswer(
        IN description_param TEXT,
        IN username_param VARCHAR(255),
        IN topic_id_param INT
    )
    BEGIN
        DECLARE user_exists INT;
        DECLARE topic_exists INT;
     
        -- Check if the username exists in the Users table
        SELECT COUNT(*) INTO user_exists FROM Users WHERE username = username_param;
         
        -- Check if the topic_id exists in the Topics table
        SELECT COUNT(*) INTO topic_exists FROM Topics WHERE topic_id = topic_id_param;
     
        -- If both user and topic exist, insert the answer
        IF user_exists > 0 AND topic_exists > 0 THEN
            INSERT INTO Answers (description, username, topic_id) VALUES (description_param, username_param, topic_id_param);
        ELSE
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User or topic does not exist';
        END IF;
    END //
