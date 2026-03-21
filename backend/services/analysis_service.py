"""
Analysis Service - WHO-standard rule-based health analysis engine.
"""
import json
from datetime import datetime, timedelta


class AnalysisService:

    SYMPTOM_RULES = {
        "hair fall": {"deficiencies": ["Iron", "Biotin", "Zinc"], "severity": "moderate"},
        "fatigue": {"deficiencies": ["Iron", "Vitamin B12", "Vitamin D"], "severity": "moderate"},
        "dandruff": {"deficiencies": ["Zinc", "Vitamin B6", "Selenium"], "severity": "mild"},
        "dry skin": {"deficiencies": ["Vitamin A", "Vitamin E", "Omega 3"], "severity": "mild"},
        "weak nails": {"deficiencies": ["Iron", "Biotin", "Calcium"], "severity": "mild"},
        "night blindness": {"deficiencies": ["Vitamin A"], "severity": "severe"},
        "bleeding gums": {"deficiencies": ["Vitamin C"], "severity": "moderate"},
        "skin irritation": {"deficiencies": ["Vitamin E", "Zinc"], "severity": "mild"},
        "digestion issues": {"deficiencies": ["Fiber", "Probiotics"], "severity": "moderate"},
        "bone pain": {"deficiencies": ["Vitamin D", "Calcium"], "severity": "severe"},
        "weakness": {"deficiencies": ["Iron", "Vitamin B12", "Magnesium"], "severity": "moderate"},
        "pale skin": {"deficiencies": ["Iron", "Vitamin B12"], "severity": "moderate"},
        "mouth ulcers": {"deficiencies": ["Vitamin B12", "Iron", "Folate"], "severity": "mild"},
        "muscle cramps": {"deficiencies": ["Magnesium", "Potassium"], "severity": "moderate"},
        "depression": {"deficiencies": ["Vitamin D", "Omega 3", "Vitamin B12"], "severity": "severe"},
        "poor concentration": {"deficiencies": ["Iron", "Omega 3"], "severity": "moderate"},
        "frequent infections": {"deficiencies": ["Vitamin C", "Zinc"], "severity": "moderate"},
        "slow wound healing": {"deficiencies": ["Vitamin C", "Zinc"], "severity": "moderate"},
        "brittle hair": {"deficiencies": ["Biotin", "Iron"], "severity": "mild"},
        "swollen joints": {"deficiencies": ["Omega 3", "Vitamin D"], "severity": "moderate"},
        "weight gain": {"deficiencies": ["Thyroid check", "Vitamin D"], "severity": "moderate"},
        "insomnia": {"deficiencies": ["Magnesium", "Vitamin B6"], "severity": "moderate"},
        "anxiety": {"deficiencies": ["Magnesium", "Vitamin B6", "Omega 3"], "severity": "moderate"},
        "acne": {"deficiencies": ["Zinc", "Vitamin A", "Omega 3"], "severity": "mild"},
        "back pain": {"deficiencies": ["Vitamin D", "Calcium", "Magnesium"], "severity": "moderate"},
    }

    COMBINED_RULES = [
        {"symptoms": ["fatigue", "pale skin", "hair fall"], "diagnosis": "Iron Deficiency Anemia", "severity": "severe", "see_doctor": True},
        {"symptoms": ["fatigue", "bone pain", "depression"], "diagnosis": "Severe Vitamin D Deficiency", "severity": "severe", "see_doctor": True},
        {"symptoms": ["hair fall", "weak nails", "pale skin"], "diagnosis": "Severe Iron Deficiency", "severity": "severe", "see_doctor": True},
        {"symptoms": ["dry skin", "dandruff", "hair fall"], "diagnosis": "Zinc and Biotin Deficiency", "severity": "moderate", "see_doctor": False},
        {"symptoms": ["muscle cramps", "insomnia", "anxiety"], "diagnosis": "Magnesium Deficiency", "severity": "moderate", "see_doctor": False},
        {"symptoms": ["depression", "fatigue", "poor concentration"], "diagnosis": "Vitamin B12 or D Deficiency", "severity": "moderate", "see_doctor": True},
        {"symptoms": ["bleeding gums", "frequent infections", "slow wound healing"], "diagnosis": "Severe Vitamin C Deficiency (Scurvy risk)", "severity": "severe", "see_doctor": True},
    ]

    FOOD_DB = {
        "Iron": {
            "veg": ["Spinach", "Lentils", "Kidney beans", "Tofu", "Pumpkin seeds", "Quinoa", "Dark chocolate", "Fortified cereals", "Chickpeas", "Soybeans"],
            "non-veg": ["Chicken liver", "Red meat", "Oysters", "Sardines", "Eggs", "Tuna", "Shrimp"],
            "vegan": ["Spinach", "Lentils", "Tofu", "Quinoa", "Pumpkin seeds"],
            "avoid": ["Tea with meals", "Coffee with meals"],
            "tips": "Eat with Vitamin C to improve absorption"
        },
        "Vitamin A": {
            "veg": ["Carrots", "Sweet potato", "Spinach", "Kale", "Mango", "Apricots", "Red pepper", "Butternut squash", "Broccoli"],
            "non-veg": ["Liver", "Eggs", "Dairy", "Salmon"],
            "vegan": ["Carrots", "Sweet potato", "Kale", "Mango", "Red pepper"],
            "avoid": ["Excessive alcohol"],
            "tips": "Eat with healthy fats for absorption"
        },
        "Vitamin C": {
            "veg": ["Oranges", "Lemon", "Kiwi", "Guava", "Strawberries", "Bell peppers", "Broccoli", "Papaya", "Pineapple"],
            "non-veg": ["Oranges", "Kiwi", "Guava", "Bell peppers", "Broccoli"],
            "vegan": ["Oranges", "Kiwi", "Bell peppers", "Broccoli", "Guava"],
            "avoid": ["Overcooking vegetables"],
            "tips": "Eat raw or lightly cooked"
        },
        "Vitamin D": {
            "veg": ["Fortified milk", "Mushrooms", "Fortified cereals", "Cheese", "Eggs"],
            "non-veg": ["Salmon", "Tuna", "Sardines", "Egg yolks", "Beef liver", "Mackerel"],
            "vegan": ["Fortified plant milk", "Mushrooms", "Fortified cereals"],
            "avoid": ["Staying indoors all day"],
            "tips": "Get 15-20 min morning sunlight daily"
        },
        "Vitamin B12": {
            "veg": ["Fortified plant milk", "Nutritional yeast", "Fortified cereals", "Dairy", "Eggs"],
            "non-veg": ["Beef", "Chicken", "Fish", "Eggs", "Dairy", "Clams"],
            "vegan": ["Fortified plant milk", "Nutritional yeast", "B12 supplements (essential)"],
            "avoid": [],
            "tips": "Vegans must supplement B12"
        },
        "Zinc": {
            "veg": ["Pumpkin seeds", "Chickpeas", "Lentils", "Cashews", "Hemp seeds", "Oats", "Quinoa", "Tofu"],
            "non-veg": ["Oysters", "Beef", "Chicken", "Crab", "Lobster", "Pork"],
            "vegan": ["Pumpkin seeds", "Hemp seeds", "Chickpeas", "Quinoa"],
            "avoid": ["Excessive calcium supplements"],
            "tips": "Soak legumes to improve absorption"
        },
        "Magnesium": {
            "veg": ["Dark chocolate", "Avocado", "Almonds", "Spinach", "Cashews", "Black beans", "Edamame", "Tofu", "Whole grains"],
            "non-veg": ["Fatty fish", "Chicken", "Beef"],
            "vegan": ["Dark chocolate", "Avocado", "Almonds", "Spinach", "Black beans"],
            "avoid": ["Excessive alcohol", "High sugar"],
            "tips": "Helps with sleep and muscle recovery"
        },
        "Calcium": {
            "veg": ["Milk", "Yogurt", "Cheese", "Tofu", "Almonds", "Broccoli", "Chia seeds", "Kale", "Fortified plant milk"],
            "non-veg": ["Sardines", "Salmon with bones", "Shrimp", "Dairy"],
            "vegan": ["Fortified plant milk", "Tofu", "Chia seeds", "Kale", "Broccoli"],
            "avoid": ["Excessive caffeine", "High sodium"],
            "tips": "Take with Vitamin D for absorption"
        },
        "Omega 3": {
            "veg": ["Flaxseeds", "Chia seeds", "Walnuts", "Hemp seeds", "Algae oil"],
            "non-veg": ["Salmon", "Sardines", "Mackerel", "Tuna", "Herring", "Eggs"],
            "vegan": ["Flaxseeds", "Chia seeds", "Walnuts", "Algae supplements"],
            "avoid": ["Excessive omega 6 oils"],
            "tips": "Essential for brain and heart health"
        },
        "Biotin": {
            "veg": ["Eggs", "Almonds", "Sweet potato", "Spinach", "Broccoli", "Avocado", "Banana"],
            "non-veg": ["Eggs", "Salmon", "Beef liver"],
            "vegan": ["Almonds", "Sweet potato", "Spinach", "Avocado", "Banana"],
            "avoid": ["Raw egg whites block biotin absorption"],
            "tips": "Biotin is destroyed by heat, eat some foods raw"
        },
        "Vitamin E": {
            "veg": ["Almonds", "Sunflower seeds", "Avocado", "Spinach", "Butternut squash", "Olive oil"],
            "non-veg": ["Eggs", "Shrimp"],
            "vegan": ["Almonds", "Sunflower seeds", "Avocado", "Spinach", "Olive oil"],
            "avoid": ["Processed foods with hydrogenated oils"],
            "tips": "Fat-soluble vitamin, eat with healthy fats"
        },
        "Vitamin B6": {
            "veg": ["Chickpeas", "Bananas", "Potatoes", "Fortified cereals", "Sunflower seeds"],
            "non-veg": ["Chicken", "Turkey", "Tuna", "Salmon"],
            "vegan": ["Chickpeas", "Bananas", "Potatoes", "Sunflower seeds"],
            "avoid": [],
            "tips": "Helps with mood regulation and sleep"
        },
        "Folate": {
            "veg": ["Spinach", "Lentils", "Black beans", "Asparagus", "Broccoli", "Avocado"],
            "non-veg": ["Liver", "Eggs"],
            "vegan": ["Spinach", "Lentils", "Black beans", "Asparagus", "Avocado"],
            "avoid": [],
            "tips": "Essential during pregnancy"
        },
        "Potassium": {
            "veg": ["Bananas", "Sweet potato", "Spinach", "Avocado", "Coconut water", "Beans"],
            "non-veg": ["Salmon", "Chicken"],
            "vegan": ["Bananas", "Sweet potato", "Spinach", "Avocado", "Coconut water"],
            "avoid": ["Excessive sodium"],
            "tips": "Important for heart and muscle function"
        },
        "Selenium": {
            "veg": ["Brazil nuts", "Whole wheat bread", "Sunflower seeds", "Mushrooms"],
            "non-veg": ["Tuna", "Shrimp", "Chicken", "Eggs"],
            "vegan": ["Brazil nuts", "Sunflower seeds", "Mushrooms"],
            "avoid": [],
            "tips": "Just 2 Brazil nuts daily covers your needs"
        },
    }

    def analyze_health(self, data):
        """Main analysis engine."""
        # --- Extract inputs ---
        height = float(data.get("height") or 0)
        weight = float(data.get("weight") or 0)
        age = int(data.get("age") or 0)
        gender = str(data.get("gender") or "male").lower()
        raw_symptoms = data.get("symptoms") or []
        symptoms = [str(s).lower().strip() for s in raw_symptoms if str(s).strip()]
        blood_pressure = str(data.get("blood_pressure") or "")
        blood_sugar = float(data.get("blood_sugar") or 0)
        hemoglobin = float(data.get("hemoglobin") or 0)
        food_pref = str(data.get("food_preference") or "veg").lower().replace("-", "").replace(" ", "")
        if "non" in food_pref:
            food_pref = "non-veg"
        elif "vegan" in food_pref:
            food_pref = "vegan"
        else:
            food_pref = "veg"
        goal = str(data.get("goal") or data.get("health_goals") or "general health").lower()
        activity = str(data.get("activity_level") or "moderate").lower()

        # --- 1. BMI ---
        height_m = height / 100 if height > 0 else 1
        bmi_val = weight / (height_m * height_m) if height_m > 0 and weight > 0 else 0
        bmi = round(bmi_val, 1)
        if bmi < 18.5:
            bmi_cat = "Underweight"
            bmi_adv = "Increase calorie intake with nutrient-dense foods like nuts, avocado, and whole grains."
        elif bmi <= 24.9:
            bmi_cat = "Normal weight"
            bmi_adv = "Maintain current diet and regular physical activity."
        elif bmi <= 29.9:
            bmi_cat = "Overweight"
            bmi_adv = "Reduce 300-500 calories daily and increase physical activity."
        else:
            bmi_cat = "Obese"
            bmi_adv = "Consult a doctor and nutritionist for a structured weight management plan."

        # --- 2. Doctor report ---
        bp_status = ""
        if blood_pressure and "/" in blood_pressure:
            try:
                parts = blood_pressure.split("/")
                sys_v = int(parts[0])
                dia_v = int(parts[1])
                if sys_v < 90 or dia_v < 60:
                    bp_status = "Low BP - increase salt and fluid intake"
                elif sys_v <= 120 and dia_v <= 80:
                    bp_status = "Normal - maintain lifestyle"
                elif sys_v <= 139 or dia_v <= 89:
                    bp_status = "Pre-hypertension - reduce salt, increase exercise"
                else:
                    bp_status = "High BP - see doctor immediately"
            except:
                bp_status = "Invalid reading"
        
        bs_status = ""
        if blood_sugar > 0:
            if blood_sugar < 70:
                bs_status = "Hypoglycemia - eat small frequent meals"
            elif blood_sugar <= 99:
                bs_status = "Normal - maintain diet"
            elif blood_sugar <= 125:
                bs_status = "Pre-diabetic - reduce sugar and refined carbs"
            else:
                bs_status = "Diabetic range - see doctor immediately"
        
        hgb_status = ""
        if hemoglobin > 0:
            if gender == "male" or gender == "m":
                if hemoglobin < 13.5:
                    hgb_status = "Anemia - increase Iron and B12 intake"
                elif hemoglobin <= 17.5:
                    hgb_status = "Normal"
                else:
                    hgb_status = "High - consult doctor"
            else:
                if hemoglobin < 12:
                    hgb_status = "Anemia - increase Iron and B12 intake"
                elif hemoglobin <= 15.5:
                    hgb_status = "Normal"
                else:
                    hgb_status = "High - consult doctor"

        # --- 3. Combined Rules ---
        symptom_set = set(symptoms)
        combined_diagnosis = None
        combined_see_doctor = False
        combined_urgency = "low"
        for rule in self.COMBINED_RULES:
            if all(s in symptom_set for s in rule["symptoms"]):
                combined_diagnosis = rule["diagnosis"]
                combined_see_doctor = rule["see_doctor"]
                combined_urgency = "high" if rule["severity"] == "severe" else "medium"
                break

        # --- 4. Individual symptom matching ---
        found = {}  # deficiency_name -> {name, severity, symptoms_matched, foods, avoid, tips}
        for s in symptoms:
            if s in self.SYMPTOM_RULES:
                rule = self.SYMPTOM_RULES[s]
                for d_name in rule["deficiencies"]:
                    if d_name not in found:
                        fd = self.FOOD_DB.get(d_name, {})
                        pref_key = food_pref if food_pref in fd else "veg"
                        found[d_name] = {
                            "name": d_name,
                            "severity": rule["severity"],
                            "symptoms_matched": [s],
                            "description": f"Potential {d_name} deficiency",
                            "foods": fd.get(pref_key, []),
                            "avoid": fd.get("avoid", []),
                            "tips": fd.get("tips", ""),
                        }
                    else:
                        if s not in found[d_name]["symptoms_matched"]:
                            found[d_name]["symptoms_matched"].append(s)
                        if rule["severity"] == "severe":
                            found[d_name]["severity"] = "severe"
                        elif rule["severity"] == "moderate" and found[d_name]["severity"] == "mild":
                            found[d_name]["severity"] = "moderate"

        deficiencies = list(found.values())

        # --- 5. Health score ---
        score = 100
        if bmi_cat != "Normal weight": score -= 15
        score -= len(deficiencies) * 4
        if combined_diagnosis: score -= 15
        if "High BP" in bp_status: score -= 15
        if "Diabetic" in bs_status: score -= 15
        if "Anemia" in hgb_status: score -= 10
        if bmi_cat == "Obese": score -= 10
        score = max(0, min(100, score))

        # --- 6. Urgency ---
        see_doctor = combined_see_doctor
        doctor_reason = ""
        urgency = combined_urgency
        if "High BP" in bp_status or "Diabetic" in bs_status:
            urgency = "high"
            see_doctor = True
            doctor_reason = "Critical vitals detected. Immediate medical attention recommended."
        elif combined_diagnosis and combined_see_doctor:
            doctor_reason = f"Symptoms strongly suggest {combined_diagnosis}."
        elif any(d["severity"] == "severe" for d in deficiencies):
            urgency = "high"
            see_doctor = True
            doctor_reason = "Severe deficiency detected."
        elif any(d["severity"] == "moderate" for d in deficiencies) or bmi_cat in ("Obese", "Underweight"):
            if urgency == "low":
                urgency = "medium"

        # --- 7. Collect foods ---
        all_foods = []
        all_avoid = []
        supplement_suggestions = []
        for d in deficiencies:
            all_foods.extend(d.get("foods", []))
            all_avoid.extend(d.get("avoid", []))
            if d["severity"] in ("severe", "moderate"):
                supplement_suggestions.append(f"{d['name']} supplement recommended")

        # --- 8. Lifestyle advice ---
        lifestyle = []
        lifestyle.append(f"BMI: {bmi} ({bmi_cat}) - {bmi_adv}")
        if bp_status:
            lifestyle.append(f"Blood Pressure: {bp_status}")
        if bs_status:
            lifestyle.append(f"Blood Sugar: {bs_status}")
        if hgb_status:
            lifestyle.append(f"Hemoglobin: {hgb_status}")
        lifestyle.append("Drink at least 8 glasses of water daily")
        lifestyle.append("Get 7-8 hours of quality sleep")
        lifestyle.append("Exercise at least 30 minutes daily")
        if "Vitamin D" in found:
            lifestyle.append("Get 15-20 minutes of morning sunlight daily")
        if any(k in found for k in ("Iron", "Vitamin B12")):
            lifestyle.append("Cook in cast iron. Eat Vitamin C with iron-rich foods.")
        if food_pref == "vegan" and "Vitamin B12" in found:
            lifestyle.append("IMPORTANT: Vegans must take B12 supplements")

        return {
            "bmi": float(bmi),
            "bmi_category": bmi_cat,
            "bmi_advice": bmi_adv,
            "deficiencies": deficiencies,
            "combined_diagnosis": combined_diagnosis,
            "health_condition": f"{bmi_cat} with {len(deficiencies)} potential deficiencies identified.",
            "health_score": int(score),
            "urgency_level": urgency,
            "see_doctor": see_doctor,
            "see_doctor_reason": doctor_reason,
            "doctor_report_analysis": {
                "blood_pressure_status": bp_status,
                "blood_sugar_status": bs_status,
                "hemoglobin_status": hgb_status,
            },
            "recommended_foods": list(set(all_foods)),
            "foods_to_avoid": list(set(all_avoid)),
            "lifestyle_advice": lifestyle,
            "supplement_suggestions": list(set(supplement_suggestions)),
        }
