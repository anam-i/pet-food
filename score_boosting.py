import pandas as pd
import numpy as np
import logging

df_products = pd.read_csv('encoded_all_products.csv')

disease_product_mapping = {
    # ===== METABOLIC/ENDOCRINE =====
    "diabetes": {
        "for": ["for_diabetes"],
        "not_for": ["not_for_diabetes"],
        "category": ["category_low carb","category_high fiber"]
    },
    "hyperthyroidism": {
        "for": ["for_hyperthyroidism"],
        "not_for": ["not_for_hyperthyroidism"],
        "category": []

    },
    "hypothyroidism": {
        "for": ["for_metabolic support"],
        "not_for": ["not_for_fat intolerant"],
        "category": ["category_moderate calorie","category_moderate fat"]
    },
    "cushings_syndrome": {
        "for": ["for_metabolic support","for_weight management"],
        "not_for": ["not_for_hyperlipidemia"],
        "category": ["category_low fat","category_low calorie"]
    },
    "addisons_disease": {
        "for": ["for_metabolic support"],
        "not_for": ["not_for_sodium depletion states","not_for_adrenal disorders"],
        "category": ["category_moderate sodium","category_moderate fat"]
    },
    "hyperlipidemia": {
        "for": ["for_hyperlipidemia"],
        "not_for": ["not_for_hyperlipidemia","not_for_fat intolerant"],
        "category": ["category_low fat"]
    },
    "obesity": {
        "for": ["for_weight management"],
        "not_for": ["not_for_overweight"],
        "category": ["category_low calorie","category_low fat","category_high fiber"]
    },
    "underweight": {
        "for": ["for_appetite stimulation"],
        "not_for": ["not_for_underweight","not_for_catabolic states"],
        "category": ["category_high calorie","category_energy-dense","category_high protein"]
    },

    # ===== GASTROINTESTINAL =====
    "pancreatitis": {
        "for": ["for_pancreatitis"],
        "not_for": ["not_for_pancreatitis", "not_for_fat intolerant"],
        "category": ["category_low fat"]
    },
    "inflammatory_bowel_disease": {
        "for": ["for_gastrointestinal health","for_food sensitivity"],
        "not_for": [],
        "category": ["category_prebiotics"]
    },
    "gastroenteritis": {
        "for": ["for_gastroenteritis"],
        "not_for": ["not_for_dehydration"],
        "category": ["category_digestive care"]
    },
    "food_sensitivity": {
        "for": ["for_food sensitivity"],
        "not_for": [],
        "category": ["category_non-allergenic"]
    },
    "diarrhea": {
        "for": ["for_diarrhea"],
        "not_for": [],
        "category": ["category_high fiber","category_digestive care"]
    },
    "constipation": {
        "for": ["for_gastrointestinal health"],
        "not_for": [],
        "category": ["category_high fiber"]
    },
    "hairballs": {
        "for": ["for_hairballs"],
        "not_for": [],
        "category": ["category_high fiber","category_digestive care"]
    },
    "protein_losing_enteropathy": {
        "for": ["for_gastrointestinal health"],
        "not_for": ["not_for_fat intolerant"],
        "category": ["category_high protein"]
    },
    "megaesophagus": {
        "for": ["for_general health"],
        "not_for": [],
        "type": ["Type_Wet"],
        "category": ["category_energy-dense","category_energy-dense"]
    },
    "hepatic_lipidosis": {
        "for": ["for_liver health"],
        "not_for": ["not_for_liver failure"],
        "category": ["category_high protein","category_moderate fat","category_high calorie"]
    },
    "lymphangiectasia": {
        "for": ["for_lymphangiectasia"],
        "not_for": ["not_for_fat intolerant"],
        "category": ["category_low fat"]
    },
    "hepatitis": {
        "for": ["for_hepatitis","for_liver health"],
        "not_for": ["not_for_liver failure"],
        "category": ["category_moderate fat"]
},
    "hepatopathy": {
        "for": ["for_hepatitis","for_liver health"],
        "not_for": ["not_for_liver failure","not_for_catabolic states"],
        "category": ["category_low fat","category_digestive care"]
},
    # ===== RENAL/URINARY =====
    "kidney_disease": {
        "for": ["for_kidney health"],
        "not_for": ["not_for_kidney disease"],
        "category": ["category_low phosphorus","category_low sodium"]
    },
    "feline_luts": {
        "for": ["for_urinary health","for_feline luts"],
        "not_for": ["not_for_struvite"],
        "category": ["category_urinary care"]
    },
    "urinary_tract_infection": {
        "for": ["for_urinary health"],
        "not_for": ["not_for_urinary problems"],
        "type": ["Type_Wet"],
        "category": ["category_urinary care"]
    },
    "bladder_stones": {
        "for": ["for_urinary health"],
        "not_for": ["not_for_struvite"],
        "category": ["category_urinary care"]
    },
    "proteinuria": {
        "for": ["for_proteinuria"],
        "not_for": ["not_for_proteinuria"],
        "category": ["category_low protein","category_low phosphorus"]
    },
    "urinary_problems": {
        "for": ["for_urinary health"],
        "not_for": ["not_for_urinary problems"],
        "type": ["Type_Wet"],
        "category": []
    },
    "struvite": {
        "for": ["for_urinary health"],
        "not_for": ["not_for_struvite"],
        "type": ["Type_Wet"],
        "category": []
    },
    "oxalate_stones": {
        "for": ["for_urinary health"],
        "not_for": ["not_for_struvite","not_for_oxalate stones","Ingredients_spinach","Ingredients_quinoa","Ingredients_soy","Ingredients_beet"],
        "type": ["Type_Wet"],
        "category": ["category_low sodium"]
    },
    # ===== DERMATOLOGICAL =====
    "atopic_dermatitis": {
        "for": ["for_atopic dermatitis","for_skin health"],
        "not_for": [],
        "category": ["category_non-allergenic"]
    },
    "flea_allergy_dermatitis": {
        "for": ["for_skin health","for_healthy immune system"],
        "not_for": [],
        "category": ["category_non-allergenic"]
    },
    "skin_rash": {
        "for": ["for_skin health","for_healthy immune system"],
        "not_for": [],
        "category": ["category_non-allergenic"]
    },
    "hot_spots": {
        "for": ["for_skin health"],
        "not_for": [],
        "category": ["category_non-allergenic"]
    },
    "ear_infections": {
        "for": ["for_skin health","for_healthy immune system"],
        "not_for": [],
        "category": ["category_non-allergenic"]
    },
    "ringworm": {
        "for": ["for_skin health","for_healthy immune system"],
        "not_for": [],
        "category": ["category_non-allergenic"]
    },
    # ===== CARDIAC =====
    "heart_murmur": {
        "for": ["for_heart health"],
        "not_for": ["not_for_cardiac issues","not_for_heart failure"],
        "category": ["category_low sodium","category_high fiber"],
        "has": ["has_Total Omega-3Fatty Acids"]
    },
    "dilated cardiomyopathy": {
        "for": ["for_heart health","for_maintain muscle mass"],
        "not_for": ["not_for_cardiac issues","not_for_heart failure"],
        "category": ["category_low sodium","category_high energy"]
    },
    "hypertrophic_cardiomyopathy": {
        "for": ["for_heart health","for_weight management","for_hydration support"],
        "not_for": ["not_for_cardiac issues","not_for_heart failure"],
        "category": ["category_low sodium","category_high energy"]
    },
    "mitral_valve_disease": {
        "for": ["for_heart health"],
        "not_for": ["not_for_heart failure"],
        "category": ["category_low sodium"]
    },
    "congestive_heart_failure": {
        "for": ["for_heart health"],
        "not_for": ["not_for_heart failure"],
        "category": ["category_low sodium"]
    },
    "hypertension": {#(High Blood Pressure)
        "for": ["for_heart health"],
        "not_for": ["not_for_cardiac issues","not_for_heart failure"],
        "category": ["category_low sodium"]
    },
    # ===== CANCER =====
    "lymphoma": {
        "for": ["for_cancer","for_healthy immune system"],
        "not_for": ["not_for_cancer"],
        "category": ["category_high energy"]
    },
    "mast_cell_tumor": {
        "for": ["for_cancer"],
        "not_for": ["not_for_cancer"],
        "category": ["category_high protein"]
    },
    "osteosarcoma": {
        "for": ["for_cancer"],
        "not_for": ["not_for_cancer"],
        "category": ["category_high calorie"]
    },
    # ===== ORTHOPEDIC =====
    "osteoarthritis": {
        "for": ["for_bone and joint health"],
        "not_for": ["not_for_overweight"],
        "category": ["category_weight management"]
    },
    "hip_dysplasia": {
        "for": ["for_bone and joint health"],
        "not_for": ["not_for_overweight"],
        "category": ["category_weight management"]
    },
    "intervertebral_disc_disease": {
        "for": ["for_bone and joint health"],
        "not_for": ["not_for_overweight"],
        "category": ["category_weight management"]
    },
    "cruciate_ligament_tear": {
        "for": ["for_bone and joint health","for_weight management"],
        "not_for": ["not_for_overweight"],
        "category": ["category_high protein"]
    },
    "arthritis": {
        "for": ["for_bone and joint health"],
        "not_for": ["not_for_overweight"],
        "category": ["category_weight management"]
    },
    # ===== NEUROLOGICAL =====
    "epilepsy": {
        "for": ["for_brain health"],
        "not_for": [],
        "category": []
    },
    "cognitive_dysfunction": {
        "for": ["for_brain health"],
        "not_for": [],
        "category": []
    },
    "vestibular_disease": {
        "for": ["for_brain health"],
        "not_for": [],
        "category": []
    },
    "degenerative_myelopathy": {
        "for": ["for_brain health"],
        "not_for": [],
        "category": []
    },
    "mental_health_disorder": {
        "for": ["for_brain health"],
        "not_for": [],
        "category": ["category_omega3_support"]
    },
    # ===== SPECIES-SPECIFIC =====
    "feline_asthma": {
        "for": ["for_respiratory_support"],
        "not_for": [],
        "category": ["category_non-allergenic"]
    },
    "canine_parvovirus": {
        "for": ["for_urgent care"],
        "not_for": ["not_for_debilitation"],
        "category": ["category_recovery"]
    },
    "brachycephalic_syndrome": {
        "for": ["for_general health"],
        "not_for": [],
        "category": ["category_energy-dense"]
    },
    # ===== METABOLIC/ENDOCRINE (ADDITIONS) =====
    "adrenal_disorders": {
        "for": ["for_metabolic support"],
        "not_for": ["not_for_adrenal disorders","not_for_hypertension"],
        "category": []
    },
    "hyperglycemia": {
        "for": ["for_diabetes"],
        "not_for": ["not_for_diabetes"],
        "category": ["category_low carb"]
    },
    # ===== GASTROINTESTINAL (ADDITIONS) =====
    "dehydration": {
        "for": ["for_hydration support"],
        "not_for": ["not_for_dehydration"],
        "type": ["Type_Wet"],
        "category": ["category_low sodium"]
    },
    "gallbladder_disease": {
        "for": ["for_liver health","for_gall bladder diseases"],
        "not_for": ["not_for_fat intolerant"],
        "category": ["category_low fat"]
    },
    # ===== NEUROLOGICAL (ADDITIONS) =====
    "seizure": {
        "for": ["for_brain health"],
        "not_for": [],
        "category": ["category_controlled_mineral_levels"]
    },
    "anxiety": {
        "for": ["for_calming support","for_anxiety support"],
        "not_for": [],
        "category": ["category_omega3_support"]
    },
    "aging": {
        "for": ["for_aging care"],
        "not_for": [],
        "category": ["category_plant_based","category_natural nutrition","category_weight management"]
    },
    "surgery": {
        "for": ["for_recovery"],
        "not_for": [],
        "category": ["category_high protein"]
    },
    "vision_problem": {
        "for": ["for_vision health"],
        "not_for": [],
        "category": ["category_antioxidant_rich"]
    },
    "dental_issue": {
        "for": ["for_dental health"],
        "not_for": [],
        "category": []
    },
    "periodontal_disease": {
        "for": ["for_dental health"],
        "not_for": [],
        "category": []
    },
    "inflammatory_mediators": {
        "for": ["for_bone and joint health", "for_skin health"],
        "not_for": [],
        "category": []
    },
    "catabolic states": {
        "for": ["for_maintain muscle mass"],
        "not_for": [],
        "category": ["category_high protein","category_high calorie"]
    },
    "debilitation": {  # (e.g., post-illness weakness)
        "for": ["for_recovery"],
        "not_for": ["not_for_debilitation"],
        "category": ["category_high calorie"]
    },
    "autoimmune diseases": {
        "for":["for_healthy immune system","for_gastrointestinal health"],
         "not_for": [],
        "category": ["category_non-allergenic"]
    },
    "chronic infections": {
        "for":["for_healthy immune system","for_gastrointestinal health"],
         "not_for": [],
        "category": []
    },
    "weak immunity": {
       "for":["for_healthy immune system"],
        "not_for": [],
        "category": ["category_high protein"]
    },
    "cachexia": {
        "for": ["for_maintain muscle mass"],
        "not_for": ["not_for_fat intolerant"],
        "category": ["category_high protein","category_high calorie"]
    },
    "otitis": {
        "for": ["for_skin health","for_food sensitivity","for_healthy immune system","for_inflammatory mediators"],
        "not_for": [],
        "category": ["category_non-allergenic"]
    },
    "portosystemic_shunt": {
        "for": ["for_liver_health","for_metabolic support","for_general health"],
        "not_for": ["not_for_liver failure"],
        "category": ["category_digestive care","category_natural nutrition","category_plant_based"]
},
    "hypocalcemia": {
        "for": ["for_bone and joint health","for_general health","for_healthy immune system","for_recovery support"],
        "not_for": ["not_for_kidney disease"],
        "category": ["category_multifunction","category_high energy"]
},
    "hypertrophic_osteodystrophy": {
        "for": ["for_bone and joint health","for_general health"],
        "not_for": [],
        "category": ["category_multifunction","category_moderate calorie","category_moderate fat","category_digestive care"]
},
    "short_bowel_syndrome": {
        "for": ["for_gastrointestinal health","for_hydration support","for_diarrhea"],
        "not_for": ["not_for_fat intolerant","not_for_liver failure","not_for_dehydration","category_high fiber"],
        "type": ["Type_Wet"],
        "category": [ "category_digestive care","category_energy-dense","category_high calorie"],
        "has": ["has_Magnesium"]
    },
    "interstitial_cystitis": {
        "for": ["for_urinary_health","for_feline luts","for_calming support"],
        "not_for": ["not_for_oxalate stones","not_for_struvite","not_for_truvite urolithiasis"],
        "category": []
},
    "high_metabolic_needs": {
        "for": ["for_maintain muscle mass"],
        "not_for": ["not_for_overweight"],
        "category": ["category_energy-dense","category_high energy", "category_high protein"]
}
    }
	
	
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Utility Functions ---
def add_score(score_dict, product_ids, points):
    for pid in product_ids:
        score_dict[pid] = score_dict.get(pid, 0) + points

