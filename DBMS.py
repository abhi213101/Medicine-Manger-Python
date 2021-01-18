from sqlite3 import *

# Connection with main Database
adminDataBase = connect("AdminData.db")
adminCursor = adminDataBase.cursor()

# Current databse connectors initially None updated at the time of login
currentDatabase = None
currentDatabaseCursor = None

# Creating tables if not exists
adminCursor.execute('''CREATE TABLE IF NOT EXISTS "AdminTable" (
					"username"	TEXT NOT NULL UNIQUE,
					"password"	TEXT NOT NULL,
					"securityQue"	TEXT NOT NULL,
					"answer"	TEXT NOT NULL,
					"hospitalName"	TEXT NOT NULL,
					"totalDatabase"	INTEGER NOT NULL DEFAULT 0,
					"currentDatabase"	TEXT,
					PRIMARY KEY("username")
					);''')

adminCursor.execute('''CREATE TABLE IF NOT EXISTS "UserDatabaseDetail" (
					"databaseName"	TEXT NOT NULL UNIQUE,
					"startYear"	INTEGER NOT NULL UNIQUE,
					"endYear"	INTEGER NOT NULL UNIQUE
				    );''')

adminDataBase.commit()

# Sign Up function for the first time user
def RegistrationDB(username, password, securityQue, answer, hospitalName):
	try:		
		adminCursor.execute("INSERT INTO AdminTable (username, password, securityQue, answer, hospitalName, totalDatabase, currentDataBase) VALUES ('"+username+"','"+password+"','"+securityQue+"','"+answer+"','"+hospitalName+"',0,NULL);")
		adminDataBase.commit()
		return True

	except:
		return False

# Regular Login function
def LoginDB(username, password):
	
	global currentDatabase
	global currentDatabaseCursor

	adminCursor.execute("SELECT password,currentDatabase FROM AdminTable WHERE username='"+username+"';")
	output = adminCursor.fetchone()
	if(output == None):
		return "Invalid username"
	
	elif(output[0] != password):
		return "Invalid password"
	
	else:

		currentDatabase = connect(output[1])
		currentDatabaseCursor = currentDatabase.cursor()
		return "true"

def passwordResetDB(username):
	adminCursor.execute("SELECT securityQue, answer, password FROM AdminTable WHERE username='"+username+"';")
	output = adminCursor.fetchone()

	if(output == None):
		return "None"
	
	else:
		return output

