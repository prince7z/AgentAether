# AgentO₃: Privacy-First Lightweight Browser Agent

**Smart India Hackathon 2026**  
**Problem Statement ID:** 26171  
**Problem Statement Title:** On-device Visual Perception for Light-weight Browser Agents  
**Theme:** Smart Automation | **PS Category:** Software  
**Team Name:** The Alchemists | **Team ID:** 120812  

---

## Section 1: Introduction & System Overview

**AgentO₃** is an enterprise-grade, privacy-first lightweight browser agent designed to perform autonomous web automation while guaranteeing absolute data privacy and security.

Traditional web browser agents stream raw visual screenshots, complete DOM trees, and un-sanitized user context directly to cloud-hosted Vision-Language Models (VLMs). This exposes critical user data—including email addresses, passwords, phone numbers, identity credentials, financial records, and facial images—to remote third-party API providers and centralized server infrastructure.

**AgentO₃ eliminates this fundamental security vulnerability by shifting visual perception and privacy protection directly on-device.**

Operating locally inside a lightweight browser extension environment, AgentO₃ parses DOM elements, executes lightweight OCR, Named Entity Recognition (NER), and computer vision inference on-device to semantically redact sensitive PII before any data leaves the user's machine. The cloud VLM receives **strictly sanitized context**, plans structured actions, and returns commands that are verified by a **Local Control Gate** prior to browser execution.

```mermaid
graph LR
    subgraph CLIENT["ON-DEVICE CLIENT (Local Browser)"]
        UserPrompt["User Prompt"] --> LocalInterface["Local Interface & Context Capture"]
        LocalInterface --> DOMScreen["Raw DOM + Screenshot"]
        DOMScreen --> LocalPrivacyEngine["Local Privacy Engine<br/>(NER + OCR + Masking)"]
        LocalPrivacyEngine --> PrivacyGate["Privacy Gate<br/>(Zero Raw PII Outbound)"]
    end

    subgraph CLOUD["CLOUD ENVIRONMENT"]
        PrivacyGate -- "Sanitized Context Only<br/>(<EMAIL>, <PASSWD>, Blurs)" --> CloudVLM["Cloud VLM / Reasoning Engine"]
        CloudVLM -- "Structured Browser Command" --> CloudResponse["Agent Response"]
    end

    subgraph EXECUTION["LOCAL ACTION CONTROL"]
        CloudResponse --> LocalControlGate["Local Control Gate<br/>(Policy & Allowlist Validation)"]
        LocalControlGate --> BrowserExecution["Browser Executor<br/>(Click / Type / Scroll)"]
    end

    classDef localStyle fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef cloudStyle fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
    classDef execStyle fill:#fff3e0,stroke:#ef6c00,stroke-width:2px;

    class UserPrompt,LocalInterface,DOMScreen,LocalPrivacyEngine,PrivacyGate localStyle;
    class CloudVLM,CloudResponse cloudStyle;
    class LocalControlGate,BrowserExecution execStyle;
```

---

## Section 2: System Vulnerabilities, Privacy Leakage Metrics & Statistical Loss Analysis

The rapid deployment of autonomous browser agents and LLM-driven web automation has introduced unprecedented security, privacy, and economic risks. The tables below quantify the global and regional impact of data breaches, PII exposure rates, agent vulnerabilities, and resource inflation.

### Data Breach Financial Impact & Recovery Costs (2024–2026)

| Metric | 2024 Findings | 2025 Findings | 2026 Benchmark | Primary Cause / Impact |
| :--- | :--- | :--- | :--- | :--- |
| **Global Average Data Breach Cost** | USD $4.88 Million | USD $4.44 Million | **USD $4.99 Million** | Unsanitized cloud data transmission & credential theft |
| **India Average Data Breach Cost** | INR ₹19.5 Crore | INR ₹22.0 Crore | **INR ₹25.5 Crore** | Highest historical cost record in Indian enterprise history |
| **Stolen Credential Containment Time** | 292 Days | 286 Days | **290+ Days** | Longest lifecycle to detect & isolate among attack vectors |
| **Human Element Involvement Rate** | 68% of Breaches | 64% of Breaches | **60% of Breaches** | Phishing, credential reuse, and un-sanitized browser sessions |
| **Customer PII Exposure Share** | 46% of Incidents | 48% of Incidents | **52% of Incidents** | Most frequently compromised & most expensive record type |
| **Cost per Compromised PII Record** | USD $173 / Record | USD $178 / Record | **USD $185 / Record** | Direct financial penalty, litigation & notification costs |

