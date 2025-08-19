// ========================================
//           TEAM SELECTOR DATA & VARIABLES
// ========================================

const teams = [
    { id: 'csk', name: 'Chennai Super Kings', logo: '/static/images/teams/csk.png', shortName: 'CSK' },
    { id: 'dc', name: 'Delhi Capitals', logo: '/static/images/teams/dc.png', shortName: 'DC' },
    { id: 'gt', name: 'Gujarat Titans', logo: '/static/images/teams/gt.png', shortName: 'GT' },
    { id: 'kkr', name: 'Kolkata Knight Riders', logo: '/static/images/teams/kkr.png', shortName: 'KKR' },
    { id: 'lsg', name: 'Lucknow Super Giants', logo: '/static/images/teams/lsg.png', shortName: 'LSG' },
    { id: 'mi', name: 'Mumbai Indians', logo: '/static/images/teams/mi.png', shortName: 'MI' },
    { id: 'pk', name: 'Punjab Kings', logo: '/static/images/teams/pk.png', shortName: 'PBKS' },
    { id: 'rr', name: 'Rajasthan Royals', logo: '/static/images/teams/rr.png', shortName: 'RR' },
    { id: 'rcb', name: 'Royal Challengers Bengaluru', logo: '/static/images/teams/rcb.png', shortName: 'RCB' },
    { id: 'srh', name: 'Sunrisers Hyderabad', logo: '/static/images/teams/srh.png', shortName: 'SRH' }
];

let selectedTeam1 = null;
let selectedTeam2 = null;

// ========================================
//           TEAM SELECTOR FUNCTIONS
// ========================================

// Initialize team grids
function initializeTeamSelectors() {
    const team1Grid = document.getElementById('team1Grid');
    const team2Grid = document.getElementById('team2Grid');

    // Only initialize if grids exist
    if (!team1Grid || !team2Grid) {
        console.log('Team selector grids not found, skipping initialization');
        return;
    }

    // Clear existing content
    team1Grid.innerHTML = '';
    team2Grid.innerHTML = '';

    // Create team cards for both grids
    teams.forEach(team => {
        team1Grid.appendChild(createTeamCard(team, 1));
        team2Grid.appendChild(createTeamCard(team, 2));
    });

    console.log('Team selectors initialized');
}

// Create a team card element
function createTeamCard(team, gridNumber) {
    const card = document.createElement('div');
    card.className = 'team-card';
    card.dataset.teamId = team.id;
    card.dataset.grid = gridNumber;
    
    card.innerHTML = `
        <div class="team-logo">
            <img src="${team.logo}" alt="${team.name}" onerror="this.src='./static/images/placeholder.png'">
        </div>
        <p class="team-name">${team.shortName}</p>
    `;
    
    card.addEventListener('click', function() {
        selectTeam(team, gridNumber, card);
    });
    
    return card;
}

