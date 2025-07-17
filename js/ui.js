// --- UI & TIME FUNCTIONS ---
function updateTime() {
    const now = new Date();
    document.getElementById('currentTime').textContent = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    document.getElementById('currentDate').textContent = now.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });
}

function populateFilters(data) {
    const provinceFilter = document.getElementById('provinceFilter');
    provinceFilter.innerHTML = '<option value="All">All Provinces</option>';
    [...new Set(data.map(item => item.Province).filter(Boolean))].sort().forEach(p => {
        provinceFilter.add(new Option(p, p));
    });
}

function populateProvinceButtons(data) {
    const provinceButtonsContainer = document.getElementById('provinceButtons');
    provinceButtonsContainer.innerHTML = '';
    const uniqueProvinces = [...new Set(data.map(item => item.Province).filter(Boolean))].sort();

    uniqueProvinces.forEach(provinceName => {
        const button = document.createElement('button');
        button.textContent = provinceName;
        button.classList.add('province-button');
        button.dataset.province = provinceName;
        button.addEventListener('click', () => {
            document.querySelectorAll('.province-button').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            updateProvincialSummaryContent(provinceName);
        });
        provinceButtonsContainer.appendChild(button);
    });
}

// --- COMPONENT UPDATE FUNCTIONS ---
function animateValue(obj, start, end, duration, isPercent = false) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = Math.floor(progress * (end - start) + start);
        obj.innerHTML = value.toLocaleString() + (isPercent ? '%' : '');
        if (progress < 1) window.requestAnimationFrame(step);
    };
    window.requestAnimationFrame(step);
}

function updateKPIs(data, currentFilterProvince) {
    const totalBeneficiaries = data.reduce((s, i) => s + (i.Beneficiary_Count_Actual || 0), 0);
    const totalTrainings = data.length;

    let overallBeneficiaryTarget = 0;
    let overallTrainingTarget = globalTargets.totalTrainingTarget;

    if (currentFilterProvince === 'All') {
        overallBeneficiaryTarget = globalTargets.totalBeneficiaryTarget;
    } else {
        const provinceTargetData = globalTargets.provinces[currentFilterProvince];
        overallBeneficiaryTarget = provinceTargetData ? provinceTargetData.target_beneficiaries : 0;
        const totalGlobalBeneficiaryTarget = Object.values(globalTargets.provinces).reduce((sum, p) => sum + p.target_beneficiaries, 0);
        const provinceBeneficiaryTargetRatio = totalGlobalBeneficiaryTarget > 0 ? (overallBeneficiaryTarget / totalGlobalBeneficiaryTarget) : 0;
        overallTrainingTarget = Math.max(1, Math.round(globalTargets.totalTrainingTarget * provinceBeneficiaryTargetRatio));
    }
    
    const beneficiariesTargetPct = overallBeneficiaryTarget > 0 ? ((totalBeneficiaries / overallBeneficiaryTarget) * 100).toFixed(1) : '0';
    const trainingsTargetPct = overallTrainingTarget > 0 ? ((totalTrainings / overallTrainingTarget) * 100).toFixed(1) : '0';

    animateValue(document.getElementById('totalBeneficiaries'), 0, totalBeneficiaries, 1000);
    document.getElementById('beneficiariesTargetPct').textContent = `${beneficiariesTargetPct}% Target`;

    animateValue(document.getElementById('totalTrainings'), 0, totalTrainings, 1000);
    document.getElementById('trainingsTargetPct').textContent = `${trainingsTargetPct}% Target`;

    let topProvince = null;
    let maxProvinceAchievedPct = -1;

    for (const pName in globalTargets.provinces) {
        const currentBeneficiaries = provinceDataSummary[pName] ? provinceDataSummary[pName].beneficiaries : 0;
        const provinceTarget = globalTargets.provinces[pName].target_beneficiaries;
        const achievedPct = provinceTarget > 0 ? (currentBeneficiaries / provinceTarget) * 100 : 0;

        if (achievedPct > maxProvinceAchievedPct) {
            maxProvinceAchievedPct = achievedPct;
            topProvince = pName;
        }
    }
    document.getElementById('topProvinceName').textContent = topProvince || 'N/A';
    document.getElementById('topProvincePct').textContent = `${maxProvinceAchievedPct.toFixed(1)}% Target Achieved`;
}

