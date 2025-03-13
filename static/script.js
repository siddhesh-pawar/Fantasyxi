document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM content loaded");

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
            const team1Select = document.getElementById('team1');
            const team2Select = document.getElementById('team2');
            try {
                console.log('Fetching popular picks...');
                const response = await fetch(`/get_popular_picks?team1=${encodeURIComponent(team1Select.value)}&team2=${encodeURIComponent(team2Select.value)}`);
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
            }
        });
    }

    // Form submission
    const fantasyForm = document.getElementById('fantasyForm');
    if (fantasyForm) {
        fantasyForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            // Show spinner and disable button
            spinner.style.display = "inline-block";
            predictButton.disabled = true;
            
            setTimeout(async function() {
                // Hide spinner and enable button after 3 seconds
                spinner.style.display = "none";
                predictButton.disabled = false;
                
                // Proceed with form submission
                document.getElementById('error').textContent = '';
                document.getElementById('result').textContent = '';

                let formData = new FormData(event.target);
                
                try {
                    let response = await fetch('/predict', {
                        method: 'POST',
                        body: formData
                    });

                    let data = await response.json();

                    if (data.error) {
                        document.getElementById('error').textContent = data.error;
                    } else {
                        const resultDiv = document.getElementById('result');
                        resultDiv.innerHTML = '';

                        data['Fantasy 11'].forEach(player => {
                            const li = document.createElement('li');
                            li.textContent = player;
                            resultDiv.appendChild(li);
                        });
                    }
                } catch (error) {
                    document.getElementById('error').textContent = 'An error occurred. Please try again.';
                    console.error('Error:', error);
                }
            }, 3000);
        });
    }
});