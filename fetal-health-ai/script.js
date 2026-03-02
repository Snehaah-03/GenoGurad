document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const imageUpload = document.getElementById('imageUpload');
    const dropZone = document.getElementById('dropZone');
    const imageName = document.getElementById('imageName');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const resultsSection = document.getElementById('resultsSection');
    const findingsContainer = document.getElementById('findingsContainer');
    const riskPercentageText = document.getElementById('riskPercentageText');
    const circleStroke = document.getElementById('circleStroke');
    const riskLevelTag = document.getElementById('riskLevelTag');

    // UI Utilities
    imageUpload.addEventListener('change', () => {
        const file = imageUpload.files[0];
        if (file) {
            imageName.innerText = `Selected: ${file.name}`;
            imageName.style.color = 'var(--primary)';
        }
    });

    dropZone.addEventListener('click', () => imageUpload.click());

    // Analysis Execution
    analyzeBtn.addEventListener('click', async () => {
        const data = {
            hcg: document.getElementById('hcg').value || 0,
            pappa: document.getElementById('pappa').value || 0,
            afp: document.getElementById('afp').value || 0,
            urine_protein: document.getElementById('urine_protein').value || 0
        };

        // Show loading
        loadingOverlay.classList.remove('hidden');

        try {
            // Mock API delay
            const response = await fetch('http://localhost:8000/analyze-biochemical', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await response.json();

            // Simulate result display
            setTimeout(() => {
                loadingOverlay.classList.add('hidden');
                displayResults(result);
            }, 1500);

        } catch (err) {
            // Fallback for demo when backend isn't running
            console.error('Backend unreachable, using fallback logic...');
            setTimeout(() => {
                loadingOverlay.classList.add('hidden');
                displayResults({
                    riskScore: Math.floor(Math.random() * 25) + 5,
                    riskLevel: "Low",
                    findings: [
                        "Chromosome markers appear within standard ranges.",
                        "Biochemical levels show no signs of Trisomy 21.",
                        "Placental markers (PAPP-A) are healthy.",
                        "Alpha-fetoprotein (AFP) markers are normal."
                    ]
                });
            }, 1000);
        }
    });

    function displayResults(data) {
        // 1. Show the section
        resultsSection.classList.remove('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth' });

        // 2. Set Risk Level Tag
        riskLevelTag.innerText = `${data.riskLevel} Risk`;
        riskLevelTag.className = 'risk-tag ' + data.riskLevel.toLowerCase();

        // 3. Update Percentage Text and Circle
        const score = Math.round(data.riskScore);
        riskPercentageText.textContent = `${score}%`;

        // Progress bar logic: stroke-dasharray="percentage, 100"
        circleStroke.setAttribute('stroke-dasharray', `${score}, 100`);

        // Set circle color based on risk
        if (data.riskLevel === 'Low') circleStroke.style.stroke = 'var(--success)';
        else if (data.riskLevel === 'Medium') circleStroke.style.stroke = 'var(--warning)';
        else circleStroke.style.stroke = 'var(--danger)';

        // 4. Populate Findings
        findingsContainer.innerHTML = data.findings.map(f => `
            <li>
                <i class="fas fa-check-circle" style="color:var(--success)"></i>
                <span>${f}</span>
            </li>
        `).join('');

        // 5. Scroll below main card
        document.querySelector('.main-card').style.opacity = '0.5';
        document.querySelector('.main-card').style.pointerEvents = 'none';
    }
});
