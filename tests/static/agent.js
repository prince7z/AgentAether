// Agent Sanitized Perception View Engine

let ws = null;

function connectWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/ws`;
  
  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    console.log('[Agent View] Connected to WebSocket perception stream');
  };

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      updateSanitizedView(data);
    } catch (err) {
      console.error('[Agent View] Error parsing payload:', err);
    }
  };

  ws.onclose = () => {
    console.log('[Agent View] WebSocket disconnected. Reconnecting...');
    setTimeout(connectWebSocket, 1000);
  };
}

function setFieldState(elementId, rawValue, sanitizedToken) {
  const el = document.getElementById(elementId);
  if (!el) return;

  if (rawValue && rawValue.trim() !== '') {
    el.value = sanitizedToken;
    el.classList.add('redacted-input');
  } else {
    el.value = '';
    el.classList.remove('redacted-input');
  }
}

function updateSanitizedView(data) {
  // 1. Non-sensitive fields (passed through as typed)
  document.getElementById('ag_fullname').value = data.fullname || '';
  document.getElementById('ag_age').value = data.age || '';
  document.getElementById('ag_gender').value = data.gender || '';
  document.getElementById('ag_dob').value = data.dob || '';

  // 2. Sensitive fields: empty initially -> transforms to sanitized token as soon as user types!
  setFieldState('ag_phone', data.phone, '<user phone>');
  setFieldState('ag_email', data.email, '<user mail>');
  setFieldState('ag_password', data.password, '<user pass>');
  setFieldState('ag_card', data.card, '<user card>');

  // 3. Process Canvas Image Blur
  const canvas = document.getElementById('blurredCanvas');
  const canvasWrapper = document.getElementById('canvasWrapper');
  const dropText = document.getElementById('ag_dropText');
  const ctx = canvas.getContext('2d');

  if (data.imageData) {
    canvasWrapper.style.display = 'inline-block';
    if (dropText) {
      dropText.innerHTML = '🔒 Visual Perception Stream — Real-Time On-Device Face Blur Active';
      dropText.style.color = '#7C3AED';
      dropText.style.fontWeight = 'bold';
    }

    const img = new Image();
    img.onload = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw blurred image
      ctx.filter = 'blur(12px)';
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      ctx.filter = 'none';

      // Draw Face Redaction Overlay Box
      ctx.strokeStyle = '#EF4444';
      ctx.lineWidth = 2;
      ctx.strokeRect(30, 20, 80, 85);

      // Redaction Tag Box
      ctx.fillStyle = '#EF4444';
      ctx.fillRect(25, 60, 90, 20);
      ctx.fillStyle = '#FFFFFF';
      ctx.font = 'bold 9px monospace';
      ctx.fillText('<FACE_BLURRED>', 28, 73);
    };
    img.src = data.imageData;
  } else {
    canvasWrapper.style.display = 'none';
    if (dropText) {
      dropText.innerHTML = '📸 Drag & Drop Passport Photo here, or click to upload';
      dropText.style.color = '#333333';
      dropText.style.fontWeight = 'normal';
    }
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }

  // 4. Update JSON Terminal Output
  const redactedCount = [data.phone, data.email, data.password, data.card, data.imageData]
    .filter(val => val && val.toString().trim() !== '').length;

  const jsonTerminal = document.getElementById('jsonPayload');
  const sanitizedJSON = {
    agent_id: "AgentO3-LocalGate-v1",
    timestamp: new Date().toISOString(),
    task_context: "Government Form Input Filter Demonstration",
    sanitized_dom_tree: {
      fullname: data.fullname || "",
      age: data.age || "",
      gender: data.gender || "",
      dob: data.dob || "",
      phone: data.phone ? "<user phone>" : "",
      email: data.email ? "<user mail>" : "",
      password: data.password ? "<user pass>" : "",
      card: data.card ? "<user card>" : ""
    },
    visual_perception: {
      image_present: !!data.imageData,
      face_region_redacted: !!data.imageData,
      visual_token: data.imageData ? "<BLURRED_FACE_GRAPHIC>" : "NULL"
    },
    privacy_metrics: {
      redacted_entities_count: redactedCount,
      raw_pii_outbound_bytes: 0,
      ner_masking_status: redactedCount > 0 ? "INTERCEPTED & SANITIZED" : "WAITING_FOR_INPUT",
      security_gate_policy: "ZERO_KNOWLEDGE_PII"
    }
  };

  jsonTerminal.textContent = JSON.stringify(sanitizedJSON, null, 2);
}

document.addEventListener('DOMContentLoaded', () => {
  connectWebSocket();
});
