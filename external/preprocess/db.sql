USE DATABASE carguru;

DROP TABLE IF EXISTS car;
CREATE TABLE car (
    listing_id INT NOT NULL,
    title VARCHAR(255), 
    make VARCHAR(255),
    model VARCHAR(255),
    description TEXT,
    manufactured VARCHAR(20),
    original_reg_date VARCHAR(20),
    reg_date VARCHAR(20),
    type_of_vehicle VARCHAR(255),
    category VARCHAR(255),
    transmission VARCHAR(20),
    curb_weight INT,
    power INT, 
    fuel_type VARCHAR(20),
    engine_cap INT,
    no_of_owners INT,
    depreciation INT, 
    coe INT,
    road_tax INT,
    dereg_value INT,
    mileage INT,
    omv INT,
    arf INT,
    opc_scheme VARCHAR(255),
    lifespan VARCHAR(20),
    eco_category VARCHAR(20),
    features TEXT,
    accessories TEXT,
    indicative_price INT,
    price INT,
    PRIMARY KEY (listing_id)
);

LOAD DATA LOCAL INFILE '~/Downloads/train_preprocessed.csv' INTO TABLE car FIELDS TERMINATED BY ',' ENCLOSED BY '"' IGNORE 1 ROWS 
(listing_id,title,make,model,description,manufactured,original_reg_date,reg_date,type_of_vehicle,category,transmission,curb_weight,power,fuel_type,engine_cap,no_of_owners,depreciation,coe,road_tax,dereg_value,mileage,omv,arf,opc_scheme,lifespan,eco_category,features,accessories,indicative_price,price);

SELECT listing_id,title,make,model,description,manufactured,original_reg_date,reg_date,type_of_vehicle,category,transmission,curb_weight,power,fuel_type,engine_cap,no_of_owners,depreciation,coe,road_tax,dereg_value,mileage,omv,arf,opc_scheme,lifespan,eco_category,features,accessories,indicative_price,price
FROM car INTO OUTFILE '~/Downloads/train_exported.csv' FIELDS ENCLOSED BY '"' TERMINATED BY ',';