// Handle team selection
function selectTeam(team, gridNumber, cardElement) {
    if (gridNumber === 1) {
        // Clear previous selection
        document.querySelectorAll('#team1Grid .team-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        // Set new selection
        selectedTeam1 = team;
        cardElement.classList.add('selected');
        
        // Update team 2 grid - disable already selected team
        updateTeam2Grid();
        
        // Store in hidden input
        const team1Input = document.getElementById('team1');
        if (team1Input) {
            team1Input.value = team.name;
            console.log('Team 1 selected:', team.name);
        }
        
    } else if (gridNumber === 2) {
        // Don't allow selecting the same team as team 1
        if (team.id === selectedTeam1?.id) {
            showError('Please select a different team for Team 2');
            return;
        }
        
        // Clear previous selection
        document.querySelectorAll('#team2Grid .team-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        // Set new selection
        selectedTeam2 = team;
        cardElement.classList.add('selected');
        
        // Store in hidden input
        const team2Input = document.getElementById('team2');
        if (team2Input) {
            team2Input.value = team.name;
            console.log('Team 2 selected:', team.name);
        }
    }
    
    // Update display
    updateSelectedTeamsDisplay();
}

// Update team 2 grid based on team 1 selection
function updateTeam2Grid() {
    document.querySelectorAll('#team2Grid .team-card').forEach(card => {
        if (selectedTeam1 && card.dataset.teamId === selectedTeam1.id) {
            card.classList.add('disabled');
        } else {
            card.classList.remove('disabled');
        }
    });
}

// Update the selected teams display
function updateSelectedTeamsDisplay() {
    const display = document.getElementById('selectedTeamsDisplay');
    
    if (!display) return;
    
    if (selectedTeam1 && selectedTeam2) {
        display.classList.add('show');
        
        const team1Logo = document.getElementById('team1DisplayLogo');
        const team1Name = document.getElementById('team1DisplayName');
        const team2Logo = document.getElementById('team2DisplayLogo');
        const team2Name = document.getElementById('team2DisplayName');
        
        if (team1Logo) team1Logo.src = selectedTeam1.logo;
        if (team1Name) team1Name.textContent = selectedTeam1.name;
        if (team2Logo) team2Logo.src = selectedTeam2.logo;
        if (team2Name) team2Name.textContent = selectedTeam2.name;
    } else {
        display.classList.remove('show');
    }
}

// Clear selection
function clearSelection() {
    selectedTeam1 = null;
    selectedTeam2 = null;
    
    document.querySelectorAll('.team-card').forEach(card => {
        card.classList.remove('selected', 'disabled');
    });
    
    const display = document.getElementById('selectedTeamsDisplay');
    if (display) {
        display.classList.remove('show');
    }
    
    // Clear hidden inputs
    const team1Input = document.getElementById('team1');
    const team2Input = document.getElementById('team2');
    if (team1Input) team1Input.value = '';
    if (team2Input) team2Input.value = '';
    
    console.log('Team selection cleared');
}

// Show error message
function showError(message) {
    const errorDiv = document.getElementById('error');
    if (errorDiv) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        errorDiv.style.animation = 'shake 0.3s ease';
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 3000);
    } else {
        // Create error div if it doesn't exist
        const newErrorDiv = document.createElement('div');
        newErrorDiv.id = 'error';
        newErrorDiv.className = 'team-selection-error';
        newErrorDiv.textContent = message;
        const selectorSection = document.querySelector('.team-selector-section');
        if (selectorSection) {
            selectorSection.appendChild(newErrorDiv);
            setTimeout(() => {
                newErrorDiv.remove();
            }, 3000);
        }
    }
}

// Validate team selection
function validateTeamSelection() {
    if (!selectedTeam1 || !selectedTeam2) {
        showError('Please select both teams before proceeding');
        return false;
    }
    return true;
}

// ========================================
//    PROFESSIONAL SELECTION UI FUNCTIONS
// ========================================

function initProfessionalSelection() {
    const preferenceItems = document.querySelectorAll('.preference-item');
    
    preferenceItems.forEach(item => {
        const checkbox = item.querySelector('input[type="checkbox"]');
        
        if (!checkbox) return;
        
        // Initialize state based on checkbox
        updateItemVisualState(item, checkbox.checked);
        
        // Handle item click (but preserve original checkbox functionality)
        item.addEventListener('click', function(e) {
            // Only toggle if clicking outside the actual checkbox
            if (e.target !== checkbox && !e.target.closest('.preference-toggle')) {
                checkbox.checked = !checkbox.checked;
                updateItemVisualState(item, checkbox.checked);
                
                // Trigger change event so your existing code still works
                const changeEvent = new Event('change', { bubbles: true });
                checkbox.dispatchEvent(changeEvent);
            }
        });
        
        // Handle checkbox changes (including programmatic ones)
        checkbox.addEventListener('change', function() {
            updateItemVisualState(item, this.checked);
        });
    });
}

function updateItemVisualState(item, isChecked) {
    if (isChecked) {
        item.classList.add('active');
        item.setAttribute('data-checked', 'true');
    } else {
        item.classList.remove('active');
        item.setAttribute('data-checked', 'false');
    }
}

