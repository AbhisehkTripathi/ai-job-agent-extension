chrome.runtime.onInstalled.addListener(() => {
  console.log("AI Job Agent extension installed");
});

chrome.action.onClicked.addListener(async (tab) => {
  console.log("AI Job Agent extension clicked");
  try {
    // Get the current tab URL
    const [currentTab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    if (currentTab.url.includes('linkedin.com/jobs') || currentTab.url.includes('naukri.com')) {
      // Open the popup
      chrome.action.setPopup({ popup: "popup.html" });
    } else {
      chrome.notifications.create({
        type: "basic",
        title: "AI Job Agent",
        message: "This doesn't appear to be a job page. Navigate to LinkedIn or Naukri job page."
      });
    }
  } catch (error) {
    console.error("Error:", error);
  }
});

// Handle messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "analyzeJob") {
    analyzeJob(request.jobUrl, request.resumeFile)
      .then(result => sendResponse({ success: true, result }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Required for async sendResponse
  }
  
  if (request.action === "applyJob") {
    applyJob(request.jobUrl, request.contactInfo)
      .then(result => sendResponse({ success: true, result }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }
});

async function analyzeJob(jobUrl, resumeFile) {
  const formData = new FormData();
  formData.append('job_url', jobUrl);
  formData.append('resume', new Blob([resumeFile]), 'resume.pdf');
  
  const response = await fetch('http://localhost:8000/match-resume', {
    method: 'POST',
    body: formData
  });
  
  if (!response.ok) {
    throw new Error('Failed to analyze job');
  }
  
  return await response.json();
}

async function applyJob(jobUrl, contactInfo) {
  const response = await fetch('http://localhost:8000/apply-job', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      job_url: jobUrl,
      contact_info: contactInfo
    })
  });
  
  if (!response.ok) {
    throw new Error('Failed to apply for job');
  }
  
  return await response.json();
}