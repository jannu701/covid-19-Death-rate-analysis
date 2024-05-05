import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import io
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import datetime
hospital_beds = pd.read_csv('data/HospitalBedsIndia.csv')
india_covid = pd.read_csv('data/india_cases.csv')
india_covid.to_csv('data/india_cases.csv',date_format='%Y-%m-%d')
india_covid_19=pd.read_csv('data/india_cases.csv')
#india_covid_19 = pd.read_csv('../input/statewisetestingdetailsindiacsv/covid_19_india.csv',sep=',')
individual_details = pd.read_csv('data/IndividualDetails.csv')
#ICMR_details = pd.read_csv('../input/covid19-in-india/ICMRTestingDetails.csv')
ICMR_labs = pd.read_csv('data/ICMRTestingLabs.csv')
state_testing = pd.read_csv('data/StatewiseTestingDetails.csv')
india_covid_19.tail()
india_covid_19.rename(columns={'State/UnionTerritory': 'State', 'Cured': 'Recovered'}, inplace=True)
unassigned=india_covid_19[india_covid_19['State']=='Unassigned'].index
india_covid_19.drop(unassigned,axis=0,inplace=True)
unassigned1=india_covid_19[india_covid_19['State']=='Nagaland#'].index
india_covid_19.drop(unassigned1,axis=0,inplace=True)
unassigned2=india_covid_19[india_covid_19['State']=='Jharkhand#'].index
india_covid_19.drop(unassigned2,axis=0,inplace=True)
unassigned3=india_covid_19[india_covid_19['State']=='Madhya Pradesh#'].index
india_covid_19.drop(unassigned3,axis=0,inplace=True)
unassigned4=india_covid_19[india_covid_19['State']=='Cases being reassigned to states'].index
india_covid_19.drop(unassigned4,axis=0,inplace=True)
unassigned5=india_covid_19[india_covid_19['State']=='Telengana***'].index
india_covid_19.drop(unassigned5,axis=0,inplace=True)
unassigned6=india_covid_19[india_covid_19['State']=='Telangana***'].index
india_covid_19.drop(unassigned6,axis=0,inplace=True)
unassigned7=india_covid_19[india_covid_19['State']=='Telangana'].index
india_covid_19.drop(unassigned7,axis=0,inplace=True)

statewise_cases = pd.DataFrame(india_covid_19.groupby('State')[['Confirmed', 'Deaths', 'Recovered']].max().reset_index())
statewise_cases["Country"] = "India"
fig = px.treemap(statewise_cases, path=['Country','State'], values='Confirmed',color='Confirmed', hover_data=['State'])
fig.show()
labels = ['Male', 'Female']
sizes = []
sizes.append(list(individual_details['gender'].value_counts())[0])
sizes.append(list(individual_details['gender'].value_counts())[1])
explode = (0.05, 0)
colors = ['#ffcc99','#66b3ff']
plt.figure(figsize= (8,8))
plt.pie(sizes, explode=explode, labels=labels,colors=colors, autopct='%1.1f',startangle=90)
plt.title('Percentage of Gender (Ignoring the Missing Values)',fontsize = 10)
plt.show ()
india_covid_19['Deaths']=india_covid_19['Deaths'].replace(['0#','NaN'],0)
india_covid_19['Deaths']=india_covid_19['Deaths'].astype('int')
state_details = pd.pivot_table(india_covid_19, values=['Confirmed','Deaths','Recovered'], index='State', aggfunc='max')
state_details['Recovery Rate'] = round(state_details['Recovered'] / state_details['Confirmed'],2)
state_details['Death Rate'] = round(state_details['Deaths'] /state_details['Confirmed'], 2)
state_details = state_details.sort_values(by='Confirmed', ascending= False)
state_details.style.background_gradient(cmap='Purples')
testing=state_testing.groupby('State')['TotalSamples'].max().sort_values(ascending=False).reset_index()
fig = px.bar(testing,
             x="TotalSamples",
             y="State",
             orientation='h',
             height=800,
             title='Statewise Testing',
            color='State')