function updateMapAndHeatmap(data) {
    markers.clearLayers();
    const heatPoints = [];
    const maxBeneficiaryCount = Math.max(...data.map(item => item.Beneficiary_Count_Actual || 0), 1);

    data.forEach(item => {
        const lat = parseFloat(item.Start_Location_Lat);
        const lon = parseFloat(item.Start_Location_Lon);

        if (!isNaN(lat) && !isNaN(lon)) {
            const latLng = [lat, lon];
            heatPoints.push([...latLng, (item.Beneficiary_Count_Actual || 0) / maxBeneficiaryCount]);

            const markerSize = 14 + ((item.Beneficiary_Count_Actual || 0) / maxBeneficiaryCount) * 20;
            const markerIcon = L.divIcon({
                html: `<div class="relative flex items-center justify-center"><div class="location-dot-pulse" style="width:${markerSize*1.5}px; height:${markerSize*1.5}px; background-color:${provinceColors[item.Province] || '#4f46e5'}1A;"></div><div class="location-dot" style="width:${markerSize}px; height:${markerSize}px; background-color:${provinceColors[item.Province] || '#4f46e5'};"><svg viewBox="0 0 24 24" fill="white" width="${markerSize*0.6}" height="${markerSize*0.6}"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5S10.62 6.5 12 6.5s2.5 1.12 2.5 2.5S13.38 11.5 12 11.5z"/></svg></div></div>`,
                className: 'leaflet-div-icon',
                iconSize: [markerSize * 1.5, markerSize * 1.5],
                iconAnchor: [markerSize * 0.75, markerSize * 0.75]
            });
            const popupContent = `<div style="font-family: 'Montserrat', sans-serif; color: #1f2937;"><div class="font-bold text-base mb-1">${item.ASPC_Name || 'N/A'}</div><div class="text-xs text-gray-600 mb-2">Duty Station: ${item.Duty_Station || 'N/A'}</div><div class="text-sm text-gray-700"><strong>Beneficiaries:</strong> <span class="text-indigo-600 font-bold">${item.Beneficiary_Count_Actual || 0}</span></div><div class="text-sm text-gray-700"><strong>Target Achieved:</strong> <span class="${parseFloat(item.Session_Target_Achieved_Pct) >= 100 ? 'text-green-600' : 'text-orange-500'} font-bold">${item.Session_Target_Achieved_Pct || '0'}%</span></div><div class="text-sm text-gray-700"><strong>Under IC:</strong> ${item.ASPC_ID || 'N/A'}</div><div class="text-sm text-gray-700"><strong>Total Trainings by Trainer:</strong> ${item.Trainer_Total_Trainings || 'N/A'}</div><div class="text-xs text-gray-500 mt-2">Date: ${item.Training_Date || 'N/A'} in ${item.District || 'N/A'}, ${item.Province || 'N/A'}</div></div>`;

            L.marker(latLng, { icon: markerIcon }).bindPopup(popupContent, { maxWidth: 250 }).addTo(markers);
        }
    });
    heatLayer.setLatLngs(heatPoints);
    if (markers.getLayers().length > 0) map.fitBounds(markers.getBounds().pad(0.1));
    else map.setView([30.3753, 69.3451], 5.5);
}

