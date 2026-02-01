# Implementation Plan: LUMEN UI/UX Redesign

- [x] 1. Establish Design System Foundation


  - Create CSS custom properties (variables) for the complete design token system including colors, typography, spacing, and shadows
  - Add Inter font import to replace Poppins font
  - Set up base styles for body, typography, and layout containers
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.10, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1_

- [x] 2. Update Core Component Styles

  - [x] 2.1 Redesign button components (primary, secondary, hover states)


    - Update .btn-primary class with new color scheme, padding, border-radius, and shadow
    - Create consistent hover and active states with transform and shadow effects
    - Apply new styling to all button variants across the application
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

  - [x] 2.2 Redesign card components


    - Update .card and .panel classes with new background, border, shadow, and border-radius
    - Add hover effects with subtle elevation changes
    - Ensure consistent spacing within cards using the 8px spacing system
    - _Requirements: 1.7, 3.2, 3.3_

  - [x] 2.3 Redesign form input components


    - Update input, textarea, and select styles with new colors and spacing
    - Implement focus states with primary color border and shadow
    - Add placeholder styling with light text color
    - _Requirements: 1.4, 1.5, 1.8, 3.1_

  - [x] 2.4 Update flash message components


    - Redesign success, error, and info flash messages with new color scheme
    - Add left border accent and appropriate background colors
    - Ensure proper spacing and typography
    - _Requirements: 1.9, 1.10_

- [x] 3. Redesign Navigation Bar



  - Update .topbar styles with white background and subtle shadow
  - Redesign navigation links with hover states and active indicators
  - Update home icon and profile icon styling
  - Ensure Wishlist and Dashboard Analytics links are present and styled consistently
  - Apply even spacing between navigation items
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