fig.show()
state_testing = state_testing.fillna(0)
state_test_details = pd.pivot_table(state_testing, values=['TotalSamples', 'Positive'], index='State', aggfunc='max')
state_test_details['Positive Test Rate'] = round(state_test_details['Positive'] / state_test_details['TotalSamples'], 2)
# state_test_details['Negative Test Rate'] = round(state_test_details['Negative'] / state_test_details['TotalSamples'])
state_test_details = state_test_details.sort_values(by='TotalSamples', ascending= False)
state_test_details.style.background_gradient(cmap='Blues')
values = list(ICMR_labs['state'].value_counts())
states = list(ICMR_labs['state'].value_counts().index)
labs = pd.DataFrame(list(zip(values, states)),
               columns =['values', 'states'])
fig = px.bar(labs,
             x="values",
             y="states",
             orientation='h',
             height=1000,
             title='Statewise Labs',
            color='states')
fig.show()
hospital_beds_states =hospital_beds.drop([36])
cols_object = list(hospital_beds_states.columns[2:8])
for cols in cols_object:
    hospital_beds_states[cols] = hospital_beds_states[cols].astype(int,errors = 'ignore')
top_5_primary = hospital_beds_states.nlargest(5,'NumPrimaryHealthCenters_HMIS')
top_5_community = hospital_beds_states.nlargest(5,'NumCommunityHealthCenters_HMIS')
top_5_district_hospitals = hospital_beds_states.nlargest(5,'NumDistrictHospitals_HMIS')
top_5_public_facility = hospital_beds_states.nlargest(5,'TotalPublicHealthFacilities_HMIS')
top_5_public_beds = hospital_beds_states.nlargest(5,'NumPublicBeds_HMIS')
top_rural_hos = hospital_beds_states.nlargest(5,'NumRuralHospitals_NHP18')
top_rural_beds = hospital_beds_states.nlargest(5,'NumRuralBeds_NHP18')
top_urban_hos = hospital_beds_states.nlargest(5,'NumUrbanHospitals_NHP18')
top_urban_beds = hospital_beds_states.nlargest(5,'NumUrbanBeds_NHP18')

plt.figure(figsize=(30,30))
plt.suptitle('Health Facilities in Top 5 States',fontsize=30)
plt.subplot(231)
plt.title('Primary Health Centers',fontsize=25)
plt.barh(top_5_primary['State/UT'],top_5_primary['NumPrimaryHealthCenters_HMIS'],color ='blue');

plt.subplot(232)
plt.title('Community Health Centers',fontsize=25)
plt.barh(top_5_community['State/UT'],top_5_community['NumCommunityHealthCenters_HMIS'],color = 'blue');

plt.subplot(233)
plt.title('Public Health Facilities',fontsize=25)
plt.barh(top_5_public_facility['State/UT'],top_5_public_facility['TotalPublicHealthFacilities_HMIS'],color='blue');

plt.subplot(234)
plt.title('District Hospitals',fontsize=25)
plt.barh(top_5_district_hospitals['State/UT'],top_5_district_hospitals['NumDistrictHospitals_HMIS'],color = 'orange');

plt.subplot(235)
plt.title('Rural Hospitals',fontsize=25)
plt.barh(top_rural_hos['State/UT'],top_rural_hos['NumRuralHospitals_NHP18'],color = 'orange');
plt.subplot(236)
plt.title('Urban Hospitals',fontsize=25)
plt.barh(top_urban_hos['State/UT'],top_urban_hos['NumUrbanHospitals_NHP18'],color = 'orange');
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.figure(figsize=(27,15))
plt.suptitle('Number of Beds in Top 5 States',fontsize=30);
plt.subplot(131)
plt.title('Rural Beds',fontsize=25)
plt.barh(top_rural_beds['State/UT'],top_rural_beds['NumRuralBeds_NHP18'],color = 'orange');

plt.subplot(132)
plt.title('Urban Beds',fontsize=25)
plt.barh(top_urban_beds['State/UT'],top_urban_beds['NumUrbanBeds_NHP18'],color = 'blue');
plt.subplot(133)
plt.title('Public Beds',fontsize=25)
plt.barh(top_5_public_beds['State/UT'],top_5_public_beds['NumPublicBeds_HMIS'],color = 'purple');
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Load data into the DataFrame
india_state_cases = pd.read_csv("data/StatewiseTestingDetails.csv")

# Sample 10 random rows from the DataFrame
india_state_cases.sample(10)
india_state_cases.sample(10)
print(india_state_cases.columns)
