document.addEventListener('DOMContentLoaded', () => {
    const elements = {
        uploadBtn: document.getElementById('uploadBtn'),
        pdfInput: document.getElementById('pdfInput'),
        submitdBtn: document.getElementById('submitdBtn'),
        aiAnswer: document.getElementById('aiAnswer'),
        resultDisplay: document.getElementById('resultDisplay')
    };

    const API_URL = 'http://localhost:8000';

    let pdfContent = null

    elements.uploadBtn?.addEventListener('click', handleFileUpload);
    elements.submitdBtn?.addEventListener('click', handleTestGeneration);

    async function handleFileUpload() {
        const file = elements.pdfInput?.files[0];
        if (!file) {
            showError('Please select a PDF file first');
            return;
        }

        try {
            showLoading('Uploading PDF...');
            const uploadResult = await uploadFile(file);

            if (uploadResult.chunks > 0) {
                showMessage(`PDF uploaded successfully. It has ${uploadResult.chunks} chunks.`);
            } else {
                showError('Something went wrong during PDF processing.');
            }
        } catch (error) {
            showError(`Error: ${error.message}`);
        } finally {
            hideLoading();
        }
    }

    async function handleTestGeneration() {
        try {
            showLoading('Generating test questions...');
            const content = await getUploadedPDFContent(); // You'll need to implement this
            if (!content) {
                showError('Please upload a PDF first.');
                return;
            }
            const testQuestions = await generateTest(content);
            displayQuestions(testQuestions);
        } catch (error) {
            showError(`Error: ${error.message}`);
        } finally {
            hideLoading();
        }
    }




    async function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Upload failed: ${response.statusText}`);
        }

        const result = await response.json();
        pdfContent = result.content;
        return result;

    }

    async function getUploadedPDFContent() {
        // TODO: Implement logic to fetch the content of the uploaded PDF.
        // This might involve storing the content in a variable after upload
        // or making another API request to retrieve it.
        try {
            const response = await fetch(`${API_URL}/content`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
    
            if (!response.ok) {
                throw new Error(`Failed to retrieve PDF content: ${response.statusText}`);
            }
    
            const data = await response.json();
            
            if (!data.content) {
                throw new Error('No PDF content available');
            }
    
            return data.content;
        } catch (error) {
            showError(`Error retrieving PDF content: ${error.message}`);
            return null;
        }

    }

    async function generateTest(content) {
        showLoading('Generating test questions...');
        const response = await fetch(`${API_URL}/test`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content }) 
        });

        if (!response.ok) {
            const error = await response.json(); 
            throw new Error(error.detail || 'Test generation failed');
        }

        const data = await response.json();
        window.questions = data.questions;
        return data.questions; 
    }


    function displayQuestions(questions) {
        if (!elements.aiAnswer) return;

        if (!Array.isArray(questions) || questions.length === 0) {
            elements.aiAnswer.textContent = "No questions generated";
            return;
        }

        elements.aiAnswer.innerHTML = questions.join('<br><br>'); 
    }


    function showError(message) {
        alert(message); 
    }

    function showMessage(message) {
        alert(message);
    }

    function showLoading(message = 'Loading...') {
        document.body.classList.add('loading'); 
    }

    function hideLoading() {
        document.body.classList.remove('loading'); 
    }
});

