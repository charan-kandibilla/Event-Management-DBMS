CREATE TABLE headorg (
    head_id INT NOT NULL PRIMARY KEY,
    head_name VARCHAR(100) NOT NULL,
    head_gender CHAR(1),
    login_cred VARCHAR(255) NOT NULL
);

INSERT INTO headorg (head_id, head_name, head_gender, login_cred) VALUES
(1, 'Alice Johnson', 'F', 'AJ'),
(2, 'Bob Smith', 'M', 'BS'),
(3, 'Carol White', 'F', 'CW'),
(4, 'David Green', 'M', 'DG');



DROP TABLE IF EXISTS EVENTS;

 CREATE TABLE EVENTS (
     event_id INT PRIMARY KEY AUTO_INCREMENT,
     event_name VARCHAR(100) NOT NULL,
     event_date DATE NOT NULL,
     head_id INT,
     FOREIGN KEY (head_id) REFERENCES headorg(head_id)
 ) AUTO_INCREMENT=101;

INSERT INTO events (event_name, event_date, head_id) VALUES
     ('Annual Charity Gala', '2024-11-15', 1),
     ('Tech Innovation Conference', '2024-12-05', 2),
     ('Local Art Fair', '2024-11-20', 3),
     ('Music Fest', '2024-12-10', 1);

CREATE TABLE volunteers (
    volunteer_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,  -- Using INT for volunteer_id with auto-increment
    vol_name VARCHAR(100) NOT NULL,
    vol_age INT NOT NULL,
    vol_gender ENUM('Male', 'Female', 'Other') NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    event_id INT,  -- Ensure this matches the type in Events table
    FOREIGN KEY (event_id) REFERENCES Events(event_id) ON DELETE CASCADE
);


INSERT INTO volunteers (volunteer_id, vol_name, vol_age, vol_gender, phone_number, event_id) VALUES
( 'Alice Smith', 25, 'Female', '123-456-7890', 101),
( 'Bob Johnson', 30, 'Male', '234-567-8901', 102),
( 'Charlie Brown', 22, 'Other', '345-678-9012', 101),
( 'Daisy White', 28, 'Female', '456-789-0123', 103);




CREATE TABLE tasks (
    head_id INT,
    volunteer_id INT,
    task VARCHAR(255),
    PRIMARY KEY (head_id, volunteer_id),
    FOREIGN KEY (head_id) REFERENCES headOrg(head_id),
    FOREIGN KEY (volunteer_id) REFERENCES volunteers(volunteer_id)
);

-- Insert sample values into tasks
INSERT INTO tasks (head_id, volunteer_id, task) VALUES 
(1, 2, 'Prepare event materials'),
(1, 5, 'Set up event venue'),
(2, 4, 'Manage registrations'),
(3, 6, 'Coordinate volunteers'),
(4, 5, 'Clean up after event');


 ALTER TABLE volunteers
     ADD head_id INT,
     ADD FOREIGN KEY (head_id) REFERENCES headOrg(head_id);
     

UPDATE volunteers SET head_id = 1 WHERE volunteer_id = 2; -- Bob Johnson -> Alice Johnson
UPDATE volunteers SET head_id = 2 WHERE volunteer_id = 4; -- Daisy White -> Bob Smith
UPDATE volunteers SET head_id = 1 WHERE volunteer_id = 5; -- Alice Brown -> Alice Johnson
UPDATE volunteers SET head_id = 3 WHERE volunteer_id = 6; -- DUMMY1 -> Carol White



ALTER TABLE events
ADD UNIQUE INDEX idx_event_id_date (event_id, event_date);


CREATE TABLE Venue (
    venue_id INT PRIMARY KEY,
    venue_name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    capacity INT NOT NULL,
    event_id INT,
    event_date DATE,
    FOREIGN KEY (event_id, event_date) REFERENCES events(event_id, event_date)
);


