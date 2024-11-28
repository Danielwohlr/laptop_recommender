from transformers import pipeline

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
