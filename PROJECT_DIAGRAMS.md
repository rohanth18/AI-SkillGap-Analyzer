# Project Diagrams and System Design

**AI-Based Skill Gap Analyzer and Personalized Learning Recommendation System**

This document contains the diagrams referenced in the Project Report, formatted using Mermaid.js.

---

## 4.1 SYSTEM PERSPECTIVE

### System Perspective Design

```mermaid
graph LR
    %% Styles
    classDef box fill:#fff,stroke:#333,stroke-width:1px;
    classDef db fill:#fff,stroke:#333,stroke-width:1px;

    subgraph UserGroup [Users]
        direction TB
        MainUser[Admin / Job Seeker]:::box
        MainUser <--> BottomBox[Manage profiles /<br/>Resume analysis /<br/>Skill gap reports /<br/>Learning roadmaps /<br/>ATS optimization]:::box
    end

    subgraph Modules
        direction TB
        Reg[Registration & Authentication Module]:::box
        Manage[Manage data of Admin<br/>and Job Seeker]:::box
    end

    Database[(AI SkillGap Analyzer<br/>Database)]:::db

    %% Connections
    MainUser <--> Reg
    MainUser <--> Manage
    
    Reg <--> Database
    Manage <--> Database
```

---

## 4.2 DATAFLOW DIAGRAM / CONTEXT DIAGRAM

### Level 0 DFD (Context Diagram)

```mermaid
graph LR
    %% Nodes
    JS[Job Seeker]:::box
    Admin[Admin]:::box
    System((AI SkillGap<br/>Analyzer)):::circle

    %% Styles
    classDef box fill:#fff,stroke:#333,stroke-width:1px;
    classDef circle fill:#fff,stroke:#333,stroke-width:1px;

    %% Job Seeker Flows
    JS -->|Uploads resume,<br/>Manual skills input,<br/>GitHub profile| System
    System -->|Skill gap analysis,<br/>Job recommendations,<br/>Learning roadmap,<br/>ATS score| JS

    %% Admin Flows
    Admin -->|Manage users,<br/>Update job roles,<br/>Monitor system| System
    System -->|Analytics reports,<br/>Skill gap heatmaps,<br/>Audit logs| Admin
```

### Level 1 DFD - Admin

```mermaid
graph LR
    %% Nodes
flowchart LR
    Admin["Admin"]
    
    P1(("Admin<br/>Login"))
    D1["User<br/>Database"]
    
    P2(("Manage<br/>Job Roles"))
    D2["Roles<br/>Database"]
    
    P3(("View<br/>Analytics"))
    D3["Analysis<br/>Database"]
    
    Admin -->|Login credentials| P1
    P1 -->|Verified| D1
    D1 -.->|Success| Admin
    
    Admin -->|Add/Edit/Delete roles| P2
    P2 <-->|Update| D2
    
    Admin -->|Request insights| P3
    D3 -->|Skill gap data| P3
    P3 -.->|Charts & reports| Admin

    style Admin fill:#fff,stroke:#000,stroke-width:2px
    style P1 fill:#fff,stroke:#000,stroke-width:1px
    style P2 fill:#fff,stroke:#000,stroke-width:1px
    style P3 fill:#fff,stroke:#000,stroke-width:1px
    style D1 fill:#fff,stroke:#000,stroke-width:1px
    style D2 fill:#fff,stroke:#000,stroke-width:1px
    style D3 fill:#fff,stroke:#000,stroke-width:1px
```

### Level 1 DFD - Job Seeker

