use associationrulemining;

create table goods ( 
   Id int,
   Flavor varchar(15), 
   Food varchar(15), 
   Price float, 
   Type varchar(5),
   constraint gpid PRIMARY KEY (Id)
);

create table location ( 
   City varchar(15),
   State varchar(15), 
   Zip int, 
   Street varchar(20), 
   StoreNum int, 
   constraint lpid PRIMARY KEY (StoreNum)
);

create table employee ( 
   Last varchar(15),
   First varchar(15), 
   HireDate  Date, 
   FireDate  Date, 
   Position varchar(15), 
   FullTime varchar(5), 
   StoreNum int, 
   EmpId int, 
   FOREIGN KEY (StoreNum) REFERENCES location(StoreNum), 
   constraint epid PRIMARY KEY (EmpId)
);

create table receipts ( 
  ReceiptNumber int,
  SaleDate date,
  Weekend varchar(5), 
  isCash varchar(5), 
  EmpId int, 
  StoreNum int, 
  FOREIGN KEY (StoreNum) REFERENCES location(StoreNum), 
  constraint rffid FOREIGN KEY (EmpId) REFERENCES employee(EmpId), 
  constraint rpid PRIMARY KEY (ReceiptNumber)
);

create table items ( 
   Receipt int,
   Quantity int, 
   Item int, 
   FOREIGN KEY (Receipt) REFERENCES receipts(ReceiptNumber), 
   FOREIGN KEY (Item) REFERENCES goods(Id),
   constraint ipid PRIMARY KEY(Receipt, Item)
 );

