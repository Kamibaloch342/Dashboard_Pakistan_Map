// --- UI & TIME FUNCTIONS ---
function updateTime() {
    const now = new Date();
    document.getElementById('currentTime').textContent = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
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
        button.addEventListener('click', () => filterByProvince(provinceName));
        provinceButtonsContainer.appendChild(button);
    });
}

// --- COMPONENT UPDATE FUNCTIONS ---
function updateKPIs(data, currentFilterProvince) {
    const totalBeneficiaries = data.reduce((s, i) => s + (i.Beneficiary_Count_Actual || 0), 0);
    const totalTrainings = data.length;

    let overallBeneficiaryTarget = globalTargets.totalBeneficiaryTarget;
    let overallTrainingTarget = globalTargets.totalTrainingTarget;

    if (currentFilterProvince !== 'All') {
        const provinceTargetData = globalTargets.provinces[currentFilterProvince];
        overallBeneficiaryTarget = provinceTargetData ? provinceTargetData.target_beneficiaries : 0;
        const totalGlobalBeneficiaryTarget = Object.values(globalTargets.provinces).reduce((sum, p) => sum + p.target_beneficiaries, 0);
        const provinceBeneficiaryTargetRatio = totalGlobalBeneficiaryTarget > 0 ? (overallBeneficiaryTarget / totalGlobalBeneficiaryTarget) : 0;
        overallTrainingTarget = Math.max(1, Math.round(globalTargets.totalTrainingTarget * provinceBeneficiaryTargetRatio));
    }
    
    const beneficiariesTargetPct = overallBeneficiaryTarget > 0 ? Math.min(100, (totalBeneficiaries / overallBeneficiaryTarget) * 100) : 0;
    const trainingsTargetPct = overallTrainingTarget > 0 ? Math.min(100, (totalTrainings / overallTrainingTarget) * 100) : 0;

    document.getElementById('totalBeneficiaries').textContent = totalBeneficiaries.toLocaleString();
    document.getElementById('beneficiariesTargetPct').textContent = `${beneficiariesTargetPct.toFixed(1)}% of target`;
    document.getElementById('beneficiariesProgressBar').style.width = `${beneficiariesTargetPct}%`;

    document.getElementById('totalTrainings').textContent = totalTrainings.toLocaleString();
    document.getElementById('trainingsTargetPct').textContent = `${trainingsTargetPct.toFixed(1)}% of target`;
    document.getElementById('trainingsProgressBar').style.width = `${trainingsTargetPct}%`;

    // Top Province KPI (based on all data, not filtered data)
    let topProvinceName = 'N/A';
    let maxProvinceAchievedPct = 0;
    for (const pName in provinceDataSummary) {
        const provinceTarget = globalTargets.provinces[pName]?.target_beneficiaries || 0;
        const achievedPct = provinceTarget > 0 ? (provinceDataSummary[pName].beneficiaries / provinceTarget) * 100 : 0;
        if (achievedPct > maxProvinceAchievedPct) {
            maxProvinceAchievedPct = achievedPct;
            topProvinceName = pName;
        }
    }
    document.getElementById('topProvinceName').textContent = topProvinceName;
    document.getElementById('topProvincePct').textContent = `${maxProvinceAchievedPct.toFixed(1)}% Target Achieved`;
    document.getElementById('topProvinceProgressBar').style.width = `${Math.min(100, maxProvinceAchievedPct)}%`;
}

function updateMap(data) {
    markerClusterGroup.clearLayers(); // Use the global marker cluster group
    
    data.forEach(item => {
        const lat = parseFloat(item.Start_Location_Lat);
        const lon = parseFloat(item.Start_Location_Lon);

        if (!isNaN(lat) && !isNaN(lon)) {
            const popupContent = `
                <div class="font-sans text-gray-50">
                    <div class="font-bold text-base mb-1 text-indigo-300">${item.ASPC_Name || 'N/A'}</div>
                    <div class="text-xs text-gray-400 mb-2">Duty Station: ${item.Duty_Station || 'N/A'}</div>
                    <div class="text-sm text-gray-300"><strong>Beneficiaries:</strong> <span class="text-indigo-400 font-bold">${item.Beneficiary_Count_Actual || 0}</span></div>
                    <div class="text-xs text-gray-400 mt-2">${item.Training_Date || 'N/A'} in ${item.District || 'N/A'}</div>
                </div>`;

            const marker = L.marker([lat, lon], {
                icon: L.divIcon({
                    html: `<div class="w-3 h-3 bg-teal-400 rounded-full border-2 border-gray-900 shadow-lg"></div>`,
                    className: '',
                    iconSize: [12, 12],
                })
            }).bindPopup(popupContent, { maxWidth: 250 });
            
            markerClusterGroup.addLayer(marker);
        }
    });
}