def filter_by_condition(df, column, value):
    """Return product IDs matching condition, or empty if column doesn't exist or is invalid."""
    if column in df.columns and df[column].any():
        return df[df[column] == value]['Product_id'].tolist()
    return []

# --- Filtering Functions (return IDs) ---
def score_disease_tags(df, disease_info, weight_map):
    scored = {}
    for tag_type, weight in weight_map.items():
        for tag in disease_info.get(tag_type, []):
            ids = filter_by_condition(df, tag, 1)
            add_score(scored, ids, weight)
    return scored

def score_life_stage(df, life_stage):
    scored = {}
    if life_stage in ['growth', 'adult', 'senior']:
        filter_expr = (
            (df[f'life_stage_{life_stage}'] == 1) |
            (df['life_stage_all'] == 1) |
            ((life_stage == 'senior') & (len(df) < 10) & (df['life_stage_adult'] == 1))
        )
        ids = df[filter_expr]['Product_id'].tolist()
        add_score(scored, ids, 5)
    return scored

# --- Allergy Filter (exclusion/hard filter) ---
def exclude_allergies(df, df_pet_info):
    if df_pet_info['allergy'] == 1:
        for ingredient in df_pet_info['allergic_to']:
            if ingredient == 'unknown':
                df = df[df['category_non-allergenic'] == 1]
            else:
                col = f'Ingredients_{ingredient}'
                if col in df.columns:
                    df = df[df[col] == 0]
    return df


