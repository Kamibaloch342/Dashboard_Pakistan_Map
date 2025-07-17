// --- GLOBAL APP STATE ---
let map, markers = L.featureGroup(), heatLayer;
let provinceDataSummary = {}; // To be filled by precalculateProvincialSummary
let monthlyTrendChart, ageGroupPieChart, fakeCnicPieChart;

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    if (!trainingData || trainingData.length === 0) {
        console.error("Mock data is missing or empty!");
        alert("Could not load mock data. Dashboard cannot be displayed.");
        return;
    }
    
    console.log("Data loaded:", trainingData.length, "rows");

    // Start clock
    updateTime();
    setInterval(updateTime, 1000);

    // Setup UI components
    populateFilters(trainingData);
    populateProvinceButtons(trainingData);
    initializeMap();
    initializeCharts();
    
    // Process data
    precalculateProvincialSummary(trainingData);

    // Initial dashboard render
    updateDashboard();

    // Add event listeners
    document.querySelector('.chart-filter-buttons').addEventListener('click', (event) => {
        if (event.target.classList.contains('chart-filter-button')) {
            document.querySelector('.chart-filter-buttons').querySelectorAll('.chart-filter-button').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            updateDashboard(); // Redraw chart with new unit
        }
    });
    
    document.getElementById('toggleHeatmap').addEventListener('click', toggleHeatmap);

    // Select the first province by default
    const firstProvinceButton = document.querySelector('#provinceButtons .province-button');
    if (firstProvinceButton) {
        firstProvinceButton.click();
    }
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
        provinceDataSummary[provinceName].accounts += (item.Accounts_Opened_MW || 0) + (item.Accounts_Opened_Bank || 0);
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
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', { 
        attribution: '&copy; <a href="https://carto.com/attributions">CARTO</a>',
        className: 'map-tiles-light' 
    }).addTo(map);
    markers.addTo(map);
    heatLayer = L.heatLayer([], { radius: 25, blur: 15, maxZoom: 10, gradient: {0.4: '#60a5fa', 0.65: '#2dd4bf', 1: '#ef4444'} });

    L.Control.Custom = L.Control.extend({
        onAdd: function(map) {
            const div = L.DomUtil.create('div');
            div.innerHTML = this.options.content;
            L.DomUtil.addClass(div, this.options.classes);
            L.DomEvent.disableClickPropagation(div);
            return div;
        },
        onRemove: function(map) {}
    });
    L.control.custom = (opts) => new L.Control.Custom(opts);

    const alertsOverlayDiv = document.getElementById('alertsOverlay');
    if (alertsOverlayDiv) {
        L.control.custom({
            position: 'bottomleft',
            content: alertsOverlayDiv.outerHTML,
            classes: 'leaflet-control-alerts-overlay'
        }).addTo(map);
        alertsOverlayDiv.remove();
    }
}

function initializeCharts() {
    const ticksColor = CHART_COLORS.text, gridColor = '#e5e7eb';
    const defaultOptions = { 
        responsive: true, maintainAspectRatio: false,
        plugins: { 
            legend: { display: false, labels: { color: ticksColor, font: { family: 'Montserrat' } } },
            tooltip: {
                titleColor: CHART_COLORS.text, bodyColor: CHART_COLORS.text, backgroundColor: '#fff',
                borderColor: '#d1d5db', borderWidth: 1, boxPadding: 4,
                bodyFont: { family: 'Montserrat' }, titleFont: { family: 'Montserrat' },
            }
        },
        scales: {
            x: { ticks: { color: ticksColor, font: { family: 'Montserrat' } }, grid: { color: gridColor } },
            y: { ticks: { color: ticksColor, font: { family: 'Montserrat' } }, grid: { color: gridColor } }
        }
    };
    
    monthlyTrendChart = new Chart(document.getElementById('monthlyTrendChart').getContext('2d'), {
        type: 'line',
        data: { labels: [], datasets: [{ data: [], borderWidth: 2, tension: 0.3, pointRadius: 3, pointBackgroundColor: CHART_COLORS.primary, borderColor: CHART_COLORS.primary }] },
        options: {
            ...defaultOptions,
            scales: {
                x: { type: 'time', time: { unit: 'month' }, ticks: { color: ticksColor, font: { family: 'Montserrat' } }, grid: { color: gridColor } },
                y: { beginAtZero: true, ticks: { color: ticksColor, font: { family: 'Montserrat' } }, grid: { color: gridColor } }
            },
            plugins: { ...defaultOptions.plugins, annotation: { annotations: { targetLine: { type: 'line', yScaleID: 'y', value: 0, borderColor: CHART_COLORS.danger, borderWidth: 2, borderDash: [6, 6], label: { content: 'Target', enabled: true, position: 'end', color: CHART_COLORS.danger, font: { family: 'Montserrat', size: 10 } } } } } }
        }
    });
}

function toggleHeatmap() {
    if (map.hasLayer(heatLayer)) {
        map.removeLayer(heatLayer);
        map.addLayer(markers);
    } else {
        map.removeLayer(markers);
        map.addLayer(heatLayer);
    }
}

// --- MAIN UPDATE ORCHESTRATOR ---
function updateDashboard() {
    const provinceFilterValue = document.getElementById('provinceFilter').value;
    const filteredData = trainingData.filter(item => provinceFilterValue === 'All' || item.Province === provinceFilterValue);
    
    // These functions use the globally available `trainingData` for rankings that should not be filtered.
    updateLeaderboard(trainingData);
    updateProvincialRanking(trainingData);
    updateAlerts(trainingData);
    
    // These functions use the `filteredData` based on the user's selection.
    updateKPIs(filteredData, provinceFilterValue);
    updateMapAndHeatmap(filteredData);
    
    const activeUnitButton = document.querySelector('.chart-filter-buttons .active');
    const currentUnit = activeUnitButton ? activeUnitButton.dataset.unit : 'month';
    updateMonthlyTrendChart(filteredData, currentUnit);
}