def createDataBase(sy,ey):
	try:
		global currentDatabase
		global currentDatabaseCursor

		name = str(sy)+"-"+str(ey)+"DATABASE.db"
		currentDatabase = connect(name)
		currentDatabaseCursor = currentDatabase.cursor()
		
			
		currentDatabaseCursor.execute('''CREATE TABLE "mainTable" (
							"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
							"schNo"	TEXT NOT NULL DEFAULT 'OS',
							"type"	TEXT NOT NULL,
							"name"	INTEGER NOT NULL UNIQUE,
							"oldPrice"	REAL NOT NULL DEFAULT 0,
							"newPrice"	REAL NOT NULL DEFAULT 0,
							"lastYearConsumption" INTEGER NOT NULL DEFAULT 0,
							"OBCurrentQuantity"	INTEGER NOT NULL DEFAULT 0,
							"RFODCurrentQuantity"	INTEGER NOT NULL DEFAULT 0,
							"RFCMSCurrentQuantity"	INTEGER NOT NULL DEFAULT 0,
							"LPCurrentQuantity"	INTEGER NOT NULL DEFAULT 0,
							"PMJAKCurrentQuantity"	INTEGER NOT NULL DEFAULT 0);''')

		currentDatabaseCursor.execute('''CREATE TABLE "receiveTable" (
							"key"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
							"ID"	INTEGER NOT NULL,
							"batch"	TEXT NOT NULL,
							"quantity"	INTEGER NOT NULL DEFAULT 0,
							"expDate"	TEXT NOT NULL,
							"date"	TEXT NOT NULL,
							"type"	TEXT NOT NULL,
							FOREIGN KEY("ID") REFERENCES "mainTable"("ID") ON DELETE CASCADE);''')

		currentDatabaseCursor.execute('''CREATE TABLE "currentTable" (
							"key"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
							"ID"	INTEGER NOT NULL,
							"batch"	TEXT NOT NULL,
							"quantity"	INTEGER NOT NULL,
							"expDate"	TEXT NOT NULL,
							"date"	INTEGER,
							"type"	INTEGER,
							FOREIGN KEY("ID") REFERENCES "mainTable"("ID") ON DELETE CASCADE);''')

		currentDatabaseCursor.execute('''CREATE TABLE "consumptionTable" (
							"key"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
							"ID"	INTEGER NOT NULL,
							"batch"	TEXT NOT NULL,
							"quantity"	INTEGER NOT NULL DEFAULT 0,
							"expDate"	TEXT NOT NULL,
							"date"	TEXT NOT NULL,
							"type"	TEXT NOT NULL,
							"useType"	TEXT NOT NULL DEFAULT 'consumption',
							"currentKey" INTEGER NOT NULL,
							FOREIGN KEY("ID") REFERENCES "mainTable"("ID") ON DELETE CASCADE);''')

		currentDatabaseCursor.execute('''CREATE TABLE "storeAccount" (
							"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
							"name"	TEXT NOT NULL UNIQUE,
							"OBQuantity"	INTEGER NOT NULL DEFAULT 0,
							"OBValue"	REAL NOT NULL DEFAULT 0,
							"RFODQuantity"	INTEGER NOT NULL DEFAULT 0,
							"RFODValue"	REAL NOT NULL DEFAULT 0,
							"RFCMSQuantity"	INTEGER NOT NULL DEFAULT 0,
							"RFCMSValue"	REAL NOT NULL DEFAULT 0,
							"LPQuantity"	INTEGER NOT NULL DEFAULT 0,
							"LPValue"	REAL NOT NULL DEFAULT 0,
							"PMJAKQuantity"	INTEGER NOT NULL DEFAULT 0,
							"PMJAKValue"	REAL NOT NULL DEFAULT 0,
							"totalRecieveQuantity"	INTEGER NOT NULL DEFAULT 0,
							"totalRecieveValue"	REAL NOT NULL DEFAULT 0,
							"consumptionQuantity"	INTEGER NOT NULL DEFAULT 0,
							"consumptionValue"	REAL NOT NULL DEFAULT 0,
							"transferQuantity"	INTEGER NOT NULL DEFAULT 0,
							"transferValue"	REAL NOT NULL DEFAULT 0,
							"totalUseQuantity"	INTEGER NOT NULL DEFAULT 0,
							"totalUseValue"	REAL NOT NULL DEFAULT 0,
							"closingQuantity"	INTEGER NOT NULL DEFAULT 0,
							"closingValue"	REAL NOT NULL DEFAULT 0,
							FOREIGN KEY("ID") REFERENCES "mainTable"("ID") ON DELETE CASCADE);''')

		currentDatabaseCursor.execute('''CREATE TABLE "scheduleIndent" (
							"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
							"schNo"	TEXT NOT NULL DEFAULT 'OS',
							"srNo"	INTEGER NOT NULL DEFAULT 0,
							"name"	TEXT NOT NULL,
							"lastYearConsumption"	INTEGER NOT NULL DEFAULT 0,
							"bufferStock"	INTEGER NOT NULL DEFAULT 0,
							"currentBalance"	INTEGER NOT NULL DEFAULT 0,
							"requirement"	INTEGER NOT NULL DEFAULT 0,
							"recieveQuantity"	INTEGER,
							"brand"	TEXT NOT NULL DEFAULT ' ',
							"company"	TEXT NOT NULL DEFAULT ' ',
							"batch"	TEXT NOT NULL DEFAULT ' ',
							"manufactureDate"	TEXT NOT NULL DEFAULT ' ',
							"expDate"	TEXT NOT NULL DEFAULT ' ',
							"dateBookNo"	TEXT NOT NULL DEFAULT ' ',
							"pageDateBookNo"	TEXT NOT NULL DEFAULT ' ',
							"sign"	TEXT NOT NULL DEFAULT ' ',
							"sign2"	TEXT NOT NULL DEFAULT ' ',
							"remark"	TEXT NOT NULL DEFAULT ' ',
							FOREIGN KEY("ID") REFERENCES "mainTable"("ID") ON DELETE CASCADE);''')

		currentDatabaseCursor.execute('''CREATE TABLE "emergencyIndent" (
							"ID"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
							"schNo"	TEXT NOT NULL DEFAULT 'OS',
							"srNo"	INTEGER NOT NULL DEFAULT 0,
							"name"	TEXT NOT NULL,
							"lastYearConsumption"	INTEGER NOT NULL DEFAULT 0,
							"bufferStock"	INTEGER NOT NULL DEFAULT 0,
							"currentBalance"	INTEGER NOT NULL DEFAULT 0,
							"requirement"	INTEGER NOT NULL DEFAULT 0,
							"recieveQuantity"	INTEGER,
							"brand"	TEXT NOT NULL DEFAULT ' ',
							"company"	TEXT NOT NULL DEFAULT ' ',
							"batch"	TEXT NOT NULL DEFAULT ' ',
							"manufactureDate"	TEXT NOT NULL DEFAULT ' ',
							"expDate"	TEXT NOT NULL DEFAULT ' ',
							"dateBookNo"	TEXT NOT NULL DEFAULT ' ',
							"pageDateBookNo"	TEXT NOT NULL DEFAULT ' ',
							"sign"	TEXT NOT NULL DEFAULT ' ',
							"sign2"	TEXT NOT NULL DEFAULT ' ',
							"remark"	TEXT NOT NULL DEFAULT ' ',
							FOREIGN KEY("ID") REFERENCES "mainTable"("ID") ON DELETE CASCADE);''')

		currentDatabaseCursor.execute('''CREATE TABLE "register" (
							"key"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
							"ID"	INTEGER NOT NULL, 
							"date"	TEXT NOT NULL,
							"info"	TEXT NOT NULL,
							"price"	INTEGER NOT NULL DEFAULT 0,
							"income"	INTEGER NOT NULL DEFAULT 0,
							"use"	INTEGER NOT NULL DEFAULT 0,
							"remain"	INTEGER NOT NULL,
							"sign"	TEXT NOT NULL DEFAULT " ",
							FOREIGN KEY("ID") REFERENCES "mainTable"("ID") ON DELETE CASCADE);''')

		currentDatabaseCursor.execute('''CREATE TRIGGER nameInsertion 
							AFTER INSERT 
							ON mainTable
							BEGIN
								INSERT INTO storeAccount (ID,
														name,
														OBValue)
												VALUES (new.ID,
														new.name,
														new.oldPrice);
								INSERT INTO scheduleIndent (ID,
															schNo,
															name,
															lastYearConsumption,
															bufferStock,
															currentBalance)
													VALUES (new.ID,
															new.schNo,
															new.name,
															new.lastYearConsumption,
															ROUND(new.lastYearConsumption*5/12, 0),
															new.OBCurrentQuantity+new.RFODCurrentQuantity+new.RFCMSCurrentQuantity+new.LPCurrentQuantity+new.PMJAKCurrentQuantity);											   											   
								INSERT INTO emergencyIndent (ID,
															schNo,
															name,
															lastYearConsumption,
															bufferStock,
															currentBalance)
													VALUES (new.ID,
															new.schNo,
															new.name,
															new.lastYearConsumption,
															ROUND(new.lastYearConsumption*3/12, 0),
															new.OBCurrentQuantity+new.RFODCurrentQuantity+new.RFCMSCurrentQuantity+new.LPCurrentQuantity+new.PMJAKCurrentQuantity);											   											   

							END;''')

		currentDatabaseCursor.execute('''CREATE TRIGGER OBReceiveUpdate 
							AFTER INSERT 
							ON receiveTable
							WHEN new.type="OB"
							BEGIN
								UPDATE mainTable SET OBCurrentQuantity=OBCurrentQuantity+new.quantity WHERE ID = new.ID;
								UPDATE storeAccount SET OBQuantity=OBQuantity+new.quantity,
														totalRecieveQuantity=totalRecieveQuantity+new.quantity,
														closingQuantity=closingQuantity+new.quantity
														WHERE ID = new.ID;
								UPDATE scheduleIndent SET currentBalance=currentBalance+new.quantity WHERE ID = new.ID;
								UPDATE emergencyIndent SET currentBalance=currentBalance+new.quantity WHERE ID = new.ID;
							END;''')

		currentDatabaseCursor.execute('''CREATE TRIGGER RFCMSReceiveUpdate 
							AFTER INSERT 
							ON receiveTable
							WHEN new.type="RFCMS"
							BEGIN
								UPDATE mainTable SET RFCMSCurrentQuantity=RFCMSCurrentQuantity+new.quantity WHERE ID = new.ID;
								UPDATE storeAccount SET RFCMSQuantity=RFCMSQuantity+new.quantity,
														totalRecieveQuantity=totalRecieveQuantity+new.quantity,
														closingQuantity=closingQuantity+new.quantity
														WHERE ID = new.ID;
								UPDATE scheduleIndent SET currentBalance=currentBalance+new.quantity WHERE ID = new.ID;
								UPDATE emergencyIndent SET currentBalance=currentBalance+new.quantity WHERE ID = new.ID;
							END;''')
		
		currentDatabaseCursor.execute('''CREATE TRIGGER RFODReceiveUpdate 
							AFTER INSERT 
							ON receiveTable
							WHEN new.type="RFOD"
							BEGIN
								UPDATE mainTable SET RFODCurrentQuantity=RFODCurrentQuantity+new.quantity WHERE ID = new.ID;
								UPDATE storeAccount SET RFODQuantity=RFODQuantity+new.quantity,
														totalRecieveQuantity=totalRecieveQuantity+new.quantity,
														closingQuantity=closingQuantity+new.quantity
														WHERE ID = new.ID;
								UPDATE scheduleIndent SET currentBalance=currentBalance+new.quantity WHERE ID = new.ID;
								UPDATE emergencyIndent SET currentBalance=currentBalance+new.quantity WHERE ID = new.ID;
							END;''')

		currentDatabaseCursor.execute('''CREATE TRIGGER LPReceiveUpdate 
							AFTER INSERT 
							ON receiveTable
							WHEN new.type="LP"
							BEGIN
								UPDATE mainTable SET LPCurrentQuantity=LPCurrentQuantity+new.quantity WHERE ID = new.ID;
								UPDATE storeAccount SET LPQuantity=LPQuantity+new.quantity,
														totalRecieveQuantity=totalRecieveQuantity+new.quantity,
														closingQuantity=closingQuantity+new.quantity
														WHERE ID = new.ID;
								UPDATE scheduleIndent SET currentBalance=currentBalance+new.quantity WHERE ID = new.ID;
								UPDATE emergencyIndent SET currentBalance=currentBalance+new.quantity WHERE ID = new.ID;
							END;''')

		currentDatabaseCursor.execute('''CREATE TRIGGER PMJAKReceiveUpdate 
							AFTER INSERT 
							ON receiveTable
							WHEN new.type="PMJAK"
							BEGIN
								UPDATE mainTable SET PMJAKCurrentQuantity=PMJAKCurrentQuantity+new.quantity WHERE ID = new.ID;
								UPDATE storeAccount SET PMJAKQuantity=PMJAKQuantity+new.quantity,
														totalRecieveQuantity=totalRecieveQuantity+new.quantity,
														closingQuantity=closingQuantity+new.quantity
														WHERE ID = new.ID;
								UPDATE scheduleIndent SET currentBalance=currentBalance+new.quantity WHERE ID = new.ID;
								UPDATE emergencyIndent SET currentBalance=currentBalance+new.quantity WHERE ID = new.ID;
							END;''')

		currentDatabaseCursor.execute('''CREATE TRIGGER recieveCurrentUpdate 
							AFTER INSERT 
							ON receiveTable
							BEGIN
								INSERT INTO currentTable VALUES (new.key,
																new.ID,
																new.batch,
																new.quantity,
																new.expDate,
																new.date,
																new.type);
							END;''')

		currentDatabaseCursor.execute('''CREATE TRIGGER LPConsumptionUpdate 
							AFTER INSERT 
							ON consumptionTable
							WHEN new.type="LP" AND new.useType="consumption"
							BEGIN
								UPDATE storeAccount SET consumptionQuantity=consumptionQuantity+new.quantity, 
														totalUseQuantity=totalUseQuantity+new.quantity, 
														closingQuantity=closingQuantity-new.quantity WHERE ID = new.ID;
								UPDATE currentTable SET quantity=quantity-new.quantity WHERE batch=new.batch AND 
																							ID=new.ID AND 
																							expDate=new.expDate AND 
																							type=new.type AND
																							key=new.currentKey;
							END''')
		
		currentDatabaseCursor.execute('''CREATE TRIGGER LPTransferUpdate 
							AFTER INSERT 
							ON consumptionTable
							WHEN new.type="LP" AND new.useType="transfer"
							BEGIN
								UPDATE storeAccount SET transferQuantity=transferQuantity+new.quantity, 
														totalUseQuantity=totalUseQuantity+new.quantity, 
														closingQuantity=closingQuantity-new.quantity WHERE ID = new.ID;
								UPDATE currentTable SET quantity=quantity-new.quantity WHERE batch=new.batch AND 
																							ID=new.ID AND 
																							expDate=new.expDate AND 
																							type=new.type AND
																							key=new.currentKey;
							END''')

		currentDatabaseCursor.execute('''CREATE TRIGGER OBConsumptionUpdate 
							AFTER INSERT 
							ON consumptionTable
							WHEN new.type="OB" AND new.useType="consumption"
							BEGIN
								UPDATE storeAccount SET consumptionQuantity=consumptionQuantity+new.quantity, 
														totalUseQuantity=totalUseQuantity+new.quantity, 
														closingQuantity=closingQuantity-new.quantity WHERE ID = new.ID;
								UPDATE currentTable SET quantity=quantity-new.quantity WHERE batch=new.batch AND 
																							ID=new.ID AND 
																							expDate=new.expDate AND 
																							type=new.type AND
																							key=new.currentKey;
							END''')	

		currentDatabaseCursor.execute('''CREATE TRIGGER OBTransferUpdate 
							AFTER INSERT 
							ON consumptionTable
							WHEN new.type="OB" AND new.useType="transfer"
							BEGIN
								UPDATE storeAccount SET transferQuantity=transferQuantity+new.quantity, 
														totalUseQuantity=totalUseQuantity+new.quantity, 
														closingQuantity=closingQuantity-new.quantity WHERE ID = new.ID;
								UPDATE currentTable SET quantity=quantity-new.quantity WHERE batch=new.batch AND 
																							ID=new.ID AND 
																							expDate=new.expDate AND 
																							type=new.type AND 
																							key=new.currentKey;
							END''')				

		currentDatabaseCursor.execute('''CREATE TRIGGER PMJAKConsumptionUpdate 
							AFTER INSERT 
							ON consumptionTable
							WHEN new.type="PMJAK" AND new.useType="consumption"
							BEGIN
								UPDATE storeAccount SET consumptionQuantity=consumptionQuantity+new.quantity, 
														totalUseQuantity=totalUseQuantity+new.quantity, 
														closingQuantity=closingQuantity-new.quantity WHERE ID = new.ID;
								UPDATE currentTable SET quantity=quantity-new.quantity WHERE batch=new.batch AND 
																							ID=new.ID AND 
																							expDate=new.expDate AND 
																							type=new.type AND
																							key=new.currentKey;
							END''')

		currentDatabaseCursor.execute('''CREATE TRIGGER PMJAKTransferUpdate 
							AFTER INSERT 
							ON consumptionTable
							WHEN new.type="PMJAK" AND new.useType="transfer"
							BEGIN
								UPDATE storeAccount SET transferQuantity=transferQuantity+new.quantity, 
														totalUseQuantity=totalUseQuantity+new.quantity, 
														closingQuantity=closingQuantity-new.quantity WHERE ID = new.ID;
								UPDATE currentTable SET quantity=quantity-new.quantity WHERE batch=new.batch AND 
																							ID=new.ID AND 
																							expDate=new.expDate AND 
																							type=new.type AND
																							key=new.currentKey;
							END''')

		currentDatabaseCursor.execute('''CREATE TRIGGER RFCMSConsumptionUpdate 
							AFTER INSERT 
							ON consumptionTable
							WHEN new.type="RFCMS" AND new.useType="consumption"
							BEGIN
								UPDATE storeAccount SET consumptionQuantity=consumptionQuantity+new.quantity, 
														totalUseQuantity=totalUseQuantity+new.quantity, 
														closingQuantity=closingQuantity-new.quantity WHERE ID = new.ID;
								UPDATE currentTable SET quantity=quantity-new.quantity WHERE batch=new.batch AND 
																							ID=new.ID AND 
																							expDate=new.expDate AND 
																							type=new.type AND
																							key=new.currentKey;
							END''')

		currentDatabaseCursor.execute('''CREATE TRIGGER RFCMSTransferUpdate 
							AFTER INSERT 
							ON consumptionTable
							WHEN new.type="RFCMS" AND new.useType="transfer"
							BEGIN
								UPDATE storeAccount SET transferQuantity=transferQuantity+new.quantity, 
														totalUseQuantity=totalUseQuantity+new.quantity, 
														closingQuantity=closingQuantity-new.quantity WHERE ID = new.ID;
								UPDATE currentTable SET quantity=quantity-new.quantity WHERE batch=new.batch AND 
																							ID=new.ID AND 
																							expDate=new.expDate AND 
																							type=new.type AND
																							key=new.currentKey;
							END''')

		currentDatabaseCursor.execute('''CREATE TRIGGER RFODConsumptionUpdate 
							AFTER INSERT 
							ON consumptionTable
							WHEN new.type="RFOD" AND new.useType="consumption"
							BEGIN
								UPDATE storeAccount SET consumptionQuantity=consumptionQuantity+new.quantity, 
														totalUseQuantity=totalUseQuantity+new.quantity, 
														closingQuantity=closingQuantity-new.quantity WHERE ID = new.ID;
								UPDATE currentTable SET quantity=quantity-new.quantity WHERE batch=new.batch AND 
																							ID=new.ID AND 
																							expDate=new.expDate AND 
																							type=new.type AND
																							key=new.currentKey;
							END''')

		currentDatabaseCursor.execute('''CREATE TRIGGER RFODTransferUpdate 
							AFTER INSERT 
							ON consumptionTable
							WHEN new.type="RFOD" AND new.useType="transfer"
							BEGIN
								UPDATE storeAccount SET transferQuantity=transferQuantity+new.quantity, 
														totalUseQuantity=totalUseQuantity+new.quantity, 
														closingQuantity=closingQuantity-new.quantity WHERE ID = new.ID;
								UPDATE currentTable SET quantity=quantity-new.quantity WHERE batch=new.batch AND 
																							ID=new.ID AND 
																							expDate=new.expDate AND 
																							type=new.type AND
																							key=new.currentKey;
							END''')

		currentDatabaseCursor.execute('''CREATE TRIGGER LPCorrection 
							AFTER UPDATE 
							ON currentTable
							WHEN new.type="LP" 
							BEGIN
								UPDATE mainTable SET LPCurrentQuantity=LPCurrentQuantity-old.quantity+new.quantity WHERE ID=new.ID;
								UPDATE scheduleIndent SET currentBalance=currentBalance-old.quantity+new.quantity WHERE ID=new.ID;
								UPDATE emergencyIndent SET currentBalance=currentBalance-old.quantity+new.quantity WHERE ID=new.ID;
							END''')

		currentDatabaseCursor.execute('''CREATE TRIGGER OBCorrection 
							AFTER UPDATE 
							ON currentTable
							WHEN new.type="OB" 
							BEGIN
								UPDATE mainTable SET OBCurrentQuantity=OBCurrentQuantity-old.quantity+new.quantity WHERE ID=new.ID;
								UPDATE scheduleIndent SET currentBalance=currentBalance-old.quantity+new.quantity WHERE ID=new.ID;
								UPDATE emergencyIndent SET currentBalance=currentBalance-old.quantity+new.quantity WHERE ID=new.ID;
							END''')
		
		currentDatabaseCursor.execute('''CREATE TRIGGER PMJAKCorrection 
							AFTER UPDATE 
							ON currentTable
							WHEN new.type="PMJAK" 
							BEGIN
								UPDATE mainTable SET PMJAKCurrentQuantity=PMJAKCurrentQuantity-old.quantity+new.quantity WHERE ID=new.ID;
								UPDATE scheduleIndent SET currentBalance=currentBalance-old.quantity+new.quantity WHERE ID=new.ID;
								UPDATE emergencyIndent SET currentBalance=currentBalance-old.quantity+new.quantity WHERE ID=new.ID;
							END''')

		currentDatabaseCursor.execute('''CREATE TRIGGER RFCMSCorrection 
							AFTER UPDATE 
							ON currentTable
							WHEN new.type="RFCMS" 
							BEGIN
								UPDATE mainTable SET RFCMSCurrentQuantity=RFCMSCurrentQuantity-old.quantity+new.quantity WHERE ID=new.ID;
								UPDATE scheduleIndent SET currentBalance=currentBalance-old.quantity+new.quantity WHERE ID=new.ID;
								UPDATE emergencyIndent SET currentBalance=currentBalance-old.quantity+new.quantity WHERE ID=new.ID;
							END''')
		
		currentDatabaseCursor.execute('''CREATE TRIGGER RFODCorrection 
							AFTER UPDATE 
							ON currentTable
							WHEN new.type="RFOD" 
							BEGIN
								UPDATE mainTable SET RFODCurrentQuantity=RFODCurrentQuantity-old.quantity+new.quantity WHERE ID=new.ID;
								UPDATE scheduleIndent SET currentBalance=currentBalance-old.quantity+new.quantity WHERE ID=new.ID;
								UPDATE emergencyIndent SET currentBalance=currentBalance-old.quantity+new.quantity WHERE ID=new.ID;
							END''')
		
		currentDatabaseCursor.execute('''CREATE TRIGGER consumptionCorrection
							AFTER UPDATE 
							ON consumptionTable
							WHEN new.useType="consumption"
							BEGIN
								UPDATE currentTable SET quantity=quantity+old.quantity-new.quantity WHERE key=new.currentKey;
								UPDATE storeAccount SET consumptionQuantity=consumptionQuantity-old.quantity+new.quantity, 
														totalUseQuantity=totalUseQuantity-old.quantity+new.quantity,
														closingQuantity=closingQuantity+old.quantity-new.quantity WHERE ID=new.ID;
							END''')

		currentDatabaseCursor.execute('''CREATE TRIGGER transferCorrection
							AFTER UPDATE 
							ON consumptionTable
							WHEN new.useType="transfer"
							BEGIN
								UPDATE currentTable SET quantity=quantity+old.quantity-new.quantity WHERE key=new.currentKey;
								UPDATE storeAccount SET transferQuantity=transferQuantity-old.quantity+new.quantity, totalUseQuantity=totalUseQuantity-old.quantity+new.quantity WHERE ID=new.ID;
							END''')

		adminCursor.execute("INSERT INTO UserDatabaseDetail VALUES('"+name+"',"+str(sy)+","+str(ey)+");")
		adminCursor.execute("UPDATE AdminTable SET currentDatabase='"+name+"', totalDatabase=totalDatabase+1;")
		adminDataBase.commit()
		currentDatabase.commit()
		
		return True
	
	except:
		return False
	