function updateProvincialSummaryContent(selectedProvinceName) {
    const provincialSummaryContent = document.getElementById('provincialSummaryContent');
    const provinceData = provinceDataSummary[selectedProvinceName];

    if (!provinceData) {
        provincialSummaryContent.innerHTML = `<p class="text-gray-500 text-sm">No data available for ${selectedProvinceName}.</p>`;
        if (ageGroupPieChart) ageGroupPieChart.destroy();
        if (fakeCnicPieChart) fakeCnicPieChart.destroy();
        return;
    }

    const avgTrainingTime = provinceData.training_count_for_avg_time > 0 ? (provinceData.total_training_time / provinceData.training_count_for_avg_time) : 0;
    const totalAgeAttendees = Object.values(provinceData.age_groups).reduce((sum, val) => sum + val, 0);
    const ageGroupLabels = Object.keys(provinceData.age_groups);
    const ageGroupPercentages = ageGroupLabels.map(group => totalAgeAttendees > 0 ? ((provinceData.age_groups[group] / totalAgeAttendees) * 100) : 0);
    const totalCNICs = provinceData.total_attendees_for_fake_cnic;
    const fakeCNICPercentage = totalCNICs > 0 ? ((provinceData.fake_cnics / totalCNICs) * 100) : 0;
    const validCNICPercentage = (100 - fakeCNICPercentage);

    provincialSummaryContent.innerHTML = `<div class="flex flex-col items-center justify-center w-full h-full"><h4 class="font-bold text-gray-800 text-lg mb-4">Detailed Performance for ${selectedProvinceName}</h4><div class="grid grid-cols-1 md:grid-cols-3 gap-4 w-full h-full flex-grow"><div class="province-metric-item"><h5 class="text-sm font-semibold text-gray-700">Avg. Training Time (Hours)</h5><div id="gauge-avg-time" class="gauge-container"></div><span class="gauge-label">Reference: ${AVERAGE_CLASSROOM_HOURS_PER_DAY} hours</span></div><div class="province-metric-item"><h5 class="text-sm font-semibold text-gray-700">Female Attendees Age Groups</h5><div class="chart-container"><canvas id="ageGroupPieChart"></canvas></div></div><div class="province-metric-item"><h5 class="text-sm font-semibold text-gray-700">Fake CNIC's vs Valid (%)</h5><div class="chart-container"><canvas id="fakeCnicPieChart"></canvas></div></div></div></div>`;
    
    drawGaugeChart('gauge-avg-time', avgTrainingTime, AVERAGE_CLASSROOM_HOURS_PER_DAY * 1.5);
    
    if (ageGroupPieChart) ageGroupPieChart.destroy();
    ageGroupPieChart = new Chart(document.getElementById('ageGroupPieChart').getContext('2d'), { type: 'pie', data: { labels: ageGroupLabels, datasets: [{ data: ageGroupPercentages, backgroundColor: ['rgba(79, 70, 229, 0.8)', 'rgba(45, 212, 191, 0.8)', 'rgba(251, 191, 36, 0.8)', 'rgba(239, 68, 68, 0.8)'], borderColor: CHART_COLORS.background, borderWidth: 1 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: true, position: 'right', labels: { color: CHART_COLORS.text, font: { family: 'Montserrat' } } }, tooltip: { callbacks: { label: (c) => `${c.label}: ${c.parsed.toFixed(1)}%` }}}} });

    if (fakeCnicPieChart) fakeCnicPieChart.destroy();
    fakeCnicPieChart = new Chart(document.getElementById('fakeCnicPieChart').getContext('2d'), { type: 'pie', data: { labels: ['Valid CNICs', 'Fake CNICs'], datasets: [{ data: [validCNICPercentage, fakeCNICPercentage], backgroundColor: [CHART_COLORS.success, CHART_COLORS.danger], borderColor: CHART_COLORS.background, borderWidth: 1 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: true, position: 'right', labels: { color: CHART_COLORS.text, font: { family: 'Montserrat' } } }, tooltip: { callbacks: { label: (c) => `${c.label}: ${c.parsed.toFixed(2)}%` }}}} });
}