# --- Hard filter for Pregnancy / Lactating ---
def exclude_pregnancy(df, df_pet_info):
    if df_pet_info['pregnant']:
        if 'not_for_pregnancy' in df.columns:
            df = df[df['not_for_pregnancy'] == 0]
    if df_pet_info['lactating']:
        if 'not_for_lactation' in df.columns:
            df = df[df['not_for_lactation'] == 0]
    return df

# --- Main Scoring Function ---
def score_products(df_pet_info, df_products):
    df = df_products.copy()
    df = exclude_allergies(df, df_pet_info)
    df = exclude_pregnancy(df, df_pet_info) #when using pregnancy hard filter
    scores = {}

    # Score by species
    species_col = f"Species_{df_pet_info['species']}"
    species_ids = filter_by_condition(df, species_col, 1)
    add_score(scores, species_ids, 100)

    # Main issue
    issue = df_pet_info['main_issue']
    if issue in disease_product_mapping:
        logger.info(f"Scoring for main issue: {issue}")
        #weights = {'for': 20, 'not_for': -50, 'type': 10, 'category': 5, 'has': 5}
        weights = {'for': 100, 'not_for': -100, 'type': 10, 'category': 20, 'has': 20}
        issue_scores = score_disease_tags(df, disease_product_mapping[issue], weights)
        for k, v in issue_scores.items():
            scores[k] = scores.get(k, 0) + v

    # Other issues
    for issue in df_pet_info['other_issues_list']:
        if issue in disease_product_mapping:
            #other_scores = score_disease_tags(df, disease_product_mapping[issue], {'for': 5, 'category': 2})
            other_scores = score_disease_tags(df, disease_product_mapping[issue], {'for': 50, 'category': 20, 'not_for': -100, 'type': 10, 'has': 5})
            for k, v in other_scores.items():
                scores[k] = scores.get(k, 0) + v

    # Body Score
    bds = df_pet_info['body score (bds)']
    if bds >= 7:
        add_score(scores, filter_by_condition(df, 'for_weight management', 1), 2)
        add_score(scores, filter_by_condition(df, 'category_low calorie', 1), 2)
    elif bds <= 3:
        add_score(scores, filter_by_condition(df, 'for_appetite stimulation', 1), 2)
        add_score(scores, filter_by_condition(df, 'category_high calorie', 1), 2)
        add_score(scores, filter_by_condition(df, 'category_high protein', 1), 2)

    # Life Stage
    life_stage = 'growth' if df_pet_info['pregnant'] or df_pet_info['lactating'] else df_pet_info['life_stage']
    life_stage_scores = score_life_stage(df, life_stage)
    for k, v in life_stage_scores.items():
        scores[k] = scores.get(k, 0) + v

    # Breed Size
    size_ids = filter_by_condition(df, f'breed_size_{df_pet_info["breed_size"]}', 1) 
    add_score(scores, size_ids, 2)

    # Activity Level
    if df_pet_info['activity level'] == 'active':
        add_score(scores, filter_by_condition(df, 'category_high calorie', 1), 2)
        add_score(scores, filter_by_condition(df, 'category_energy-dense', 1), 2)

    # Final score sort
    scored_df = pd.DataFrame({'Product_id': list(scores.keys()), 'Score': list(scores.values())})
    top_products = scored_df.sort_values(by='Score', ascending=False).head(20) #Display top 20 products
    return top_products['Product_id'].tolist(), top_products['Score'].tolist()
