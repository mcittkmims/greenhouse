# System Requirements Development Methodology

## Introduction to System Requirements

Overview of the System Requirements Development

### 1. Objective

-  Provide a structured approach to align requirements with stakeholder expectations and project goals.

-  Translate high-level needs into actionable, specific, and measurable requirements.

-  Support clear and consistent communication between stakeholders and development teams.

### 2. Scope

-  Encompass the full lifecycle of requirement management, including elicitation, analysis, development, traceability, validation, and release.

-  Establish consistent requirements across all levels of the project.

-  Ensure that requirements align with technical and business goals throughout the project.

### 3. Process Overview

-  Refine and validate requirements iteratively to ensure alignment and traceability.

-  Use systematic methods to manage changes, prioritize requirements, and maintain documentation.

-  Support collaboration and consistency between project members at all stages

## Requirements Development Workflow

Managing Requirements Effectively through Workflow Stages

### 1. Backlog

-  The starting point for all requirements, where ideas, requests, and stakeholder inputs are collected and prioritized.

-  Requirements in this stage need clear categorization and evaluation based on project scope and stakeholder needs.

### 2. In Work

-  Requirements that are actively being analyzed, clarified, and refined.

-  The team engages in defining key elements and finalizing requirements based on stakeholder feedback.

### 5. Invalid

-  Requirements that were found to be irrelevant, conflicting, or infeasible and thus discarded.

-  Documentation of the decision process for invalid requirements helps maintain transparency and avoid revisiting issues later.

### 3. Proposed

-  Refined requirements that have been reviewed and are ready for further validation.

-  Proposed requirements indicate they are mature enough for formal validation but may still require minor refinements..

### 4. Project Accepted

-  Requirements approved for implementation after thorough review and agreement.

-  Project-accepted status signals readiness for integration into the project plan.

## Analyze Stakeholder Requirements

Assigning Responsibility for Each SH Requirement

### 1. Team Assignment

-  Allocate stakeholder requirements (SH requirements) to relevant team members based on expertise and project roles.

-  This approach ensures each requirement is handled by someone with relevant domain knowledge, improving the quality of analysis.

### 2. Status Update

-  Mark each requirement in Jira as "In Work" to indicate that the analysis phase is active.

-  Setting this status in the project management tool helps the entire team track progress and responsibilities.

### 3. Communication

-  Establish clear lines of communication to ensure all team members understand their assigned requirements and expected outcomes.

-  Regular meetings and updates prevent misunderstandings and keep the analysis phase moving forward efficiently.

## Analyze Stakeholder Requirements

Analyzing User, Actions, and Outcomes in Requirements

### 1. Identify Users

-  Determine who interacts with the system within each User Story or Job Story.

-  Define user roles and their responsibilities based on the context of the story.

### 2. Define Actions and Outcomes

-  Clarify what actions users perform and the expected outcomes specified in each story.

-  Align the system's expected behavior with the "who," "what," and "why" of each story.

### 3. List Artifacts

-  Identify any associated artifacts, such as documents, prototypes, or technical components mentioned in the stories.

-  List relevant artifacts to provide context and support the requirements defined in each story.

## Analyze Stakeholder Requirements

Refining SH Requirements Using Feedback and Insights

### 1. Review Feedback

-  Incorporate feedback on User Stories and Job Stories gathered during initial discussions and reviews.

-  Use this feedback to refine story elements, clarify intent, and align with stakeholder expectations.

-  Address concerns and questions raised by team members or stakeholders.

### 2. Clarify Ambiguities

-  Replace vague terms in User Stories or Job Stories with specific, clear language.

-  Ensure that all aspects of the stories are easily understandable by stakeholders and team members.

-  Add clarifying notes or comments to prevent misunderstandings in the future.

### 3. Propose Requirements

-  Move refined User Stories and Job Stories to the "Proposed" status, indicating readiness for validation.

-  Confirm that stories are comprehensive, aligned with stakeholder goals, and prepared for the next phase.

-  Prepare the stories for formal review by key stakeholders or team leads.

## Develop System Requirements Translate SH

Requirements into Converting High-Level Needs into Concrete System

### 1. Identify System Behaviors

-  Translate SH requirements into clear system behaviors or actions.

-  Define functional aspects, focusing on “shall do” requirements.

-  Ensure each behavior aligns with stakeholder expectations.

### 2. Focus on Outcomes

-  Ensure each system requirement clearly specifies the expected outcome.

-  Provide a measurable indicator or standard for each outcome.

-  Align outcomes with both technical and stakeholder requirements.

### 3. Keep it Measurable

-  Define system requirements in a way that allows testing or verification.

-  Include specific metrics, standards, or thresholds for assessment.

