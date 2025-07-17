// --- GLOBAL APP STATE ---
let map, markerClusterGroup, geoJsonLayer;
let provinceDataSummary = {};
let monthlyTrendChart;

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    if (!trainingData || trainingData.length === 0) {
        console.error("Mock data is missing or empty!");
        alert("Could not load mock data.");
        return;
    }
    
    updateTime();
    setInterval(updateTime, 1000);

    populateFilters(trainingData);
    populateProvinceButtons(trainingData);
    initializeMap();
    initializeCharts();
    
    precalculateProvincialSummary(trainingData);
    updateDashboard();

    // Add event listeners
    document.getElementById('provinceFilter').addEventListener('change', updateDashboard);
});

// --- CORE FUNCTIONS ---
function precalculateProvincialSummary(data) {
    provinceDataSummary = {};
    data.forEach(item => {
        const provinceName = item.Province;
        if (!provinceDataSummary[provinceName]) {
            provinceDataSummary[provinceName] = {
                trainings: 0, beneficiaries: 0, accounts: 0,
                total_training_time: 0, training_count_for_avg_time: 0,
                age_groups: {'20-25': 0, '26-35': 0, '36-45': 0, '45+': 0},
                fake_cnics: 0, total_attendees_for_fake_cnic: 0
            };
        }
        provinceDataSummary[provinceName].trainings++;
        provinceDataSummary[provinceName].beneficiaries += item.Beneficiary_Count_Actual || 0;
        if (item.Avg_Training_Time_Hours) {
            provinceDataSummary[provinceName].total_training_time += parseFloat(item.Avg_Training_Time_Hours);
            provinceDataSummary[provinceName].training_count_for_avg_time++;
        }
        provinceDataSummary[provinceName].age_groups['20-25'] += item.Age_Group_20_25 || 0;
        provinceDataSummary[provinceName].age_groups['26-35'] += item.Age_Group_26_35 || 0;
        provinceDataSummary[provinceName].age_groups['36-45'] += item.Age_Group_36_45 || 0;
        provinceDataSummary[provinceName].age_groups['45+'] += item.Age_Group_45_Plus || 0;
        provinceDataSummary[provinceName].fake_cnics += item.Fake_CNIC_Count || 0;
        provinceDataSummary[provinceName].total_attendees_for_fake_cnic += item.Total_Attendees_For_Fake_CNIC_Session || 0;
    });
}

function initializeMap() {
    map = L.map('map', { zoomControl: false, attributionControl: false }).setView([30.3753, 69.3451], 5.5);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', { 
        attribution: '&copy; <a href="https://carto.com/attributions">CARTO</a>',
    }).addTo(map);

    markerClusterGroup = L.markerClusterGroup().addTo(map);

    // Initialize GeoJSON layer for provinces
    geoJsonLayer = L.geoJson(provincesData, {
        style: function(feature) {
            return {
                color: provinceColors[feature.properties.PROVINCE] || '#ffffff',
                weight: 1.5,
                opacity: 0.6,
                fillColor: provinceColors[feature.properties.PROVINCE] || '#ffffff',
                fillOpacity: 0.1
            };
        },
        onEachFeature: function(feature, layer) {
            layer.on({
                mouseover: e => {
                    const l = e.target;
                    l.setStyle({ weight: 3, opacity: 1, fillOpacity: 0.3 });
                },
                mouseout: e => geoJsonLayer.resetStyle(e.target),
                click: e => filterByProvince(e.target.feature.properties.PROVINCE)
            });
        }
    }).addTo(map);
}

function initializeCharts() {
    const ticksColor = '#9ca3af', gridColor = 'rgba(55, 65, 81, 0.5)';
    
    monthlyTrendChart = new Chart(document.getElementById('monthlyTrendChart').getContext('2d'), {
        type: 'line',
        data: { labels: [], datasets: [{ 
            data: [], 
            borderColor: CHART_COLORS.primary,
            backgroundColor: 'rgba(79, 70, 229, 0.2)',
            borderWidth: 2, 
            tension: 0.4, 
            pointRadius: 0,
            pointHoverRadius: 5,
            pointBackgroundColor: CHART_COLORS.primary,
            fill: true
        }] },
        options: {
            responsive: true, maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { type: 'time', time: { unit: 'month' }, ticks: { color: ticksColor }, grid: { color: gridColor } },
                y: { beginAtZero: true, ticks: { color: ticksColor }, grid: { color: gridColor } }
            }
        }
    });
}

function filterByProvince(provinceName) {
    // Update the dropdown
    document.getElementById('provinceFilter').value = provinceName;
    
    // Update the active button
    document.querySelectorAll('.province-button').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.province === provinceName);
    });

    // Update the map style
    geoJsonLayer.eachLayer(layer => {
        if (layer.feature.properties.PROVINCE === provinceName) {
            layer.setStyle({ weight: 4, opacity: 1, fillOpacity: 0.4 });
        } else {
            geoJsonLayer.resetStyle(layer);
        }
    });

    // Re-render the dashboard with the new filter
    updateDashboard();
}


// --- MAIN UPDATE ORCHESTRATOR ---
function updateDashboard() {
    const provinceFilterValue = document.getElementById('provinceFilter').value;
    const filteredData = trainingData.filter(item => provinceFilterValue === 'All' || item.Province === provinceFilterValue);
    
    // Update components
    updateKPIs(filteredData, provinceFilterValue);
    updateMap(filteredData);
    updateMonthlyTrendChart(filteredData);
    updateProvincialRanking(trainingData); // Always show all provinces for ranking
    updateLeaderboard(trainingData); // Based on all data

    // If a specific province is selected, show its summary. Otherwise, show a default message.
    if (provinceFilterValue !== 'All') {
        updateProvincialSummaryContent(provinceFilterValue);
        document.querySelectorAll('.province-button').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.province === provinceFilterValue);
        });
    } else {
        document.getElementById('provincialSummaryContent').innerHTML = `<p class="text-gray-500 text-sm col-span-3 text-center">Select a province to see details.</p>`;
        document.querySelectorAll('.province-button').forEach(btn => btn.classList.remove('active'));
        geoJsonLayer.eachLayer(layer => geoJsonLayer.resetStyle(layer));
    }
}
