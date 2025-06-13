fetch('http://localhost:5000/answers')
  .then(res => res.json())
  .then(data => {
    const qaList = document.getElementById('qa-list');
    qaList.innerHTML = '';
    data.forEach((qa, idx) => {
      qaList.innerHTML += `
        <div class="qa">
          <div class="question">${idx + 1}. ${qa.question}</div>
          <div class="answer">Answer: ${qa.answer}</div>
        </div>
      `;
    });
  })
  .catch(err => {
    document.getElementById('qa-list').textContent = 'Failed to load answers.';
  });