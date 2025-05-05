import streamlit as st
import pandas as pd
from Rule_Based_Script__V3 import add_recommendations_to_pets, disease_product_mapping

# Load product data
df_products = pd.read_csv("encoded_all_products.csv")

# ------------------ Hardcoded Lists ------------------

dog_breeds = sorted([
    "Beagle", "Boxer", "Bulldog", "Dachshund", "German Shepherd",
    "Golden Retriever", "Labrador Retriever", "Poodle", "Shih Tzu", "Yorkshire Terrier",
	"Bullmastiff", "English spaniel", "Husky", "Doberman", "Beagle", "English bulldog",
	"Shiba Inu", "Australian shepherd", "Pinscher"
])

cat_breeds = sorted([
    "Domestic Shorthair", "American Shorthair", "Domestic Longhair", "Ragdoll",
    "Siamese", "Bengal", "Maine Coon", "British Shorthair", "Persian", "Russian Blue",
    "Sphynx", "Scottish Fold", "Exotic Shorthair", "Oriental Shorthair", "Burmese",
    "Devon Rex", "Himalayan", "Abyssinian", "Birman", "Norwegian Forest Cat"
])

health_conditions = sorted([
    "Addisons_disease", "Adrenal_disorders", "Aging", "Anxiety", "Arthritis", "Atopic_dermatitis",
    "Autoimmune Diseases", "Brachycephalic_syndrome", "Bladder_stones", "Cancer", "Canine_parvovirus",
    "Catabolic_states", "cachexia", "Chronic Infections", "Cognitive_dysfunction", "Congestive_heart_failure",
    "Constipation", "Cruciate_ligament_tear", "Cushings_syndrome", "Debilitation", "Dehydration", "Degenerative_myelopathy",
    "Dental_issue", "Diabetes", "Diarrhea", "Dilated cardiomyopathy", "Epilepsy", "Ear_infections",
    "Feline_asthma", "Feline_luts", "Flea_allergy_dermatitis", "Food_sensitivity", "Gallbladder_disease", "Gastroenteritis",
    "Gastrointestinal", "Hairballs", "Heart_murmur", "Hepatic_lipidosis", "Hepatitis", "Hepatopathy", "High_metabolic_needs",
    "Hip_dysplasia", "Hot_spots", "Hyperglycemia", "Hyperlipidemia", "Hyperthyroidism", "Hypertension (High Blood Pressure)",
    "Hypocalcemia", "Hypothyroidism", "Inflammatory_bowel_disease", "Inflammatory_mediators", "Intervertebral_disc_disease",
    "interstitial_cystitis", "Kidney_disease", "Lymphangiectasia", "Lymphoma", "Mast_cell_tumor", "Megaesophagus", "Mental_health_disorder",
    "Metabolic/Endocrine", "Mitral_valve_disease", "Obesity", "Osteoarthritis", "Osteosarcoma", "Otitis", "Oxalate_stones", "Pancreatitis",
    "Periodontal_disease", "portosystemic_shunt", "Protein_losing_enteropathy", "Proteinuria", "Renal/Urinary", "Ringworm", "Seizure",
    "Short_bowel_syndrome", "Skin_rash", "Struvite", "Surgery", "Urinary_problems", "Urinary_tract_infection", "Vestibular_disease",
    "Vision_problem", "Weak Immunity"
])

cat_specific_conditions = sorted([
    "Hairballs", "PLE", "Lymphangiectasia", "Feline_luts"
])

allergy_list = sorted([
    "unknown", "Barley", "Beef", "Carrot", "Chicken", "Corn", "Dairy", "Duck", "Egg", "Fish", "Flaxseed",
    "Lamb", "Oat", "Pea", "Pork", "Potato", "Pumpkin", "Rice", "Salmon", "Soy", "Sweet Potato",
    "Tomato", "Turkey", "Wheat", "Brown Rice", "Coconut", "Chickpea", "Fava Beans", "Quinoa", "Sorghum", "Tapioca",
    "Black Beans", "Broccoli", "Algae", "Millet", "Venison", "Kangaroo", "Duck Liver", "Liver",
    "Rabbit", "Spinach", "Milk"
])

