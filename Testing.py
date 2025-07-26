import json
import random
from datetime import datetime, timedelta

def generate_random_data_and_save():
    """Generates a comprehensive JSON dataset for the DFLT Phase 2 dashboards and saves it to a file."""

    # --- Configuration and Constants ---
    NUM_TRAININGS = 5000  # Total number of training sessions to simulate
    NUM_BENEFICIARIES_PER_TRAINING = 30 # Cohort size
    NUM_ICS = 20
    NUM_TRAINERS = 100
    NUM_QA_OBSERVATIONS = 500 # Number of direct QA observations
    NUM_RECORDING_REVIEWS = 800 # Number of recording reviews

    START_DATE = datetime(2024, 11, 1) # Start date for data generation
    END_DATE = datetime(2025, 7, 26) # End date for data generation

    PROVINCES = ["Punjab", "Sindh", "Khyber Pakhtunkhwa", "Balochistan", "Azad Jammu & Kashmir", "Gilgit-Baltistan", "Islamabad Capital Territory"]
    DISTRICTS_BY_PROVINCE = {
        "Punjab": ["Lahore", "Rawalpindi", "Faisalabad", "Multan", "Sialkot", "Gujranwala", "Bahawalpur", "Sargodha", "Gujrat", "Rahim Yar Khan"],
        "Sindh": ["Karachi", "Hyderabad", "Sukkur", "Larkana", "Mirpur Khas", "Nawabshah", "Jacobabad", "Shikarpur", "Thatta"],
        "Khyber Pakhtunkhwa": ["Peshawar", "Swat", "Mardan", "Abbottabad", "Kohat", "Bannu", "D.I. Khan", "Mansehra", "Haripur"],
        "Balochistan": ["Quetta", "Khuzdar", "Gwadar", "Dera Bugti", "Sibi", "Turbat", "Loralai", "Chaman", "Zhob"],
        "Azad Jammu & Kashmir": ["Muzaffarabad", "Mirpur", "Kotli", "Bhimber", "Neelum Valley", "Rawalakot"],
        "Gilgit-Baltistan": ["Gilgit", "Skardu", "Ghanche", "Diamer", "Astore", "Hunza"],
        "Islamabad Capital Territory": ["Islamabad"]
    }
    TRAINER_NAMES = [f"Trainer {i:03d}" for i in range(1, NUM_TRAINERS + 1)]
    IC_NAMES = [f"IC-{i:03d}" for i in range(1, NUM_ICS + 1)]
    QA_NAMES = [f"QA-{i:03d}" for i in range(1, 15)]
    REVIEWER_NAMES = [f"Reviewer-{i:03d}" for i in range(1, 10)]

    TRAINING_LANGUAGES = ["Urdu", "English", "Punjabi", "Sindhi", "Pashto"]
    OCCUPATIONS = ["Farmer", "Daily Wage Laborer", "Housewife", "Small Business Owner", "Student", "Other"]
    LOAN_SOURCES = ["Microfinance Bank", "Commercial Bank", "Family/Friends", "Local Money Lender", "Shopkeeper", "Other"]
    CLIMATE_CHANGE_BELIEF = ["Strongly Agree", "Agree", "Neutral", "Disagree", "Strongly Disagree"]
    EDUCATION_LEVELS = ["No formal Education", "Primary", "Middle", "Matric", "FA", "FSc", "Bachelor's", "Above Bachelor's"]
    TRAINING_TOPICS = [f"Section {i}" for i in range(1, 11)] # Simplified for mock data
    IC_MONITORING_MODES = ["In-person", "Phone Call", "Video Call"]
    FEEDBACK_CATEGORIES = ["Positive", "Constructive", "Urgent Issue", "Logistics Query"]
    BOTTLENECK_REASONS = ["Lack of Venue Availability", "Trainer Absences", "Material Shortages", "Low Beneficiary Mobilization", "Technical Issues", "Slow Reporting"]
    DUTY_STATIONS = ["Karachi Hub", "Lahore HQ", "Peshawar Centre", "Quetta Branch", "Multan Field", "Hyderabad Support", "Islamabad Office", "Faisalabad Node", "Sialkot Operations", "Gwadar Port"]

    # Global Targets (for Status Deck)
    GLOBAL_BENEFICIARY_TARGET = 500000
    GLOBAL_TRAINING_TARGET = 15000
    PROVINCIAL_TARGETS = {
        "Punjab": {"beneficiaries": 200000, "trainings": 6000},
        "Sindh": {"beneficiaries": 120000, "trainings": 3500},
        "Khyber Pakhtunkhwa": {"beneficiaries": 80000, "trainings": 2500},
        "Balochistan": {"beneficiaries": 40000, "trainings": 1200},
        "Azad Jammu & Kashmir": {"beneficiaries": 30000, "trainings": 900},
        "Gilgit-Baltistan": {"beneficiaries": 20000, "trainings": 600},
        "Islamabad Capital Territory": {"beneficiaries": 10000, "trainings": 300}
    }

    # Trainer Monthly Target (for Trainer Deck & IC Deck)
    TRAINER_MONTHLY_BENEFICIARY_TARGET = 250 # Avg. target per trainer per month

    # --- Helper Functions ---
    def get_random_date(start, end):
        return start + timedelta(days=random.randint(0, (end - start).days))

    def get_random_coords_pakistan():
        # Approximate bounds for Pakistan
        lat = random.uniform(24.0, 37.0)
        lon = random.uniform(60.0, 78.0)
        return lat, lon

    def get_random_choice(arr):
        return random.choice(arr)

    def get_random_int(min_val, max_val):
        return random.randint(min_val, max_val)

    def get_random_float(min_val, max_val, decimals=1):
        return round(random.uniform(min_val, max_val), decimals)

    def get_random_subset(arr, min_count, max_count):
        num_items = random.randint(min_count, max_count)
        return random.sample(arr, min(num_items, len(arr)))

    # --- Raw Data Simulation (Mimicking SurveyCTO Forms) ---
    trainings_raw = []
    beneficiaries_raw = []
    ic_reports_raw = []
    qa_reports_raw = []
    recording_reviews_raw = []

    trainer_locations = {name: get_random_coords_pakistan() for name in TRAINER_NAMES}
    trainer_ic_mapping = {name: get_random_choice(IC_NAMES) for name in TRAINER_NAMES} # Each trainer assigned to an IC
    trainer_duty_stations = {name: get_random_choice(DUTY_STATIONS) for name in TRAINER_NAMES}

    # Simulate Trainings and Beneficiaries
    for i in range(NUM_TRAININGS):
        training_date = get_random_date(START_DATE, END_DATE)
        trainer_name = get_random_choice(TRAINER_NAMES)
        province = get_random_choice(PROVINCES)
        district = get_random_choice(DISTRICTS_BY_PROVINCE[province]) if province in DISTRICTS_BY_PROVINCE else "N/A"
        
        # Ensure consistent location for a trainer (with slight daily variation)
        base_lat, base_lon = trainer_locations[trainer_name]
        training_lat = base_lat + random.uniform(-0.05, 0.05)
        training_lon = base_lon + random.uniform(-0.05, 0.05)

        training_session_id = f"{training_date.strftime('%Y%m%d')}-{trainer_name.replace(' ', '')}-{i:05d}"
        beneficiary_count_actual = get_random_int(20, 35) # Closer to 30
        
        # Training Session Reporting Form data
        trainings_raw.append({
            "training_session_id": training_session_id,
            "trainer_name": trainer_name,
            "training_day": training_date.strftime('%A'),
            "training_date": training_date.strftime('%Y-%m-%d'),
            "training_start_time": f"{get_random_int(8, 10):02d}:00",
            "training_end_time": f"{get_random_int(12, 14):02d}:00",
            "language_of_training": get_random_subset(TRAINING_LANGUAGES, 1, 2),
            "beneficiaries_count_reported_by_trainer": beneficiary_count_actual,
            "ic_contacted_trainer": random.choice([True, False]),
            "mode_of_contact": get_random_choice(["Phone Call", "WhatsApp"]) if random.random() < 0.8 else None,
            "ic_questions_feedback": "N/A",
            "trainer_issue_ic": random.choice([True, False]),
            "trainer_issue_beneficiaries": random.choice([True, False]),
            "describe_issue_query": "Some minor issues encountered." if random.random() < 0.1 else None,
            "topics_covered_session": get_random_subset(TRAINING_TOPICS, 7, 10),
            "training_location_latitude": training_lat,
            "training_location_longitude": training_lon,
            "training_audio_recording_url": f"https://example.com/audio/{training_session_id}.mp3" if random.random() < 0.9 else None,
            "created_at": (training_date + timedelta(minutes=get_random_int(60, 180))).isoformat(),
            "province": province, # ADDED: province
            "district": district # ADDED: district
        })

        # Beneficiary Details Form data (30 per training)
        for j in range(NUM_BENEFICIARIES_PER_TRAINING):
            is_rural = random.random() < 0.7 # 70% rural
            cnic_fake = random.random() < 0.03 # 3% fake CNICs
            age = get_random_int(18, 65)
            
            # Simulate age groups
            age_group_20_25 = 1 if 20 <= age <= 25 else 0
            age_group_26_35 = 1 if 26 <= age <= 35 else 0
            age_group_36_45 = 1 if 36 <= age <= 45 else 0
            age_group_45_plus = 1 if age > 45 else 0

            beneficiaries_raw.append({
                "beneficiary_id": f"{training_session_id}-B{j+1:02d}",
                "training_session_id": training_session_id,
                "full_name": f"Beneficiary {j+1}",
                "cnic_number": f"{random.randint(10000, 99999)}{random.randint(1000000, 9999999)}{random.randint(0, 9)}",
                "cnic_front_picture_url": f"https://placehold.co/150x100/000/FFF?text=CNIC_Front_{j+1}",
                "cnic_back_picture_url": f"https://placehold.co/150x100/000/FFF?text=CNIC_Back_{j+1}",
                "cell_phone_number": f"03{random.randint(0,9)}{random.randint(10000000, 99999999)}",
                "whatsapp_number": f"03{random.randint(0,9)}{random.randint(10000000, 99999999)}" if random.random() < 0.8 else None,
                "address": f"Street {random.randint(1,100)}",
                "union_council": f"UC-{random.randint(1,20)}",
                "tehsil": district, # Tehsil is often same as district for mock
                "districts": district,
                "educational_level": get_random_choice(EDUCATION_LEVELS),
                "age": age,
                "occupation": get_random_choice(OCCUPATIONS),
                "mobile_money_account_available": random.choice([True, False]),
                "household_income_monthly": get_random_int(15000, 80000),
                "household_members_count": get_random_int(3, 10),
                "school_going_children": get_random_int(0, 5),
                "adults_count": get_random_int(2, 7),
                "own_cell_phone": random.choice([True, False]),
                "access_cell_phone": random.choice([True, False]),
                "phone_sim_owner": get_random_choice(["Self", "Family Member"]) if random.random() < 0.9 else "Other",
                "whatsapp_owner": get_random_choice(["Self", "Family Member"]) if random.random() < 0.9 else "Other",
                "have_mob_money_account": random.choice([True, False]),
                "own_bank_account": random.choice([True, False]),
                "avg_savings_money": f"{get_random_int(0, 5000)}", # Simplified range
                "taken_loan_6months": random.choice([True, False]),
                "loan_amount": get_random_int(1000, 50000) if random.random() < 0.3 else 0,
                "loan_source": get_random_choice(LOAN_SOURCES) if random.random() < 0.3 else None,
                "climate_change_affecting_community": get_random_choice(CLIMATE_CHANGE_BELIEF),
                "is_rural": is_rural,
                "is_fake_cnic": cnic_fake,
                "age_group_20_25": age_group_20_25,
                "age_group_26_35": age_group_26_35,
                "age_group_36_45": age_group_36_45,
                "age_group_45_plus": age_group_45_plus,
                "created_at": (training_date + timedelta(minutes=get_random_int(180, 300))).isoformat()
            })

    # Simulate IC Reports
    for i in range(NUM_ICS):
        ic_name = IC_NAMES[i]
        # Simulate monitoring for trainers under this IC
        trainers_under_ic = [t_name for t_name, ic_id in trainer_ic_mapping.items() if ic_id == ic_name]
        
        for _ in range(get_random_int(10, 30)): # Each IC makes 10-30 reports
            monitored_trainer = get_random_choice(trainers_under_ic) if trainers_under_ic else get_random_choice(TRAINER_NAMES)
            
            # Find a recent training session by this trainer to link to
            recent_trainings_by_trainer = [t for t in trainings_raw if t['trainer_name'] == monitored_trainer]
            if not recent_trainings_by_trainer:
                continue # Skip if trainer has no trainings yet

            linked_training = get_random_choice(recent_trainings_by_trainer)
            monitoring_date = get_random_date(datetime.strptime(linked_training['training_date'], '%Y-%m-%d'), END_DATE)
            
            ic_reports_raw.append({
                "ic_report_id": f"ICR-{i}-{_}",
                "training_session_id_monitored": linked_training['training_session_id'],
                "ic_name": ic_name,
                "training_day_monitored": linked_training['training_day'],
                "monitoring_date": monitoring_date.strftime('%Y-%m-%d'),
                "trainer_monitored_name": monitored_trainer,
                "mode_of_monitoring": get_random_choice(IC_MONITORING_MODES),
                "questions_asked_trainer": "Checked on attendance and content delivery.",
                "trainer_performance_rating": get_random_int(5, 10),
                "topics_covered_by_trainer_observed": get_random_int(5, 10),
                "faced_query_issue": random.choice([True, False]),
                "query_issue_other": "Venue issue" if random.random() < 0.1 else None,
                "pc_contacted_ic": random.choice([True, False]),
                "ic_location_latitude": get_random_coords_pakistan()[0], # IC's location
                "ic_location_longitude": get_random_coords_pakistan()[1],
                "created_at": monitoring_date.isoformat()
            })

    # Simulate QA Reports (direct observations)
    for i in range(NUM_QA_OBSERVATIONS):
        qa_name = get_random_choice(QA_NAMES)
        observed_trainer = get_random_choice(TRAINER_NAMES)
        
        # Find a recent training session by this trainer to link to
        recent_trainings_by_trainer = [t for t in trainings_raw if t['trainer_name'] == observed_trainer]
        if not recent_trainings_by_trainer:
            continue

        linked_training = get_random_choice(recent_trainings_by_trainer)
        observation_date = get_random_date(datetime.strptime(linked_training['training_date'], '%Y-%m-%d'), END_DATE)
        
        qa_reports_raw.append({
            "qa_report_id": f"QAR-{i}",
            "observer_name": qa_name,
            "trainer_name_observed": observed_trainer,
            "training_date_observed": linked_training['training_date'],
            "province": linked_training['province'],
            "tehsil_district": linked_training['district'],
            "place": "Community Hall",
            "concepts_covered_during_training_qa": get_random_subset(TRAINING_TOPICS, 5, 10),
            "observations_notes_qa": "Trainer showed good engagement." if random.random() < 0.8 else "Some weaknesses observed.",
            "qa_monitoring_location_latitude": get_random_coords_pakistan()[0],
            "qa_monitoring_location_longitude": get_random_coords_pakistan()[1],
            "created_at": observation_date.isoformat()
        })

    # Simulate Recording Reviews
    for i in range(NUM_RECORDING_REVIEWS):
        reviewer_name = get_random_choice(REVIEWER_NAMES)
        
        # Select a training session that has an audio recording
        trainings_with_audio = [t for t in trainings_raw if t.get('training_audio_recording_url')]
        if not trainings_with_audio:
            continue
        
        linked_training = get_random_choice(trainings_with_audio)
        review_date = get_random_date(datetime.strptime(linked_training['training_date'], '%Y-%m-%d'), END_DATE)
        
        recording_reviews_raw.append({
            "review_id": f"RR-{i}",
            "reviewer_name": reviewer_name,
            "trainer_name_reviewed": linked_training['trainer_name'],
            "training_date_reviewed": linked_training['training_date'],
            "training_session_id_reviewed": linked_training['training_session_id'],
            "audio_recording_quality_rating": get_random_int(1, 5),
            "trainer_performance_audio_engagement": get_random_int(5, 10),
            "trainer_performance_audio_clarity": get_random_int(5, 10),
            "trainer_performance_audio_adherence": get_random_int(5, 10),
            "trainer_performance_audio_overall": get_random_int(5, 10),
            "concepts_covered_from_recording": get_random_subset(TRAINING_TOPICS, 5, 10),
            "key_observations_feedback": "Clear audio, good content flow." if random.random() < 0.8 else "Muffled audio, some concepts rushed.",
            "recommendations_for_trainer": random.choice(["More interactive activities.", "Focus on time management.", "Improve clarity in explanations."]) if random.random() < 0.5 else None,
            "created_at": review_date.isoformat()
        })


    # --- Aggregation and Dashboard-Specific Data Preparation ---
    dashboard_data = {
        "status_deck_data": {},
        "ic_deck_data": {},
        "trainer_deck_data": {},
        "qa_deck_data": {},
        "recording_review_deck_data": {}
    }

    # --- Status Deck Data ---
    total_beneficiaries_trained = sum(t['beneficiaries_count_reported_by_trainer'] for t in trainings_raw)
    total_trainings_conducted = len(trainings_raw)

    rural_beneficiaries = sum(1 for b in beneficiaries_raw if b['is_rural'])
    urban_beneficiaries = len(beneficiaries_raw) - rural_beneficiaries
    
    rural_beneficiaries_pct = (rural_beneficiaries / len(beneficiaries_raw) * 100) if len(beneficiaries_raw) > 0 else 0
    urban_beneficiaries_pct = (urban_beneficiaries / len(beneficiaries_raw) * 100) if len(beneficiaries_raw) > 0 else 0

    trainings_by_location_type = {"Rural": 0, "Urban": 0}
    for t in trainings_raw:
        # Determine if a training is rural/urban based on its beneficiaries
        session_beneficiaries_are_rural = any(b['is_rural'] for b in beneficiaries_raw if b['training_session_id'] == t['training_session_id'])
        if session_beneficiaries_are_rural:
            trainings_by_location_type["Rural"] += 1
        else:
            trainings_by_location_type["Urban"] += 1
    
    rural_trainings_pct = (trainings_by_location_type["Rural"] / total_trainings_conducted * 100) if total_trainings_conducted > 0 else 0
    urban_trainings_pct = (trainings_by_location_type["Urban"] / total_trainings_conducted * 100) if total_trainings_conducted > 0 else 0

    handbooks_distributed = int(total_beneficiaries_trained * random.uniform(0.7, 0.9)) # 70-90% of beneficiaries received handbooks
    handbooks_distributed_pct = (handbooks_distributed / total_beneficiaries_trained * 100) if total_beneficiaries_trained > 0 else 0


    # Provincial Ranking
    provincial_data = {}
    for p in PROVINCES:
        provincial_data[p] = {
            "total_trained": 0,
            "trainings_conducted": 0,
            "avg_cohort_size_sum": 0,
            "avg_cohort_size_count": 0,
            "target_beneficiaries": PROVINCIAL_TARGETS.get(p, {}).get("beneficiaries", 0),
            "target_trainings": PROVINCIAL_TARGETS.get(p, {}).get("trainings", 0)
        }
    
    for t in trainings_raw:
        province = t['province']
        if province in provincial_data:
            provincial_data[province]["total_trained"] += t['beneficiaries_count_reported_by_trainer']
            provincial_data[province]["trainings_conducted"] += 1
            provincial_data[province]["avg_cohort_size_sum"] += t['beneficiaries_count_reported_by_trainer']
            provincial_data[province]["avg_cohort_size_count"] += 1

    provincial_ranking_list = []
    for p, data in provincial_data.items():
        pct_achieved_beneficiaries = (data["total_trained"] / data["target_beneficiaries"] * 100) if data["target_beneficiaries"] > 0 else 0
        pct_achieved_trainings = (data["trainings_conducted"] / data["target_trainings"] * 100) if data["target_trainings"] > 0 else 0
        avg_cohort_size = (data["avg_cohort_size_sum"] / data["avg_cohort_size_count"]) if data["avg_cohort_size_count"] > 0 else 0
        provincial_ranking_list.append({
            "province": p,
            "total_trained": data["total_trained"],
            "pct_achieved_beneficiaries": round(pct_achieved_beneficiaries, 1),
            "trainings_conducted": data["trainings_conducted"],
            "pct_achieved_trainings": round(pct_achieved_trainings, 1),
            "avg_cohort_size": round(avg_cohort_size, 1)
        })
    provincial_ranking_list.sort(key=lambda x: x['total_trained'], reverse=True)


    # Beneficiaries Trend (8 Months)
    eight_months_ago = END_DATE - timedelta(days=8*30) # Approx 8 months
    monthly_trend = {}
    daily_trend = {}
    monthly_accounts = {}

    # Initialize all months/days in range to 0 to ensure continuous lines
    current_date_iterator = START_DATE
    while current_date_iterator <= END_DATE:
        month_key = current_date_iterator.strftime('%Y-%m-01')
        day_key = current_date_iterator.strftime('%Y-%m-%d')
        monthly_trend.setdefault(month_key, {"beneficiaries": 0, "accounts": 0})
        daily_trend.setdefault(day_key, {"beneficiaries": 0, "accounts": 0})
        monthly_accounts.setdefault(month_key, {"accounts": 0})
        current_date_iterator += timedelta(days=1)

    for b in beneficiaries_raw:
        b_date = datetime.strptime(b['created_at'].split('T')[0], '%Y-%m-%d')
        if b_date >= eight_months_ago:
            month_key = b_date.strftime('%Y-%m-01')
            day_key = b_date.strftime('%Y-%m-%d')
            
            monthly_trend[month_key]["beneficiaries"] += 1
            daily_trend[day_key]["beneficiaries"] += 1
            
            if b['have_mob_money_account'] or b['own_bank_account']:
                monthly_trend[month_key]["accounts"] += 1
                daily_trend[day_key]["accounts"] += 1
                monthly_accounts[month_key]["accounts"] += 1
    
    monthly_trend_list = [{"date": k, "beneficiaries": v["beneficiaries"], "accounts": v["accounts"]} for k, v in sorted(monthly_trend.items())]
    daily_trend_list = [{"date": k, "beneficiaries": v["beneficiaries"], "accounts": v["accounts"]} for k, v in sorted(daily_trend.items())]
    monthly_accounts_list = [{"date": k, "accounts": v["accounts"]} for k, v in sorted(monthly_accounts.items())]

    # Top Trainers (Monthly Ranking)
    trainer_monthly_performance = {}
    current_month_start = datetime(END_DATE.year, END_DATE.month, 1)
    for t in trainings_raw:
        train_date = datetime.strptime(t['training_date'], '%Y-%m-%d')
        if train_date >= current_month_start:
            trainer_name = t['trainer_name']
            trainer_monthly_performance.setdefault(trainer_name, {"total_trained": 0, "trainings_conducted": 0, "avg_cohort_size_sum": 0, "avg_cohort_size_count": 0})
            trainer_monthly_performance[trainer_name]["total_trained"] += t['beneficiaries_count_reported_by_trainer']
            trainer_monthly_performance[trainer_name]["trainings_conducted"] += 1
            trainer_monthly_performance[trainer_name]["avg_cohort_size_sum"] += t['beneficiaries_count_reported_by_trainer']
            trainer_monthly_performance[trainer_name]["avg_cohort_size_count"] += 1
    
    top_trainers_ranking_list = []
    for trainer, stats in trainer_monthly_performance.items():
        pct_achieved = (stats["total_trained"] / TRAINER_MONTHLY_BENEFICIARY_TARGET * 100) if TRAINER_MONTHLY_BENEFICIARY_TARGET > 0 else 0
        avg_cohort_size = (stats["avg_cohort_size_sum"] / stats["avg_cohort_size_count"]) if stats["avg_cohort_size_count"] > 0 else 0
        
        # Get QA rating for this trainer (average of their QA_Reports and Recording_Reviews)
        qa_scores = [r['trainer_performance_rating'] for r in ic_reports_raw if r['trainer_monitored_name'] == trainer]
        qa_scores.extend([r['trainer_performance_audio_overall'] for r in recording_reviews_raw if r['trainer_name_reviewed'] == trainer])
        avg_qa_rating = sum(qa_scores) / len(qa_scores) if qa_scores else 0

        top_trainers_ranking_list.append({
            "trainer_name": trainer,
            "total_trained": stats["total_trained"],
            "pct_achieved": round(pct_achieved, 1),
            "trainings_conducted": stats["trainings_conducted"],
            "avg_cohort_size": round(avg_cohort_size, 1),
            "qa_rating": round(avg_qa_rating, 1)
        })
    top_trainers_ranking_list.sort(key=lambda x: x['total_trained'], reverse=True) # Sort by total trained by default

    # Performance Overviews & KPIs (CNIC, Age, Avg Training Time, Engagement, Retention, Education)
    total_cnics_scanned = len(beneficiaries_raw)
    fake_cnics_count = sum(1 for b in beneficiaries_raw if b['is_fake_cnic'])
    valid_cnics_count = total_cnics_scanned - fake_cnics_count
    valid_cnics_pct = (valid_cnics_count / total_cnics_scanned * 100) if total_cnics_scanned > 0 else 0
    fake_cnics_pct = (fake_cnics_count / total_cnics_scanned * 100) if total_cnics_scanned > 0 else 0

    age_groups_counts = {"20-25": 0, "26-35": 0, "36-45": 0, "45+": 0}
    education_counts = {level: 0 for level in EDUCATION_LEVELS}
    total_beneficiaries_for_demographics = len(beneficiaries_raw)
    
    for b in beneficiaries_raw:
        age_groups_counts["20-25"] += b['age_group_20_25']
        age_groups_counts["26-35"] += b['age_group_26_35']
        age_groups_counts["36-45"] += b['age_group_36_45']
        age_groups_counts["45+"] += b['age_group_45_plus']
        education_counts[b['educational_level']] += 1

    age_demographics_pct = {k: (v / total_beneficiaries_for_demographics * 100) if total_beneficiaries_for_demographics > 0 else 0 for k, v in age_groups_counts.items()}
    education_graphics_pct = {k: (v / total_beneficiaries_for_demographics * 100) if total_beneficiaries_for_demographics > 0 else 0 for k, v in education_counts.items()}

    avg_training_time_sum = sum(int(t['training_end_time'].split(':')[0]) - int(t['training_start_time'].split(':')[0]) for t in trainings_raw) # Simplified duration
    avg_training_time = (avg_training_time_sum / total_trainings_conducted) if total_trainings_conducted > 0 else 0

    # Avg engagement rate (from Recording Reviews)
    total_engagement_score = sum(r['trainer_performance_audio_engagement'] for r in recording_reviews_raw)
    avg_engagement_rate = (total_engagement_score / len(recording_reviews_raw)) if len(recording_reviews_raw) > 0 else 0
    
    # Avg retention rate (not directly in forms, so we'll simulate or proxy)
    avg_retention_rate = avg_engagement_rate * random.uniform(0.8, 0.95)


    dashboard_data["status_deck_data"] = {
        "overall_kpis": {
            "total_beneficiaries_trained": total_beneficiaries_trained,
            "total_beneficiary_target": GLOBAL_BENEFICIARY_TARGET,
            "total_trainings_conducted": total_trainings_conducted,
            "total_training_target": GLOBAL_TRAINING_TARGET,
            "top_province_name": max(provincial_ranking_list, key=lambda x: x['pct_achieved_beneficiaries'])['province'] if provincial_ranking_list else "N/A",
            "top_province_pct": max(provincial_ranking_list, key=lambda x: x['pct_achieved_beneficiaries'])['pct_achieved_beneficiaries'] if provincial_ranking_list else 0,
            "rural_beneficiaries_pct": round(rural_beneficiaries_pct, 1),
            "urban_beneficiaries_pct": round(urban_beneficiaries_pct, 1),
            "rural_trainings_pct": round(rural_trainings_pct, 1),
            "urban_trainings_pct": round(urban_trainings_pct, 1),
            "handbooks_distributed_pct": round(handbooks_distributed_pct, 1)
        },
        "provincial_ranking": provincial_ranking_list,
        "beneficiaries_trend": {
            "monthly": monthly_trend_list,
            "daily": daily_trend_list,
            "monthly_accounts": monthly_accounts_list
        },
        "top_trainers_ranking": top_trainers_ranking_list,
        "performance_overviews_kpis": {
            "cnic_verification": {
                "valid_count": valid_cnics_count,
                "fake_count": fake_cnics_count,
                "valid_pct": round(valid_cnics_pct, 1),
                "fake_pct": round(fake_cnics_pct, 1)
            },
            "age_demographics": {
                "20-25_pct": round(age_demographics_pct["20-25"], 1),
                "26-35_pct": round(age_demographics_pct["26-35"], 1),
                "36-45_pct": round(age_demographics_pct["36-45"], 1),
                "45+_pct": round(age_demographics_pct["45+"], 1)
            },
            "avg_training_time_hours": round(avg_training_time, 1),
            "avg_engagement_rate_pct": round(avg_engagement_rate, 1),
            "avg_retention_rate_pct": round(avg_retention_rate, 1),
            "education_graphics": {level.replace(' ', '_').replace("'", "") + "_pct": round(pct, 1) for level, pct in education_graphics_pct.items()}
        },
        "map_data": [
            {
                "training_session_id": t['training_session_id'],
                "aspc_name": t['trainer_name'],
                "total_beneficiaries_trained": t['beneficiaries_count_reported_by_trainer'],
                "total_target_pct_achieved": round(t['beneficiaries_count_reported_by_trainer'] / NUM_BENEFICIARIES_PER_TRAINING * 100, 1), # Simplified session target
                "under_ic": trainer_ic_mapping.get(t['trainer_name'], "N/A"),
                "duty_station": trainer_duty_stations.get(t['trainer_name'], "N/A"),
                "district": t['district'],
                "total_trainings_this_month": 1, # This is per training record
                "latitude": t['training_location_latitude'],
                "longitude": t['training_location_longitude'],
                "province": t['province']
            } for t in trainings_raw
        ],
        "system_alerts": [] # Will be populated by JS based on thresholds
    }

    # --- IC Deck Data ---
    # Aggregations for IC Deck will be more dynamic based on filtered IC/Province
    
    # Calculate overall IC performance for Top ICs ranking
    ic_performance_summary = {}
    for ic_id in IC_NAMES:
        ic_performance_summary[ic_id] = {
            "total_trainers_supervised": 0,
            "total_handbooks_distributed": 0,
            "avg_retention_rate_sum": 0,
            "avg_retention_rate_count": 0,
            "total_beneficiaries": 0,
            "total_target_beneficiaries": 0,
            "monitoring_visits_count": 0,
            "total_monitoring_target": 0 # Per IC target
        }
    
    # Link trainers to ICs for aggregation
    trainers_by_ic = {ic_id: [] for ic_id in IC_NAMES}
    for trainer_name, ic_id in trainer_ic_mapping.items():
        trainers_by_ic[ic_id].append(trainer_name)

    for ic_id, trainers in trainers_by_ic.items():
        ic_performance_summary[ic_id]["total_trainers_supervised"] = len(trainers)
        
        ic_related_trainings = [t for t in trainings_raw if t['trainer_name'] in trainers]
        ic_related_beneficiaries = [b for b in beneficiaries_raw if b['training_session_id'] in [t['training_session_id'] for t in ic_related_trainings]]
        
        ic_performance_summary[ic_id]["total_beneficiaries"] = sum(t['beneficiaries_count_reported_by_trainer'] for t in ic_related_trainings)
        ic_performance_summary[ic_id]["total_handbooks_distributed"] = int(ic_performance_summary[ic_id]["total_beneficiaries"] * random.uniform(0.7, 0.9)) # Proxy

        # Calculate avg retention rate for trainers under this IC
        trainer_retention_rates = []
        for trainer_name in trainers:
            # Find relevant recording reviews for this trainer
            trainer_reviews = [r for r in recording_reviews_raw if r['trainer_name_reviewed'] == trainer_name]
            if trainer_reviews:
                avg_trainer_retention = sum(r['trainer_performance_audio_overall'] for r in trainer_reviews) / len(trainer_reviews) # Use overall audio performance as proxy
                trainer_retention_rates.append(avg_trainer_retention)
        
        if trainer_retention_rates:
            ic_performance_summary[ic_id]["avg_retention_rate_sum"] = sum(trainer_retention_rates)
            ic_performance_summary[ic_id]["avg_retention_rate_count"] = len(trainer_retention_rates)
        
        # Sum up monitoring visits by this IC
        ic_performance_summary[ic_id]["monitoring_visits_count"] = sum(1 for r in ic_reports_raw if r['ic_name'] == ic_id)

        # Calculate total target beneficiaries for trainers under this IC
        ic_performance_summary[ic_id]["total_target_beneficiaries"] = len(trainers) * TRAINER_MONTHLY_BENEFICIARY_TARGET
        ic_performance_summary[ic_id]["total_monitoring_target"] = len(trainers) * 2 # Example: 2 visits per trainer per month

    top_ics_ranking_list = []
    for ic_id, stats in ic_performance_summary.items():
        target_achieved_pct = (stats["total_beneficiaries"] / stats["total_target_beneficiaries"] * 100) if stats["total_target_beneficiaries"] > 0 else 0
        avg_retention_rate = (stats["avg_retention_rate_sum"] / stats["avg_retention_rate_count"]) if stats["avg_retention_rate_count"] > 0 else 0
        top_ics_ranking_list.append({
            "ic_name": ic_id,
            "total_trainers_supervised": stats["total_trainers_supervised"],
            "total_handbooks_distributed": stats["total_handbooks_distributed"],
            "avg_retention_rate": round(avg_retention_rate, 1),
            "target_achieved_pct": round(target_achieved_pct, 1),
            "monitoring_visits": stats["monitoring_visits_count"]
        })
    top_ics_ranking_list.sort(key=lambda x: x['target_achieved_pct'], reverse=True)


    # Trainer performance for IC Deck's Team Performance Ranking
    trainer_performance_for_ic_deck = {}
    for trainer_name in TRAINER_NAMES:
        trainer_trainings_current_month = [t for t in trainings_raw if t['trainer_name'] == trainer_name and datetime.strptime(t['training_date'], '%Y-%m-%d').month == END_DATE.month]
        beneficiaries_this_month = sum(t['beneficiaries_count_reported_by_trainer'] for t in trainer_trainings_current_month)
        trainings_this_month = len(trainer_trainings_current_month)
        
        target_pct = (beneficiaries_this_month / TRAINER_MONTHLY_BENEFICIARY_TARGET * 100) if TRAINER_MONTHLY_BENEFICIARY_TARGET > 0 else 0
        
        # Determine status based on recent activity (e.g., last 7 days)
        last_activity_date = max([datetime.strptime(t['training_date'], '%Y-%m-%d') for t in trainer_trainings_current_month], default=None)
        status = "Inactive"
        if last_activity_date:
            days_since_last_activity = (END_DATE - last_activity_date).days
            if days_since_last_activity <= 2: status = "Active"
            elif days_since_last_activity <= 7: status = "Low Activity"
            else: status = "Stale Data" # Active trainer but no recent reports

        trainer_performance_for_ic_deck[trainer_name] = {
            "trainer_name": trainer_name,
            "province": [t['province'] for t in trainer_trainings_current_month if 'province' in t][0] if trainer_trainings_current_month else "N/A",
            "district": [t['district'] for t in trainer_trainings_current_month if 'district' in t][0] if trainer_trainings_current_month else "N/A",
            "beneficiaries_this_month": beneficiaries_this_month,
            "trainings_this_month": trainings_this_month,
            "target_pct": round(target_pct, 1),
            "status": status,
            "trainer_lat": trainer_locations[trainer_name][0],
            "trainer_lon": trainer_locations[trainer_name][1],
            "ic_id": trainer_ic_mapping[trainer_name]
        }
    
    team_performance_ranking_list = list(trainer_performance_for_ic_deck.values())
    team_performance_ranking_list.sort(key=lambda x: x['beneficiaries_this_month'], reverse=True)

    # Attendance & Compliance Trend (IC Deck)
    attendance_compliance_trend_data = {}
    for t in trainings_raw:
        train_date = datetime.strptime(t['training_date'], '%Y-%m-%d')
        month_key = train_date.strftime('%Y-%m')
        attendance_compliance_trend_data.setdefault(month_key, {"attendance_sum": 0, "attendance_count": 0, "compliance_sum": 0, "compliance_count": 0})
        
        # Simulating attendance & compliance per training
        attendance_score = get_random_float(70, 100)
        compliance_score = get_random_float(75, 100)
        
        attendance_compliance_trend_data[month_key]["attendance_sum"] += attendance_score
        attendance_compliance_trend_data[month_key]["attendance_count"] += 1
        attendance_compliance_trend_data[month_key]["compliance_sum"] += compliance_score
        attendance_compliance_trend_data[month_key]["compliance_count"] += 1
    
    attendance_compliance_trend_list = []
    for month_key, data in sorted(attendance_compliance_trend_data.items()):
        avg_attendance = (data["attendance_sum"] / data["attendance_count"]) if data["attendance_count"] > 0 else 0
        avg_compliance = (data["compliance_sum"] / data["compliance_count"]) if data["compliance_count"] > 0 else 0
        attendance_compliance_trend_list.append({
            "month": month_key,
            "avg_attendance_pct": round(avg_attendance, 1),
            "avg_compliance_pct": round(avg_compliance, 1)
        })

    # Bottleneck Identification (IC Deck)
    bottleneck_counts = {}
    for t in trainings_raw:
        if random.random() < 0.25: # 25% chance of a bottleneck
            reason = get_random_choice(BOTTLENECK_REASONS)
            bottleneck_counts[reason] = bottleneck_counts.get(reason, 0) + 1
    bottleneck_identification_list = [{"reason": k, "count": v} for k, v in sorted(bottleneck_counts.items(), key=lambda item: item[1], reverse=True)]

    # Training Type Distribution (IC Deck)
    training_type_counts = {}
    for t in trainings_raw:
        training_type_counts[t['training_start_time']] = training_type_counts.get(t['training_start_time'], 0) + 1 # Using start time as proxy for type
    training_type_distribution_list = [{"type": k, "count": v} for k, v in sorted(training_type_counts.items(), key=lambda item: item[1], reverse=True)]

    # Recent Field Updates (IC Deck)
    recent_field_updates_list = []
    recent_trainings_for_updates = sorted(trainings_raw, key=lambda x: x['created_at'], reverse=True)[:20] # Get 20 most recent
    for t in recent_trainings_for_updates:
        feedback_type = get_random_choice(FEEDBACK_CATEGORIES)
        feedback_note = f"{feedback_type} feedback on training by {t['trainer_name']} in {t['district']}."
        recent_field_updates_list.append({
            "date": t['training_date'],
            "trainer": t['trainer_name'],
            "type": feedback_type,
            "notes": feedback_note
        })
    
    dashboard_data["ic_deck_data"] = {
        "overall_summary_kpis": {
            "total_trainers_under_ic": len(TRAINER_NAMES),
            "active_trainers": len(TRAINER_NAMES) - get_random_int(5, 15), # Simulate some inactive
            "monthly_beneficiaries": sum(t['beneficiaries_count_reported_by_trainer'] for t in trainings_raw if datetime.strptime(t['training_date'], '%Y-%m-%d').month == END_DATE.month),
            "beneficiary_target_achieved_pct": round(sum(t['beneficiaries_count_reported_by_trainer'] for t in trainings_raw if datetime.strptime(t['training_date'], '%Y-%m-%d').month == END_DATE.month) / (TRAINER_MONTHLY_BENEFICIARY_TARGET * NUM_TRAINERS) * 100, 1),
            "monthly_trainings": sum(1 for t in trainings_raw if datetime.strptime(t['training_date'], '%Y-%m-%d').month == END_DATE.month),
            "trainings_vs_last_month_pct": get_random_float(-10, 15), # Simulate change
            "avg_attendance_rate": get_random_float(80, 95),
            "pending_reports": get_random_int(5, 20),
            "field_monitoring_visits": sum(1 for r in ic_reports_raw if datetime.strptime(r['monitoring_date'], '%Y-%m-%d').month == END_DATE.month),
            "visits_target_achieved_pct": get_random_float(70, 110)
        },
        "team_performance_ranking": team_performance_ranking_list,
        "attendance_compliance_trend": attendance_compliance_trend_list,
        "bottleneck_identification": bottleneck_identification_list,
        "training_type_distribution": training_type_distribution_list,
        "recent_field_updates": recent_field_updates_list,
        "trainer_activity_map_data": [
            {
                "trainer_name": t['trainer_name'],
                "ic_id": trainer_ic_mapping.get(t['trainer_name'], "N/A"),
                "latitude": t['training_location_latitude'],
                "longitude": t['training_location_longitude'],
                "status": "Active" if random.random() > 0.1 else "Inactive", # Simplified status for map dot
                "beneficiaries_last_report": t['beneficiaries_count_reported_by_trainer'],
                "last_activity_date": t['training_date']
            } for t in trainings_raw
        ],
        "top_ics_ranking": top_ics_ranking_list
    }

    # --- Trainer Deck Data ---
    dashboard_data["trainer_deck_data"] = {
        "all_trainers_data": {}, # Store all trainers' data here
        "profiles": {name: {"name": name, "id": f"TRN-{i+1:03d}", "location": f"{get_random_choice(DISTRICTS_BY_PROVINCE[get_random_choice(PROVINCES)])}, {get_random_choice(PROVINCES)}", "ic": trainer_ic_mapping[name], "status": random.choice(["Active", "On Watch", "Inactive"]), "target": TRAINER_MONTHLY_BENEFICIARY_TARGET} for i, name in enumerate(TRAINER_NAMES)}
    }
    
    for trainer_name in TRAINER_NAMES:
        trainer_trainings = [t for t in trainings_raw if t['trainer_name'] == trainer_name]
        trainer_beneficiaries = [b for b in beneficiaries_raw if b['training_session_id'] in [t['training_session_id'] for t in trainer_trainings]]
        trainer_ic_reports = [r for r in ic_reports_raw if r['trainer_monitored_name'] == trainer_name]
        trainer_qa_reports = [r for r in qa_reports_raw if r['trainer_name_observed'] == trainer_name]
        trainer_recording_reviews = [r for r in recording_reviews_raw if r['trainer_name_reviewed'] == trainer_name]

        # Monthly Trend for Trainer Deck
        trainer_trends = {}
        # Ensure trend covers the last 6 months for the chart
        trend_start_date = END_DATE - timedelta(days=6*30)
        current_date_iterator = trend_start_date
        while current_date_iterator <= END_DATE:
            month_key = current_date_iterator.strftime('%Y-%m-01')
            trainer_trends.setdefault(month_key, {"beneficiaries": 0, "accounts": 0, "date": current_date_iterator.strftime('%Y-%m-%d')})
            current_date_iterator += timedelta(days=30) # Approximate month increment
        
        for t in trainer_trainings:
            t_date = datetime.strptime(t['training_date'], '%Y-%m-%d')
            if t_date >= trend_start_date:
                month_key = t_date.strftime('%Y-%m-01')
                trainer_trends.setdefault(month_key, {"beneficiaries": 0, "accounts": 0, "date": t_date.strftime('%Y-%m-%d')}) # Ensure date is present
                trainer_trends[month_key]["beneficiaries"] += t['beneficiaries_count_reported_by_trainer']
                
                # Count accounts from beneficiaries linked to this training
                session_beneficiaries = [b for b in trainer_beneficiaries if b['training_session_id'] == t['training_session_id']]
                trainer_trends[month_key]["accounts"] += sum(1 for b in session_beneficiaries if b['have_mob_money_account'] or b['own_bank_account'])
        
        trainer_trends_list = [{"date": k, "beneficiaries": v["beneficiaries"], "accounts": v["accounts"]} for k, v in sorted(trainer_trends.items())]
        
        # Skill Assessment (Self vs QA)
        latest_ic_report = max(trainer_ic_reports, key=lambda x: x['monitoring_date']) if trainer_ic_reports else None
        latest_review = max(trainer_recording_reviews, key=lambda x: x['created_at']) if trainer_recording_reviews else None
        
        self_scores = [get_random_int(70, 95) for _ in range(4)] # Mock self-assessment
        # QA scores from IC report (performance_rating is 1-10, scale to 1-100)
        qa_scores_from_ic = [latest_ic_report['trainer_performance_rating'] * 10 for _ in range(4)] if latest_ic_report else [get_random_int(60, 90) for _ in range(4)]
        # QA scores from recording review (overall is 1-10, scale to 1-100)
        qa_scores_from_review = [latest_review['trainer_performance_audio_overall'] * 10 for _ in range(4)] if latest_review else [get_random_int(60, 90) for _ in range(4)]
        
        # Average the two QA sources if both exist, otherwise use one
        final_qa_scores = []
        for i in range(4):
            if latest_ic_report and latest_review:
                final_qa_scores.append(round((qa_scores_from_ic[i] + qa_scores_from_review[i]) / 2))
            elif latest_ic_report:
                final_qa_scores.append(qa_scores_from_ic[i])
            elif latest_review:
                final_qa_scores.append(qa_scores_from_review[i])
            else:
                final_qa_scores.append(get_random_int(60, 90)) # Fallback random if no QA data

        # Activity Calendar (dates with activity for this trainer)
        activity_dates = sorted(list(set(t['training_date'] for t in trainer_trainings)))

        # Recent Sessions Log
        recent_sessions = sorted(trainer_trainings, key=lambda x: x['training_date'], reverse=True)[:5]
        recent_sessions_log_formatted = []
        for s in recent_sessions:
            session_beneficiaries = [b for b in beneficiaries_raw if b['training_session_id'] == s['training_session_id']]
            accounts_opened = sum(1 for b in session_beneficiaries if b['have_mob_money_account'] or b['own_bank_account'])
            qa_score_for_session = next((r['trainer_performance_rating'] for r in trainer_ic_reports if r['training_session_id_monitored'] == s['training_session_id']), get_random_int(6, 9))
            audio_available = s['training_audio_recording_url'] is not None
            
            alert = None
            if s['beneficiaries_count_reported_by_trainer'] < 20:
                alert = {"type": "warning", "message": "Low attendance detected."}
            elif accounts_opened / s['beneficiaries_count_reported_by_trainer'] < 0.2 and s['beneficiaries_count_reported_by_trainer'] > 0:
                alert = {"type": "warning", "message": "Low conversion rate."}
            
            recent_sessions_log_formatted.append({
                "ID": s['training_session_id'],
                "Date": s['training_date'],
                "District": s['district'],
                "Beneficiaries": s['beneficiaries_count_reported_by_trainer'],
                "Accounts": accounts_opened,
                "QA": qa_score_for_session,
                "Self": {"Clarity": get_random_int(70,95), "Engagement": get_random_int(70,95), "Content": get_random_int(70,95), "Logistics": get_random_int(70,95)},
                "Audio": audio_available,
                "Alert": alert
            })

        # Alerts & Recommendations (from IC reports and Recording Reviews)
        trainer_alerts = []
        for r in trainer_ic_reports:
            if r['faced_query_issue']:
                trainer_alerts.append({"type": "warning", "message": f"Issue reported by IC on {r['monitoring_date']}: {r['query_issue_other'] or 'N/A'}", "date": r['monitoring_date']})
        for r in trainer_recording_reviews:
            if r['audio_recording_quality_rating'] < 3:
                trainer_alerts.append({"type": "danger", "message": f"Poor audio quality in recording from {r['training_date_reviewed']}.", "date": r['training_date_reviewed']})
            if r['trainer_performance_audio_overall'] < 6:
                trainer_alerts.append({"type": "danger", "message": f"Low performance score in recording from {r['training_date_reviewed']}.", "date": r['training_date_reviewed']})
            if r['recommendations_for_trainer']:
                 trainer_alerts.append({"type": "info", "message": f"Recommendation: {r['recommendations_for_trainer']}", "date": r['created_at'].split('T')[0]})
        
        dashboard_data["trainer_deck_data"]["all_trainers_data"][trainer_name] = {
            "monthly_target_achievement": {
                "achieved": sum(s['Beneficiaries'] for s in recent_sessions_log_formatted),
                "target": TRAINER_MONTHLY_BENEFICIARY_TARGET,
                "percentage": round(sum(s['Beneficiaries'] for s in recent_sessions_log_formatted) / TRAINER_MONTHLY_BENEFICIARY_TARGET * 100, 1) if TRAINER_MONTHLY_BENEFICIARY_TARGET > 0 else 0,
                "status": "On Track" # Simplified
            },
            "performance_trend": trainer_trends_list,
            "skill_assessment": {
                "labels": ["Clarity", "Engagement", "Content", "Logistics"],
                "self": self_scores,
                "qa": final_qa_scores
            },
            "activity_calendar": {
                "dates_with_activity": activity_dates
            },
            "recent_sessions_log": recent_sessions_log_formatted,
            "alerts_recommendations": trainer_alerts
        }

    # --- QA Deck Data ---
    total_trainings_qa_checked = len(qa_reports_raw)
    avg_qa_score = sum(r['trainer_performance_rating'] for r in ic_reports_raw) / len(ic_reports_raw) if ic_reports_raw else 0 # Using IC reports as proxy for QA score
    trainers_monitored_by_qa = len(set(r['trainer_name_observed'] for r in qa_reports_raw))
    
    critical_trainings_count = sum(1 for r in ic_reports_raw if r['trainer_performance_rating'] < 6) # Below 6 is critical
    critical_trainings_pct = (critical_trainings_count / len(ic_reports_raw) * 100) if ic_reports_raw else 0

    qa_score_distribution_counts = {"Excellent": 0, "Good": 0, "Average": 0, "Needs Improvement": 0, "Critical": 0}
    for r in ic_reports_raw:
        score = r['trainer_performance_rating']
        if score >= 9: qa_score_distribution_counts["Excellent"] += 1
        elif score >= 7: qa_score_distribution_counts["Good"] += 1
        elif score >= 5: qa_score_distribution_counts["Average"] += 1
        elif score >= 3: qa_score_distribution_counts["Needs Improvement"] += 1
        else: qa_score_distribution_counts["Critical"] += 1

    # Concept Coverage Analysis (from QA reports)
    concept_coverage_counts = {topic: 0 for topic in TRAINING_TOPICS}
    for r in qa_reports_raw:
        for concept in r['concepts_covered_during_training_qa']:
            concept_coverage_counts[concept] = concept_coverage_counts.get(concept, 0) + 1
    
    concept_coverage_analysis_list = []
    for concept, count in concept_coverage_counts.items():
        covered_pct = (count / total_trainings_qa_checked * 100) if total_trainings_qa_checked > 0 else 0
        concept_coverage_analysis_list.append({"concept": concept, "covered_pct": round(covered_pct, 1)})

    # QA Trend by Month
    qa_trend_by_month_data = {}
    for r in ic_reports_raw:
        report_date = datetime.strptime(r['monitoring_date'], '%Y-%m-%d')
        month_key = report_date.strftime('%Y-%m')
        qa_trend_by_month_data.setdefault(month_key, {"total_score": 0, "count": 0, "trainings_qa": 0})
        qa_trend_by_month_data[month_key]["total_score"] += r['trainer_performance_rating']
        qa_trend_by_month_data[month_key]["count"] += 1
        qa_trend_by_month_data[month_key]["trainings_qa"] += 1
    
    qa_trend_by_month_list = []
    for month_key, data in sorted(qa_trend_by_month_data.items()):
        avg_score = (data["total_score"] / data["count"]) if data["count"] > 0 else 0
        qa_trend_by_month_list.append({"month": month_key, "avg_qa_score": round(avg_score, 1), "trainings_qa": data["trainings_qa"]})

    # Top QA Team Members
    qa_member_performance = {}
    for r in qa_reports_raw:
        qa_member_performance.setdefault(r['observer_name'], {"total_score": 0, "count": 0, "trainings_monitored": 0})
        qa_member_performance[r['observer_name']]["total_score"] += get_random_int(7, 10) # Mock score for QA member
        qa_member_performance[r['observer_name']]["count"] += 1
        qa_member_performance[r['observer_name']]["trainings_monitored"] += 1
    
    top_qa_team_members_list = []
    for name, stats in qa_member_performance.items():
        avg_score = (stats["total_score"] / stats["count"]) if stats["count"] > 0 else 0
        top_qa_team_members_list.append({"name": name, "avg_score": round(avg_score, 1), "trainings_monitored": stats["trainings_monitored"]})
    top_qa_team_members_list.sort(key=lambda x: x['avg_score'], reverse=True)

    qa_alerts_list = []
    for r in ic_reports_raw:
        if r['trainer_performance_rating'] < 6:
            qa_alerts_list.append({"type": "danger", "message": f"Trainer {r['trainer_monitored_name']} scored low ({r['trainer_performance_rating']}) on {r['monitoring_date']}.", "date": r['monitoring_date']})
    for r in qa_reports_raw:
        if "weakness" in r['observations_notes_qa'].lower() or "issues" in r['observations_notes_qa'].lower():
            qa_alerts_list.append({"type": "warning", "message": f"Observation for {r['trainer_name_observed']} on {r['training_date_observed']}: {r['observations_notes_qa']}.", "date": r['training_date_observed']})


    dashboard_data["qa_deck_data"] = {
        "overall_kpis": {
            "total_trainings_qa_checked": total_trainings_qa_checked,
            "avg_qa_score": round(avg_qa_score, 1),
            "trainers_monitored": trainers_monitored_by_qa,
            "critical_trainings_pct": round(critical_trainings_pct, 1)
        },
        "qa_score_distribution": {
            "labels": list(qa_score_distribution_counts.keys()),
            "counts": list(qa_score_distribution_counts.values())
        },
        "concept_coverage_analysis": concept_coverage_analysis_list,
        "qa_trend_by_month": qa_trend_by_month_list,
        "top_qa_team_members": top_qa_team_members_list,
        "qa_alerts": qa_alerts_list,
        "qa_map_data": [
            {
                "qa_id": r['observer_name'],
                "trainer_name": r['trainer_name_observed'],
                "training_date": r['training_date_observed'],
                "province": r['province'],
                "district": r['tehsil_district'],
                "latitude": r['qa_monitoring_location_latitude'],
                "longitude": r['qa_monitoring_location_longitude'],
                "qa_score": get_random_int(6, 10) # Mock QA score for map dot
            } for r in qa_reports_raw
        ]
    }

    # --- Recording Review Deck Data ---
    total_recordings_reviewed = len(recording_reviews_raw)
    avg_audio_quality_rating = sum(r['audio_recording_quality_rating'] for r in recording_reviews_raw) / total_recordings_reviewed if total_recordings_reviewed > 0 else 0
    avg_trainer_performance_rating = sum(r['trainer_performance_audio_overall'] for r in recording_reviews_raw) / total_recordings_reviewed if total_recordings_reviewed > 0 else 0
    
    flagged_recordings_count = sum(1 for r in recording_reviews_raw if r['audio_recording_quality_rating'] < 3 or r['trainer_performance_audio_overall'] < 6)
    flagged_recordings_pct = (flagged_recordings_count / total_recordings_reviewed * 100) if total_recordings_reviewed > 0 else 0

    audio_quality_distribution_counts = {"Excellent": 0, "Good": 0, "Average": 0, "Poor": 0, "Very Poor": 0}
    for r in recording_reviews_raw:
        rating = r['audio_recording_quality_rating']
        if rating == 5: audio_quality_distribution_counts["Excellent"] += 1
        elif rating == 4: audio_quality_distribution_counts["Good"] += 1
        elif rating == 3: audio_quality_distribution_counts["Average"] += 1
        elif rating == 2: audio_quality_distribution_counts["Poor"] += 1
        else: audio_quality_distribution_counts["Very Poor"] += 1

    trainer_performance_breakdown_scores_from_reviews = {
        "engagement": [], "clarity": [], "adherence": [], "overall": []
    }
    for r in recording_reviews_raw:
        trainer_performance_breakdown_scores_from_reviews["engagement"].append(r['trainer_performance_audio_engagement'])
        trainer_performance_breakdown_scores_from_reviews["clarity"].append(r['trainer_performance_audio_clarity'])
        trainer_performance_breakdown_scores_from_reviews["adherence"].append(r['trainer_performance_audio_adherence'])
        trainer_performance_breakdown_scores_from_reviews["overall"].append(r['trainer_performance_audio_overall'])

    # Using average of values from recording_reviews_raw for QA scores
    avg_qa_scores_from_reviews_final = [
        sum(trainer_performance_breakdown_scores_from_reviews["engagement"]) / len(trainer_performance_breakdown_scores_from_reviews["engagement"]) if trainer_performance_breakdown_scores_from_reviews["engagement"] else 0,
        sum(trainer_performance_breakdown_scores_from_reviews["clarity"]) / len(trainer_performance_breakdown_scores_from_reviews["clarity"]) if trainer_performance_breakdown_scores_from_reviews["clarity"] else 0,
        sum(trainer_performance_breakdown_scores_from_reviews["adherence"]) / len(trainer_performance_breakdown_scores_from_reviews["adherence"]) if trainer_performance_breakdown_scores_from_reviews["adherence"] else 0,
        sum(trainer_performance_breakdown_scores_from_reviews["overall"]) / len(trainer_performance_breakdown_scores_from_reviews["overall"]) if trainer_performance_breakdown_scores_from_reviews["overall"] else 0
    ]
    avg_self_scores_mock = [get_random_int(7,10) for _ in range(4)] # Mock self-scores

    # Concept Coverage from Audio
    concept_coverage_from_audio_counts = {topic: 0 for topic in TRAINING_TOPICS}
    for r in recording_reviews_raw:
        for concept in r['concepts_covered_from_recording']:
            concept_coverage_from_audio_counts[concept] = concept_coverage_from_audio_counts.get(concept, 0) + 1
    
    concept_coverage_from_audio_list = []
    for concept, count in concept_coverage_from_audio_counts.items():
        covered_pct = (count / total_recordings_reviewed * 100) if total_recordings_reviewed > 0 else 0
        concept_coverage_from_audio_list.append({"concept": concept, "covered_pct": round(covered_pct, 1)})

    # Review Trend by Month
    review_trend_by_month_data = {}
    for r in recording_reviews_raw:
        review_date = datetime.strptime(r['created_at'].split('T')[0], '%Y-%m-%d')
        month_key = review_date.strftime('%Y-%m')
        review_trend_by_month_data.setdefault(month_key, {"total_performance_score": 0, "count": 0, "recordings_reviewed": 0})
        review_trend_by_month_data[month_key]["total_performance_score"] += r['trainer_performance_audio_overall']
        review_trend_by_month_data[month_key]["count"] += 1
        review_trend_by_month_data[month_key]["recordings_reviewed"] += 1
    
    review_trend_by_month_list = []
    for month_key, data in sorted(review_trend_by_month_data.items()):
        avg_performance_score = (data["total_performance_score"] / data["count"]) if data["count"] > 0 else 0
        review_trend_by_month_list.append({"month": month_key, "avg_performance_score": round(avg_performance_score, 1), "recordings_reviewed": data["recordings_reviewed"]})

    # Top Reviewers
    reviewer_performance = {}
    for r in recording_reviews_raw:
        reviewer_performance.setdefault(r['reviewer_name'], {"total_score": 0, "count": 0, "recordings_reviewed": 0})
        reviewer_performance[r['reviewer_name']]["total_score"] += r['trainer_performance_audio_overall']
        reviewer_performance[r['reviewer_name']]["count"] += 1
        reviewer_performance[r['reviewer_name']]["recordings_reviewed"] += 1
    
    top_reviewers_list = []
    for name, stats in reviewer_performance.items():
        avg_score = (stats["total_score"] / stats["count"]) if stats["count"] > 0 else 0
        top_reviewers_list.append({"name": name, "avg_score": round(avg_score, 1), "recordings_reviewed": stats["recordings_reviewed"]})
    top_reviewers_list.sort(key=lambda x: x['avg_score'], reverse=True)

    # Recommendations Summary
    recommendation_counts = {}
    for r in recording_reviews_raw:
        if r['recommendations_for_trainer']:
            recommendation_counts[r['recommendations_for_trainer']] = recommendation_counts.get(r['recommendations_for_trainer'], 0) + 1
    
    recommendations_summary_list = [{"recommendation_type": k, "count": v} for k, v in recommendation_counts.items()]


    dashboard_data["recording_review_deck_data"] = {
        "overall_kpis": {
            "total_recordings_reviewed": total_recordings_reviewed,
            "avg_audio_quality_rating": round(avg_audio_quality_rating, 1),
            "avg_trainer_performance_rating": round(avg_trainer_performance_rating, 1),
            "flagged_recordings_pct": round(flagged_recordings_pct, 1)
        },
        "audio_quality_distribution": {
            "labels": list(audio_quality_distribution_counts.keys()),
            "counts": list(audio_quality_distribution_counts.values())
        },
        "trainer_performance_breakdown": {
            "labels": ["Engagement", "Clarity", "Adherence", "Overall"],
            "self_scores": [round(s, 1) for s in avg_self_scores_mock],
            "qa_scores": [round(s, 1) for s in avg_qa_scores_from_reviews_final]
        },
        "concept_coverage_from_audio": concept_coverage_from_audio_list,
        "review_trend_by_month": review_trend_by_month_list,
        "top_reviewers": top_reviewers_list,
        "recommendations_summary": recommendations_summary_list
    }

    # Save the generated data to a JSON file
    output_filename = "dflt_dashboard_data.json"
    with open(output_filename, 'w') as f:
        json.dump(dashboard_data, f, indent=4)
    
    print(f"Generated data saved to {output_filename}")

# Call the function to generate and save data
generate_random_data_and_save()
