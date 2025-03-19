const applicationSelect = document.getElementById('application-select');
const askQuestionBtn = document.getElementById('ask-question-btn');
const answerContent = document.getElementById('answer-content');
const questionInput = document.getElementById('question-input');

askQuestionBtn.addEventListener('click', async () => {
    const selectedApplication = applicationSelect.value;
    const question = questionInput.value;

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                application: selectedApplication,
                question: question,
            }),
        });

        const data = await response.json();

        if (data.error) {
            answerContent.textContent = `Error: ${data.error}`;
        } else {
            answerContent.textContent = data.answer;
        }
    } catch (error) {
        answerContent.textContent = `Error: ${error}`;
    }
});