// ========================================
//           MAIN DOM CONTENT LOADED
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM content loaded");

    // Initialize team selectors
    initializeTeamSelectors();

    // Get slider elements
    const riskSlider = document.getElementById('riskSlider');
    const riskValue = document.getElementById('riskValue');

    // Risk slider functionality
    if (riskSlider && riskValue) {  // Only execute if both elements exist
        function updateRiskValue(value) {
            const riskLabels = {
                '1': 'Very Low Risk',
                '2': 'Low Risk',
                '3': 'Medium Risk',
                '4': 'High Risk',
                '5': 'Very High Risk'
            };
            console.log('Updating risk value:', value, riskLabels[value]);
            riskValue.textContent = riskLabels[value];
        }

        // Set initial value
        console.log('Initial slider value:', riskSlider.value);
        updateRiskValue(riskSlider.value);

        // Add event listeners for both input and change events
        riskSlider.addEventListener('input', function(e) {
            console.log('Slider value changed:', e.target.value);
            updateRiskValue(e.target.value);
        });

        riskSlider.addEventListener('change', function(e) {
            console.log('Slider final value:', e.target.value);
            updateRiskValue(e.target.value);
        });
    }

    // Popular picks functionality
    const showPopularPicksBtn = document.getElementById('showPopularPicks');
    const popularPicksList = document.getElementById('popularPicksList');
    const popularPicksSection = document.getElementById('popularPicks');

    console.log('Popular picks elements:', {
        button: showPopularPicksBtn,
        list: popularPicksList,
        section: popularPicksSection
    });

    if (showPopularPicksBtn && popularPicksList && popularPicksSection) {
        // Event listener for the button click
        showPopularPicksBtn.addEventListener('click', async function () {
            console.log('Button clicked!');
            
            // Validate team selection first
            if (!validateTeamSelection()) {
                return;
            }
            
            const team1Value = document.getElementById('team1').value;
            const team2Value = document.getElementById('team2').value;
            
            try {
                console.log('Fetching popular picks...');
                const response = await fetch(`/get_popular_picks?team1=${encodeURIComponent(team1Value)}&team2=${encodeURIComponent(team2Value)}`);
                const data = await response.json();
                console.log('Received data:', data);
                
                if (data.error) {
                    alert(data.error);
                    return;
                }

                popularPicksList.innerHTML = ''; // Clear any previous picks

                // Populate the list with popular picks
                data.popular_picks.forEach(player => {
                    const li = document.createElement('li');
                    li.textContent = player;
                    popularPicksList.appendChild(li);
                });
                
                // Toggle visibility of the section
                popularPicksSection.style.display = 
                    popularPicksSection.style.display === 'none' ? 'block' : 'none';

                // Update button text
                this.textContent = popularPicksSection.style.display === 'block' ? 
                    'Hide Most Popular Picks' : 'Show Most Popular Picks';

            } catch (error) {
                console.error('Error fetching popular picks:', error);
                showError('Error fetching popular picks. Please try again.');
            }
        });
    }

    // Form submission
    const fantasyForm = document.getElementById('fantasyForm');
    const spinner = document.getElementById('spinner');
    const predictButton = document.getElementById('predictButton');
    
    if (fantasyForm) {
        fantasyForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            // Validate team selection first
            if (!validateTeamSelection()) {
                return;
            }
            
            // Show spinner and disable button
            if (spinner) spinner.style.display = "inline-block";
            if (predictButton) predictButton.disabled = true;
            
            setTimeout(async function() {
                // Hide spinner and enable button after 3 seconds
                if (spinner) spinner.style.display = "none";
                if (predictButton) predictButton.disabled = false;
                
                // Clear previous results
                const errorDiv = document.getElementById('error');
                const resultDiv = document.getElementById('result');
                
                if (errorDiv) errorDiv.textContent = '';
                if (resultDiv) resultDiv.textContent = '';

                let formData = new FormData(event.target);
                
                try {
                    let response = await fetch('/predict', {
                        method: 'POST',
                        body: formData
                    });

                    let data = await response.json();

                    if (data.error) {
                        if (errorDiv) {
                            errorDiv.textContent = data.error;
                        }
                    } else {
                        if (resultDiv) {
                            resultDiv.innerHTML = '';

                            data['Fantasy 11'].forEach(player => {
                                const li = document.createElement('li');
                                li.textContent = player;
                                resultDiv.appendChild(li);
                            });
                        }
                    }
                } catch (error) {
                    if (errorDiv) {
                        errorDiv.textContent = 'An error occurred. Please try again.';
                    }
                    console.error('Error:', error);
                }
            }, 3000);
        });
    }
    
    // Initialize professional selection UI
    initProfessionalSelection();
    
    // Add keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            clearSelection();
        }
    });
});

// Make clearSelection available globally for the button onclick
window.clearSelection = clearSelection;