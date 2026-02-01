# Requirements Document

## Introduction

This document outlines the requirements for a comprehensive UI/UX redesign of the LUMEN financial management application. The redesign aims to establish a consistent, modern, and professional design system across all pages while maintaining full compatibility with existing functionality including OCR processing, Gmail sync, AI analysis, wishlist management, and database operations.

## Glossary

- **LUMEN Application**: The financial management web application that processes receipts, transactions, and provides spending analytics
- **Design System**: A collection of reusable components, patterns, and design tokens (colors, spacing, typography) that ensure visual consistency
- **OCR Module**: Optical Character Recognition system that extracts data from receipt images using NVIDIA Vision AI
- **Gmail Sync**: OAuth 2.0-based integration that imports receipts and transactions from Gmail
- **Anomaly Detection**: AI-powered system that identifies unusual spending patterns
- **Wishlist System**: Feature for tracking desired purchases
- **Primary Color**: The main brand color used for primary actions and key UI elements (#4F46E5)
- **Accent Color**: Secondary color used for success states and positive actions (#10B981)
- **Dropzone**: Drag-and-drop file upload interface component

## Requirements

### Requirement 1: Global Design System Implementation

**User Story:** As a user, I want a visually consistent interface across all pages, so that the application feels professional and cohesive.

#### Acceptance Criteria

1. THE LUMEN Application SHALL apply Primary Color #4F46E5 to all primary buttons, active navigation items, and key interactive elements
2. THE LUMEN Application SHALL apply Primary Hover Color #4338CA to all primary buttons when the user hovers over them
3. THE LUMEN Application SHALL apply Accent Color #10B981 to all success messages, positive indicators, and secondary call-to-action elements
4. THE LUMEN Application SHALL apply Text Dark color #1F2937 to all primary text content
5. THE LUMEN Application SHALL apply Text Light color #6B7280 to all secondary text, labels, and helper text
6. THE LUMEN Application SHALL apply Background color #F9FAFB to all page backgrounds
7. THE LUMEN Application SHALL apply Card BG color #FFFFFF to all card components with Card Shadow rgba(0,0,0,0.05)
8. THE LUMEN Application SHALL apply Border color #E5E7EB to all borders, dividers, and input field outlines
9. THE LUMEN Application SHALL apply Error color #EF4444 to all error messages and destructive actions
10. THE LUMEN Application SHALL apply Success color #10B981 to all success confirmations and positive feedback

### Requirement 2: Typography Standardization

**User Story:** As a user, I want consistent and readable typography throughout the application, so that content is easy to read and visually harmonious.

#### Acceptance Criteria

1. THE LUMEN Application SHALL use Inter font family for all text elements
2. THE LUMEN Application SHALL use font weight 400 for body text
3. THE LUMEN Application SHALL use font weight 500 for emphasized text and labels
4. THE LUMEN Application SHALL use font weight 600 for headings and titles
5. THE LUMEN Application SHALL remove all inline font style declarations from HTML templates

### Requirement 3: Spacing System Consistency

**User Story:** As a user, I want consistent spacing between elements, so that the interface feels organized and easy to scan.

#### Acceptance Criteria

1. THE LUMEN Application SHALL use spacing values that are multiples of 8 pixels for all margins and padding
2. THE LUMEN Application SHALL ensure no overlapping elements exist on any page
3. THE LUMEN Application SHALL ensure all elements are properly aligned within their containers
4. THE LUMEN Application SHALL ensure tables fit within their containers without horizontal overflow
5. THE LUMEN Application SHALL ensure charts are centered with consistent margins

### Requirement 4: Login Page Enhancement

**User Story:** As a user, I want to see a clear disclaimer about data usage on the login page, so that I understand how my financial data will be used.

#### Acceptance Criteria

1. WHEN the user views the login page, THE LUMEN Application SHALL display a disclaimer below the login buttons
2. THE LUMEN Application SHALL display the disclaimer text: "This project uses your consented financial data (receipts, bank statements) to analyze spending patterns and suggest potential insights. It is not professional financial advice and should not replace consultation with a qualified financial advisor. Always consult a professional for financial planning and decisions."
3. THE LUMEN Application SHALL style the disclaimer with Text Light color #6B7280
4. THE LUMEN Application SHALL center-align the disclaimer text
5. THE LUMEN Application SHALL apply 12 pixels of top padding to the disclaimer
6. THE LUMEN Application SHALL render the disclaimer in small font size without borders

### Requirement 5: Gmail Sync Button Redesign

**User Story:** As a user, I want an attractive and trustworthy Gmail sync button, so that I feel confident connecting my Gmail account.

#### Acceptance Criteria

1. THE LUMEN Application SHALL display the Gmail sync button with a Google icon on the left side
2. THE LUMEN Application SHALL apply 10-pixel border radius to the Gmail sync button
3. THE LUMEN Application SHALL apply an indigo gradient background to the Gmail sync button
4. THE LUMEN Application SHALL display the text "Sync Gmail Receipts & Transactions" on the Gmail sync button
5. THE LUMEN Application SHALL display a sub-label "Secure OAuth 2.0 Login" below the main button text
6. THE LUMEN Application SHALL display a lock icon indicating security on the Gmail sync button
7. WHEN the user hovers over the Gmail sync button, THE LUMEN Application SHALL apply a slight scale transformation and shadow effect

### Requirement 6: Dashboard Analytics Layout Optimization

**User Story:** As a user, I want a clean and organized dashboard, so that I can quickly understand my financial overview.

#### Acceptance Criteria

1. THE LUMEN Application SHALL align the dashboard title consistently with other page elements
2. THE LUMEN Application SHALL display Total Debits, Total Credits, and Net Flow cards in a vertical layout
3. THE LUMEN Application SHALL position the financial summary cards on the right side below the Refresh button
4. THE LUMEN Application SHALL ensure consistent spacing between all dashboard cards
5. THE LUMEN Application SHALL ensure all graphs are properly aligned without overlapping text
6. THE LUMEN Application SHALL reduce chart sizes where necessary to maintain clean layout proportions

### Requirement 7: Anomaly Detection Visual Indicators

**User Story:** As a user, I want to quickly identify the severity of spending anomalies, so that I can prioritize which ones to review.

#### Acceptance Criteria

1. WHEN an anomaly has high risk level, THE LUMEN Application SHALL display the anomaly card with a red border
2. WHEN an anomaly has medium risk level, THE LUMEN Application SHALL display the anomaly card with a yellow border
3. WHEN an anomaly has low risk level, THE LUMEN Application SHALL display the anomaly card with a green border
4. THE LUMEN Application SHALL display anomalies in clean card format with consistent spacing

### Requirement 8: Gmail Receipts Page Error Handling

**User Story:** As a user, I want the receipts page to display correctly without broken elements, so that I can view my receipt data reliably.

#### Acceptance Criteria

1. IF a receipt does not have an attachmentId, THEN THE LUMEN Application SHALL hide the Gmail attachment download link
2. THE LUMEN Application SHALL display OCR receipts in a simple table format
3. THE LUMEN Application SHALL apply clean card row styling to receipt entries
4. THE LUMEN Application SHALL ensure consistent spacing on the receipts page
5. THE LUMEN Application SHALL display a consistent title with icon on the receipts page

### Requirement 9: OCR Upload Interface Modernization

**User Story:** As a user, I want an intuitive and modern file upload interface, so that uploading receipts is easy and clear.

#### Acceptance Criteria

1. THE LUMEN Application SHALL display the OCR upload area with a dashed border Dropzone style
2. THE LUMEN Application SHALL enable drag-and-drop functionality for the OCR upload area
3. THE LUMEN Application SHALL display an icon in the center of the Dropzone
4. THE LUMEN Application SHALL display the title "Upload Receipt (Image/PDF)" in large bold text
5. THE LUMEN Application SHALL display the subtext "Automatically extracted using NVIDIA Vision AI" below the title
6. THE LUMEN Application SHALL apply a soft shadow to the Dropzone
7. THE LUMEN Application SHALL apply 12-pixel border radius to the Dropzone
8. THE LUMEN Application SHALL display OCR extraction results in a clean card format

### Requirement 10: Navigation Bar Consistency

**User Story:** As a user, I want a clean and organized navigation bar, so that I can easily access different sections of the application.

#### Acceptance Criteria

1. THE LUMEN Application SHALL apply Background color #FFFFFF to the navigation bar
2. THE LUMEN Application SHALL apply a subtle bottom shadow to the navigation bar
3. THE LUMEN Application SHALL include a Wishlist navigation link
4. THE LUMEN Application SHALL include a Dashboard Analytics navigation link
5. THE LUMEN Application SHALL space navigation items evenly across the navigation bar
6. THE LUMEN Application SHALL apply consistent icon styling to all navigation items

### Requirement 11: Button Consistency

**User Story:** As a user, I want all buttons to have consistent styling, so that the interface feels cohesive and predictable.

#### Acceptance Criteria

1. THE LUMEN Application SHALL apply consistent size to all buttons of the same type
2. THE LUMEN Application SHALL apply Primary Color to all primary action buttons
3. THE LUMEN Application SHALL apply consistent border radius to all buttons
4. THE LUMEN Application SHALL apply consistent padding to all buttons
5. WHEN the user hovers over any button, THE LUMEN Application SHALL apply the appropriate hover state color

### Requirement 12: Backward Compatibility Preservation

**User Story:** As a developer, I want all existing functionality to remain intact after the redesign, so that no features are broken.

#### Acceptance Criteria

1. THE LUMEN Application SHALL maintain all existing route handlers without modification
2. THE LUMEN Application SHALL maintain all existing database models without modification
3. THE LUMEN Application SHALL maintain all existing OCR processing logic without modification
4. THE LUMEN Application SHALL maintain all existing Gmail sync functionality without modification
5. THE LUMEN Application SHALL maintain all existing AI analysis workflows without modification
6. THE LUMEN Application SHALL maintain all existing Wishlist System functionality without modification
7. THE LUMEN Application SHALL maintain all existing JavaScript chart functionality without modification
