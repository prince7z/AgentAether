// User Form Logic & Real-time WebSocket Synchronization

let ws = null;
let currentImageData = null;

// Initialize WebSocket Connection
function connectWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/ws`;
  
  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    console.log('[User Window] Connected to AgentO3 WebSocket server');
    sendFormData();
  };

  ws.onclose = () => {
    console.log('[User Window] WebSocket disconnected. Retrying in 1s...');
    setTimeout(connectWebSocket, 1000);
  };

  ws.onerror = (err) => {
    console.error('[User Window] WebSocket error:', err);
  };
}

// Collect form field values and image data
function getFormData() {
  return {
    fullname: document.getElementById('fullname').value,
    age: document.getElementById('age').value,
    gender: document.getElementById('gender').value,
    dob: document.getElementById('dob').value,
    phone: document.getElementById('phone').value,
    email: document.getElementById('email').value,
    password: document.getElementById('password').value,
    card: document.getElementById('card').value,
    imageData: currentImageData
  };
}

// Broadcast form state over WebSocket
function sendFormData() {
  if (ws && ws.readyState === WebSocket.OPEN) {
    const payload = getFormData();
    ws.send(JSON.stringify(payload));
  }
}

// Generate Default Sample Face SVG -> Data URL
function loadSampleFace() {
  const canvas = document.createElement('canvas');
  canvas.width = 140;
  canvas.height = 160;
  const ctx = canvas.getContext('2d');

  // Background
  ctx.fillStyle = '#E2E8F0';
  ctx.fillRect(0, 0, 140, 160);

  // Shoulders
  ctx.fillStyle = '#1E293B';
  ctx.beginPath();
  ctx.ellipse(70, 150, 50, 30, 0, 0, Math.PI * 2);
  ctx.fill();

  // Head / Face
  ctx.fillStyle = '#F4A261';
  ctx.beginPath();
  ctx.arc(70, 65, 32, 0, Math.PI * 2);
  ctx.fill();

  // Hair
  ctx.fillStyle = '#2B2D42';
  ctx.beginPath();
  ctx.arc(70, 55, 34, Math.PI, 0);
  ctx.fill();

  // Eyes
  ctx.fillStyle = '#111111';
  ctx.beginPath();
  ctx.arc(58, 62, 3.5, 0, Math.PI * 2);
  ctx.arc(82, 62, 3.5, 0, Math.PI * 2);
  ctx.fill();

  // Smile
  ctx.strokeStyle = '#8D4925';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(70, 72, 12, 0.2, Math.PI - 0.2);
  ctx.stroke();

  // Stamp label
  ctx.fillStyle = '#002B49';
  ctx.font = '10px Arial';
  ctx.fillText('CITIZEN ID PHOTO', 22, 145);

  currentImageData = canvas.toDataURL('image/png');
  const imgPreview = document.getElementById('imagePreview');
  imgPreview.src = currentImageData;
  imgPreview.style.display = 'block';

  sendFormData();
}

// Attach Event Listeners
document.addEventListener('DOMContentLoaded', () => {
  // Input change triggers live broadcast
  const inputs = document.querySelectorAll('.gov-input');
  inputs.forEach(input => {
    input.addEventListener('input', sendFormData);
    input.addEventListener('change', sendFormData);
  });

  // Drag and Drop Zone setup
  const dropZone = document.getElementById('dropZone');
  const fileInput = document.getElementById('fileInput');
  const imgPreview = document.getElementById('imagePreview');
  const sampleBtn = document.getElementById('samplePhotoBtn');
  const resetBtn = document.getElementById('resetBtn');

  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, (e) => {
      e.preventDefault();
      e.stopPropagation();
    }, false);
  });

  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.add('drag-over'), false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.remove('drag-over'), false);
  });

  dropZone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 0) {
      handleFile(files[0]);
    }
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      handleFile(e.target.files[0]);
    }
  });

  sampleBtn.addEventListener('click', () => {
    loadSampleFace();
  });

  resetBtn.addEventListener('click', () => {
    document.getElementById('citizenForm').reset();
    currentImageData = null;
    imgPreview.style.display = 'none';
    imgPreview.src = '';
    sendFormData();
  });

  function handleFile(file) {
    if (!file.type.startsWith('image/')) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      currentImageData = e.target.result;
      imgPreview.src = currentImageData;
      imgPreview.style.display = 'block';
      sendFormData();
    };
    reader.readAsDataURL(file);
  }

  // Connect WebSocket
  connectWebSocket();
});
