document.addEventListener('DOMContentLoaded', () => {
    const outfitForm = document.getElementById('outfit-form');
    const shoppingForm = document.getElementById('shopping-form');
    const form = outfitForm || shoppingForm;
    
    if (!form) return;

    const resultContainer = document.getElementById('result-container');
    const loading = document.getElementById('loading');
    const resultContent = document.getElementById('result-content');
    const generateBtn = document.getElementById('generate-btn');
    const imageInput = document.getElementById('image-upload');
    const imagePreview = document.getElementById('image-preview');

    // Handle Image Preview
    imageInput.addEventListener('change', function() {
        imagePreview.innerHTML = '';
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                imagePreview.appendChild(img);
                imagePreview.classList.remove('hidden');
            }
            reader.readAsDataURL(this.files[0]);
        } else {
            imagePreview.classList.add('hidden');
        }
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // UI State
        resultContainer.classList.remove('hidden');
        resultContent.innerHTML = '';
        loading.classList.remove('hidden');
        generateBtn.disabled = true;
        const btnOriginalText = generateBtn.textContent;
        generateBtn.textContent = 'Consulting AI...';

        // Prepare FormData for multipart/form-data upload
        const formData = new FormData();
        
        // Determine mode based on which form is active
        const mode = shoppingForm ? 'shopping' : 'outfit';
        formData.append('mode', mode);
        
        formData.append('gender', document.getElementById('gender').value);
        formData.append('budget', document.getElementById('budget').value);
        
        if (mode === 'shopping') {
            formData.append('shopping_prompt', document.getElementById('shopping-prompt').value);
            if (document.getElementById('height')) formData.append('height', document.getElementById('height').value);
            if (document.getElementById('weight')) formData.append('weight', document.getElementById('weight').value);
            if (document.getElementById('skin-tone')) formData.append('skin_tone', document.getElementById('skin-tone').value);
            if (document.getElementById('body-type')) formData.append('body_type', document.getElementById('body-type').value);
        } else {
            formData.append('occasion', document.getElementById('occasion').value);
            formData.append('region', document.getElementById('region').value);
            formData.append('vibe', document.getElementById('vibe').value);
            formData.append('venue', document.getElementById('venue').value);
            formData.append('available_clothes', document.getElementById('available-clothes').value);
        }
        
        if (imageInput.files[0]) {
            formData.append('image', imageInput.files[0]);
        }

        const useLocation = document.getElementById('use-location').checked;
        if (useLocation && navigator.geolocation) {
            try {
                const position = await getPosition();
                formData.append('lat', position.coords.latitude);
                formData.append('lon', position.coords.longitude);
            } catch (err) {
                console.warn('Geolocation failed or denied. Proceeding without specific location weather.', err);
            }
        }

        // Fetch from API
        try {
            const response = await fetch('/api/suggest-outfit', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Server Error (${response.status}): ${errorText}`);
            }

            const data = await response.json();
            
            // Parse markdown response using marked
            if (window.marked) {
                resultContent.innerHTML = marked.parse(data.suggestion);
            } else {
                resultContent.innerText = data.suggestion;
            }

        } catch (error) {
            resultContent.innerHTML = `<p style="color: #ef4444;">Error: ${error.message}</p>`;
        } finally {
            loading.classList.add('hidden');
            generateBtn.disabled = false;
            generateBtn.textContent = btnOriginalText;
            
            // Scroll to results
            resultContainer.scrollIntoView({ behavior: 'smooth' });
        }
    });

    // Helper for geolocation Promise
    function getPosition(options) {
        return new Promise((resolve, reject) => 
            navigator.geolocation.getCurrentPosition(resolve, reject, options)
        );
    }
});