def medicineNameInsertionDB(schNo, type, name, oldPrice, lastYearConsumption):
	
	try:
		query = "INSERT INTO mainTable (schNo, type, name, oldPrice, lastYearConsumption) VALUES ('"+schNo+"','"+type+"','"+name+"',"+oldPrice+","+lastYearConsumption+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()
		return True
	
	except:
		return False

def IDGet(name):

	query= "SELECT ID FROM mainTable WHERE name='"+name+"';"
	currentDatabaseCursor.execute(query)
	result = currentDatabaseCursor.fetchone()
	return str(result[0])

def OBSubmitionDB(ID, batch, quantity, expDate, date):
	try:
		name = nameGet(ID)
		query = "INSERT INTO receiveTable (ID, batch, quantity, expDate, date, type) VALUES ("+ID+",'"+batch+"',"+quantity+",'"+expDate+"','"+date+"','OB');"
		currentDatabaseCursor.execute(query)
		info = "Opening Balance , Batch No: "+batch+", Expiry Date: "+expDate
		query = "INSERT INTO register (ID, date, info, income, remain) VALUES ("+ID+",'"+date+"','"+info+"',"+quantity+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()
		return True
	
	except:
		return False
	
def LPPMJAKSuggestions():

	currentDatabaseCursor.execute("SELECT name FROM mainTable;")
	output = currentDatabaseCursor.fetchall()
	result = []

	for i in range(len(output)):
		result.append(output[i][0])

	return result
	
def LPPMJAKSubmitionDB(name, batch, quantity, expDate, date, receivetype, price):
	try:
		ID = IDGet(name)
		query = "INSERT INTO receiveTable (ID, batch, quantity, expDate, date, type) VALUES ("+ID+",'"+batch+"',"+quantity+",'"+expDate+"','"+date+"','"+receivetype+"');"
		currentDatabaseCursor.execute(query)
		info = "Purchased through "+receivetype+", Batch No: "+batch+", Expiry Date: "+expDate
		query = "INSERT INTO register (ID, date, info, income, remain, price) VALUES ("+ID+",'"+date+"','"+info+"',"+quantity+","+currentBalanceGet(name)+","+price+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()
		return True

	except:
		return False

