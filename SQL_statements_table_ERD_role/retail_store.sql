CREATE DATABASE retail_platform;

\c retail_platform;

CREATE TABLE customers(
    customerid VARCHAR(50) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    segement VARCHAR(100),
    customer_type VARCHAR(50),
    state VARCHAR(60),
    city VARCHAR(60),
    PRIMARY KEY(customerid)
);

CREATE TABLE sales(
    saleid VARCHAR(50) NOT NULL,
    invoiceid VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    tax DECIMAL(10, 5) NOT NULL,
    PRIMARY KEY(saleid)
);

CREATE TABLE products(
    productid VARCHAR(50) NOT NULL,
    saleid VARCHAR(50) NOT NULL,
    customerid VARCHAR(50) NOT NULL,
    producttype VARCHAR(100) NOT NULL,
    PRIMARY KEY(productid),
    FOREIGN KEY (saleid) REFERENCES sales(saleid),
    FOREIGN KEY (customerid) REFERENCES customers(customerid)
);

CREATE TABLE stores(
    storeid VARCHAR(50) NOT NULL,
    storestate VARCHAR(2) NOT NULL,
    storecity VARCHAR(100) NOT NULL,
    storestreet VARCHAR(100) NOT NULL,
    storezip INT NOT NULL, 
    PRIMARY KEY(storeid)
);



CREATE TABLE payments(
    paymentid VARCHAR(50) NOT NULL,
    customerid VARCHAR(50) NOT NULL,
    productid VARCHAR(50) NOT NULL,
    storeid VARCHAR(50) NOT NULL,
    saleid VARCHAR(50) NOT NULL,
    transaction_date date NOT NULL,
    transaction_time VARCHAR NOT NULL,
    transaction_num VARCHAR(100) NOT NULL,
    is_fraud INT NOT NULL,
    PRIMARY KEY(paymentid),
    FOREIGN KEY (customerid) REFERENCES customers(customerid), 
    FOREIGN KEY (productid) REFERENCES products(productid),
    FOREIGN KEY(storeid) REFERENCES stores(storeid),
    FOREIGN KEY(saleid) REFERENCES sales(saleid)   
);

CREATE TABLE inventory(
    inventoryid VARCHAR(50) NOT NULL,
    productid VARCHAR(50) NOT NULL,
    product_description VARCHAR(100) NOT NULL,
    stock_quantity INT NOT NULL,
    warranty_period INT NOT NULL,
    product_dimentions VARCHAR(100) NOT NULL,
    manufacturing_date DATE NOT NULL,
    expiration_date DATE NOT NULL,
    sku VARCHAR(100) NOT NULL,
    product_tags VARCHAR(100) NOT NULL,
    color VARCHAR(100) NOT NULL,
    product_rating INT NOT NULL,
    PRIMARY KEY(inventoryid),
    FOREIGN KEY (productid) REFERENCES products(productid)
);