- [x] 4. Redesign Landing Page

  - [x] 4.1 Update landing page layout and hero section


    - Update split-screen layout with proper flex properties
    - Apply gradient background to left section using primary colors
    - Update hero image and text styling
    - Ensure responsive behavior for mobile devices
    - _Requirements: 1.1, 1.2, 1.6, 2.1, 2.2, 2.3, 2.4_

  - [x] 4.2 Add disclaimer text to landing page


    - Add disclaimer text below login buttons with specified content
    - Style with light text color (#6B7280), center alignment, and 12px top padding
    - Use small font size without borders
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

  - [x] 4.3 Redesign Gmail sync button


    - Create enhanced button with Google icon on left
    - Apply gradient indigo background with 10px border-radius
    - Add main text "Sync Gmail Receipts & Transactions"
    - Add sub-label "Secure OAuth 2.0 Login" below main text
    - Include lock icon for security indication
    - Implement hover effect with scale transformation and shadow
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

- [x] 5. Redesign Dashboard Analytics Page

  - [x] 5.1 Update dashboard layout structure


    - Implement top section with summary cards and upload area side-by-side
    - Create vertical stack for Total Debits, Total Credits, and Net Flow cards
    - Position financial summary cards on the right side below Refresh button
    - Ensure consistent spacing between all dashboard sections
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 3.4_

  - [x] 5.2 Redesign summary cards with gradients

    - Apply gradient backgrounds to debit (red-pink), credit (blue-cyan), and net flow (green-teal) cards
    - Update card typography and spacing
    - Add hover effects with slight translation
    - _Requirements: 1.1, 1.2, 1.3, 3.1, 3.2_

  - [x] 5.3 Redesign upload dropzone

    - Create modern dropzone with dashed border style
    - Add large icon in center
    - Display title "Upload Receipt (Image/PDF)" in large bold text
    - Add subtitle "Automatically extracted using NVIDIA Vision AI"
    - Apply soft shadow and 12px border-radius
    - Implement hover effect with border color change
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7_

  - [x] 5.4 Update chart containers and alignment

    - Ensure all graphs are properly aligned without overlapping text
    - Reduce chart sizes where necessary for clean layout
    - Apply consistent spacing and card styling to chart containers
    - _Requirements: 6.5, 6.6, 3.4, 3.5_

  - [x] 5.5 Implement color-coded anomaly indicators


    - Add red border for high-risk anomalies
    - Add yellow border for medium-risk anomalies
    - Add green border for low-risk anomalies
    - Display anomalies in clean card format with consistent spacing
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [x] 6. Redesign Receipts Page

  - [x] 6.1 Update receipts page layout and card structure


    - Implement single-column layout with max-width 1200px
    - Update receipt card styling with rounded corners and subtle shadow
    - Apply consistent spacing between receipt items
    - Ensure proper typography hierarchy (vendor name, date, total)
    - _Requirements: 8.3, 8.4, 8.5, 3.1, 3.2, 3.3_

  - [x] 6.2 Fix Gmail attachment conditional rendering

    - Add conditional check for attachmentId before displaying download link
    - Hide Gmail attachment download link if attachmentId does not exist
    - Ensure OCR receipts display "View OCR Receipt" button correctly
    - _Requirements: 8.1, 8.2_

  - [x] 6.3 Update receipt type badges and action buttons

    - Style Gmail and OCR type badges with appropriate colors
    - Update action button styling with new color scheme
    - Ensure buttons have consistent size and hover effects
    - _Requirements: 1.1, 1.2, 1.3, 11.1, 11.2, 11.3, 11.4, 11.5_

- [x] 7. Redesign Transactions Page

  - [x] 7.1 Update transaction card layout


    - Implement horizontal card layout with left/right sections
    - Update transaction card background, border, and spacing
    - Add hover effects with elevation and border color change
    - Ensure responsive grid layout
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

  - [x] 7.2 Implement transaction type color coding

    - Apply green color to credit transaction amounts and badges
    - Apply red color to debit transaction amounts and badges
    - Style type badges (Credit/Debit) with appropriate background colors
    - Update category badges with primary color scheme
    - _Requirements: 1.1, 1.2, 1.3, 1.9, 1.10_

  - [x] 7.3 Update transaction details and action buttons

    - Style merchant name, date, and amount with proper typography
    - Update "View Details" button with new styling
    - Ensure consistent spacing and alignment within cards
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 11.1, 11.2, 11.3, 11.4, 11.5_

- [x] 8. Redesign Wishlist Page

  - [x] 8.1 Update wishlist page layout and add item form


    - Style add item form with gradient background and dashed border
    - Update form inputs with new styling (item name, expected price, notes)
    - Style submit button with gradient background and hover effects
    - Ensure proper spacing and typography throughout form
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3, 2.4, 3.1_

  - [x] 8.2 Redesign wishlist item cards

    - Implement responsive grid layout for wishlist items
    - Update card styling with background, border, and shadow
    - Add hover effects with elevation change
    - Style item name, price, category badge, and notes
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

  - [x] 8.3 Update wishlist action buttons and AI advice modal

    - Style "Get AI Advice" button with gradient background
    - Update delete button with error color scheme
    - Ensure AI advice modal uses new color scheme and typography
    - Update modal sections (item info, recommendation, reasons, risk/confidence, summary)
    - _Requirements: 1.1, 1.2, 1.3, 1.9, 1.10, 11.1, 11.2, 11.3, 11.4, 11.5_

- [x] 9. Update OCR Upload Interface

  - Create modern dropzone component with dashed border
  - Add drag-and-drop visual indicators
  - Display large icon in center with primary color
  - Add bold title and subtitle text
  - Apply soft shadow and 12px border-radius
  - Implement hover state with border color change
  - Style OCR result display in clean card format
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8_

- [x] 10. Fix Spacing and Alignment Issues

  - Review all pages for overlapping elements and fix
  - Ensure all spacing uses multiples of 8px
  - Verify proper alignment of all elements within containers
  - Fix table horizontal overflow issues
  - Center all charts with consistent margins
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 11. Update Empty States and Error Handling

  - Create consistent empty state styling for pages with no data
  - Update error message styling with new color scheme
  - Ensure all flash messages use new design system
  - Add proper visual feedback for loading states
  - _Requirements: 1.9, 1.10, 3.1, 3.2_

- [x] 12. Verify Backward Compatibility

  - Confirm all existing routes function correctly
  - Verify database models remain unchanged
  - Test OCR processing functionality
  - Test Gmail sync OAuth flow
  - Test AI analysis workflows
  - Test wishlist CRUD operations
  - Verify chart.js integration still works
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7_

- [x] 13. Cross-Browser and Responsive Testing


  - Test layout on desktop (1024px+)
  - Test layout on tablet (768px-1023px)
  - Test layout on mobile (<768px)
  - Verify all interactive elements work on touch devices
  - Test in Chrome, Firefox, Safari, and Edge
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_