def RFODSuggestions():

	currentDatabaseCursor.execute("SELECT name FROM mainTable;")
	output = currentDatabaseCursor.fetchall()
	result = []

	for i in range(len(output)):
		result.append(output[i][0])

	return result

def indentSuggestions():

	currentDatabaseCursor.execute("SELECT name FROM mainTable;")
	output = currentDatabaseCursor.fetchall()
	result = []

	for i in range(len(output)):
		result.append(output[i][0])

	return result

def RFODSubmitionDB(name, batch, quantity, expDate, date, dispensary):
	try:	
		ID = IDGet(name)
		query = "INSERT INTO receiveTable (ID, batch, quantity, expDate, date, type) VALUES ("+ID+",'"+batch+"',"+quantity+",'"+expDate+"','"+date+"','RFOD');"
		currentDatabaseCursor.execute(query)
		info = "Received from "+dispensary+", Batch No: "+batch+", Expiry Date: "+expDate
		query = "INSERT INTO register (ID, date, info, income, remain) VALUES ("+ID+",'"+date+"','"+info+"',"+quantity+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()
		return True

	except:
		return False	

def currentBalanceGet(name):

	query= "SELECT currentBalance FROM scheduleIndent WHERE name='"+name+"';"
	currentDatabaseCursor.execute(query)
	result = currentDatabaseCursor.fetchall()
	if(result == None or result == []):
		return 0
	else:
		return str(result[0][0])

def consumptionSuggestions():

	currentDatabaseCursor.execute("SELECT name FROM scheduleIndent WHERE currentBalance > 0;")
	output = currentDatabaseCursor.fetchall()
	result = []

	for i in range(len(output)):
		result.append(output[i][0])

	return result

def consumptionSubmitionDB(name, quantity, useDate):
	try:
		totalQty = quantity		
		ID = IDGet(name)
		currentDatabaseCursor.execute("SELECT * FROM currentTable WHERE ID="+ID+" AND quantity>0 ORDER BY date(expDate);")
		output = currentDatabaseCursor.fetchall()
		i = 0

		while(quantity > 0):
			if(quantity >= output[i][3]):
				currentDatabaseCursor.execute("INSERT INTO consumptionTable (ID, batch, quantity, expDate, date, type, useType, currentKey) VALUES ("+str(output[i][1])+",'"+output[i][2]+"',"+str(output[i][3])+",'"+output[i][4]+"','"+useDate+"','"+output[i][6]+"','consumption',"+str(output[i][0])+");")
				quantity = quantity - output[i][3]
				i=i+1
			
			else:
				query = "INSERT INTO consumptionTable (ID, batch, quantity, expDate, date, type, useType, currentKey) VALUES ("+str(output[i][1])+",'"+output[i][2]+"',"+str(quantity)+",'"+output[i][4]+"','"+useDate+"','"+output[i][6]+"','consumption',"+str(output[i][0])+");"
				currentDatabaseCursor.execute(query)
				quantity = 0
				break
		
		currentDatabaseCursor.execute("INSERT INTO register (ID, date, info, use, remain) VALUES ("+ID+",'"+useDate+"','Consumption in OPD',"+str(totalQty)+","+currentBalanceGet(name)+");")
		currentDatabase.commit()

		return True

	except:
		return False

def indentDataGet(indentType):

	currentDatabaseCursor.execute("SELECT ID,name,schNo,bufferStock,currentBalance FROM "+indentType+"Indent WHERE currentBalance < bufferStock;")
	result = currentDatabaseCursor.fetchall()
	return result

def closeExpDateGet(name):

	ID = IDGet(name)
	
	currentDatabaseCursor.execute("SELECT expDate FROM currentTable WHERE ID="+ID+" AND quantity>0 ORDER BY date(expDate);")
	output = currentDatabaseCursor.fetchall()
	
	if(output == None or output == []):
		return "NA"

	else:
		return output[0][0]

def indentRequirementSubmitionDB(indentType, name, quantity):
	try:
		currentDatabaseCursor.execute("UPDATE "+indentType+"Indent SET requirement="+quantity+" WHERE name='"+name+"';")
		currentDatabase.commit()
		return True
	
	except:
		return False

def indentPDFData(indentType):

	currentDatabaseCursor.execute("SELECT * FROM "+indentType+"Indent WHERE requirement>0 ORDER BY ID;")
	output = currentDatabaseCursor.fetchall()

	return output

def RFCMSData(indentType):
	
	currentDatabaseCursor.execute("SELECT name,requirement FROM "+indentType+"Indent WHERE requirement>0;")
	output = currentDatabaseCursor.fetchall()
	return output

def RFCMSSubmitionDB(name, batch, quantity, expDate, date, indentNo, indentType):
	
	try:
		ID = IDGet(name)
		query = "INSERT INTO receiveTable (ID, batch, quantity, expDate, date, type) VALUES ("+ID+",'"+batch+"',"+quantity+",'"+expDate+"','"+date+"','RFCMS');"
		currentDatabaseCursor.execute(query)
		currentDatabaseCursor.execute("UPDATE "+indentType+"Indent SET requirement=0 WHERE name='"+name+"';")
		info = "Received from CMS, Indent No: "+indentNo+", Batch No: "+batch+", Expiry Date: "+expDate
		query = "INSERT INTO register (ID, date, info, income, remain) VALUES ("+ID+",'"+date+"','"+info+"',"+quantity+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()
		return True

	except:
		return False	

def RFCMSSuggestion():

	currentDatabaseCursor.execute("SELECT name FROM mainTable;")
	output = currentDatabaseCursor.fetchall()
	result = []

	for i in range(len(output)):
		result.append(output[i][0])

	return result

def transferSuggestion():

	currentDatabaseCursor.execute("SELECT name FROM emergencyIndent WHERE currentBalance>0;")
	output = currentDatabaseCursor.fetchall()
	result = []

	for i in range(len(output)):
		result.append(output[i][0])

	return result

def transferBatchSuggestion(name):

	ID = IDGet(name)

	currentDatabaseCursor.execute("SELECT batch FROM currentTable WHERE ID="+ID+" AND quantity>0;")
	output = currentDatabaseCursor.fetchall()
	result = []

	for i in range(len(output)):
		result.append(output[i][0])

	return result

def getBatchQuantity(batch,name):

	currentDatabaseCursor.execute("SELECT quantity FROM currentTable WHERE batch='"+batch+"' AND ID="+IDGet(name)+";")
	output = currentDatabaseCursor.fetchall()
	return output[0][0]

def getBatchType(batch,name):

	currentDatabaseCursor.execute("SELECT type FROM currentTable WHERE batch='"+batch+"' AND ID="+IDGet(name)+";")
	output = currentDatabaseCursor.fetchall()
	return output[0][0]

def getBatchExpDate(batch, name):

	currentDatabaseCursor.execute("SELECT expDate FROM currentTable WHERE batch='"+batch+"' AND ID="+IDGet(name)+";")
	output = currentDatabaseCursor.fetchall()
	return output[0][0]

def getBatchKey(batch, name):

	currentDatabaseCursor.execute("SELECT key FROM currentTable WHERE batch='"+batch+"' AND ID="+IDGet(name)+";")
	output = currentDatabaseCursor.fetchall()
	return str(output[0][0])

def transferSubmitionDB(name, batch, quantity, transferDate, expDate):
	try:
		receiveType = getBatchType(batch, name)
		ID = IDGet(name)
		currentKey = getBatchKey(batch, name)
		currentDatabaseCursor.execute("INSERT INTO consumptionTable (ID, batch, quantity, expDate, date, type, useType, currentKey) VALUES ("+ID+",'"+batch+"',"+quantity+",'"+expDate+"','"+transferDate+"','"+receiveType+"','transfer',"+currentKey+");")
		info = "Transfered to other disp. , Batch No: "+batch+", Expiry Date: "+expDate
		query = "INSERT INTO register (ID, date, info, use, remain) VALUES ("+ID+",'"+transferDate+"','"+info+"',"+quantity+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)	
		currentDatabase.commit()
		return True

	except:
		return False
	
def storeAccountNames():

	currentDatabaseCursor.execute("SELECT name FROM storeAccount ORDER BY ID;")
	output = currentDatabaseCursor.fetchall()
	result = []

	for i in range(len(output)):
		result.append(output[i][0])

	return result

def storeAccountSubmitionDB(newPrice, name):

	try:
		ID = IDGet(name)

		currentDatabaseCursor.execute("UPDATE mainTable SET newPrice="+newPrice+" WHERE ID="+ID+";")

		data = storeAccountData(name)

		RFCMSValue = data[1][6]*float(newPrice)
		RFODValue = data[1][4]*float(newPrice)
		transferValue = data[1][16]*float(newPrice)
		totalReceiveValue = data[1][3]+RFCMSValue+RFODValue
		try:
			closingValue = (data[0][1]*(data[1][2]/data[1][3]))+(data[0][2]*float(newPrice))+(data[0][3]*float(newPrice))
		except:
			closingValue = (data[0][1]*(data[1][2]/1.0))+(data[0][2]*float(newPrice))+(data[0][3]*float(newPrice))
		totalUseValue = totalReceiveValue - closingValue
		consumptionValue = totalUseValue - transferValue

		currentDatabaseCursor.execute("UPDATE storeAccount SET RFCMSValue="+str(RFCMSValue)+", RFODValue="+str(RFODValue)+", transferValue="+str(transferValue)+", totalRecieveValue="+str(totalReceiveValue)+", closingValue="+str(closingValue)+", totalUseValue="+str(totalUseValue)+", consumptionValue="+str(consumptionValue)+" WHERE ID="+ID+";")
		currentDatabase.commit()
		return True

	except:
		return False

