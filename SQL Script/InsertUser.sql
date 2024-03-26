CREATE PROCEDURE InsertUser(IN username_param VARCHAR(255))
    BEGIN
    DECLARE user_count INT;
    SELECT COUNT(*) INTO user_count FROM Users WHERE username = username_param;
    IF user_count = 0 THEN
        INSERT INTO Users (username) VALUES (username_param);
    END IF;
    END //