function updateProvincialSummaryContent(selectedProvinceName) {
    const container = document.getElementById('provincialSummaryContent');
    const provinceData = provinceDataSummary[selectedProvinceName];

    if (!provinceData) {
        container.innerHTML = `<p class="text-gray-500 text-sm col-span-3">No data available for ${selectedProvinceName}.</p>`;
        return;
    }

    // 1. Calculate data for charts
    const avgTrainingTime = provinceData.training_count_for_avg_time > 0 ? (provinceData.total_training_time / provinceData.training_count_for_avg_time) : 0;
    const avgTimePct = Math.min(100, (avgTrainingTime / (AVERAGE_CLASSROOM_HOURS_PER_DAY * 1.5)) * 100);

    const totalAgeAttendees = Object.values(provinceData.age_groups).reduce((sum, val) => sum + val, 0);
    const ageGroupData = Object.entries(provinceData.age_groups).map(([group, count]) => ({
        label: group,
        percent: totalAgeAttendees > 0 ? (count / totalAgeAttendees) * 100 : 0
    }));

    const totalCNICs = provinceData.total_attendees_for_fake_cnic;
    const fakeCNICPercentage = totalCNICs > 0 ? (provinceData.fake_cnics / totalCNICs) * 100 : 0;

    // 2. Draw the new visualizations
    container.innerHTML = `
        <!-- Chart 1: Avg Training Time -->
        <div class="flex flex-col items-center justify-center gap-2 p-2 rounded-lg bg-gray-900/50">
            <h5 class="text-xs font-semibold text-gray-400">Avg. Training Time</h5>
            ${createRadialBar(avgTrainingTime.toFixed(1), 'hrs', avgTimePct, CHART_COLORS.primary)}
        </div>

        <!-- Chart 2: Age Groups -->
        <div class="flex flex-col items-center justify-center gap-2 p-2 rounded-lg bg-gray-900/50">
            <h5 class="text-xs font-semibold text-gray-400">Female Attendee Age Groups</h5>
            ${createHorizontalBarChart(ageGroupData, [CHART_COLORS.primary, CHART_COLORS.secondary, CHART_COLORS.tertiary, CHART_COLORS.danger])}
        </div>

        <!-- Chart 3: CNIC Validity -->
        <div class="flex flex-col items-center justify-center gap-2 p-2 rounded-lg bg-gray-900/50">
            <h5 class="text-xs font-semibold text-gray-400">CNIC Validity</h5>
            ${createProportionalBar(fakeCNICPercentage)}
        </div>
    `;
}

function createRadialBar(value, label, percent, color) {
    const strokeWidth = 8;
    const size = 80;
    const radius = (size / 2) - (strokeWidth * 2);
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (percent / 100) * circumference;

    return `
        <div class="relative" style="width:${size}px; height:${size}px;">
            <svg class="absolute top-0 left-0" width="${size}" height="${size}" viewbox="0 0 ${size} ${size}" style="transform: rotate(-90deg);">
                <circle class="stroke-current text-gray-700" stroke-width="${strokeWidth}" fill="transparent" r="${radius}" cx="${size/2}" cy="${size/2}"></circle>
                <circle class="stroke-current" style="color:${color};"
                    stroke-width="${strokeWidth}"
                    stroke-linecap="round"
                    fill="transparent"
                    r="${radius}"
                    cx="${size/2}"
                    cy="${size/2}"
                    stroke-dasharray="${circumference} ${circumference}"
                    stroke-dashoffset="${offset}"
                    transform-origin="center"
                    ></circle>
            </svg>
            <div class="absolute top-0 left-0 w-full h-full flex flex-col items-center justify-center">
                <span class="text-xl font-extrabold text-white">${value}</span>
                <span class="text-xs text-gray-400">${label}</span>
            </div>
        </div>
    `;
}

function createHorizontalBarChart(data, colors) {
    let barsHtml = data.map((item, index) => `
        <div class="h-bar-item">
            <div class="h-bar-label">${item.label}</div>
            <div class="h-bar-bg">
                <div class="h-bar-value" style="width: ${item.percent}%; background-color:${colors[index % colors.length]};"></div>
            </div>
            <div class="h-bar-percent">${item.percent.toFixed(0)}%</div>
        </div>
    `).join('');
    return `<div class="h-bar-chart-container">${barsHtml}</div>`;
}