def storeAccountData(name):

	currentDatabaseCursor.execute("SELECT oldPrice,OBCurrentQuantity,RFCMSCurrentQuantity,RFODCurrentQuantity FROM mainTable WHERE name='"+name+"';")
	result1 = currentDatabaseCursor.fetchone()

	currentDatabaseCursor.execute("SELECT * FROM storeAccount WHERE name='"+name+"';")
	result2 = currentDatabaseCursor.fetchone()

	return [result1, result2]

def storeAccountPDFData():
	 
	currentDatabaseCursor.execute("SELECT * FROM storeAccount WHERE totalRecieveValue>0 ORDER BY ID;")
	output = currentDatabaseCursor.fetchall()
	return output

def nameGet(ID):

	currentDatabaseCursor.execute("SELECT name FROM mainTable WHERE ID="+ID+";")
	result = currentDatabaseCursor.fetchall()
	return str(result[0][0])

def usageRegisterData(name, startDate, endDate):

	ID = IDGet(name)
	
	currentDatabaseCursor.execute("SELECT date,info,price,income,use,remain,sign FROM register WHERE ID="+ID+" AND date(date)>=date('"+startDate+"') AND date(date)<=date('"+endDate+"');")
	result = currentDatabaseCursor.fetchall()
	return result

def nextDataBaseCreator(sy, ey):
	try:
		createDataBase(sy, ey)
		data = nextDatabaseData(int(sy)-1, int(ey)-1)

		for i in range(len(data[0])):
			medicineNameInsertionDB(data[0][i][0], data[0][i][1], str(data[0][i][2]), str(data[1][i][1]), str(data[1][i][0]))

		for j in range(len(data[2])):
			OBSubmitionDB(str(data[2][j][0]), str(data[2][j][1]), str(data[2][j][2]), data[2][j][3], str(sy)+"-04-01")
		
		return True
	
	except:
		return False

def nextDatabaseData(sy, ey):

	tempDatabase = connect(str(sy)+"-"+str(ey)+"DATABASE.db")
	tempDatabaseCursor = tempDatabase.cursor()

	tempDatabaseCursor.execute("SELECT schNo,type,name,newPrice FROM mainTable ORDER BY ID;")
	result1 = tempDatabaseCursor.fetchall()

	tempDatabaseCursor.execute("SELECT consumptionQuantity,closingValue FROM storeAccount ORDER BY ID;")
	result2 = tempDatabaseCursor.fetchall()

	tempDatabaseCursor.execute("SELECT ID,batch,quantity,expDate FROM currentTable;")
	result3 = tempDatabaseCursor.fetchall()

	return [result1, result2, result3]

def getConsumptionQuantity(name, date):

	ID = IDGet(name)

	currentDatabaseCursor.execute("SELECT use FROM register WHERE date='"+date+"' AND ID="+ID+" AND info='Consumption in OPD';")
	output = currentDatabaseCursor.fetchall()
	result = 0
	if(len(output) > 0):
		for i in  range(len(output)):
			result += output[i][0]

	return result

def getTransferQuantity(name, date):
	ID = IDGet(name)

	currentDatabaseCursor.execute("SELECT quantity FROM consumptionTable WHERE date='"+date+"' AND ID="+ID+" AND useType='transfer';")
	output = currentDatabaseCursor.fetchall()
	result = 0
	if(len(output) > 0):
		for i in  range(len(output)):
			result += output[i][0]

	return result

def consumptionIncreaseDB(name, quantity, useDate, date):
	try:
		totalQty = quantity		
		ID = IDGet(name)
		currentDatabaseCursor.execute("SELECT * FROM currentTable WHERE ID="+ID+" AND quantity>0 AND ORDER BY date(expDate);")
		output = currentDatabaseCursor.fetchall()
		i = 0

		while(quantity > 0):
			if(quantity >= output[i][3]):
				currentDatabaseCursor.execute("INSERT INTO consumptionTable (ID, batch, quantity, expDate, date, type, useType, currentKey) VALUES ("+str(output[i][1])+",'"+output[i][2]+"',"+str(output[i][3])+",'"+output[i][4]+"','"+useDate+"','"+output[i][6]+"','consumption',"+str(output[i][0])+");")
				quantity = quantity - output[i][3]
				i=i+1
			
			else:
				query = "INSERT INTO consumptionTable (ID, batch, quantity, expDate, date, type, useType, currentKey) VALUES ("+str(output[i][1])+",'"+output[i][2]+"',"+str(quantity)+",'"+output[i][4]+"','"+useDate+"','"+output[i][6]+"','consumption',"+str(output[i][0])+");"
				currentDatabaseCursor.execute(query)
				quantity = 0
				break

		query = "INSERT INTO register (ID, date, info, use, remain) VALUES ("+ID+",'"+date+"','Mistake made in consumption in OPD on date:"+useDate+"',"+str(totalQty)+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()
		return True

	except:
		return False

def consumptionDecreaseDB(name, quantity, useDate, date):
	try:
		ID = IDGet(name)
		query = "SELECT * FROM consumptionTable WHERE date='"+useDate+"' AND ID="+ID+" AND useType='consumption' ORDER BY ID DESC;"
		currentDatabaseCursor.execute(query)
		data = currentDatabaseCursor.fetchall()
		totalQty = quantity
		i = 0

		while(quantity>0):

			if(quantity >= data[i][3]):
				query = "UPDATE consumptionTable SET quantity=0 WHERE key="+str(data[i][0])+";"
				currentDatabaseCursor.execute(query)
				quantity = quantity - data[i][3]
				i = i + 1

			else:
				query = "UPDATE consumptionTable SET quantity="+str(data[i][3]-quantity)+" WHERE key="+str(data[i][0])+";"
				currentDatabaseCursor.execute(query)
				quantity = 0
				break

		query = "INSERT INTO register (ID, date, info, income, remain) VALUES ("+ID+",'"+date+"','Mistake made in consumption in OPD on date:"+useDate+"',"+str(totalQty)+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()
		return True
	
	except:
		return False

def getReceivedQuantity(name, date, batch):

	ID = IDGet(name)
	query = "SELECT quantity FROM receiveTable WHERE batch='"+batch+"' AND date='"+date+"' AND ID="+ID+";"
	currentDatabaseCursor.execute(query)

	output = currentDatabaseCursor.fetchall()
	result = 0

	if(len(output) > 0):
		for i in range(len(output)):
			result += output[i][0]

	return result

def getCurrentQuantity(name, date, batch):

	ID = IDGet(name)
	query = "SELECT quantity FROM currentTable WHERE batch='"+batch+"' AND date='"+date+"' AND ID="+ID+";"
	currentDatabaseCursor.execute(query)

	output = currentDatabaseCursor.fetchall()
	result = 0

	if(len(output) > 0):
		for i in range(len(output)):
			result += output[i][0]

	return result

def RFODIncreaseDB(name, quantity, entryDate, date, batch):
	try:
		ID = IDGet(name)
		query = "UPDATE currentTable SET quantity=quantity+"+str(quantity)+" WHERE ID="+ID+" AND date='"+entryDate+"' AND batch='"+batch+"';"
		currentDatabaseCursor.execute(query)

		query = "UPDATE receiveTable SET quantity=quantity+"+str(quantity)+" WHERE ID="+ID+" AND date='"+entryDate+"' AND batch='"+batch+"';"
		currentDatabaseCursor.execute(query)

		query = "UPDATE storeAccount SET RFODQuantity=RFODQuantity+"+str(quantity)+", totalRecieveQuantity=totalRecieveQuantity+"+str(quantity)+", closingQuantity=closingQuantity+"+str(quantity)+" WHERE ID="+ID+";"
		currentDatabaseCursor.execute(query)

		query = "INSERT INTO register (ID, date, info, income, remain) VALUES ("+ID+",'"+date+"','Mistake made in Received from other disp. on date:"+entryDate+"',"+str(quantity)+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()

		return True

	except:
		return False

