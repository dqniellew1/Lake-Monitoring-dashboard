

import requests
import json
import pandas as pd
def ml_model():
    st.markdown("""# Predictions 📈

    This portion of the app takes in a json file that have been preprocessed.
    The file is sent to a machine learning model.
    The model then returns the median sale value prediction of a property.
    """)
    st.subheader("Upload test data here either (JSON or CSV):")
    st.markdown('')
    uploaded_file = st.file_uploader("Choose a json file")
    

    # def check_format(filedata):
    #     try:
    #         json.loads(filedata)
    #         return 'JSON'
    #     except ValueError:
    #         return 'CSV'
    if uploaded_file is not None:
        test_data = pd.read_json(uploaded_file)
        test_data_dict = test_data.to_dict(orient='records')
        test_json = json.dumps(test_data_dict)


    if st.button('Run'):
        st.info('Prediction has started, with uploaded file.')
        my_bar = st.progress(0)
        for percent_complete in range(100):
            my_bar.progress(percent_complete + 1)
        url = 'https://guess-model.herokuapp.com/v1/predict/lakePrediction'

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        x = requests.post(url, data = test_json, headers = headers)
        Model_Info = pd.DataFrame.from_dict(x.json())
        st.write("The predictions from the test data gives us a median sale value of  $%s." % Model_Info['predictions'].values)