function drawGaugeChart(containerId, value, maxValue) {
    const container = document.getElementById(containerId);
    if (!container) return;
    const size = 150, radius = 45, circumference = Math.PI * radius;
    let normalizedValue = maxValue > 0 ? Math.min(Math.max(value / maxValue, 0), 1) : 0;
    const arcLength = normalizedValue * circumference;
    const pathData = `M ${size/2 - radius} ${size/2} A ${radius} ${radius} 0 0 1 ${size/2 + radius} ${size/2}`;
    container.innerHTML = `<svg width="${size}" height="${size/2 + 20}" viewBox="0 0 ${size} ${size/2 + 20}" style="overflow:visible;"><path class="gauge-arc" d="${pathData}" transform="rotate(90 ${size/2} ${size/2})"></path><path class="gauge-value-arc" d="${pathData}" stroke-dasharray="${arcLength} ${circumference}" transform="rotate(90 ${size/2} ${size/2})" style="stroke: ${CHART_COLORS.primary};"></path></svg><div class="gauge-text" style="font-family: 'Montserrat', sans-serif !important;">${value.toFixed(1)} hrs</div>`;
}

function updateMonthlyTrendChart(data, unit = 'month') {
    const aggregatedData = {};
    const allDates = data.map(item => new Date(item.Training_Date));
    const latestDate = allDates.length > 0 ? new Date(Math.max(...allDates)) : new Date();
    const eightMonthsAgo = new Date(latestDate);
    eightMonthsAgo.setMonth(latestDate.getMonth() - 7);
    eightMonthsAgo.setDate(1);

    data.forEach(item => {
        const date = new Date(item.Training_Date);
        if (date >= eightMonthsAgo && date <= latestDate) {
            let key = (unit === 'day') ? date.toISOString().split('T')[0] : `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-01`;
            aggregatedData[key] = (aggregatedData[key] || 0) + (item.Beneficiary_Count_Actual || 0);
        }
    });

    const filledData = {};
    let currentDateIterator = new Date(eightMonthsAgo);
    while (currentDateIterator <= latestDate) {
        let key = (unit === 'day') ? currentDateIterator.toISOString().split('T')[0] : `${currentDateIterator.getFullYear()}-${(currentDateIterator.getMonth() + 1).toString().padStart(2, '0')}-01`;
        filledData[key] = aggregatedData[key] || 0;
        if (unit === 'day') currentDateIterator.setDate(currentDateIterator.getDate() + 1);
        else currentDateIterator.setMonth(currentDateIterator.getMonth() + 1);
    }
    
    const sortedKeys = Object.keys(filledData).sort();
    const labels = sortedKeys.map(key => new Date(key));
    const values = sortedKeys.map(key => filledData[key]);
    const targetPerMonth = globalTargets.totalBeneficiaryTarget / 8;
    let currentTargetValue = (unit === 'day') ? targetPerMonth / 30.4 : targetPerMonth;

    monthlyTrendChart.data.labels = labels;
    monthlyTrendChart.data.datasets[0].data = values.map((val, idx) => ({x: labels[idx], y: val}));
    monthlyTrendChart.data.datasets[0].label = `Beneficiaries per ${unit}`;
    monthlyTrendChart.options.scales.x.time.unit = unit;
    if (monthlyTrendChart.options.plugins.annotation.annotations.targetLine) {
        monthlyTrendChart.options.plugins.annotation.annotations.targetLine.value = currentTargetValue;
    }
    monthlyTrendChart.update();
}

