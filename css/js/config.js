// --- GLOBAL VARIABLES & CONSTANTS ---
const globalTargets = {
    provinces: { 
        "Punjab": {target_beneficiaries: 90000}, 
        "Sindh": {target_beneficiaries: 60000}, 
        "Khyber Pakhtunkhwa": {target_beneficiaries: 35000}, 
        "Balochistan": {target_beneficiaries: 20000},
        "Gilgit-Baltistan": {target_beneficiaries: 10000},
        "Azad Jammu & Kashmir": {target_beneficiaries: 15000}
    },
    totalBeneficiaryTarget: 230000,
    totalTrainingTarget: 1500
}; 

const AVERAGE_CLASSROOM_HOURS_PER_DAY = 4;
const MONTHLY_TARGET_PER_TRAINER = 240;

const CHART_COLORS = {
    primary: '#4f46e5', // Indigo-600
    secondary: '#2dd4bf', // Teal-500
    tertiary: '#fbbf24', // Amber-400
    danger: '#ef4444', // Red-500
    info: '#60a5fa', // Blue-400
    success: '#34d399', // Green-500
    background: '#f3f4f6',
    text: '#1f2937'
};

const provinceColors = { 
    "Punjab": "#22c55e", 
    "Sindh": "#3b82f6", 
    "Khyber Pakhtunkhwa": "#f97316", 
    "Balochistan": "#ef4444", 
    "Gilgit-Baltistan": "#a855f7", 
    "Azad Jammu & Kashmir": "#06b6d4" 
};
