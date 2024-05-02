from sklearn.preprocessing import OneHotEncoder

# Load the OneHotEncoder if you've saved it along with the pipeline
# For example:
# enc = pickle.load(open('encoder.pkl','rb'))

st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams))

selected_city = st.selectbox('Select host city', sorted(cities))

target = st.number_input('Target')

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Score')
with col4:
    overs = st.number_input('Over completed')
with col5:
    wickets = st.number_input('Wickets out')

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets = 10 - wickets
    crr = score / overs
    rrr = (runs_left * 6) / balls_left

    # Preprocess categorical features
    batting_team_encoded = enc.transform([[batting_team]]).toarray()
    bowling_team_encoded = enc.transform([[bowling_team]]).toarray()
    selected_city_encoded = enc.transform([[selected_city]]).toarray()

    input_df = pd.DataFrame({
        'batting_team': batting_team_encoded,
        'bowling_team': bowling_team_encoded,
        'city': selected_city_encoded,
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets': [wickets],
        'total_runs_x': [target],
        'crr': [crr],
        'rrr': [rrr]
    })

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + "-" + str(round(win * 100)) + "%")
    st.header(bowling_team + "-" + str(round(loss * 100)) + "%")
