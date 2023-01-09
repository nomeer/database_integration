def redis_insert():
    import csv,os,shutil
    from datetime import datetime, timedelta
    import logging
    now = datetime.now()
    date_time = now.strftime("%Y%m%d")
    o = storage.Storage()
    form = SQLFORM.factory(
        Field('csv_file', 'upload' ,uploadfolder='/tmp'),
        )

    if form.process(keepvalues=True).accepted:

        # Check if the CSV file was uploaded using the HTTP request
        if form.vars.csv_file:
            # Get the file object, if the field contains a file
            if hasattr(form.vars.csv_file, 'file'):
                file_obj = form.vars.csv_file.file
            else:
                file_obj = form.vars.csv_file        
            #if os.path.exists(dest_file):
            # Open the file for reading
            with open('/tmp/' + file_obj, 'r') as file:
                    # Create a CSV reader
                csv_reader = csv.reader(file)
                    # Read the data into a list
                data = list(csv_reader)

            # Iterate through the data and add each row to the Redis set
            for row in data:
                row_str = str(row)
            # Convert the row to a string
                row_str = str(row)
                # Remove the square brackets and any whitespace characters from the beginning and end of the string
                clean_row_str = row_str.strip('[]')
                # Remove any remaining whitespace characters from the beginning and end of the string
                clean_row_str = clean_row_str.strip()
                # Remove the quotation marks from the string
                clean_row_str = clean_row_str.replace('"', '')
                # Add the clean row string to the Redis set
                rdb.sadd('csv_data', clean_row_str)

            return "CSV data successfully loaded into Redis!"
        else:
            return "No CSV file was uploaded."

    elif form.errors:
        response.flash = 'form has errors, please fix'
    return dict(form=form)