```mermaid
flowchart TB
    JobSeeker["Job Seeker"]
    
    P1(("Registration<br/>& Login"))
    D1["User<br/>Database"]
    
    P2(("Upload<br/>Resume"))
    D2["Resume<br/>Repository"]
    
    P3(("AI Skill<br/>Extraction"))
    D3["Analysis<br/>Database"]
    
    P4(("Gap<br/>Analysis"))
    D4["Job Roles<br/>Database"]
    
    P5(("Generate<br/>Roadmap"))
    D5["Learning<br/>Resources"]
    
    JobSeeker -->|Register/Login| P1
    P1 <-->|Verify| D1
    
    JobSeeker -->|Upload PDF| P2
    P2 -->|Store| D2
    P2 -->|Extract text| P3
    
    P3 -->|Skills extracted| D3
    D4 -->|Required skills| P4
    D3 -->|User skills| P4
    
    P4 -->|Missing skills| P5
    D5 -->|Resources| P5
    P5 -.->|Roadmap & Projects| JobSeeker

    style JobSeeker fill:#fff,stroke:#000,stroke-width:2px
    style P1 fill:#fff,stroke:#000,stroke-width:1px
    style P2 fill:#fff,stroke:#000,stroke-width:1px
    style P3 fill:#fff,stroke:#000,stroke-width:1px
    style P4 fill:#fff,stroke:#000,stroke-width:1px
    style P5 fill:#fff,stroke:#000,stroke-width:1px
    style D1 fill:#fff,stroke:#000,stroke-width:1px
    style D2 fill:#fff,stroke:#000,stroke-width:1px
    style D3 fill:#fff,stroke:#000,stroke-width:1px
    style D4 fill:#fff,stroke:#000,stroke-width:1px
    style D5 fill:#fff,stroke:#000,stroke-width:1px
```

---

## 5.1 USE CASE DIAGRAMS

### Use Case Diagram - Admin

```mermaid
graph LR
    %% Actor
    Admin((Admin))
    
    %% System Boundary
    subgraph System ["AI SkillGap Analyzer"]
        UC1(Admin Login)
        UC2(Manage Users)
        UC3(Manage Job Roles)
        UC4(View Analytics Dashboard)
        UC5(View Skill Gap Trends)
        UC6(Monitor AI Performance)
    end

    %% Styles
    classDef uc fill:#fff,stroke:#333,stroke-width:1px,rx:20,ry:20;
    class UC1,UC2,UC3,UC4,UC5,UC6 uc;

    %% Connections
    Admin --- UC1
    Admin --- UC2
    Admin --- UC3
    Admin --- UC4
    Admin --- UC5
    Admin --- UC6
```

### Use Case Diagram - Job Seeker

```mermaid
graph LR
    %% Actor
    JS((Job Seeker))
    
    %% System Boundary
    subgraph System ["AI SkillGap Analyzer"]
        UC1(Register & Login)
        UC2(Upload Resume)
        UC3(Input Manual Skills)
        UC4(View Skill Gap Analysis)
        UC5(Get Job Recommendations)
        UC6(View Learning Roadmap)
        UC7(Get Project Suggestions)
        UC8(Optimize Resume - ATS)
        UC9(Download Report)
    end

    %% Styles
    classDef uc fill:#fff,stroke:#333,stroke-width:1px,rx:20,ry:20;
    class UC1,UC2,UC3,UC4,UC5,UC6,UC7,UC8,UC9 uc;

    %% Connections
    JS --- UC1
    JS --- UC2
    JS --- UC3
    JS --- UC4
    JS --- UC5
    JS --- UC6
    JS --- UC7
    JS --- UC8
    JS --- UC9
```

---

## 5.2 SEQUENCE DIAGRAMS

### Sequence Diagram - Job Seeker Analysis Flow

```mermaid
sequenceDiagram
    actor JS as Job Seeker
    participant UI as React Frontend
    participant API as Flask Backend
    participant AI as AI Engine<br/>(spaCy + SBERT)
    participant ML as ML Model<br/>(RandomForest)
    participant DB as SQLite Database

    JS->>UI: Upload Resume (PDF)
    UI->>API: POST /api/upload
    API->>API: Extract Text (PyPDF2)
    API->>DB: Save Resume
    DB-->>API: Resume ID
    API-->>UI: Resume ID

    JS->>UI: Select Target Role & Analyze
    UI->>API: POST /api/analyze
    API->>DB: Fetch Role Requirements
    DB-->>API: Required Skills List
    
    API->>AI: Extract Skills (spaCy + SBERT)
    AI->>AI: Hybrid Extraction
    AI-->>API: Extracted Skills + Confidence
    
    API->>API: Calculate Skill Gap
    API->>API: Calculate ATS Score
    API->>DB: Save Analysis
    
    API->>ML: Predict Job Roles
    ML-->>API: Top 3 Recommendations
    
    API-->>UI: Analysis Results JSON
    UI-->>JS: Display Skill Gap Charts
```