-  Use these criteria to ensure consistency and alignment.

## Develop System Requirements Organize and Classify

Structuring Requirements for Easy Management and

### 1. Use Templates

-  Organize system requirements using standardized templates like MASTER and EARS.

-  Label each requirement with the template used, e.g., "MASTER-Functionality" or "EARS-Event.“

-  Ensure consistent structuring and formatting for clear communication.

### 2. Classify Requirements

-  Categorize requirements as functional or non-functional based on their nature.

-  Functional requirements describe actions and processes, while non-functional requirements cover constraints like security and performance.

-  Clearly mark requirements to differentiate them easily.

### 3. Group into chapters

-  Group requirements into chapters or major themes.

-  Assign related requirements within each Epic to create a clear hierarchy and traceability path.

-  Ensure Epics correspond to distinct parts of the system architecture for clarity.

## Ensure Requirements Traceability

Structuring Requirements for Easy Management and

### 1. Import Requirements as Stories

-  Import each refined requirement into Jira as a Story, derived directly from SH requirements.

-  Ensure that each Story is aligned with the defined format and linked back to the originating SH requirement.

-  Clearly mark each Story with relevant labels to indicate whether it is functional or non-functional.

### 2. Group Stories into Epics

-  Group related Stories into Epics to reflect major chapters or system components.

-  Organize Stories based on specific features or key components as defined in the project’s structure.

-  Establish clear relationships between Epics and SH requirements for better traceability.

### 3. Inherit Priority

-  Ensure that the priority of each Story is inherited from the corresponding SH requirement.

-  Align priorities consistently within each Epic based on SH requirements.

-  Use the inherited priority to manage planning and resource allocation effectively.

## Ensure Requirements Traceability

Linking Requirements to Ensure Bidirectional Traceability

### 1. Link Stories to SH Requirements

-  Create explicit traceability links between system requirements (Stories) and their corresponding SH requirements in Jira.

-  Clearly establish which SH requirements each Story is derived from or satisfies.

-  Ensure that links are consistent and comprehensively documented to maintain transparency.

### 2. Handle Complex Relationships

-  Manage many-to-one and one-to-many relationships between SH requirements and Stories.

-  Maintain bidirectional traceability to track changes and their impact effectively.

-  Use appropriate labels and tags to identify and navigate complex links.

### 3. Regularly Review Traceability

-  Conduct regular reviews of traceability links to verify their validity and completeness.

-  Use Jira’s built-in features to create visual traceability matrices and validate relationships.

-  Document any findings and promptly resolve inconsistencies or missing links.

## Review of System Requirements

Conducting Review Sessions for Requirement Validation

### 1. Schedule In-Person or Online Reviews

-  Plan and organize regular review meetings, either in-person or online, with stakeholders and team members.

-  Set clear objectives and agendas for each session, specifying the Stories or Epics to be reviewed.

-  Share relevant documents and Stories in advance to prepare attendees.

### 2. Present Requirements and Provide Justifications

-  Assign requirement owners to present their Stories and link them back to SH requirements.

-  Encourage stakeholders to ask questions and provide constructive feedback on each Story.

-  Focus on resolving ambiguities, clarifying intent, and addressing potential conflicts.

### 3. Document Review Outcomes

-  Record all feedback, decisions, and next steps discussed during the review meeting.

-  Use standardized review checklists to ensure consistency in the validation process.

-  Store review minutes securely and share them with relevant team members.

## Review of System Requirements

Verifying Requirements and Updating Status in Jira

### 1. Perform Compliance Checks

-  Use compliance checklists to validate that each requirement adheres to project standards and SH expectations.

-  Confirm that each requirement is technically feasible and aligns with the project’s overall vision.

-  Address and resolve any issues that arise during the compliance checks.

### 2. Update Requirement Status in Jira

-  Move requirements that pass validation to the "Project Accepted" status.

-  Reassign requirements needing additional refinement to "In Work" with clear comments for necessary changes.

-  Mark discarded requirements as "Invalid" and provide documented justifications.

### 3. Share Validation Results

-  Communicate the results of compliance checks and status updates to stakeholders and team members.

-  Provide a summary report highlighting key changes and reasons for discarded requirements.

-  Ensure that all decisions and updates are clearly documented in Jira.

## Review of System Requirements

Capturing Review Findings and Implementing Changes

### 1. Record Key Findings and Feedback

-  Document all critical findings and recommendations shared during review sessions.

-  Include specific action items linked to Stories or Epics in Jira for easy tracking.

-  Ensure that all feedback is accurately captured and organized for implementation.

### 2. Assign Action Items with Deadlines

-  Allocate each action item to the responsible team member with a clear deadline.

