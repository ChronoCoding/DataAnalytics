# %% [markdown]
# **- Imports**

# %%
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error
import pickle
import json


# %% [markdown]
# **1. LOAD DATASET**
# - Cleaning data yang value dalam columnnya kosong
# - Replace data kosong jadi NaN
# - Konversi kolom numerik ke tipe Float

# %%
data = pd.read_csv("/datasets/cardekho.csv")

data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)


data.replace("", np.nan, inplace=True)

numeric_columns = ['year', 'selling_price', 'km_driven', 'mileage(km/ltr/kg)', 'engine', 'seats']
for col in numeric_columns:
    data[col] = pd.to_numeric(data[col], errors='coerce')


# %% [markdown]
# **2. Preprocessing Data**
# - Preprocess data
# - Hapus barisan dengan nilai kosong setelah imputasi

# %%
numeric_features = ['mileage(km/ltr/kg)', 'engine', 'max_power', 'seats']
imputer = SimpleImputer(strategy='mean')
data[numeric_features] = imputer.fit_transform(data[numeric_features])
data['max_power'] = pd.to_numeric(data['max_power'], errors='coerce')

data = data.dropna() 

categorical_cols = ['fuel', 'seller_type', 'transmission', 'owner']
label_encoders = {col: LabelEncoder() for col in categorical_cols}
for col in categorical_cols:
    data[col] = label_encoders[col].fit_transform(data[col].astype(str))


# %% [markdown]
# **3. Split Data**

# %%
X = data[['year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner',
          'mileage(km/ltr/kg)', 'engine', 'max_power', 'seats']]
y = data['selling_price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# %% [markdown]
# **4. Train Models**
# - Mencari model terbaik dari antara 3:
#     - Linear Regression
#     - Random Forest 
#     - Gradient Boosting

# %%
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42)
}

results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    results[name] = mae

best_model_name = min(results, key=results.get)
best_model = models[best_model_name]

print(f"\nModel terbaik: {best_model_name} dengan MAE = {results[best_model_name]}")

# %% [markdown]
# **5. Save Model dan Preprocessing**

# %%
with open("models/label_encoders.pkl", "wb") as f:
    pickle.dump(label_encoders, f)

with open("models/imputer.pkl", "wb") as f:
    pickle.dump(imputer, f)

with open("models/best_model.pkl", "wb") as f:
    pickle.dump(best_model, f)


# %% [markdown]
# **6. Prediction Function**
# - Prediksi harga mobil berdasarkan input JSON, menggunakan model yg sudah disimpan & preprocessing steps
# - Parameters:
#     - Input data (dict): input data di JSON format untuk menyesuaikan struktur dataset
# - Conversi input data ke dataframe
# - Prediksi harga

# %%
def predict_car_price(input_data):
    with open("models/label_encoders.pkl", "rb") as f:
        label_encoders = pickle.load(f)

    with open("models/imputer.pkl", "rb") as f:
        imputer = pickle.load(f)

    with open("models/best_model.pkl", "rb") as f:
        best_model = pickle.load(f)


    input_df = pd.DataFrame([input_data])

    for col in categorical_cols:
        if col in input_df and input_df[col].iloc[0] in label_encoders[col].classes_:
            input_df[col] = label_encoders[col].transform(input_df[col].astype(str))
        else:
            input_df[col] = -1  

    input_df[numeric_features] = imputer.transform(input_df[numeric_features])

    # Prediksi harga
    predicted_price = best_model.predict(input_df)[0]
    return predicted_price


# %% [markdown]
# **7. Interactive Input Function**
# - Menerima input pengguna untuk fitur mobil, prediksi harga, dan display output
# - Encode categorical features
# - Prediksi harga

# %%
def get_user_input_and_predict():
    
    user_input = {
        'year': int(input("Enter the year of the car: ")),
        'km_driven': int(input("Enter the kilometers driven: ")),
        'fuel': input("Enter the fuel type (e.g., Petrol, Diesel): "),
        'seller_type': input("Enter the seller type (e.g., Individual, Dealer): "),
        'transmission': input("Enter the transmission type (e.g., Manual, Automatic): "),
        'owner': input("Enter the ownership status (e.g., First Owner, Second Owner): "),
        'mileage(km/ltr/kg)': float(input("Enter the mileage (e.g., 18.0): ")),
        'engine': float(input("Enter the engine capacity (e.g., 1200.0): ")),
        'max_power': float(input("Enter the max power (e.g., 85.0): ")),
        'seats': int(input("Enter the number of seats: "))
    }

    # Encode categorical features
    for col in categorical_cols:
        if col in user_input:
            user_input[col] = label_encoders[col].transform([str(user_input[col])])[0]

    # Predict price
    predicted_price = predict_car_price(user_input)
    print(f"\nPredicted Selling Price: {predicted_price}")


# %% [markdown]
# **8. Contoh Penggunaan Langsung**

# %%
# Contoh prediksi berdasarkan dataset
example_input = {
    'year': 2015,
    'km_driven': 50000,
    'fuel': 'Petrol',
    'seller_type': 'Individual',
    'transmission': 'Manual',
    'owner': 'First Owner',
    'mileage(km/ltr/kg)': 18.0,
    'engine': 1200.0,
    'max_power': 85.0,
    'seats': 5.0
}

for col in categorical_cols:
    if col in example_input:
        example_input[col] = label_encoders[col].transform([str(example_input[col])])[0]

predicted_price = predict_car_price(example_input)
print(f"\nPredicted Selling Price: {predicted_price}")


# %% [markdown]
# **# INPUT MANUAL DARI DATASET "cardekho.csv"**

# %%
# Contoh input manual dari dataset 
if __name__ == "__main__":
    get_user_input_and_predict()


