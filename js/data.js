// Function to generate random data
function generateRandomTrainingData(numRecords = 500) {
    const provinces = ["Punjab", "Sindh", "Khyber Pakhtunkhwa", "Balochistan", "Azad Jammu & Kashmir", "Gilgit-Baltistan"];
    const districtsByProvince = {
        "Punjab": ["Lahore", "Rawalpindi", "Faisalabad", "Multan", "Sialkot", "Gujranwala"],
        "Sindh": ["Karachi", "Hyderabad", "Sukkur", "Larkana", "Mirpur Khas", "Nawabshah"],
        "Khyber Pakhtunkhwa": ["Peshawar", "Swat", "Mardan", "Abbottabad", "Kohat", "Bannu"],
        "Balochistan": ["Quetta", "Khuzdar", "Gwadar", "Dera Bugti", "Sibi", "Turbat"],
        "Azad Jammu & Kashmir": ["Muzaffarabad", "Mirpur", "Kotli", "Bhimber", "Neelum Valley"],
        "Gilgit-Baltistan": ["Gilgit", "Skardu", "Ghanche", "Diamer"]
    };
    const aspcNames = ["Ayesha Khan", "Ahmed Shah", "Nida Khan", "Omar Farooq", "Rubina Iqbal", "Tariq Mahmood", "Yusra Khan", "Sana Ali", "Ali Raza", "Zara Saleem", "Usman Anwar", "Fatima Zahra", "Kamran Baig", "Hafsa Malik", "Iqbal Hussain", "Samina Butt", "Zainab Abbas", "Bilal Khan"];
    const dutyStations = ["Karachi Hub", "Lahore HQ", "Peshawar Centre", "Quetta Branch", "Multan Field", "Hyderabad Support", "Islamabad Office", "Faisalabad Node"];

    const data = [];
    const today = new Date();
    const eightMonthsAgo = new Date(today);
    eightMonthsAgo.setMonth(today.getMonth() - 7);
    eightMonthsAgo.setDate(1);

    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function getRandomFloat(min, max) {
        return (Math.random() * (max - min) + min);
    }

    function getRandomDate(start, end) {
        return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
    }

    const trainerStats = {};
    aspcNames.forEach(name => {
        trainerStats[name] = { totalTrainings: getRandomInt(5, 20), totalBeneficiaries: getRandomInt(100, 500) };
    });

    for (let i = 1; i <= numRecords; i++) {
        const randomProvince = provinces[getRandomInt(0, provinces.length - 1)];
        const randomDistrict = districtsByProvince[randomProvince] ? districtsByProvince[randomProvince][getRandomInt(0, districtsByProvince[randomProvince].length - 1)] : "N/A";
        const randomASPCName = aspcNames[getRandomInt(0, aspcNames.length - 1)];
        const randomDutyStation = dutyStations[getRandomInt(0, dutyStations.length - 1)];
        const randomDate = getRandomDate(eightMonthsAgo, today);
        const beneficiaryCount = getRandomInt(15, 40);
        const sessionTargetAchievedPct = parseFloat(getRandomFloat(40, 100).toFixed(1));
        const accountsOpenedMW = getRandomInt(0, Math.floor(beneficiaryCount * 0.3));
        const accountsOpenedBank = getRandomInt(0, Math.floor(beneficiaryCount * 0.2));
        const lastReportDaysAgo = getRandomInt(0, 10);
        const avgTrainingTimeHours = parseFloat(getRandomFloat(3.5, 5.0).toFixed(1));
        
        let age20_25 = getRandomInt(Math.floor(beneficiaryCount * 0.1), Math.floor(beneficiaryCount * 0.3));
        let age26_35 = getRandomInt(Math.floor(beneficiaryCount * 0.2), Math.floor(beneficiaryCount * 0.5));
        let age36_45 = getRandomInt(Math.floor(beneficiaryCount * 0.1), Math.floor(beneficiaryCount * 0.3));
        let age45_Plus = beneficiaryCount - (age20_25 + age26_35 + age36_45);
        if (age45_Plus < 0) {
            age45_Plus = 0;
            age36_45 = Math.max(0, beneficiaryCount - (age20_25 + age26_35));
        }
        const currentSum = age20_25 + age26_35 + age36_45 + age45_Plus;
        if (currentSum !== beneficiaryCount) {
            age26_35 += (beneficiaryCount - currentSum);
        }

        const fakeCNICCount = getRandomInt(0, Math.floor(beneficiaryCount * 0.05));
        const latMin = 24.0, latMax = 37.0;
        const lonMin = 60.0, lonMax = 78.0;

        data.push({
            "TrainingID": i, "Training_Date": randomDate.toISOString().split('T')[0], "Province": randomProvince,
            "District": randomDistrict, "ASPC_ID": `ASPC${getRandomInt(100, 150)}`, "ASPC_Name": randomASPCName,
            "Duty_Station": randomDutyStation, "Beneficiary_Count_Actual": beneficiaryCount,
            "Session_Target_Achieved_Pct": sessionTargetAchievedPct, "Accounts_Opened_MW": accountsOpenedMW,
            "Accounts_Opened_Bank": accountsOpenedBank, "Last_Report_Days_Ago": lastReportDaysAgo,
            "Trainer_Total_Trainings": trainerStats[randomASPCName].totalTrainings++,
            "Avg_Training_Time_Hours": avgTrainingTimeHours, "Age_Group_20_25": age20_25,
            "Age_Group_26_35": age26_35, "Age_Group_36_45": age36_45, "Age_Group_45_Plus": age45_Plus,
            "Fake_CNIC_Count": fakeCNICCount, "Total_Attendees_For_Fake_CNIC_Session": beneficiaryCount,
            "Start_Location_Lat": parseFloat(getRandomFloat(latMin, latMax).toFixed(4)),
            "Start_Location_Lon": parseFloat(getRandomFloat(lonMin, lonMax).toFixed(4))
        });
    }
    return data;
}

// Generate the data and store it in a global constant
const trainingData = generateRandomTrainingData(500);