-  Use Jira’s task management features to track the progress of action items and changes.

-  Provide reminders and follow-ups to ensure timely completion of tasks.

### 3. Store and Share Review Minutes

-  Compile comprehensive review minutes, summarizing findings, action items, and deadlines.

-  Store the minutes in a central, easily accessible repository.

-  Share the minutes with stakeholders to keep them updated on decisions and changes.

## Release System Requirements Implement

Recommendations and Applying Review Recommendations and Finalizing

### 1. Apply Feedback and Make Necessary Changes

-  Implement all approved recommendations from the review sessions.

-  Update requirement documentation in Jira to reflect the changes made.

-  Validate each change to confirm alignment with SH requirements and project goals.

### 2. Conduct Final Validation Checks

-  Perform a final validation to ensure that all requirements meet the agreed-upon quality criteria.

-  Confirm that all requirements are aligned with project standards and SH expectations.

-  Document the outcomes of the final validation checks in Jira.

### 3. Release Requirements for Implementation

-  Officially release the finalized requirements to stakeholders and the project team.

-  Communicate the release effectively and highlight any critical updates or changes.

-  Ensure that all stakeholders have access to the latest version of requirements documentation.

## Release System Requirements Perform Iterative Reviews

Refining Requirements through Additional Review Sessions

### 1. Schedule Follow-Up Reviews

-  Plan follow-up review sessions to confirm that implemented changes align with project goals and SH expectations.

-  Invite key stakeholders and requirement owners to review the revised requirements.

-  Set clear goals and an agenda for each session to maintain focus on critical areas..

### 2. Validate Completeness and Accuracy

-  Evaluate each requirement for completeness, consistency, and alignment with project standards.

-  Confirm that all requirements link back to SH needs and technical constraints.

-  Ensure that no critical elements are missing or misaligned with stakeholder expectations.

### 3. Document and Communicate Changes

-  Record any additional changes and recommendations arising from follow-up reviews.

-  Update the requirements documentation in Jira to reflect the latest revisions.

-  Communicate key updates to stakeholders and relevant team members for ongoing alignment.

## Release System Requirements Release System

Finalizing and Approving Requirements for Release

### 1. Approve Requirements for Release

-  Conduct a final review session with key stakeholders to validate all system requirements.

-  After validation, set each requirement to the "Project Accepted" status in Jira, indicating formal approval for implementation.

-  Document any additional conditions or changes required for final acceptance.

### 2. Publish Requirements in Jira

-  Officially release the finalized requirements in Jira for stakeholders and the project team.

-  Make sure that all team members have access to the latest version of requirements documentation.

-  Use project communication channels to notify stakeholders of the release, highlighting critical updates.

### 3. Update Documentation for Traceability

-  Maintain updated documentation of all requirements, including traceability links and version history.

-  Confirm that any changes made during the release phase are accurately recorded and communicated.

-  Store documentation securely and organize it for easy access and future reference.

## Requirements Development Workflow

Managing Requirements Effectively through Workflow Stages

### 1. Backlog

-  The starting point for all requirements, where ideas, requests, and stakeholder inputs are collected and prioritized.

-  Requirements in this stage need clear categorization and evaluation based on project scope and stakeholder needs.

### 2. In Work

-  Requirements that are actively being analyzed, clarified, and refined.

-  The team engages in defining key elements and finalizing requirements based on stakeholder feedback.

### 5. Invalid

-  Requirements that were found to be irrelevant, conflicting, or infeasible and thus discarded.

-  Documentation of the decision process for invalid requirements helps maintain transparency and avoid revisiting issues later.

### 3. Proposed

-  Refined requirements that have been reviewed and are ready for further validation.

-  Proposed requirements indicate they are mature enough for formal validation but may still require minor refinements..

### 4. Project Accepted

-  Requirements approved for implementation after thorough review and agreement.

-  Project-accepted status signals readiness for integration into the project plan.

## Summary and Q&A

Recap of Key Steps in System Requirements

### 1. Clear and Detailed Analysis

-  Thoroughly analyze stakeholder requirements to create a robust foundation for system requirements.

-  Use AI tools and feedback loops to enhance the quality of requirement analysis.

-  Document key elements of each SH requirement for consistency and clarity.

### 2. Structured and Organized Development

-  Translate SH requirements into system requirements using standardized templates and traceability practices.

-  Focus on consistency and alignment across all levels of requirements.

-  Group requirements into Epics to facilitate better management and organization.

### 3. Maintaining Consistent Traceability

-  Establish and maintain bidirectional traceability between SH and system requirements.

-  Validate requirements through rigorous review sessions and iterative feedback cycles.

-  Ensure transparency in the relationships between requirements to manage changes efficiently.
