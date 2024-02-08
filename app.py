from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import secrets
import uuid, os
import operations


app = Flask(__name__)
app.secret_key = secrets.token_hex(16) 
app.config['SESSION_TYPE'] = 'filesystem'  # Use in-memory storage for session data

UPLOAD_FOLDER = 'temp'

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    print(request.method)
    if request.method == 'POST':
        print('POST START')
        selection_option = request.form.get('options')
        file = request.files['file-upload']
        
        if file:

            file_name = str(uuid.uuid4()) + '.xlsx'
            file_path = os.path.join(app.root_path, UPLOAD_FOLDER, file_name)
            file.save(file_path)
            session['uploaded-file'] = file_path
            session['option'] = selection_option
            print('READ FILE')
            return redirect(url_for('display_dataframe'))
        
    return render_template('upload.html')

@app.route('/display')
def display_dataframe():
    
    na_values = ['', 'NaN', 'NA', 'N/A']
    df = pd.read_excel(session.get('uploaded-file'), na_values=na_values)
    os.remove(session.get('uploaded-file'))
    selection_option = session['option']

    #Here we go into a switch that will select the correct script to use in the file
    #according to the type of file and option selected in the form
    result = operations.operationSelection(df, selection_option)

    tariffs_messages = zip(result['Tariffs-affected'], result['Printout'], result['Details'])

    

    if(selection_option == 'hts' and result != 'Not a valid HTS file'):
        return render_template('display.html', 
                                list_messages=tariffs_messages,
                                table=result['Final-df'].to_html())
    else:
        return render_template('nodata.html', message=result)
    
if __name__ == '__main__':
    app.run(debug=True)