def RFODDecreaseDB(name, quantity, entryDate, date, batch, currentQuantity):
	try:
		ID = IDGet(name)

		if(quantity > currentQuantity):
			query = "SELECT * FROM consumptionTable WHERE currentKey IN (SELECT key FROM currentTable WHERE ID="+ID+" AND date='"+entryDate+"' AND batch='"+batch+"') AND useType='consumption' ORDER BY key DESC;"
			currentDatabaseCursor.execute(query)
			result = currentDatabaseCursor.fetchall()
			useDate = result[0][5]
			returnedQuantity = 0
			i=0
			
			while(returnedQuantity < (quantity-currentQuantity)):

				if(quantity-returnedQuantity-currentQuantity < result[i][3]):

					query = "UPDATE consumptionTable SET quantity=quantity-"+str(quantity-returnedQuantity-currentQuantity)+" WHERE key="+str(result[i][0])+";"
					currentDatabaseCursor.execute(query)
					returnedQuantity = quantity-currentQuantity
					i+=1

				else:

					query = "UPDATE consumptionTable SET quantity=0 WHERE key="+str(result[i][0])+";"
					currentDatabaseCursor.execute(query)
					returnedQuantity += result[i][3]
					i+=1

		i=0
		decreasedQunatity = quantity
		query = "SELECT * FROM currentTable WHERE ID="+ID+" AND batch='"+batch+"' AND date='"+entryDate+"' ORDER BY key DESC;"
		currentDatabaseCursor.execute(query)
		result1 = currentDatabaseCursor.fetchall()

		while(decreasedQunatity > 0):
			if(decreasedQunatity < result1[i][3]):

				query = "UPDATE currentTable SET quantity=quantity-"+str(decreasedQunatity)+" WHERE key="+str(result1[i][0])+";" 
				currentDatabaseCursor.execute(query)
				query = "UPDATE receiveTable SET quantity=quantity-"+str(decreasedQunatity)+" WHERE key="+str(result1[i][0])+";"
				currentDatabaseCursor.execute(query)
				query = "UPDATE storeAccount SET RFODQuantity=RFODQuantity-"+str(decreasedQunatity)+" WHERE ID="+ID+";"
				currentDatabaseCursor.execute(query)
				decreasedQunatity = 0
				i+=1

			else:

				query = "UPDATE currentTable SET quantity=0 WHERE key="+str(result1[i][0])+";"
				currentDatabaseCursor.execute(query)
				query = "UPDATE receiveTable SET quantity=quantity-"+str(result1[i][3])+" WHERE key="+str(result1[i][0])+";"
				currentDatabaseCursor.execute(query)
				query = "UPDATE storeAccount SET RFODQuantity=RFODQuantity-"+str(result1[i][3])+" WHERE ID="+ID+";"
				currentDatabaseCursor.execute(query)
				decreasedQunatity = decreasedQunatity - result1[i][3]
				i += 1

		if(quantity > currentQuantity):

			currentDatabaseCursor.execute("SELECT * FROM currentTable WHERE ID="+ID+" AND quantity>0 ORDER BY date(expDate);")
			output = currentDatabaseCursor.fetchall()
			i = 0

			while(returnedQuantity > 0):
				if(returnedQuantity >= output[i][3]):
					currentDatabaseCursor.execute("INSERT INTO consumptionTable (ID, batch, quantity, expDate, date, type, useType, currentKey) VALUES ("+str(output[i][1])+",'"+output[i][2]+"',"+str(output[i][3])+",'"+output[i][4]+"','"+useDate+"','"+output[i][6]+"','consumption',"+str(output[i][0])+");")
					returnedQuantity = returnedQuantity - output[i][3]
					i=i+1
				
				else:
					query = "INSERT INTO consumptionTable (ID, batch, quantity, expDate, date, type, useType, currentKey) VALUES ("+str(output[i][1])+",'"+output[i][2]+"',"+str(returnedQuantity)+",'"+output[i][4]+"','"+useDate+"','"+output[i][6]+"','consumption',"+str(output[i][0])+");"
					currentDatabaseCursor.execute(query)
					returnedQuantity = 0
					break
		
		query = "INSERT INTO register (ID, date, info, use, remain) VALUES ("+ID+",'"+date+"','Mistake made in Receievd from other disp. on date:"+entryDate+"',"+str(quantity)+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()
		return True

	except:
		return False

def LPDecreaseDB(name, quantity, entryDate, date, batch, currentQuantity):
	try:
		ID = IDGet(name)

		if(quantity > currentQuantity):
			query = "SELECT * FROM consumptionTable WHERE currentKey IN (SELECT key FROM currentTable WHERE ID="+ID+" AND date='"+entryDate+"' AND batch='"+batch+"') AND useType='consumption' ORDER BY key DESC;"
			currentDatabaseCursor.execute(query)
			result = currentDatabaseCursor.fetchall()
			useDate = result[0][5]
			returnedQuantity = 0
			i=0
			
			while(returnedQuantity < (quantity-currentQuantity)):

				if(quantity-returnedQuantity-currentQuantity < result[i][3]):

					query = "UPDATE consumptionTable SET quantity=quantity-"+str(quantity-returnedQuantity-currentQuantity)+" WHERE key="+str(result[i][0])+";"
					currentDatabaseCursor.execute(query)
					returnedQuantity = quantity-currentQuantity
					i+=1

				else:

					query = "UPDATE consumptionTable SET quantity=0 WHERE key="+str(result[i][0])+";"
					currentDatabaseCursor.execute(query)
					returnedQuantity += result[i][3]
					i+=1

		i=0
		decreasedQunatity = quantity
		query = "SELECT * FROM currentTable WHERE ID="+ID+" AND batch='"+batch+"' AND date='"+entryDate+"' ORDER BY key DESC;"
		currentDatabaseCursor.execute(query)
		result1 = currentDatabaseCursor.fetchall()

		while(decreasedQunatity > 0):
			if(decreasedQunatity < result1[i][3]):

				query = "UPDATE currentTable SET quantity=quantity-"+str(decreasedQunatity)+" WHERE key="+str(result1[i][0])+";" 
				currentDatabaseCursor.execute(query)
				query = "UPDATE receiveTable SET quantity=quantity-"+str(decreasedQunatity)+" WHERE key="+str(result1[i][0])+";"
				currentDatabaseCursor.execute(query)
				query = "UPDATE storeAccount SET LPQuantity=LPQuantity-"+str(decreasedQunatity)+" WHERE ID="+ID+";"
				currentDatabaseCursor.execute(query)
				decreasedQunatity = 0
				i+=1

			else:

				query = "UPDATE currentTable SET quantity=0 WHERE key="+str(result1[i][0])+";"
				currentDatabaseCursor.execute(query)
				query = "UPDATE receiveTable SET quantity=quantity-"+str(result1[i][3])+" WHERE key="+str(result1[i][0])+";"
				currentDatabaseCursor.execute(query)
				query = "UPDATE storeAccount SET LPQuantity=LPQuantity-"+str(result1[i][3])+" WHERE ID="+ID+";"
				currentDatabaseCursor.execute(query)
				decreasedQunatity = decreasedQunatity - result1[i][3]
				i += 1

		if(quantity > currentQuantity):

			currentDatabaseCursor.execute("SELECT * FROM currentTable WHERE ID="+ID+" AND quantity>0 ORDER BY date(expDate);")
			output = currentDatabaseCursor.fetchall()
			i = 0

			while(returnedQuantity > 0):
				if(returnedQuantity >= output[i][3]):
					currentDatabaseCursor.execute("INSERT INTO consumptionTable (ID, batch, quantity, expDate, date, type, useType, currentKey) VALUES ("+str(output[i][1])+",'"+output[i][2]+"',"+str(output[i][3])+",'"+output[i][4]+"','"+useDate+"','"+output[i][6]+"','consumption',"+str(output[i][0])+");")
					returnedQuantity = returnedQuantity - output[i][3]
					i=i+1
				
				else:
					query = "INSERT INTO consumptionTable (ID, batch, quantity, expDate, date, type, useType, currentKey) VALUES ("+str(output[i][1])+",'"+output[i][2]+"',"+str(returnedQuantity)+",'"+output[i][4]+"','"+useDate+"','"+output[i][6]+"','consumption',"+str(output[i][0])+");"
					currentDatabaseCursor.execute(query)
					returnedQuantity = 0
					break
		
		query = "INSERT INTO register (ID, date, info, use, remain) VALUES ("+ID+",'"+date+"','Mistake made in Local Purchase on date:"+entryDate+"',"+str(quantity)+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()
		return True
	
	except:
		return False

def PMJAKDecreaseDB(name, quantity, entryDate, date, batch, currentQuantity):
	try:
		ID = IDGet(name)

		if(quantity > currentQuantity):
			query = "SELECT * FROM consumptionTable WHERE currentKey IN (SELECT key FROM currentTable WHERE ID="+ID+" AND date='"+entryDate+"' AND batch='"+batch+"') AND useType='consumption' ORDER BY key DESC;"
			currentDatabaseCursor.execute(query)
			result = currentDatabaseCursor.fetchall()
			useDate = result[0][5]
			returnedQuantity = 0
			i=0
			
			while(returnedQuantity < (quantity-currentQuantity)):

				if(quantity-returnedQuantity-currentQuantity < result[i][3]):

					query = "UPDATE consumptionTable SET quantity=quantity-"+str(quantity-returnedQuantity-currentQuantity)+" WHERE key="+str(result[i][0])+";"
					currentDatabaseCursor.execute(query)
					returnedQuantity = quantity-currentQuantity
					i+=1

				else:

					query = "UPDATE consumptionTable SET quantity=0 WHERE key="+str(result[i][0])+";"
					currentDatabaseCursor.execute(query)
					returnedQuantity += result[i][3]
					i+=1

		i=0
		decreasedQunatity = quantity
		query = "SELECT * FROM currentTable WHERE ID="+ID+" AND batch='"+batch+"' AND date='"+entryDate+"' ORDER BY key DESC;"
		currentDatabaseCursor.execute(query)
		result1 = currentDatabaseCursor.fetchall()

		while(decreasedQunatity > 0):
			if(decreasedQunatity < result1[i][3]):

				query = "UPDATE currentTable SET quantity=quantity-"+str(decreasedQunatity)+" WHERE key="+str(result1[i][0])+";" 
				currentDatabaseCursor.execute(query)
				query = "UPDATE receiveTable SET quantity=quantity-"+str(decreasedQunatity)+" WHERE key="+str(result1[i][0])+";"
				currentDatabaseCursor.execute(query)
				query = "UPDATE storeAccount SET PMJAKQuantity=PMJAKQuantity-"+str(decreasedQunatity)+" WHERE ID="+ID+";"
				currentDatabaseCursor.execute(query)
				decreasedQunatity = 0
				i+=1

			else:

				query = "UPDATE currentTable SET quantity=0 WHERE key="+str(result1[i][0])+";"
				currentDatabaseCursor.execute(query)
				query = "UPDATE receiveTable SET quantity=quantity-"+str(result1[i][3])+" WHERE key="+str(result1[i][0])+";"
				currentDatabaseCursor.execute(query)
				query = "UPDATE storeAccount SET PMJAKQuantity=PMJAKQuantity-"+str(result1[i][3])+" WHERE ID="+ID+";"
				currentDatabaseCursor.execute(query)
				decreasedQunatity = decreasedQunatity - result1[i][3]
				i += 1

		if(quantity > currentQuantity):

			currentDatabaseCursor.execute("SELECT * FROM currentTable WHERE ID="+ID+" AND quantity>0 ORDER BY date(expDate);")
			output = currentDatabaseCursor.fetchall()
			i = 0

			while(returnedQuantity > 0):
				if(returnedQuantity >= output[i][3]):
					currentDatabaseCursor.execute("INSERT INTO consumptionTable (ID, batch, quantity, expDate, date, type, useType, currentKey) VALUES ("+str(output[i][1])+",'"+output[i][2]+"',"+str(output[i][3])+",'"+output[i][4]+"','"+useDate+"','"+output[i][6]+"','consumption',"+str(output[i][0])+");")
					returnedQuantity = returnedQuantity - output[i][3]
					i=i+1
				
				else:
					query = "INSERT INTO consumptionTable (ID, batch, quantity, expDate, date, type, useType, currentKey) VALUES ("+str(output[i][1])+",'"+output[i][2]+"',"+str(returnedQuantity)+",'"+output[i][4]+"','"+useDate+"','"+output[i][6]+"','consumption',"+str(output[i][0])+");"
					currentDatabaseCursor.execute(query)
					returnedQuantity = 0
					break
		
		query = "INSERT INTO register (ID, date, info, use, remain) VALUES ("+ID+",'"+date+"','Mistake made in PMJAK on date:"+entryDate+"',"+str(quantity)+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()
		return True
	
	except:
		return False