INSERT INTO Venue (venue_id, venue_name, address, capacity, event_id, event_date) VALUES
(1, 'Grand Hall', '123 Charity St., City A', 500, 101, '2024-11-15'),
(2, 'Innovation Center', '456 Tech Ave., City B', 300, 102, '2024-12-05'),
(3, 'Art Pavilion', '789 Art St., City C', 200, 103, '2024-11-20'),
(4, 'Open-Air Stage', '321 Music Rd., City D', 1000, 104, '2024-12-10');

ALTER TABLE venue MODIFY venue_id INT NOT NULL AUTO_INCREMENT;


ALTER TABLE tasks
DROP FOREIGN KEY tasks_ibfk_2;  -- Drop the existing foreign key constraint

ALTER TABLE tasks
ADD CONSTRAINT tasks_ibfk_2
FOREIGN KEY (volunteer_id) REFERENCES volunteers(volunteer_id)
ON DELETE CASCADE;  -- Add the foreign key with cascading delete


CREATE TABLE vendors (
    vendor_id INT AUTO_INCREMENT PRIMARY KEY,
    vendor_name VARCHAR(255) NOT NULL,
    contact_details VARCHAR(255) NOT NULL,
    services_provided TEXT NOT NULL,
    vendor_fee DECIMAL(10, 2) NOT NULL,
    head_id INT,
    FOREIGN KEY (head_id) REFERENCES heads(head_id) ON DELETE CASCADE
);


INSERT INTO vendors (vendor_name, contact_details, services_provided, vendor_fee, head_id) VALUES
('Gourmet Catering Co.', '555-1234', 'Catering Services', 1500.00, 1),  -- For Annual Charity Gala
('AV Tech Solutions', '555-5678', 'Audio/Visual Equipment Rental', 800.00, 2),  -- For Tech Innovation Conference
('Local Artists Collective', '555-8765', 'Art Displays and Supplies', 600.00, 3),  -- For Local Art Fair
('Sound & Light Productions', '555-4321', 'Sound and Lighting Services', 1200.00, 1);  -- For Music Fest


ALTER TABLE vendors
DROP FOREIGN KEY vendors_ibfk_1;

ALTER TABLE vendors
ADD CONSTRAINT vendors_ibfk_1 
FOREIGN KEY (head_id) REFERENCES headorg(head_id) 
ON DELETE SET NULL;

-- Step 1: Add the event_id column
ALTER TABLE vendors
ADD event_id INT;

-- Step 2: Add foreign key constraint
ALTER TABLE vendors
ADD CONSTRAINT fk_event
FOREIGN KEY (event_id) REFERENCES events(event_id);

UPDATE vendors SET event_id = 101 WHERE vendor_id = 1; -- Gourmet Catering Co.
UPDATE vendors SET event_id = 102 WHERE vendor_id = 2; -- AV Tech Solutions
UPDATE vendors SET event_id = 103 WHERE vendor_id = 3; -- Local Artists Collective
UPDATE vendors SET event_id = 104 WHERE vendor_id = 4; -- Sound & Light Productions

<<<<<<< HEAD:codes.txt
------------------------------------------------------------------------------------
=======
>>>>>>> abc8be6657ef3531e96df1d7e338a70cf9d351c9:codes.sql

