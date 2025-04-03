CREATE TABLE weather_data (
    id INT PRIMARY KEY IDENTITY(1,1),
    base_date DATE,
    base_time VARCHAR(4),
    category VARCHAR(10),
    value VARCHAR(10),
	exec_date datetime
);