### Sequence Diagram - Admin Role Management

```mermaid
sequenceDiagram
    actor Admin
    participant UI as Admin Dashboard
    participant API as Flask Backend
    participant DB as SQLite Database

    Admin->>UI: Login as Admin
    UI->>API: POST /api/login
    API->>DB: Verify Admin Credentials
    DB-->>API: User Data
    API-->>UI: JWT Token (is_admin: true)

    Admin->>UI: Add New Job Role
    UI->>API: POST /api/admin/roles
    Note over API: {name: "DevOps Engineer",<br/>skills: ["Docker", "Kubernetes"]}
    API->>DB: Insert Role & Skills
    DB-->>API: Success
    API-->>UI: Role Created
    UI-->>Admin: Show Confirmation
    
    Admin->>UI: View Analytics
    UI->>API: GET /api/admin/insights/analytics
    API->>DB: Aggregate Missing Skills
    DB-->>API: Skill Frequency Data
    API-->>UI: Analytics Data JSON
    UI-->>Admin: Display Charts
```

---

## 5.3 ACTIVITY DIAGRAMS

### Activity Diagram - Job Seeker Workflow

```mermaid
flowchart TD
    Start([Start]) --> Login{Already<br/>Registered?}
    Login -- No --> Register[Register Account]
    Register --> Login
    Login -- Yes --> Auth[Authenticate]
    
    Auth --> Dashboard[User Dashboard]
    
    Dashboard --> Action{Choose Action}
    Action -- Upload --> Upload[Upload Resume PDF]
    Action -- Manual --> ManualInput[Enter Skills Manually]
    Action -- History --> ViewHistory[View Past Analyses]
    
    Upload --> SelectRole[Select Target Job Role]
    ManualInput --> SelectRole
    
    SelectRole --> Analyze[Run AI Analysis]
    
    Analyze --> Processing{AI Processing}
    Processing -- Error --> ErrorMsg[Show Error Message] --> Dashboard
    Processing -- Success --> Results[View Skill Gap Results]
    
    Results --> ViewCharts[View Radar Charts]
    ViewCharts --> GetRecs[Get Recommendations]
    
    GetRecs --> Choice{What Next?}
    Choice -- Roadmap --> Roadmap[View Learning Roadmap]
    Choice -- Projects --> Projects[View Project Suggestions]
    Choice -- ATS --> ATS[Optimize Resume for ATS]
    
    Roadmap --> Download[Download PDF Report]
    Projects --> Download
    ATS --> Download
    
    Download --> End([End])
    ViewHistory --> End
```

### Activity Diagram - Admin Workflow

```mermaid
flowchart TD
    Start([Start]) --> Auth[Admin Login]
    Auth --> Verify{Valid<br/>Credentials?}
    Verify -- No --> AccessDenied([Access Denied])
    Verify -- Yes --> AdminDash[Admin Dashboard]
    
    AdminDash --> Choice{Select Task}
    
    Choice -- Users --> ManageUsers[View User List]
    ManageUsers --> UserActions{Action}
    UserActions -- View --> ViewUser[View User Details]
    UserActions -- Delete --> DeleteUser[Delete User]
    
    Choice -- Roles --> ManageRoles[Manage Job Roles]
    ManageRoles --> RoleActions{Action}
    RoleActions -- Add --> AddRole[Add New Role & Skills]
    RoleActions -- Edit --> EditRole[Edit Existing Role]
    RoleActions -- Delete --> DeleteRole[Delete Role]
    
    Choice -- Analytics --> ViewAnalytics[View System Analytics]
    ViewAnalytics --> AnalyticsType{View Type}
    AnalyticsType -- Gaps --> Charts[Skill Gap Charts]
    AnalyticsType -- Trends --> Trends[Domain Trends Chart]
    AnalyticsType -- Stats --> Stats[Overall Statistics]
    
    AddRole --> SaveDB[(Save to Database)]
    EditRole --> SaveDB
    DeleteRole --> SaveDB
    DeleteUser --> SaveDB
    
    SaveDB --> AdminDash
    ViewUser --> AdminDash
    Charts --> AdminDash
    Trends --> AdminDash
    Stats --> AdminDash
    
    AdminDash --> Logout{Logout?}
    Logout -- Yes --> End([End])
    Logout -- No --> AdminDash
```