CREATE TABLE performance (
    performance_name VARCHAR(255) PRIMARY KEY,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    no_of_performers INT NOT NULL,
    event_id INT,
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

INSERT INTO performance (performance_name, start_time, end_time, no_of_performers, event_id)
VALUES 
    ('Opening Act', '2024-11-06 18:00:00', '2024-11-06 18:30:00', 5, 101),
    ('Main Event', '2024-11-06 19:00:00', '2024-11-06 21:00:00', 10, 102),
    ('Closing Ceremony', '2024-11-06 22:00:00', '2024-11-06 22:45:00', 8, 103);

<<<<<<< HEAD:codes.txt
-------------------------------------------------------------------------------------
=======

>>>>>>> abc8be6657ef3531e96df1d7e338a70cf9d351c9:codes.sql

CREATE TABLE performer (
    performer_id INT AUTO_INCREMENT PRIMARY KEY,
    performer_name VARCHAR(255) NOT NULL,
    dob DATE NOT NULL,
    phone_no VARCHAR(15) NOT NULL,
    event_id INT,
    FOREIGN KEY (event_id) REFERENCES performance(event_id) ON DELETE CASCADE
);

ALTER TABLE performer AUTO_INCREMENT = 1001;

CREATE TABLE performed_by (
    performance_name VARCHAR(255),
    performer_id INT,
    role VARCHAR(100),
    FOREIGN KEY (performance_name) REFERENCES performance(performance_name) ON DELETE CASCADE,
    FOREIGN KEY (performer_id) REFERENCES performer(performer_id) ON DELETE CASCADE,
    PRIMARY KEY (performance_name, performer_id)
);


<<<<<<< HEAD:codes.txt
------------------------------------------------------------------------------------------
=======

>>>>>>> abc8be6657ef3531e96df1d7e338a70cf9d351c9:codes.sql

CREATE TABLE attendees (
    reg_id INT AUTO_INCREMENT PRIMARY KEY,
    att_name VARCHAR(100) NOT NULL,
    att_age INT NOT NULL,
    amount_paid DECIMAL(10, 2) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    reg_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    category ENUM('general', 'vip') NOT NULL,
    event_id INT,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE SET NULL
);

<<<<<<< HEAD:codes.txt
-------------------------------------------------------------------------------------------

DELIMITER $$

CREATE DEFINER=`root`@`localhost` TRIGGER `check_performer_limit`
BEFORE INSERT ON `performed_by`
=======


DELIMITER $$

CREATE DEFINER=root@localhost TRIGGER check_performer_limit
BEFORE INSERT ON performed_by
>>>>>>> abc8be6657ef3531e96df1d7e338a70cf9d351c9:codes.sql
FOR EACH ROW
BEGIN
    DECLARE performer_limit INT;
    DECLARE current_performers INT;

    -- Get the limit on the number of performers from the performance table
    SELECT no_of_performers INTO performer_limit
    FROM performance
    WHERE performance_name = NEW.performance_name;

    -- Count the number of current performers already assigned to this performance
    SELECT COUNT(*) INTO current_performers
    FROM performed_by
    WHERE performance_name = NEW.performance_name;

    -- If the current performers exceed or equal the limit, signal an error
    IF current_performers >= performer_limit THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Number of performers exceeded, cannot add more performers';
    END IF;
END $$

DELIMITER ;

<<<<<<< HEAD:codes.txt
---------------------------------------------------------------------------------------------------

=======

CREATE TRIGGER before_insert_vendor
BEFORE INSERT ON vendors
FOR EACH ROW
BEGIN
    IF NEW.vendor_fee < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Vendor fee cannot be negative';
    END IF;
END;


DELIMITER //

CREATE TRIGGER before_update_vendor_fee
BEFORE UPDATE ON vendors
FOR EACH ROW
BEGIN
    IF NEW.vendor_fee < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Vendor fee cannot be negative';
    END IF;
END;

//

DELIMITER ;


CREATE TRIGGER IF NOT EXISTS before_insert_venue
          BEFORE INSERT ON venue
          FOR EACH ROW
          BEGIN
              -- Check if there is already a venue for the given event_id
          IF EXISTS (SELECT 1 FROM venue WHERE event_id = NEW.event_id) THEN
          SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Each event can only have one venue.';
          END IF;

              -- Check if a venue with the same name and address exists for the same event_date
          IF EXISTS (
             SELECT 1 FROM venue 
             WHERE venue_name = NEW.venue_name 
             AND address = NEW.address 
             AND event_date = NEW.event_date
          ) THEN
             SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'A venue with the same name, address, and event date already exists.';
          END IF;
          END;


CREATE FUNCTION total_vendor_revenue(event_id INT) 
        RETURNS DECIMAL(10, 2)
        DETERMINISTIC
        BEGIN
            DECLARE total_revenue DECIMAL(10, 2);
            SELECT IFNULL(SUM(vendor_fee), 0) INTO total_revenue
            FROM vendors
            WHERE vendors.event_id = event_id;
            RETURN total_revenue;
        END
>>>>>>> abc8be6657ef3531e96df1d7e338a70cf9d351c9:codes.sql

