document.addEventListener('DOMContentLoaded', () => {
    const uploadBtn = document.getElementById('uploadBtn');
    const pdfInput = document.getElementById('pdfInput');

    uploadBtn.addEventListener('click', async () => {
        const file = pdfInput.files[0];
        if (!file) {
            alert('Please select a PDF file first');
            return;
        }


        // Here you'll add the connection to your FastAPI backend
        // Example:
        /*
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('http://localhost:8000/upload', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            console.log(data);
        } catch (error) {
            console.error('Error:', error);
        }
        */
    });
});