activity_levels = ["Active", "Not Active"]
life_stages = ["Growth", "Adult", "Senior"]

# ------------------ Streamlit UI ------------------

st.set_page_config(page_title="Pet Nutrition Recommender", layout="centered")
st.title("🐾 Pet Food Recommendation Tool")

# Gender selector
has_gender = st.radio("Gender", options=["Male", "Female"], index=None)

# Species dropdown
species = st.selectbox("Species", ["-- Select species --", "Dog", "Cat"])

breed_list = []
breed_name = "-- Select a breed --"

if species == "Dog":
    breed_list = dog_breeds
elif species == "Cat":
    breed_list = cat_breeds

if breed_list:
    breed_name = st.selectbox("Breed Name", ["-- Select a breed --"] + breed_list)

# Allergy selector (updated to include Unknown)
has_allergy = st.radio("Allergies", options=["Yes", "No"], index=None)

selected_allergies = []
if has_allergy == "Yes":
    selected_allergies = st.multiselect("Allergies", allergy_list, placeholder="Choose an option")

# Conditional display for lactation and pregnancy
if has_gender == "Female":
    has_lactation = st.radio("Lactating", options=["Yes", "No"], index=None)
    has_pregnant = st.radio("Pregnant", options=["Yes", "No"], index=None)

# ------------------ Main Form ------------------

with st.form("pet_form"):
    breed_size = st.selectbox("Breed Size", ["-- Select breed size --", "Small", "Medium", "Large"])
    life_stage = st.selectbox("Life Stage", ["-- Select life stage --"] + life_stages)
    activity_level = st.selectbox("Activity Level", ["-- Select activity level --"] + activity_levels)

    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1, value=0.0)
    age = st.number_input("Age (months)", min_value=0, step=1, value=0)
    body_score = st.slider("Body Score (1-9)", min_value=1, max_value=9, step=1)

    # Main health issue: exactly 1
    main_health_condition = st.selectbox("Main Health Issue", ["-- Select main issue --"] + health_conditions)

    # Other issues: up to 2
    other_health_conditions = st.multiselect(
        "Other Health Issues (up to 2)", health_conditions,
        placeholder="Choose up to two issues",
        max_selections=2
    )

    # Cat-specific (optional)
    cat_specific_conditions_selected = []
    if species == "Cat":
        cat_specific_conditions_selected = st.multiselect(
            "Cat-Specific Conditions",
            cat_specific_conditions,
            placeholder="Choose an option"
        )

    submit = st.form_submit_button("Get Recommendations")

# ------------------ Output ------------------
if submit:
    errors = []

    if species == "-- Select species --":
        errors.append("Please select a species.")
    if breed_name == "-- Select a breed --":
        errors.append("Please select a breed.")
    if breed_size == "-- Select breed size --":
        errors.append("Please select a breed size.")
    if life_stage == "-- Select life stage --":
        errors.append("Please select a life stage.")
    if activity_level == "-- Select activity level --":
        errors.append("Please select an activity level.")
    if has_allergy is None:
        errors.append("Please select whether the pet has allergies.")
    if main_health_condition == "-- Select main issue --":
        errors.append("Please select a main health issue.")

    if errors:
        for err in errors:
            st.error(err)
    else:
        df_pet_info = pd.DataFrame([{
            "species": species,
            "life_stage": life_stage,
            "weight": weight,
            "age (months)": age,
            "activity level": activity_level,
            "main issue": main_health_condition,
            "other issues": other_health_conditions,
            "gender": has_gender,
            "breed": breed_name,
            "breed_size": breed_size,
            "body score (bds)": body_score,
            "pregnant": has_pregnant if has_gender == "Female" else "No",
            "lactating": has_lactation if has_gender == "Female" else "No",
            "allergy": has_allergy == "Yes",
            "allergic_to": selected_allergies
        }])

        results_df = add_recommendations_to_pets(df_pet_info, df_products, disease_product_mapping)

        st.markdown("🍽️ **Recommended Products:**")

        if not results_df.empty:
            for product in results_df["product_name"]:
                st.write(f"- {product}")
            st.success(f"{len(results_df)} products recommended.")
        else:
            st.warning("No suitable products found based on the provided details.")

    