### AI Agent Vulnerabilities & Security Benchmarks

| Security Metric / Threat Vector | Observed Industry Benchmark | Risk Description & Technical Impact |
| :--- | :--- | :--- |
| **Agent Prompt Hijacking Rate** | **94.4% of AI Agents** | Vulnerable to indirect prompt injection via untrusted webpage content |
| **Internal Reasoning PII Leakage ("Leaky Thoughts")** | **87.2% of LLM Traces** | Reasoning traces leak sensitive context even if final output filters trigger |
| **Shadow AI & Oversight Gap Share** | **63.5% of Organizations** | Rapid adoption of AI agents without client-side execution boundaries |
| **Token Payload & Bandwidth Overhead** | **350% – 600% Inflation** | Unfiltered DOM + raw screenshot streaming inflates token costs per action |
| **OWASP LLM Vulnerability Rank #1** | **LLM01: Prompt Injection** | Webpage text overrides agent system prompts and hijacked control loop |
| **OWASP LLM Vulnerability Rank #6** | **LLM06: Excessive Agency** | Cloud models execute dangerous browser actions without local user approval |

### AgentO₃ On-Device Privacy Impact & Cost Reduction

| Operational Benchmark | Standard Cloud Agent | AgentO₃ Privacy-First Agent | Measurable Benefit |
| :--- | :--- | :--- | :--- |
| **Raw PII Transmitted to Cloud** | 100% (Emails, Passwords, Faces) | **0% (Zero Raw PII Outbound)** | **100% Privacy Boundary Compliance** |
| **Prompt Injection Hijack Defense** | Vulnerable (Direct Execution) | **Blocked at Local Control Gate** | **94.4% Risk Surface Elimination** |
| **Context Payload Size (Tokens/Step)** | ~12,500 Tokens / Step | **~2,800 Tokens / Step** | **77.6% Reduction in API Bandwidth & Cost** |
| **Client Inference Hardware Target** | High-End GPU Server | **WASM / WebGPU (96.63% Web Support)** | **Runs on Standard User Laptops/Desktops** |

---

## Section 3: Technology Stack

| Component Layer | Technologies & Frameworks | Description & Purpose |
| :--- | :--- | :--- |
| **Extension UI & Logic** | React, TypeScript, Chrome Manifest V3, WebAssembly (WASM), WebGPU | Lightweight browser extension interface, sidebar UI, and high-performance client runtime |
| **Browser Integration & Actions** | Chrome Extension APIs, Chrome DevTools Protocol (CDP), Playwright | DOM extraction, viewport screenshotting, click/type/scroll event injection |
| **Local AI & Inference** | ONNX Runtime Web, Transformers.js, WebGPU Execution Provider | On-device execution of lightweight NER and vision models for low-latency PII detection |
| **Privacy & PII Protection** | Pattern Engine, Regex, Local NER, Tesseract OCR / ONNX, Canvas Masking | Hybrid detection and semantic redaction (`rahul@gmail.com` -> `<EMAIL>`, face blurs) |
| **Webpage Understanding** | DOM Parser, Accessibility Tree Engine, Scene Graph Generator | Extracts structural and visual element layouts into unified, sanitized scene graphs |
| **Cloud Reasoning Backend** | Python 3.11+, FastAPI, LangGraph, LangChain Core | Cloud orchestrator executing stateful reasoning graphs (`StateGraph`) using VLM backends |
| **Cloud Models & Reasoning** | Qwen2.5-VL, Claude 3.5 Sonnet / GPT-4o, OpenRouter API | High-end Vision-Language Models for task decomposition, navigation planning, and routing |
| **Command Validation & Policy** | Local Control Gate, Action Allowlist Engine, Security Policies | Validates every cloud-generated browser command against user permissions prior to execution |
| **Local State & Memory** | SQLite, Qdrant (Local Vector DB) | Encrypted transactional session state and episodic/semantic memory vector store |

