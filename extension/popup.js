document.addEventListener('DOMContentLoaded', async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  document.getElementById('jobUrl').textContent = tab.url;
  
  const analyzeBtn = document.getElementById('analyzeBtn');
  const applyBtn = document.getElementById('applyBtn');
  const resumeUpload = document.getElementById('resumeUpload');
  
  let analysisData = null;
  
  analyzeBtn.addEventListener('click', async () => {
    // alert("analyzeBtn clicked");
    if (!resumeUpload.files.length) {
      showStatus('Please upload your resume first', 'error');
      return;
    }
    
    showStatus('Analyzing job match...', 'info');
    
    try {
      const file = resumeUpload.files[0];
      const fileData = await readFileAsArrayBuffer(file);
      
      const result = await chrome.runtime.sendMessage({
        action: "analyzeJob",
        jobUrl: tab.url,
        // resumeFile: fileData
      });
      
      if (result.success) {
        analysisData = result.result;
        displayAnalysis(analysisData);
        document.getElementById('contactForm').classList.remove('hidden');
        showStatus('Analysis complete!', 'success');
      } else {
        console.error(result.error);
        throw new Error(result.error);
      }
    } catch (error) {
      showStatus(`Error: ${error.message}`, 'error');
    }
  });
  
  applyBtn.addEventListener('click', async () => {
    const fullName = document.getElementById('fullName').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    
    if (!fullName || !email || !phone) {
      showStatus('Please fill all contact information fields', 'error');
      return;
    }
    
    showStatus('Applying for job...', 'info');
    
    try {
      const result = await chrome.runtime.sendMessage({
        action: "applyJob",
        jobUrl: tab.url,
        contactInfo: { fullName, email, phone }
      });
      
      if (result.success) {
        showStatus('Application submitted successfully!', 'success');
      } else {
        throw new Error(result.error);
      }
    } catch (error) {
      showStatus(`Error: ${error.message}`, 'error');
    }
  });
});

function readFileAsArrayBuffer(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsArrayBuffer(file);
  });
}

function displayAnalysis(data) {
  const analysisResult = document.getElementById('analysisResult');
  analysisResult.classList.remove('hidden');
  
  // Parse the analysis text (simplified - in reality you'd want a more structured response)
  document.getElementById('matchScore').textContent = data.analysis;
}

function showStatus(message, type) {
  const statusElement = document.getElementById('statusMessage');
  statusElement.textContent = message;
  statusElement.className = type;
}