from typing import Union

import pandas as pd
from transformers import pipeline
from scipy.spatial import distance

# Initialize the LLM pipeline (run once to avoid reinitialization)
summarizer = pipeline("text2text-generation", model="t5-small")  # Replace with your chosen model

def process_user_inputs(form_data):
    """
    Processes user inputs and generates metrics using an LLM.
    """
    # Create a prompt based on form data
    llm_prompt = (
        f"Summarize the following user preferences into a list of metrics:\n\n"
        f"Price Range: {form_data['price_range']}\n"
        f"Charger Type: {form_data['charger_type']}\n"
        f"Color Preference: {form_data['color']}\n"
        f"Graphics Card Importance: {form_data['graphics_card']}\n"
        f"Battery Lifetime Importance: {form_data['battery_lifetime']}\n"
        f"Usage Description: {form_data['usage_description']}\n\n"
        f"Output metrics for: graphics card, weight, screen size, keyboard size, touchpad size, "
        f"camera quality, operating system flexibility, color, battery lifetime, battery consumption, "
        f"ports/docks, and charger type, each on a scale of 0-100."
    )

    # Use the LLM to generate metrics
    llm_output = summarizer(llm_prompt, max_length=200, truncation=True)[0]["generated_text"]

    return llm_output

def get_user_output(
        form_data
    ) -> pd.DataFrame:
    """
    Substitute method to get the user data. NOTE: This is to be replaced by an LLM.
    
    Returns
    -------
    pd.DataFrame:
        columns are the metrics, including 'id'= 'My_Laptop'
    """
    if form_data:
        user_laptop = {
            'id': 'My_Laptop',
            'Expensive': 50,
            'CPU usage': 70,
            'GPU': 100,
            'Storage space': 80,
            'RAM usage': 90,
            'Screen resolution': 90,
            'Weight': 60,
            'Battery Life': 70,
            'Camera Quality': 80,
            'Indestructibility': 100
        }
    # Convert user_laptop to a DataFrame
    user_laptop_df = pd.DataFrame([user_laptop])

    return user_laptop_df

def compute_closest_laptop(
        laptop_db: pd.DataFrame,
        user_laptop: pd.DataFrame
    ) -> Union[pd.DataFrame, str, pd.DataFrame]:
    """
    Takes laptop database and user data and finds the laptop from db that is closest in distance w.r.t. given metrics.
    """
    db_metrics = laptop_db.drop(columns=['id'])
    user_laptop_metrics = user_laptop.drop(columns=['id'])

    distances = db_metrics.apply(
        lambda row: distance.cityblock(row, user_laptop_metrics.iloc[0]),
        axis = 1
    )


    top_five = laptop_db.loc[distances.nsmallest(5).index]
    
    laptop_name = top_five.iloc[0]['id']
    
    closest_laptop = top_five.iloc[0]

    return closest_laptop, laptop_name, top_five