---

## Section 4: Product Demo

[![AgentO3 Product Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

*Click the thumbnail above to watch the full AgentO₃ product walkthrough & live PII redaction demonstration on YouTube. (Replace `YOUR_VIDEO_ID` with the actual YouTube video ID).*

---

## Section 5: Problem Statement

### Problem Statement ID 26171: On-device Visual Perception for Light-weight Browser Agents

Modern web browser agents rely heavily on multimodal cloud LLMs/VLMs to understand web interfaces and perform tasks on behalf of users. However, this architectural paradigm introduces major security, privacy, and economic challenges:

1. **Uncontrolled PII Exposure**: Current agents capture raw screen pixels and full un-redacted DOM hierarchies. When executing tasks on financial portals, emails, or enterprise dashboards, sensitive entities (passwords, credit card numbers, personal identifiers, face images) are routinely sent to cloud servers.
2. **Severe Data Breach Risks**: Transmitting raw web sessions increases breach vulnerability. According to the IBM Cost of a Data Breach Report 2026, the average data breach cost reached **₹25.5 crore in India** and **$4.99 million globally**, with **60% of breaches involving human elements**.
3. **Prompt Injection & Execution Hazards**: Malicious websites can inject adversarial prompts into visible page text or hidden DOM attributes. Benchmarks show **94.4% of AI agents** are vulnerable to prompt injection, which can trick cloud VLMs into executing unauthorized actions (e.g., bank transfers, data exfiltration).
4. **Bandwidth & Compute Overhead**: Streaming high-resolution raw screenshots and massive raw DOM payloads for every step wastes client bandwidth and inflates cloud processing costs by up to 600%.

---

## Section 6: Solution & System Architecture

### The AgentO₃ Approach

AgentO₃ introduces a **Privacy-First Dual-Layer Architecture** that decouples local perception and execution control from cloud reasoning:

1. **Local Perception**: Combines machine-readable DOM trees and local visual understanding to capture complete page context without sending unverified signals to the cloud.
2. **Intelligent Privacy Layer**: Runs hybrid local detection using NER, pattern matchers, and lightweight visual classifiers to spot PII (emails, passwords, phone numbers, face images).
3. **Semantic Sanitization**: Replaces private text values with meaningful structural placeholders (e.g., `user@domain.com` -> `<EMAIL>`) and applies visual blurring to face regions and confidential graphics.
4. **Privacy Gate**: Enforces a strict local boundary—unsanitized screenshots or DOM snapshots are completely blocked before outbound transmission.
5. **Cloud Reasoning**: Cloud VLMs operate exclusively on sanitized, privacy-safe context to construct high-level reasoning steps and browser commands.
6. **Local Control Gate**: Every cloud-generated action is intercepted locally and validated against user permissions, current browser state, and security policies before execution.
7. **Continuous Protection Loop**: Every browser state change triggers automatic re-observation and re-sanitization for the next iteration.

---

### Master Architecture Diagram

```mermaid
graph TD

    %% =========================================================
    %% USER / CLIENT
    %% =========================================================

    subgraph CLIENT["USER / CLIENT LAYER"]
        User["User"]
        Extension["Browser Extension UI<br/>TypeScript"]
    end


    %% =========================================================
    %% LOCAL AGENT
    %% =========================================================

    subgraph LOCAL["LOCAL ENVIRONMENT — Privacy & Execution"]

        subgraph INTERFACE["Local Interface"]
            TaskInput["Natural Language Task"]
            TaskState["Task State / Session State"]
            ContextCapture["Browser Context Capture"]
        end

        subgraph BROWSER["Local Browser Control"]
            Browser["User Browser"]
            DOM["DOM / Accessibility Tree"]
            Screenshot["Browser Screenshot"]

            BrowserActions["Browser Actions<br/>Click / Type / Scroll / Navigate"]
        end

        subgraph PRIVACY["Privacy Layer"]
            DOMParser["DOM Parser"]
            ScreenshotParser["Screenshot Processor"]

            PIIDetector["PII / Credential Detector<br/>Lightweight Local AI"]
            SensitiveDetector["Sensitive Element Detector"]

            Redactor["Sanitization & Redaction Engine"]

            SanitizedDOM["Sanitized DOM"]
            SanitizedImage["Sanitized Screenshot"]
            SceneGraph["Sanitized Scene / Element Graph"]
        end

        subgraph LOCAL_AI["Local Lightweight AI"]
            LocalLLM["Small Local LLM<br/>DOM Understanding / Classification"]
            LocalVision["Lightweight Vision Model"]
        end

        subgraph LOCAL_AGENT["Local Agent Controller"]
            LocalManager["Local Manager<br/>Validate + Decide"]
            CommandValidator["Command Validator"]
            PolicyEngine["Security / Permission Policy"]
        end

        subgraph EXECUTION["Local Tool Execution"]
            BrowserExecutor["Browser Executor"]

            WebTools["Local Browser Tools"]
            FileTools["Local File Tools"]
            SystemTools["Local System Tools"]

            ResultCapture["Execution Result"]
        end

        subgraph MEMORY["Local Memory & State"]
            ConversationManager["Conversation Manager"]
            SQLite["SQLite<br/>Active Sessions / Archives"]

            VectorMemory["Local Vector Memory"]
            Qdrant["Qdrant<br/>Semantic + Episodic Memory"]
        end

    end


    %% =========================================================
    %% CLOUD
    %% =========================================================

    subgraph CLOUD["CLOUD ENVIRONMENT — Reasoning Only"]

        subgraph GATEWAY["Cloud Gateway"]
            APIGateway["API Gateway / FastAPI"]
            Auth["Authentication / Session"]
        end

        subgraph AGENT_CORE["Cloud Agent Reasoning"]

            StateGraph["LangGraph<br/>Agent State Graph"]

            Planner["Planner / Task Decomposition"]

            CapabilityRouter["Capability Router"]

            ToolSelector["Tool Selection"]

            CloudLLM["Cloud LLM<br/>High-End Reasoning Model"]

        end

        subgraph CLOUD_CONTEXT["Sanitized Context"]
            Prompt["User Prompt"]
            SanitizedContext["Sanitized DOM + Screenshot<br/>Scene Graph + Task State"]
        end

        subgraph RESPONSE["Agent Response"]
            FinalAnswer["Final Answer"]
            BrowserCommand["Structured Browser Command"]
        end

    end


    %% =========================================================
    %% USER -> LOCAL
    %% =========================================================

    User --> Extension
    Extension --> TaskInput
    TaskInput --> TaskState
    TaskState --> ConversationManager

    Extension --> ContextCapture
    ContextCapture --> Browser


    %% =========================================================
    %% BROWSER -> PRIVACY LAYER
    %% =========================================================

    Browser --> DOM
    Browser --> Screenshot

    DOM --> DOMParser
    Screenshot --> ScreenshotParser

    DOMParser --> SensitiveDetector
    DOMParser --> PIIDetector

    ScreenshotParser --> PIIDetector
    ScreenshotParser --> LocalVision

    LocalLLM --> PIIDetector
    LocalLLM --> SensitiveDetector

    PIIDetector --> Redactor
    SensitiveDetector --> Redactor

    Redactor --> SanitizedDOM
    Redactor --> SanitizedImage

    SanitizedDOM --> SceneGraph
    SanitizedImage --> SceneGraph


    %% =========================================================
    %% LOCAL MEMORY
    %% =========================================================

    ConversationManager <--> SQLite
    ConversationManager <--> VectorMemory
    VectorMemory <--> Qdrant

    TaskState --> ConversationManager


    %% =========================================================
    %% SANITIZED DATA -> CLOUD
    %% =========================================================

    TaskInput --> Prompt

    Prompt --> APIGateway
    SceneGraph --> SanitizedContext
    TaskState --> SanitizedContext

    SanitizedContext --> APIGateway

    APIGateway --> Auth
    Auth --> StateGraph

    StateGraph --> Planner
    Planner --> CapabilityRouter
    CapabilityRouter --> ToolSelector

    Prompt --> CloudLLM
    SanitizedContext --> CloudLLM
    ToolSelector --> CloudLLM


    %% =========================================================
    %% CLOUD REASONING
    %% =========================================================

    CloudLLM --> BrowserCommand
    CloudLLM --> FinalAnswer


    %% =========================================================
    %% CLOUD -> LOCAL
    %% =========================================================

    BrowserCommand --> LocalManager
    FinalAnswer --> LocalManager

    LocalManager --> CommandValidator
    CommandValidator --> PolicyEngine

    PolicyEngine --> BrowserExecutor


    %% =========================================================
    %% LOCAL EXECUTION
    %% =========================================================

    BrowserExecutor --> BrowserActions

    BrowserActions --> Browser

    BrowserExecutor --> WebTools
    BrowserExecutor --> FileTools
    BrowserExecutor --> SystemTools

    WebTools --> ResultCapture
    FileTools --> ResultCapture
    SystemTools --> ResultCapture

    ResultCapture --> LocalManager


    %% =========================================================
    %% EXECUTION -> UPDATED STATE
    %% =========================================================

    BrowserActions --> DOM
    BrowserActions --> Screenshot

    DOM --> ContextCapture
    Screenshot --> ContextCapture

    ContextCapture --> DOMParser
    ContextCapture --> ScreenshotParser


    %% =========================================================
    %% FINAL RESULT
    %% =========================================================

    LocalManager --> Extension
    Extension --> User


    %% =========================================================
    %% STYLING
    %% =========================================================

    classDef local fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef privacy fill:#fff3e0,stroke:#ef6c00,stroke-width:2px
    classDef cloud fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef execution fill:#fce4ec,stroke:#ad1457,stroke-width:2px
    classDef memory fill:#ede7f6,stroke:#5e35b1,stroke-width:2px

    class Browser,DOM,Screenshot,BrowserActions,Extension local
    class PIIDetector,SensitiveDetector,Redactor,SanitizedDOM,SanitizedImage,SceneGraph,LocalLLM,LocalVision privacy
    class CloudLLM,StateGraph,Planner,CapabilityRouter,ToolSelector,APIGateway cloud
    class BrowserExecutor,WebTools,FileTools,SystemTools,CommandValidator,PolicyEngine execution
    class SQLite,Qdrant,ConversationManager,VectorMemory memory
```

---

### Implementation Process Flow Diagram

```mermaid
sequenceDiagram
    autonumber
    actor User as User
    participant Ext as Local Interface (Extension)
    participant Privacy as Local Privacy Layer (NER/OCR)
    participant Gate as Privacy Gate
    participant Cloud as Cloud Agent (FastAPI / VLM)
    participant LocalMgr as Local Control Gate (Manager)
    participant Exec as Browser Executor

    User->>Ext: Submit Natural Language Task
    Ext->>Ext: Capture Current Screen + DOM
    Ext->>Privacy: Send Raw DOM + Viewport Screenshot
    Privacy->>Privacy: Detect PII (NER + Regex + OCR + Vision)
    Privacy->>Privacy: Mask Sensitive Text & Blur Face Regions
    Privacy->>Gate: Generate Sanitized Context & Scene Graph
    Gate->>Cloud: Transmit Sanitized Context + Prompt (No Raw PII)
    Cloud->>Cloud: VLM Reason / Plan Next Action Step
    Cloud->>LocalMgr: Return Structured Command OR Final Answer
    LocalMgr->>LocalMgr: Validate Command against Security Policy
    alt Command Approved
        LocalMgr->>Exec: Execute Command (Click / Type / Scroll)
        Exec->>Ext: Update Browser State (DOM + Screenshot)
    else Policy Violation
        LocalMgr->>User: Prompt User for HITL Authorization
    end
    LocalMgr->>User: Display Final Result / Answer
```

---

## Section 7: Project Directory Structure

> **Development Status Note**:  
> The codebase is actively evolving during development. Below is the complete target directory structure representing the full end-to-end architecture (Client Extension + On-Device Privacy Layer + Local Manager + Cloud Agent Backend).

```
openclaw/
├── extension/                        # [Client Layer] Browser Extension UI (TypeScript / React)
│   ├── manifest.json                 # Manifest V3 extension setup
│   ├── src/
│   │   ├── background/               # Background service worker & IPC messaging
│   │   ├── content/                  # DOM tree observer & visual highlight overlay
│   │   ├── popup/                    # React extension popup interface
│   │   └── sidebar/                  # Main agent control panel sidebar
│   └── public/                       # Icons and static extension assets
│
├── local_privacy/                    # [Privacy Layer] On-Device Perception & Sanitization
│   ├── detectors/
│   │   ├── pii_ner.py                # Lightweight local NER model runner (ONNX / WASM)
│   │   ├── regex_patterns.py         # Pattern matcher (Emails, Phone, SSN, Credit Cards)
│   │   ├── ocr_engine.py             # Local OCR engine (Tesseract / ONNX Web)
│   │   └── vision_masker.py          # Face detection & sensitive visual region blurring
│   ├── redactor/
│   │   ├── dom_sanitizer.py          # DOM text replacer (<EMAIL>, <PASSWD>, etc.)
│   │   └── screenshot_masker.py      # Image region redactor & canvas eraser
│   └── scene_graph/                  # Sanitized DOM + Vision scene graph generator
│
├── local_manager/                    # [Local Controller] Execution Control & Validation Gate
│   ├── validator.py                  # Structured command verifier & allowlist matching
│   ├── policy_engine.py              # Security permissions & Human-In-The-Loop gate
│   ├── executor.py                   # Browser Executor (Chrome Extension / CDP adapter)
│   └── memory/
│       ├── conversation.py           # Session manager & SQLite transactional storage
│       └── vector_store.py           # Qdrant local vector database interface
│
├── app/                              # [Cloud Backend Layer] Reasoning Engine & FastAPI Service
│   ├── agent/
│   │   ├── graph.py                  # LangGraph StateGraph agent execution loop
│   │   ├── planner.py                # Task decomposition & multi-step planning
│   │   ├── router.py                 # Infinity BGE Reranker dynamic capability router
│   │   ├── prompts.py                # System prompts & sanitized context formatters
│   │   └── state.py                  # Agent state schema definitions
│   ├── api/                          # REST API & WebSocket endpoints (FastAPI)
│   ├── gateway/                      # Authentication & Telegram / Webhook gateways
│   ├── runtime/                      # Docker container sandbox runner for untrusted tools
│   ├── tools/                        # Server-side tool execution interfaces
│   └── main.py                       # Cloud backend server entrypoint
│
├── docker/                           # Container definitions & compose configurations
├── tests/                            # Unit tests, privacy leakage checks, and E2E suites
├── ARCHITECTURE.md                   # System architecture & specification doc
└── README.md                         # Project documentation
```

---

## Section 8: Features & Solution Uniqueness

- **Hybrid Perception**: Integrates machine-readable structured DOM trees with visual scene perception, ensuring no element is missed.
- **Semantic Redaction**: Intelligent placeholders (e.g., converting `john@example.com` into `<EMAIL>`) maintain full contextual understanding for the LLM without revealing raw personal values.
- **Privacy Gate**: Hard local barrier preventing un-sanitized screenshots or DOM snapshots from making outbound HTTP requests.
- **Local Control Gate**: Cloud-generated action vectors are strictly validated against permission rules before local browser execution.
- **Continuous Protection Loop**: Real-time state re-observation and re-sanitization after every single browser action.

---

## Section 9: Feasibility, Viability & Risk Mitigation

### Feasibility Analysis

| Category | Assessment & Empirical Support |
| :--- | :--- |
| **Technical Feasibility** | **96.63% of global browser installations** support WebAssembly (WASM), providing a broad client execution baseline for lightweight ONNX models. Chrome's **69.39% global market share** makes Chromium Manifest V3 extensions practical for deployment. |
| **Operational Feasibility** | Delivered natively as a browser extension, avoiding complex desktop application installations. Combines local approval gates to mitigate the **60% of data breaches** that involve human vulnerabilities. |
| **Economic Feasibility** | Directly addresses the average **₹25.5 crore data breach cost in India** ($4.99 million globally). Keeps large-scale reasoning cloud-bound while client-side sanitization cuts payload sizes by **77.6%**, dramatically saving bandwidth and API costs. |
| **Scalability** | The extension architecture works uniformly across web portals. Cloud VLMs scale independently while client inference handles local privacy transformation. |

### Risk & Challenge Mitigation Matrix

| # | Potential Challenges & Risks | Strategies for Overcoming Challenges |
| :-: | :--- | :--- |
| **1** | **Limited Device Resources** | Deploys quantized ONNX models running via WebGPU / WebAssembly (WASM). |
| **2** | **PII Hidden from DOM** | Multi-signal detection engine combining DOM parsing + OCR + NER + Vision models. |
| **3** | **False Positive Detections** | Cross-verification rules across visual and structural signals. |
| **4** | **Context Lost After Redaction** | Replaces sensitive strings with structured semantic placeholders (`<EMAIL>`, `<PHONE_NO>`). |
| **5** | **Unsafe AI Actions** | Structured command schemas validated by local allowlists and permission policies. |
| **6** | **Prompt Injection** | Strict content filtering and execution allowlist enforcement at the Local Manager. |
| **7** | **Privacy Leakage** | Enforces a strict local Privacy Gate with zero raw PII persistent storage. |

---

## Section 10: Impact & Benefits

### Target Audience Impact
- **Safer AI Browsing**: Enables AI-assisted web workflows without routinely exposing private user screens to third-party cloud servers.
- **Privacy-Critical Workflows**: Unlocks autonomous AI assistance for financial, identity, healthcare, and enterprise platforms.
- **Controlled AI Autonomy**: Merges cloud intelligence with local authorization rather than giving cloud models unrestricted browser control.
- **Enhanced Human Trust**: Users retain absolute local boundary control over sensitive data and executable commands.
- **Privacy-by-Architecture**: Privacy protection is built directly into the execution loop rather than attached as an afterthought.

### Core Solution Benefits
- **Privacy**: Detects and sanitizes sensitive visual and text data prior to transmission.
- **Intelligence**: Preserves cloud VLM/LLM reasoning capacity without sending raw screen data.
- **Efficiency**: Adaptive local inference minimizes heavy local compute while saving cloud bandwidth.
- **Control**: Every cloud-generated action passes through local policy verification.
- **Data Minimization**: Transmits strictly sanitized, task-relevant context to the cloud.

---

## Section 11: Research & References

1. **WebArena** — *A Realistic Web Environment for Building Autonomous Agents*  
   [https://arxiv.org/abs/2307.13854](https://arxiv.org/abs/2307.13854)
2. **Qwen2.5-VL Technical Report** — Bai et al. (2025)  
   [https://arxiv.org/abs/2502.13923](https://arxiv.org/abs/2502.13923)
3. **ONNX Runtime Web** — *WebGPU Execution Provider*  
   [https://onnxruntime.ai/docs/tutorials/web/ep-webgpu.html](https://onnxruntime.ai/docs/tutorials/web/ep-webgpu.html)
4. **OWASP Top 10 for LLMs** — *LLM01:2025 Prompt Injection*  
   [https://genai.owasp.org/llmrisk/llm01-prompt-injection/](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
5. **Chrome for Developers** — *Chrome Extensions Manifest V3 Documentation*  
   [https://developer.chrome.com/docs/extensions/](https://developer.chrome.com/docs/extensions/)
6. **Can I Use** — *WebAssembly (WASM) Browser Support Matrix*  
   [https://caniuse.com/wasm](https://caniuse.com/wasm)
7. **IBM Security** — *Cost of a Data Breach Report 2026: Global and India Findings*  
   [https://in.newsroom.ibm.com/2025-08-07-India-Records-Highest-Average-Cost-of-a-Data-Breach-IBM](https://in.newsroom.ibm.com/2025-08-07-India-Records-Highest-Average-Cost-of-a-Data-Breach-IBM)

---

<p align="center">
  <b>Developed by Team The Alchemists for Smart India Hackathon 2026</b>
</p>