def RFCMSDecreaseDB(name, quantity, entryDate, date, batch, currentQuantity):
	try:
		ID = IDGet(name)

		if(quantity > currentQuantity):
			query = "SELECT * FROM consumptionTable WHERE currentKey IN (SELECT key FROM currentTable WHERE ID="+ID+" AND date='"+entryDate+"' AND batch='"+batch+"') AND useType='consumption' ORDER BY key DESC;"
			currentDatabaseCursor.execute(query)
			result = currentDatabaseCursor.fetchall()
			useDate = result[0][5]
			returnedQuantity = 0
			i=0
			
			while(returnedQuantity < (quantity-currentQuantity)):

				if(quantity-returnedQuantity-currentQuantity < result[i][3]):

					query = "UPDATE consumptionTable SET quantity=quantity-"+str(quantity-returnedQuantity-currentQuantity)+" WHERE key="+str(result[i][0])+";"
					currentDatabaseCursor.execute(query)
					returnedQuantity = quantity-currentQuantity
					i+=1

				else:

					query = "UPDATE consumptionTable SET quantity=0 WHERE key="+str(result[i][0])+";"
					currentDatabaseCursor.execute(query)
					returnedQuantity += result[i][3]
					i+=1

		i=0
		decreasedQunatity = quantity
		query = "SELECT * FROM currentTable WHERE ID="+ID+" AND batch='"+batch+"' AND date='"+entryDate+"' ORDER BY key DESC;"
		currentDatabaseCursor.execute(query)
		result1 = currentDatabaseCursor.fetchall()

		while(decreasedQunatity > 0):
			if(decreasedQunatity < result1[i][3]):

				query = "UPDATE currentTable SET quantity=quantity-"+str(decreasedQunatity)+" WHERE key="+str(result1[i][0])+";" 
				currentDatabaseCursor.execute(query)
				query = "UPDATE receiveTable SET quantity=quantity-"+str(decreasedQunatity)+" WHERE key="+str(result1[i][0])+";"
				currentDatabaseCursor.execute(query)
				query = "UPDATE storeAccount SET RFCMSQuantity=RFCMSQuantity-"+str(decreasedQunatity)+" WHERE ID="+ID+";"
				currentDatabaseCursor.execute(query)
				decreasedQunatity = 0
				i+=1

			else:

				query = "UPDATE currentTable SET quantity=0 WHERE key="+str(result1[i][0])+";"
				currentDatabaseCursor.execute(query)
				query = "UPDATE receiveTable SET quantity=quantity-"+str(result1[i][3])+" WHERE key="+str(result1[i][0])+";"
				currentDatabaseCursor.execute(query)
				query = "UPDATE storeAccount SET RFCMSQuantity=RFCMSQuantity-"+str(result1[i][3])+" WHERE ID="+ID+";"
				currentDatabaseCursor.execute(query)
				decreasedQunatity = decreasedQunatity - result1[i][3]
				i += 1

		if(quantity > currentQuantity):

			currentDatabaseCursor.execute("SELECT * FROM currentTable WHERE ID="+ID+" AND quantity>0 ORDER BY date(expDate);")
			output = currentDatabaseCursor.fetchall()
			i = 0

			while(returnedQuantity > 0):
				if(returnedQuantity >= output[i][3]):
					currentDatabaseCursor.execute("INSERT INTO consumptionTable (ID, batch, quantity, expDate, date, type, useType, currentKey) VALUES ("+str(output[i][1])+",'"+output[i][2]+"',"+str(output[i][3])+",'"+output[i][4]+"','"+useDate+"','"+output[i][6]+"','consumption',"+str(output[i][0])+");")
					returnedQuantity = returnedQuantity - output[i][3]
					i=i+1
				
				else:
					query = "INSERT INTO consumptionTable (ID, batch, quantity, expDate, date, type, useType, currentKey) VALUES ("+str(output[i][1])+",'"+output[i][2]+"',"+str(returnedQuantity)+",'"+output[i][4]+"','"+useDate+"','"+output[i][6]+"','consumption',"+str(output[i][0])+");"
					currentDatabaseCursor.execute(query)
					returnedQuantity = 0
					break
		
		query = "INSERT INTO register (ID, date, info, use, remain) VALUES ("+ID+",'"+date+"','Mistake made in 	Receievd from CMS on date:"+entryDate+"',"+str(quantity)+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()
		return True
	
	except:
		return False

def OBDecreaseDB(name, quantity, entryDate, date, batch, currentQuantity):
	try:
		ID = IDGet(name)

		if(quantity > currentQuantity):
			query = "SELECT * FROM consumptionTable WHERE currentKey IN (SELECT key FROM currentTable WHERE ID="+ID+" AND date='"+entryDate+"' AND batch='"+batch+"') AND useType='consumption' ORDER BY key DESC;"
			currentDatabaseCursor.execute(query)
			result = currentDatabaseCursor.fetchall()
			useDate = result[0][5]
			returnedQuantity = 0
			i=0
			
			while(returnedQuantity < (quantity-currentQuantity)):

				if(quantity-returnedQuantity-currentQuantity < result[i][3]):

					query = "UPDATE consumptionTable SET quantity=quantity-"+str(quantity-returnedQuantity-currentQuantity)+" WHERE key="+str(result[i][0])+";"
					currentDatabaseCursor.execute(query)
					returnedQuantity = quantity-currentQuantity
					i+=1

				else:

					query = "UPDATE consumptionTable SET quantity=0 WHERE key="+str(result[i][0])+";"
					currentDatabaseCursor.execute(query)
					returnedQuantity += result[i][3]
					i+=1

		i=0
		decreasedQunatity = quantity
		query = "SELECT * FROM currentTable WHERE ID="+ID+" AND batch='"+batch+"' AND date='"+entryDate+"' ORDER BY key DESC;"
		currentDatabaseCursor.execute(query)
		result1 = currentDatabaseCursor.fetchall()

		while(decreasedQunatity > 0):
			if(decreasedQunatity < result1[i][3]):

				query = "UPDATE currentTable SET quantity=quantity-"+str(decreasedQunatity)+" WHERE key="+str(result1[i][0])+";" 
				currentDatabaseCursor.execute(query)
				query = "UPDATE receiveTable SET quantity=quantity-"+str(decreasedQunatity)+" WHERE key="+str(result1[i][0])+";"
				currentDatabaseCursor.execute(query)
				query = "UPDATE storeAccount SET OBQuantity=OBQuantity-"+str(decreasedQunatity)+" WHERE ID="+ID+";"
				currentDatabaseCursor.execute(query)
				decreasedQunatity = 0
				i+=1

			else:

				query = "UPDATE currentTable SET quantity=0 WHERE key="+str(result1[i][0])+";"
				currentDatabaseCursor.execute(query)
				query = "UPDATE receiveTable SET quantity=quantity-"+str(result1[i][3])+" WHERE key="+str(result1[i][0])+";"
				currentDatabaseCursor.execute(query)
				query = "UPDATE storeAccount SET OBQuantity=OBQuantity-"+str(result1[i][3])+" WHERE ID="+ID+";"
				currentDatabaseCursor.execute(query)
				decreasedQunatity = decreasedQunatity - result1[i][3]
				i += 1

		if(quantity > currentQuantity):

			currentDatabaseCursor.execute("SELECT * FROM currentTable WHERE ID="+ID+" AND quantity>0 ORDER BY date(expDate);")
			output = currentDatabaseCursor.fetchall()
			i = 0

			while(returnedQuantity > 0):
				if(returnedQuantity >= output[i][3]):
					currentDatabaseCursor.execute("INSERT INTO consumptionTable (ID, batch, quantity, expDate, date, type, useType, currentKey) VALUES ("+str(output[i][1])+",'"+output[i][2]+"',"+str(output[i][3])+",'"+output[i][4]+"','"+useDate+"','"+output[i][6]+"','consumption',"+str(output[i][0])+");")
					returnedQuantity = returnedQuantity - output[i][3]
					i=i+1
				
				else:
					query = "INSERT INTO consumptionTable (ID, batch, quantity, expDate, date, type, useType, currentKey) VALUES ("+str(output[i][1])+",'"+output[i][2]+"',"+str(returnedQuantity)+",'"+output[i][4]+"','"+useDate+"','"+output[i][6]+"','consumption',"+str(output[i][0])+");"
					currentDatabaseCursor.execute(query)
					returnedQuantity = 0
					break
		
		query = "INSERT INTO register (ID, date, info, use, remain) VALUES ("+ID+",'"+date+"','Mistake made in Opening Balance on date:"+entryDate+"',"+str(quantity)+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()
		return True
	
	except:
		return False
	
