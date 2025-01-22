### Intron Health Take Home Interview

Thank you for taking out time to work on this application. 

To get started, you should familiarize yourself with the structure of this application.

This is a Flask Application. Its HTML files live in the `app/templates` folder and its Javascript and CSS files should live 
in the `app/static` directory. This project uses the `Blueprint` structure provided natively by Flask. 

All Database Model Objects live in the `app/models.py` file. 

All migration files are in the `intron_health_migrations/versions` directory. `Alembic` is the tool used for database migrations. 

`instance/config.py` houses all configurations for this application.  

All required dependencies are in `requirements.txt` file. 

A virtual environment - `venv` - was created for this project as well for python-3.7.

Sqlite database [`instance/intron_db.db`]
 
#### Getting Started
Before you get started, you should execute these exports:
```
export FLASK_APP=application.py;
export APP_SETTINGS=instance.config.IntronConfig;
export FLASK_ENV=development;
```

#### Tips
To create a new versioned migration file, run:

```flask db migrate -m <name_of_file>```

To run an database upgrade operation, execute:

```flask db upgrade```

To run an database downgrade operation, execute:

```flask db downgrade```

To start the application, execute:

```flask run```

When you start the application, visit http://127.0.0.1:5000/home/all/users to ensure the application starts correctly. 

### Instructions

##### Problem (Submit Claim): 

Patients on a HMO plan do not need to pay cash when they go for health services. For example, when patients go to get lab services, they simply walk in, get the lab test done and leave with lab results.

A Laboratory Center typically needs to get reimbursed (paid) for services provided to patients. To get paid/reimbursed, the Lab typically needs to file a claim and send to the health insurance companies (HMOs). 

Claim filing process: At the end of each month, the claims officer collects all services provided to the patient over the course of a month, and enters them into a claim form. The completed claim displays each service provided along with the date, service provider (doctor), source hospital, patient information (name, age, gender), the problem for which the patient was seen (Diagnosis) and the cost of the lab test. The claim displays the aggregate (total) cost after all claims have been entered. This completed form is then sent to the HMO for reimbursement. 

A number of objects can be identified from the story above along with the interactions between them. You are required to extend/amend the current user class and create new classes/models as needed.

##### CREATE CLAIM

Create a simple CRUD feature where a claims officer can select a patient, fill out claims for a given month, and submit to the database. To keep things simple, you can consider implementing this as a form with 3 sections having the following fields:

1. Patient Data Section
- Patient Full Name (select): patient must already exist in the application/db
- Patient Age (int): Age must be an integer between 0 and 150.
- Patient Gender (radio): This should be a boolen field
- Diagnosis (string): Suspected Problem the doctor is trying to investigate
- Select HMO provider: Options are `HMO1`, `HMO2`, `HMO3`, and `HMO4`

(Hint: for extra points, it might be useful to auto-populate age and gender from the database to improve user experience)

2. Services Provided (user should be able to enter one or more of these). For example, if patient had 4 lab tests done in the course of a month, these fields will be repeated for each service. That is, 4 claim items will be added to the claim form.
- Service Date: Input must conform to DD-MM-YYY format.
- Service Name (string): Name of specific lab test
- Service Type (checkbox): Options are `Hematology`, `Microbiology`, `Chemical Pathology`, `Histopathology` and `Immunology`
- Provider Name (string): Full name of doctor who ordered the test
- Source (string): Name of Hospital where doctor works.
- Cost of Service

(Hint: For extra points, the form should support an unlimited number of services)

3. Total cost of all services
- Total cost: sum of all Cost of Service fields above
- Service charge/processing fee: 10% of total fee
- Final cost: Sum of Total cost and processing fee

(Hint: for extra points -- not required -- it might be useful to auto-sum all prices, update this sum as more services are added and display total cost to improve user experience).

Where field description or data type is not provided above, feel free to use your best guess.
		
##### READ CLAIM

Create a page that displays all claims (patient, HMO, total cost) along with their status: in progress, sent (completed), or paid. The Claim officer should be able to read (display) each claim.

##### OUT OF SCOPE
Do not bother about how the claim is sent to the HMO, how it is paid, or how the status changes from `in progress` to `completed`. Submitting the form successfuly with adequate validation is sufficient.
No need to build a separate feature for adding patients to the database. You might want to populate your patient table with 2 patients from the flask shell (or insert them directly in sqlite). Same applies to other objects.
Ability to edit/update and delete the claims are good but not required. 

#### EVALUATION CRITERIA

Your solution will be evaluated for:
1. Design/Architecture Quality
2. Code Quality
3. Input (Form) validation
4. User Experience (Frontend)
5. DB Migration
6. Tests

In addition, please, style pages with CSS and/or JavaScript; as you see fit to demonstrate front-end capabilities.
 
Again, thank you for considering joining our burgeoning team. 

