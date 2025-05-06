import streamlit as st
import pandas as pd
from rule_based_script__v3 import disease_product_mapping, filter_products, filter_by_condition, filter_for_tags, filter_not_for_tags, filter_type_tags, filter_category_tags, filter_has_tags, filter_life_stage

# Load product data
df_products = pd.read_csv("encoded_all_products.csv")
df_productdata = pd.read_csv("Products_final_cleaned.csv")

# ------------------ Hardcoded Lists ------------------

dog_breeds = sorted([
    "Beagle", "Boxer", "Bulldog", "Dachshund", "German Shepherd",
    "Golden Retriever", "Labrador Retriever", "Poodle", "Shih Tzu", "Yorkshire Terrier",
	"Bullmastiff", "English spaniel", "Husky", "Doberman", "English bulldog",
	"Shiba Inu", "Australian shepherd", "Pinscher"
])

cat_breeds = sorted([
    "Domestic Shorthair", "American Shorthair", "Domestic Longhair", "Ragdoll",
    "Siamese", "Bengal", "Maine Coon", "British Shorthair", "Persian", "Russian Blue",
    "Sphynx", "Scottish Fold", "Exotic Shorthair", "Oriental Shorthair", "Burmese",
    "Devon Rex", "Himalayan", "Abyssinian", "Birman", "Norwegian Forest Cat"
])

health_conditions = sorted([
	"addisons_disease", "adrenal_disorders", "aging", "anxiety", "arthritis", "atopic_dermatitis",
	"autoimmune diseases", "brachycephalic_syndrome", "bladder_stones", "cancer", "canine_parvovirus",
	"catabolic states", "cachexia", "chronic infections", "cognitive_dysfunction", "congestive_heart_failure",
	"constipation", "cruciate_ligament_tear", "cushings_syndrome", "debilitation", "dehydration", "degenerative_myelopathy",
	"dental_issue", "diabetes", "diarrhea", "dilated_cardiomyopathy", "epilepsy", "ear_infections",
	"feline_asthma", "feline_luts", "flea_allergy_dermatitis", "food_sensitivity", "gallbladder_disease", "gastroenteritis",
	"hairballs", "heart_murmur", "hepatic_lipidosis", "hepatitis", "hepatopathy", "high_metabolic_needs",
	"hip_dysplasia", "hot_spots", "hyperglycemia", "hyperlipidemia", "hyperthyroidism", "hypertension",
	"hypocalcemia", "hypothyroidism", "inflammatory_bowel_disease", "inflammatory_mediators", "intervertebral_disc_disease",
	"interstitial_cystitis", "kidney_disease", "lymphangiectasia", "lymphoma", "mast_cell_tumor", "megaesophagus", "mental_health_disorder",
	"metabolic/endocrine", "mitral_valve_disease", "obesity", "osteoarthritis", "osteosarcoma", "otitis", "oxalate_stones", "pancreatitis",
	"periodontal_disease", "portosystemic_shunt", "protein_losing_enteropathy", "proteinuria", "ringworm", "seizure",
	"short_bowel_syndrome", "skin_rash", "struvite", "surgery", "urinary_problems", "urinary_tract_infection", "vestibular_disease",
	"vision_problem", "weak immunity", "underweight", "hypertrophic_cardiomyopathy", "hypertrophic_osteodystrophy"
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
st.title("🐾🐶Pet Food Recommendation Tool Rule-Based Recommendations🐱🐾")

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
    has_lactation = st.radio("Lactating", options=["TRUE", "FALSE"], index=None, format_func=lambda x: "TRUE" if x else "FALSE")
    has_pregnant = st.radio("Pregnant", options=["TRUE", "FALSE"], index=None, format_func=lambda x: "TRUE" if x else "FALSE")

with st.form("pet_form"):
    breed_size = st.selectbox("Breed Size", ["-- Select breed size --", "Small", "Medium", "Large"])
    life_stage = st.selectbox("Life Stage", ["-- Select life stage --"] + life_stages)
    activity_level = st.selectbox("Activity Level", ["-- Select activity level --"] + activity_levels)

    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1, value=0.0)
    age = st.number_input("Age (months)", min_value=0, step=1, value=0)
    body_score = st.slider("Body Score (1-9)", min_value=1, max_value=9, step=1)

    # Main health issue: exactly 1
    main_issue = st.selectbox("Main Health Issue", ["-- Select main issue --"] + health_conditions)

    # Other issues: up to 2
    other_issues = st.multiselect(
        "Other Health Issues (up to 2)", health_conditions,
        placeholder="Choose up to two issues",
        max_selections=3
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
    if main_issue == "-- Select main issue --":
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
            "main_issue": main_issue,
            "other_issues": other_issues,
            "gender": has_gender,
            "breed": breed_name,
            "breed_size": breed_size,
            "body score (bds)": body_score,
            "pregnant": has_pregnant if has_gender == "Female" else "FALSE",
            "lactating": has_lactation if has_gender == "Female" else "FALSE",
            "allergy": has_allergy == "Yes",
            "allergic_to": selected_allergies
        }])
    product_ids, count = filter_products(df_pet_info, df_products)


    # Filter rows from the CSV where Product_id matches
recommended_products = df_productdata[df_productdata['Product_ID'].isin(product_ids)]
    # Display the filtered products
# st.write(f"Recommended Products: {product_ids}")
	# Display the product names in Streamlit
st.write("### Recommended Products:")
for _, row in recommended_products.iterrows():
	st.write(f"- {row['Product_Name']} (ID: {row['Product_ID']})")