def RFCMSIncreaseDB(name, quantity, entryDate, date, batch):
	try:
		ID = IDGet(name)
		query = "UPDATE currentTable SET quantity=quantity+"+str(quantity)+" WHERE ID="+ID+" AND date='"+entryDate+"' AND batch='"+batch+"';"
		currentDatabaseCursor.execute(query)

		query = "UPDATE receiveTable SET quantity=quantity+"+str(quantity)+" WHERE ID="+ID+" AND date='"+entryDate+"' AND batch='"+batch+"';"
		currentDatabaseCursor.execute(query)

		query = "UPDATE storeAccount SET RFCMSQuantity=RFCMSQuantity+"+str(quantity)+", totalRecieveQuantity=totalRecieveQuantity+"+str(quantity)+", closingQuantity=closingQuantity+"+str(quantity)+" WHERE ID="+ID+";"
		currentDatabaseCursor.execute(query)

		query = "INSERT INTO register (ID, date, info, income, remain) VALUES ("+ID+",'"+date+"','Mistake made in Received from CMS on date:"+entryDate+"',"+str(quantity)+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()

		return True
	
	except:
		return False

def LPIncreaseDB(name, quantity, entryDate, date, batch):
	try:
		ID = IDGet(name)
		query = "UPDATE currentTable SET quantity=quantity+"+str(quantity)+" WHERE ID="+ID+" AND date='"+entryDate+"' AND batch='"+batch+"';"
		currentDatabaseCursor.execute(query)

		query = "UPDATE receiveTable SET quantity=quantity+"+str(quantity)+" WHERE ID="+ID+" AND date='"+entryDate+"' AND batch='"+batch+"';"
		currentDatabaseCursor.execute(query)

		query = "UPDATE storeAccount SET LPQuantity=LPQuantity+"+str(quantity)+", totalRecieveQuantity=totalRecieveQuantity+"+str(quantity)+", closingQuantity=closingQuantity+"+str(quantity)+" WHERE ID="+ID+";"
		currentDatabaseCursor.execute(query)

		query = "INSERT INTO register (ID, date, info, income, remain) VALUES ("+ID+",'"+date+"','Mistake made in Local Purchase on date:"+entryDate+"',"+str(quantity)+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()

		return True
	
	except:
		return False

def OBIncreaseDB(name, quantity, entryDate, date, batch):
	try:
		ID = IDGet(name)
		query = "UPDATE currentTable SET quantity=quantity+"+str(quantity)+" WHERE ID="+ID+" AND date='"+entryDate+"' AND batch='"+batch+"';"
		currentDatabaseCursor.execute(query)

		query = "UPDATE receiveTable SET quantity=quantity+"+str(quantity)+" WHERE ID="+ID+" AND date='"+entryDate+"' AND batch='"+batch+"';"
		currentDatabaseCursor.execute(query)

		query = "UPDATE storeAccount SET OBQuantity=OBQuantity+"+str(quantity)+", totalRecieveQuantity=totalRecieveQuantity+"+str(quantity)+", closingQuantity=closingQuantity+"+str(quantity)+" WHERE ID="+ID+";"
		currentDatabaseCursor.execute(query)

		query = "INSERT INTO register (ID, date, info, income, remain) VALUES ("+ID+",'"+date+"','Mistake made in Opening Balance on date:"+entryDate+"',"+str(quantity)+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()

		return True
	
	except:
		return False

def PMJAKIncreaseDB(name, quantity, entryDate, date, batch):
	try:
		ID = IDGet(name)
		query = "UPDATE currentTable SET quantity=quantity+"+str(quantity)+" WHERE ID="+ID+" AND date='"+entryDate+"' AND batch='"+batch+"';"
		currentDatabaseCursor.execute(query)

		query = "UPDATE receiveTable SET quantity=quantity+"+str(quantity)+" WHERE ID="+ID+" AND date='"+entryDate+"' AND batch='"+batch+"';"
		currentDatabaseCursor.execute(query)

		query = "UPDATE storeAccount SET PMJAKQuantity=PMJAKQuantity+"+str(quantity)+", totalRecieveQuantity=totalRecieveQuantity+"+str(quantity)+", closingQuantity=closingQuantity+"+str(quantity)+" WHERE ID="+ID+";"
		currentDatabaseCursor.execute(query)

		query = "INSERT INTO register (ID, date, info, income, remain) VALUES ("+ID+",'"+date+"','Mistake made in PMJAK on date:"+entryDate+"',"+str(quantity)+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()

		return True
	
	except:
		return False

def transferDecreaseDB(name, quantity, useDate, date):
	try:
		ID = IDGet(name)
		query = "SELECT * FROM consumptionTable WHERE date='"+useDate+"' AND ID="+ID+" AND useType='transfer' ORDER BY ID DESC;"
		currentDatabaseCursor.execute(query)
		data = currentDatabaseCursor.fetchall()
		totalQty = quantity
		i = 0

		while(quantity>0):

			if(quantity >= data[i][3]):
				query = "UPDATE consumptionTable SET quantity=0 WHERE key="+str(data[i][0])+";"
				currentDatabaseCursor.execute(query)
				quantity = quantity - data[i][3]
				i = i + 1

			else:
				query = "UPDATE consumptionTable SET quantity="+str(data[i][3]-quantity)+" WHERE key="+str(data[i][0])+";"
				currentDatabaseCursor.execute(query)
				quantity = 0
				break

		query = "INSERT INTO register (ID, date, info, income, remain) VALUES ("+ID+",'"+date+"','Mistake made in transfer to other disp. on date:"+useDate+"',"+str(totalQty)+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()
		return True
	
	except:
		return False

def transferIncreaseDB(name, quantity, useDate, date):
	try:
		totalQty = quantity		
		ID = IDGet(name)
		currentDatabaseCursor.execute("SELECT * FROM currentTable WHERE ID="+ID+" AND quantity>0 AND ORDER BY date(expDate);")
		output = currentDatabaseCursor.fetchall()
		i = 0

		while(quantity > 0):
			if(quantity >= output[i][3]):
				currentDatabaseCursor.execute("INSERT INTO consumptionTable (ID, batch, quantity, expDate, date, type, useType, currentKey) VALUES ("+str(output[i][1])+",'"+output[i][2]+"',"+str(output[i][3])+",'"+output[i][4]+"','"+useDate+"','"+output[i][6]+"','transfer',"+str(output[i][0])+");")
				quantity = quantity - output[i][3]
				i=i+1
			
			else:
				query = "INSERT INTO consumptionTable (ID, batch, quantity, expDate, date, type, useType, currentKey) VALUES ("+str(output[i][1])+",'"+output[i][2]+"',"+str(quantity)+",'"+output[i][4]+"','"+useDate+"','"+output[i][6]+"','transfer',"+str(output[i][0])+");"
				currentDatabaseCursor.execute(query)
				quantity = 0
				break

		query = "INSERT INTO register (ID, date, info, use, remain) VALUES ("+ID+",'"+date+"','Mistake made in transfer to other disp. on date:"+useDate+"',"+str(totalQty)+","+currentBalanceGet(name)+");"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()
		return True
	
	except:
		return False

def getKey(name, receiveDate, expDate, batch):
	
	ID = IDGet(name)
	query = "SELECT key FROM receiveTable WHERE ID="+ID+" AND date='"+receiveDate+"' AND expDate='"+expDate+"' AND batch='"+batch+"';"
	currentDatabaseCursor.execute(query)
	result = currentDatabaseCursor.fetchall()

	if(len(result) > 0):
		return str(result[0][0])

def otherChangesDB(name, oldExpDate, newExpDate, receiveDate, oldBatch, newBatch):
	try:
		key = getKey(name, receiveDate, oldExpDate, oldBatch)
		query = "UPDATE currentTable SET expDate='"+newExpDate+"', batch='"+newBatch+"' WHERE key="+key+";"
		currentDatabaseCursor.execute(query)
		query = "UPDATE receiveTable SET expDate='"+newExpDate+"', batch='"+newBatch+"' WHERE key="+key+";"
		currentDatabaseCursor.execute(query)
		query = "UPDATE consumptionTable SET expDate='"+newExpDate+"', batch='"+newBatch+"' WHERE currentKey="+key+";"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()
		return True
	
	except:
		return False

def deleteMedicineDB(name):
	try:
		ID = IDGet(name)

		query = "DELETE FROM mainTable WHERE ID="+ID+";"
		currentDatabaseCursor.execute(query)
		query = "DELETE FROM currentTable WHERE ID="+ID+";"
		currentDatabaseCursor.execute(query)
		query = "DELETE FROM receiveTable WHERE ID="+ID+";"
		currentDatabaseCursor.execute(query)
		query = "DELETE FROM consumptionTable WHERE ID="+ID+";"
		currentDatabaseCursor.execute(query)
		query = "DELETE FROM register WHERE ID="+ID+";"
		currentDatabaseCursor.execute(query)
		query = "DELETE FROM storeAccount WHERE ID="+ID+";"
		currentDatabaseCursor.execute(query)
		query = "DELETE FROM scheduleIndent WHERE ID="+ID+";"
		currentDatabaseCursor.execute(query)
		query = "DELETE FROM emergencyIndent WHERE ID="+ID+";"
		currentDatabaseCursor.execute(query)
		currentDatabase.commit()
		return True
	
	except:
		return False

def currentStockData(name):
	
	ID = IDGet(name)
	query = "SELECT date, batch, type, quantity, expDate FROM currentTable WHERE ID="+ID+" AND quantity>0;"
	currentDatabaseCursor.execute(query)
	result = currentDatabaseCursor.fetchall()
	return result

def usedStockData(name, startDate, endDate):

	ID = IDGet(name)
	query = "SELECT date, batch, useType, quantity, expDate FROM consumptionTable WHERE ID="+ID+" AND date(date)>=date('"+startDate+"') AND date(date)<=date('"+endDate+"') ORDER BY date(date);"
	print(query)
	currentDatabaseCursor.execute(query)
	result = currentDatabaseCursor.fetchall()
	return result

def getDisp():
	query = "SELECT hospitalName FROM AdminTable;"
	adminCursor.execute(query)
	try:
		result = (adminCursor.fetchall())[0][0]

	except:
		result = "NA"

	return result	