function updateProvincialRanking(data) {
    const tableBody = document.getElementById('provincialRankingTableBody');
    tableBody.innerHTML = '';
    const sortedProvinces = Object.entries(provinceDataSummary)
        .map(([name, summary]) => [name, summary.beneficiaries])
        .sort((a, b) => b[1] - a[1]);
        
    if (sortedProvinces.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="3" class="px-4 py-2 text-center text-gray-500">No provincial data.</td></tr>`;
    } else {
        sortedProvinces.forEach(([provinceName, total], index) => {
            tableBody.innerHTML += `<tr class="border-b border-gray-200"><td class="px-4 py-2 font-medium text-gray-800">${index + 1}</td><td class="px-4 py-2 text-gray-700">${provinceName}</td><td class="px-4 py-2 text-gray-700">${total.toLocaleString()}</td></tr>`;
        });
    }
}

function updateLeaderboard(data) {
    const now = new Date();
    const monthlyData = data.filter(item => {
        const trainingDate = new Date(item.Training_Date);
        return trainingDate.getMonth() === now.getMonth() && trainingDate.getFullYear() === now.getFullYear();
    });

    const trainerPerformance = monthlyData.reduce((acc, item) => {
        if (item.ASPC_Name) {
            if (!acc[item.ASPC_Name]) acc[item.ASPC_Name] = 0;
            acc[item.ASPC_Name] += (item.Beneficiary_Count_Actual || 0);
        }
        return acc;
    }, {});
    const sortedTrainers = Object.entries(trainerPerformance).sort((a, b) => b[1] - a[1]).slice(0, 5);

    const tableBody = document.getElementById('leaderboardTableBody');
    tableBody.innerHTML = '';
    if (sortedTrainers.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="3" class="px-4 py-2 text-center text-gray-500">No trainer data this month.</td></tr>`;
    } else {
        sortedTrainers.forEach(([name, total]) => {
            const percent = Math.min(100, Math.round((total / MONTHLY_TARGET_PER_TRAINER) * 100));
            tableBody.innerHTML += `<tr class="border-b border-gray-200"><td class="px-4 py-2 font-medium text-gray-800">${name}</td><td class="px-4 py-2 text-gray-700">${total.toLocaleString()}</td><td class="px-4 py-2 text-gray-700"><div class="w-full bg-gray-300 rounded-full h-2.5"><div class="bg-green-500 h-2.5 rounded-full" style="width: ${percent}%"></div></div></td></tr>`;
        });
    }
}

function updateAlerts(data) {
    const alertsList = document.querySelector('.leaflet-control-alerts-overlay #alertsList');
    const alertsOverlayDiv = document.querySelector('.leaflet-control-alerts-overlay');

    if (!alertsList || !alertsOverlayDiv) {
        setTimeout(() => updateAlerts(data), 200);
        return;
    }

    alertsList.innerHTML = '';
    let hasAlerts = false;
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

    const recentData = data.filter(item => new Date(item.Training_Date) >= oneWeekAgo);

    recentData.filter(item => (item.Last_Report_Days_Ago || 0) > 3).slice(0, 3).forEach(item => {
        alertsList.innerHTML += `<li class="p-2 bg-yellow-100 border border-yellow-300 rounded-lg"><p class="font-bold text-yellow-700 text-xs">${item.ASPC_Name}</p><p class="text-xs text-gray-600">No report in ${item.Last_Report_Days_Ago} days (last training: ${item.Training_Date}).</p></li>`;
        hasAlerts = true;
    });
    
    recentData.filter(d => (d.Beneficiary_Count_Actual || 0) < 15).slice(0, 3).forEach(item => {
        alertsList.innerHTML += `<li class="p-2 bg-red-100 border border-red-300 rounded-lg"><p class="font-bold text-red-700 text-xs">${item.ASPC_Name} in ${item.District}</p><p class="text-xs text-gray-600">Low attendance (${item.Beneficiary_Count_Actual}) on ${item.Training_Date}.</p></li>`;
        hasAlerts = true;
    });

    if (!hasAlerts) {
        alertsList.innerHTML = `<li class="p-2 text-center text-gray-500">No system alerts.</li>`;
    }
    alertsOverlayDiv.style.display = hasAlerts ? 'flex' : 'none';
}
