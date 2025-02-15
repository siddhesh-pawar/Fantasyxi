document.addEventListener('DOMContentLoaded', function() {
    // Get slider elements
    const riskSlider = document.getElementById('riskSlider');
    const riskValue = document.getElementById('riskValue');

    if (!riskSlider || !riskValue) {
        console.error('Risk slider elements not found!');
        return;
    }

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

    // Popular picks functionality
    const showPopularPicksBtn = document.getElementById('showPopularPicks'); // Button to show/hide popular picks
    const popularPicksList = document.getElementById('popularPicksList'); // List of popular picks
    const popularPicksSection = document.getElementById('popularPicks'); // Section to toggle visibility

    // Event listener for the button click
    showPopularPicksBtn.addEventListener('click', async function () {
        try {
            const response = await fetch('/get_popular_picks');
            const data = await response.json();
            
            if (data.error) {
                alert(data.error);
                return;
            }

            popularPicksList.innerHTML = ''; // Clear any previous picks

            // Populate the list with popular picks
            data.popular_picks.forEach(player => {
                const li = document.createElement('li');
                li.textContent = player;  // Just use the player name
                popularPicksList.appendChild(li);
            });
            

            // Toggle visibility of the section
            popularPicksSection.style.display = 
                popularPicksSection.style.display === 'none' ? 'block' : 'none';

            // Update button text
            this.textContent = popularPicksSection.style.display === 'none' ? 
                'Show Most Popular Picks' : 'Hide Most Popular Picks';

        } catch (error) {
            console.error('Error fetching popular picks:', error);
        }
    });
    

    // Form submission
    const fantasyForm = document.getElementById('fantasyForm');
    if (fantasyForm) {
        fantasyForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            
            document.getElementById('error').textContent = '';
            document.getElementById('result').textContent = '';
            document.getElementById('justification').textContent = '';
            
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
                    document.getElementById('result').textContent = data['Fantasy 11'].join(', ');
                    document.getElementById('justification').textContent = data['Justification'];
                }
            } catch (error) {
                document.getElementById('error').textContent = 'An error occurred. Please try again.';
                console.error('Error:', error);
            }
        });
    }
});