---

## 5.4 DATABASE SCHEMA (ER DIAGRAM)

```mermaid
erDiagram
    USERS ||--o{ RESUMES : uploads
    USERS ||--o{ ANALYSES : owns
    USERS ||--o{ AUDIT_LOGS : generates
    USERS ||--o{ RESUME_REWRITES : requests
    
    RESUMES ||--o{ ANALYSES : analyzed_in
    
    ROLES ||--o{ ROLE_SKILLS : defines
    
    ANALYSES ||--o{ ROLE_RECOMMENDATIONS : includes
    ANALYSES ||--o{ LEARNING_ROADMAPS : generates
    ANALYSES ||--o{ PROJECT_RECOMMENDATIONS : suggests
    ANALYSES ||--o{ REPORT_DOWNLOADS : produces
    
    USERS {
        int id PK
        string name
        string email UK
        string password_hash
        boolean is_admin
        datetime created_at
    }

    RESUMES {
        int id PK
        int user_id FK
        string filename
        text text_content
        datetime created_at
    }

    ANALYSES {
        int id PK
        int user_id FK
        int resume_id FK
        string job_role
        json extracted_skills
        json manual_skills
        json github_skills
        json missing_skills
        float confidence_score
        int ats_score
        datetime created_at
    }

    ROLES {
        int id PK
        string name UK
        text description
    }

    ROLE_SKILLS {
        int id PK
        int role_id FK
        string skill
    }

    ROLE_RECOMMENDATIONS {
        int id PK
        int analysis_id FK
        int user_id FK
        json recommended_roles
        datetime created_at
    }

    LEARNING_ROADMAPS {
        int id PK
        int analysis_id FK
        int user_id FK
        string job_role
        json roadmap_json
        datetime created_at
    }

    PROJECT_RECOMMENDATIONS {
        int id PK
        int analysis_id FK
        int user_id FK
        json projects_json
        datetime created_at
    }

    RESUME_REWRITES {
        int id PK
        int user_id FK
        text original_text
        text rewritten_text
        datetime created_at
    }

    AUDIT_LOGS {
        int id PK
        int user_id FK
        string action
        text details
        datetime created_at
    }

    REPORT_DOWNLOADS {
        int id PK
        int analysis_id FK
        int user_id FK
        string report_path
        datetime created_at
    }
```

---

## 5.5 TECHNOLOGY STACK OVERVIEW

```mermaid
mindmap
  root((AI SkillGap Analyzer))
    Frontend
      React.js
      Vite Build Tool
      Chart.js Visualization
      Axios HTTP Client
    Backend
      Python 3.9+
      Flask Framework
      Flask-SQLAlchemy ORM
      Flask-JWT-Extended
      Flask-CORS
    AI & ML
      spaCy NLP
      Sentence-BERT
      Scikit-learn
      RandomForest Classifier
      TF-IDF Vectorizer
      FuzzyWuzzy
    Database
      SQLite
      SQLAlchemy Models
    External APIs
      YouTube Data API
      GitHub API
    Development Tools
      Git Version Control
      VS Code
      Jupyter Notebook
```

---

## 5.6 DEPLOYMENT ARCHITECTURE

```mermaid
graph TB
    subgraph Client
        Browser[Web Browser]
    end
    
    subgraph Frontend Server
        ReactApp[React App<br/>Port: 5173]
    end
    
    subgraph Backend Server
        FlaskAPI[Flask API<br/>Port: 5000]
        
        subgraph AI Services
            NLP[spaCy NLP Engine]
            SBERT[SBERT Model]
            ML[RandomForest Model]
        end
    end
    
    subgraph Data Storage
        SQLite[(SQLite DB<br/>skillgap.db)]
        Files[File Storage<br/>uploads/]
        Models[ML Models<br/>models/]
    end
    
    Browser <-->|HTTP/HTTPS| ReactApp
    ReactApp <-->|REST API| FlaskAPI
    FlaskAPI <--> NLP
    FlaskAPI <--> SBERT
    FlaskAPI <--> ML
    FlaskAPI <--> SQLite
    FlaskAPI <--> Files
    ML <--> Models
```