function createProportionalBar(fakePercent) {
    const validPercent = 100 - fakePercent;
    return `
        <div class="prop-bar-container w-full flex-grow justify-center">
            <div class="prop-bar">
                <div class="prop-bar-segment" style="width: ${validPercent}%; background-color: ${CHART_COLORS.success};"></div>
                <div class="prop-bar-segment" style="width: ${fakePercent}%; background-color: ${CHART_COLORS.danger};"></div>
            </div>
            <div class="prop-bar-legend">
                <div class="prop-bar-legend-item">
                    <div class="legend-dot" style="background-color: ${CHART_COLORS.success};"></div>
                    <span>Valid (${validPercent.toFixed(1)}%)</span>
                </div>
                <div class="prop-bar-legend-item">
                    <div class="legend-dot" style="background-color: ${CHART_COLORS.danger};"></div>
                    <span>Fake (${fakePercent.toFixed(1)}%)</span>
                </div>
            </div>
        </div>
    `;
}


function updateMonthlyTrendChart(data) {
    const aggregatedData = {};
    const eightMonthsAgo = new Date();
    eightMonthsAgo.setMonth(eightMonthsAgo.getMonth() - 7);
    eightMonthsAgo.setDate(1);

    data.forEach(item => {
        const date = new Date(item.Training_Date);
        if (date >= eightMonthsAgo) {
            const key = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-01`;
            aggregatedData[key] = (aggregatedData[key] || 0) + (item.Beneficiary_Count_Actual || 0);
        }
    });

    const labels = [];
    const values = [];
    for (let i = 0; i < 8; i++) {
        const date = new Date(eightMonthsAgo);
        date.setMonth(eightMonthsAgo.getMonth() + i);
        const key = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-01`;
        labels.push(new Date(key));
        values.push(aggregatedData[key] || 0);
    }

    monthlyTrendChart.data.labels = labels;
    monthlyTrendChart.data.datasets[0].data = values;
    monthlyTrendChart.update();
}

function updateProvincialRanking(data) {
    const tableBody = document.getElementById('provincialRankingTableBody');
    tableBody.innerHTML = '';
    
    const sortedProvinces = Object.entries(provinceDataSummary)
        .map(([name, summary]) => {
            const target = globalTargets.provinces[name]?.target_beneficiaries || 0;
            const percent = target > 0 ? (summary.beneficiaries / target) * 100 : 0;
            return { name, beneficiaries: summary.beneficiaries, percent };
        })
        .sort((a, b) => b.beneficiaries - a.beneficiaries);
        
    if (sortedProvinces.length === 0) {
        tableBody.innerHTML = `<tr><td colspan="4" class="px-4 py-3 text-center text-gray-500">No provincial data.</td></tr>`;
    } else {
        sortedProvinces.forEach((province, index) => {
            const color = province.percent > 80 ? CHART_COLORS.success : province.percent > 50 ? CHART_COLORS.tertiary : CHART_COLORS.danger;
            const row = document.createElement('tr');
            row.className = 'border-b border-gray-800';
            row.innerHTML = `
                <td class="px-4 py-3 font-medium text-gray-300">${index + 1}</td>
                <td class="px-4 py-3 text-gray-300">${province.name}</td>
                <td class="px-4 py-3 text-gray-300">${province.beneficiaries.toLocaleString()}</td>
                <td class="px-4 py-3">
                    <div class="flex items-center gap-2">
                        <div class="w-full bg-gray-700 rounded-full h-2">
                            <div class="h-2 rounded-full" style="width: ${Math.min(100, province.percent)}%; background-color: ${color};"></div>
                        </div>
                        <span class="font-semibold text-xs" style="color: ${color};">${province.percent.toFixed(1)}%</span>
                    </div>
                </td>`;
            tableBody.appendChild(row);
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
        tableBody.innerHTML = `<tr><td colspan="3" class="px-4 py-3 text-center text-gray-500">No trainer data this month.</td></tr>`;
    } else {
        sortedTrainers.forEach(([name, total]) => {
            const percent = Math.min(100, (total / MONTHLY_TARGET_PER_TRAINER) * 100);
            tableBody.innerHTML += `
                <tr class="border-b border-gray-800">
                    <td class="px-4 py-3 font-medium text-gray-300">${name}</td>
                    <td class="px-4 py-3 text-gray-300">${total.toLocaleString()}</td>
                    <td class="px-4 py-3">
                        <div class="w-full bg-gray-700 rounded-full h-2">
                            <div class="bg-green-500 h-2 rounded-full" style="width: ${percent}%"></div>
                        </div>
                    </td>
                </tr>`;
        });
    }
}
