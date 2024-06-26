It is impossible to change a nullable field 'patientId' on appointment to non-nullable without providing a default. This is because the database needs something to populate existing rows.
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Ignore for now. Existing rows that contain NULL values will have to be handled manually, for example with a RunPython or RunSQL operation.
 3) Quit and manually define a default value in models.py.
Select an option: Please select a valid option: Please select a valid option: Please select a valid option: Please select a valid option: Please select a valid option: 