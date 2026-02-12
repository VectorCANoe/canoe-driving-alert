# Mentoring 06: V-Model Pivot & Feedback Analysis

**Date**: 2026.02.12
**Attendee**: Monitor (Mentor), Team
**Topic**: Project Direction Realignment & Architecture Feedback

---

## 1. Feedback Summary

The mentor provided critical feedback on the team's current trajectory, emphasizing a shift from an implementation-focused "Agile" approach to a structured "V-Model" approach typical in automotive software engineering.

### Key Points
-   **Methodology Mismatch**: The team was proceeding with an "Agile" mindset (fast prototyping, iterative development), whereas vehicle systems require a "V-Model" approach (thorough definition before implementation).
-   **Architecture Errors**: The current system architecture depicted an Ethernet-like star topology instead of the correct CAN Bus linear topology.
-   **Tool vs. System**: CANoe was being treated as part of the system architecture rather than a simulation environment/tool.
-   **Documentation Sequence**: DBC and CAPL development was premature. Functional definition and system architecture must be solidified first.

---

## 2. Problem Definition

**"We were building the roof before the foundation."**

The project was suffering from a misalignment between the team's output and the domain-specific expectations of the automotive industry.

1.  **Premature Implementation**: Detailed implementation (DBC, CAPL) started before high-level design was frozen.
2.  **Incorrect Topology**: The fundamental network architecture (Physical/Data Link Layer) was represented incorrectly.
3.  **Missing "Function Definition"**: There was a gap between "Requirements" and "Implementation," missing the crucial step of defining *what* functions satisfy the requirements and *how* they map to signals.

---

## 3. Root Cause Analysis

| Problem | Root Cause |
| :--- | :--- |
| **Methodology Mismatch** | Misapplication of web/app development "Agile" habits to embedded systems. Failure to understand the rigorous V-Cycle requirements of ISO 26262/ASPICE. |
| **Topology Error** | Lack of domain knowledge regarding physical CAN bus limitations and standard automotive network topologies (Bus vs. Star). |
| **Premature DBC** | Eagerness to see working results (simulation) led to skipping the abstract "System/Functional Design" phase. |
| **Tool Confusion** | Conflating the *test environment* (CANoe) with the *system under test* (Vehicle Network). |

---

## 4. Solution Strategy

We will realign the project by adopting the structure of the provided **Sample Project (`Project Result_Sample.xlsx`)**.

### A. Process Pivot: V-Model Adoption
-   **Stop**: Pause all CAPL coding and DBC signal editing.
-   **Restart**: Return to the "System Design" phase of the V-Model.
-   **Flow**: Requirements $\rightarrow$ **Function Definition** $\rightarrow$ System Architecture $\rightarrow$ Network Design $\rightarrow$ DBC/Implementation.

### B. Architecture Redesign
-   **Topology**: Redraw Level 1 architecture to show a linear CAN Bus with drop lines to ECUs.
-   **Hierarchy**: Clearly separate the "System" (Vehicle), "Domain" (e.g., Body, Chassis), and "Component" (ECU) levels.
-   **Function-First**: Define the *data flow* between domains before defining the *signals*.

### C. Documentation Alignment
-   Adopt the sample excel structure:
    -   **Sheet 01 (Requirements)**: Simplify to "What" needs to happen.
    -   **Sheet 03 (Function Definition)**: The missing link. Map inputs (Sensors/Switches) $\rightarrow$ Logic $\rightarrow$ Outputs (Actuators/Displays).

---

## 5. Implementation Roadmap (Direction)

By following this strategy, we will achieve:

1.  **Domain Correctness**: An architecture that looks and functions like a real vehicle network.
2.  **Traceability**: A clear line from "Requirement" to "Function" to "Signal," enabling easier verification later.
3.  **Mentor Alignment**: Meeting the specific expectations of the mentor's "V-Cycle" grading criteria.

### Immediate Action Items (This Week)
-   [ ] **Concept Design**: Re-draw L1/L2 Architecture (Hand-drawn prefered initially).
-   [ ] **Service List**: Define the list of services/functions each ECU provides.
-   [ ] **Network Configuration**: Define which domains communicate with each other (Data Flow).
-   [ ] **Sample Analysis**: Fully deconstruct the `Project Result_Sample.xlsx` to understand the depth of "Function Definition."
