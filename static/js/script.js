document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file-input');
    const uploadArea = document.getElementById('upload-area');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const predictBtn = document.getElementById('predict-btn');
    const btnText = document.querySelector('.btn-text');
    const loadingSpinner = document.querySelector('.loading-spinner');
    const uploadForm = document.getElementById('upload-form');
    const previewPlaceholder = document.getElementById('preview-placeholder');
    const previewImage = document.getElementById('preview-image');
    const previewImg = document.getElementById('preview-img');

    uploadArea.addEventListener('click', function() {
        console.log('Upload area clicked');
        fileInput.click();
    });

    fileInput.addEventListener('change', function() {
        if (this.files[0]) {
            handleFile(this.files[0]);
        }
    });

    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('dragover');
        
        if (e.dataTransfer.files[0]) {
            fileInput.files = e.dataTransfer.files;
            fileInput.dispatchEvent(new Event('change'));
        }
    });

    function handleFile(file) {
        console.log('Processing file:', file.name);
        
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
        if (!allowedTypes.includes(file.type)) {
            alert('Please upload a valid image file (JPEG, PNG, GIF)');
            resetForm();
            return;
        }

        const maxSize = 16 * 1024 * 1024;
        if (file.size > maxSize) {
            alert('File size too large. Maximum 16MB allowed.');
            resetForm();
            return;
        }

        fileName.textContent = file.name;
        fileSize.textContent = `${(file.size / 1024 / 1024).toFixed(2)} MB`;
        fileInfo.style.display = 'block';

        predictBtn.disabled = false;

        const reader = new FileReader();
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            previewPlaceholder.style.display = 'none';
            previewImage.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }

    function resetForm() {
        fileInput.value = '';
        predictBtn.disabled = true;
        fileInfo.style.display = 'none';
        previewPlaceholder.style.display = 'block';
        previewImage.style.display = 'none';
        btnText.style.display = 'block';
        loadingSpinner.style.display = 'none';
        predictBtn.innerHTML = '<span class="btn-text">Classify Image</span><div class="loading-spinner" style="display: none;"></div>';
    }

    uploadForm.addEventListener('submit', function(e) {
        if (!fileInput.files[0]) {
            e.preventDefault();
            alert('Please select an image first');
            return false;
        }

        btnText.textContent = 'Classifying...';
        loadingSpinner.style.display = 'block';
        predictBtn.disabled = true;
        
        return true;
    });
});