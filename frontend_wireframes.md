# ModularGrid Price Monitor - Frontend Wireframes

## Overview

This document outlines the user interface design for the ModularGrid Price Monitor web application. The wireframes provide a visual representation of the key screens and components that will be implemented in the Vue.js frontend.

## Login Page

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│                 ModularGrid Price Monitor               │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │                                                 │    │
│  │                    [Logo]                       │    │
│  │                                                 │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │                                                 │    │
│  │  Username: [                              ]     │    │
│  │                                                 │    │
│  │  Password: [                              ]     │    │
│  │                                                 │    │
│  │             [       Log In        ]             │    │
│  │                                                 │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  Note: This application requires a ModularGrid          │
│  Unicorn account to access price history data.          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Dashboard Page

```
┌─────────────────────────────────────────────────────────┐
│  ModularGrid Price Monitor           [User] ▼           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Dashboard] [Deals] [Watchlist] [Settings]             │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Monitoring Status                                      │
│  ┌─────────────────────────────────────────────────┐    │
│  │                                                 │    │
│  │  Status: [Active/Inactive]                      │    │
│  │  Last Scan: 2025-04-06 10:15:22                 │    │
│  │  Next Scan: 2025-04-06 11:15:22                 │    │
│  │  Deals Found: 12                                │    │
│  │                                                 │    │
│  │  [Run Single Scan]    [Start/Stop Monitoring]   │    │
│  │                                                 │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  Recent Deals                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │                                                 │    │
│  │  • Make Noise Maths - $220 (25% below avg)      │    │
│  │  • Mutable Instruments Plaits - $180 (15% below)│    │
│  │  • Intellijel Quadrax - $245 (18% below avg)    │    │
│  │                                                 │    │
│  │  [View All Deals]                               │    │
│  │                                                 │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  Watchlist Alerts                                       │
│  ┌─────────────────────────────────────────────────┐    │
│  │                                                 │    │
│  │  • Mutable Instruments Beads - $350 (10% below) │    │
│  │  • Expert Sleepers Disting - $165 (22% below)   │    │
│  │                                                 │    │
│  │  [Manage Watchlist]                             │    │
│  │                                                 │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Deals Page

```
┌─────────────────────────────────────────────────────────┐
│  ModularGrid Price Monitor           [User] ▼           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Dashboard] [Deals] [Watchlist] [Settings]             │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Current Deals                                          │
│                                                         │
│  Filters: [Min % ▼] [Region ▼] [Condition ▼] [Apply]    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ Module          | Price | % Below | Listed | Region  │
│  ├─────────────────────────────────────────────────┤    │
│  │ Make Noise Maths | $220 |   25%   | Apr 5 | US      │
│  ├─────────────────────────────────────────────────┤    │
│  │ MI Plaits        | $180 |   15%   | Apr 6 | EU      │
│  ├─────────────────────────────────────────────────┤    │
│  │ Intellijel Quadrax| $245|   18%   | Apr 4 | US      │
│  ├─────────────────────────────────────────────────┤    │
│  │ Expert Sleepers  | $165 |   22%   | Apr 6 | UK      │
│  │ Disting                                              │
│  ├─────────────────────────────────────────────────┤    │
│  │ Mutable Instruments| $350|   10%   | Apr 5 | EU     │
│  │ Beads                                                │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  [< Previous]                [Next >]                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Deal Detail Modal

```
┌─────────────────────────────────────────────────────────┐
│  Deal Details                                [X]        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Make Noise Maths                                       │
│  ┌─────────────┐                                        │
│  │             │  Price: $220                           │
│  │   [Image]   │  Condition: Excellent                  │
│  │             │  Seller: eurorack_enthusiast           │
│  │             │  Region: US                            │
│  │             │  Listed: April 5, 2025                 │
│  └─────────────┘                                        │
│                                                         │
│  Deal Analysis                                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │                                                 │    │
│  │  Average Price: $293                            │    │
│  │  Median Price: $285                             │    │
│  │  This deal: 25% below average                   │    │
│  │                                                 │    │
│  │  [Price History Chart]                          │    │
│  │                                                 │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  [Add to Watchlist]    [Open on ModularGrid]           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Watchlist Page

```
┌─────────────────────────────────────────────────────────┐
│  ModularGrid Price Monitor           [User] ▼           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Dashboard] [Deals] [Watchlist] [Settings]             │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Your Watchlist                     [Add Module]        │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ Module          | Threshold | Max Price | Actions    │
│  ├─────────────────────────────────────────────────┤    │
│  │ Mutable Instruments|   15%   |   $400   | [Edit]     │
│  │ Beads                                  | [Remove]    │
│  ├─────────────────────────────────────────────────┤    │
│  │ Expert Sleepers  |   20%   |   $200   | [Edit]      │
│  │ Disting                               | [Remove]    │
│  ├─────────────────────────────────────────────────┤    │
│  │ Make Noise       |   10%   |   $350   | [Edit]      │
│  │ Morphagene                            | [Remove]    │
│  ├─────────────────────────────────────────────────┤    │
│  │ Intellijel       |   15%   |   $300   | [Edit]      │
│  │ Metropolis                            | [Remove]    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Add to Watchlist Modal

```
┌─────────────────────────────────────────────────────────┐
│  Add Module to Watchlist                      [X]       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Search Module:                                         │
│  [                                            ] [Search]│
│                                                         │
│  Search Results:                                        │
│  ┌─────────────────────────────────────────────────┐    │
│  │                                                 │    │
│  │  • Mutable Instruments Stages                   │    │
│  │  • Mutable Instruments Marbles                  │    │
│  │  • Mutable Instruments Rings                    │    │
│  │                                                 │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  Selected: Mutable Instruments Stages                   │
│                                                         │
│  Deal Threshold: [15] %                                 │
│  Maximum Price: [$300]                                  │
│                                                         │
│  [Cancel]                     [Add to Watchlist]        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Settings Page

```
┌─────────────────────────────────────────────────────────┐
│  ModularGrid Price Monitor           [User] ▼           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Dashboard] [Deals] [Watchlist] [Settings]             │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Account Settings                                       │
│  ┌─────────────────────────────────────────────────┐    │
│  │                                                 │    │
│  │  ModularGrid Username: [                  ]     │    │
│  │  ModularGrid Password: [                  ]     │    │
│  │                                                 │    │
│  │  [Test Credentials]     [Save Account Settings] │    │
│  │                                                 │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  Monitoring Settings                                    │
│  ┌─────────────────────────────────────────────────┐    │
│  │                                                 │    │
│  │  Scan Interval: [60] minutes                    │    │
│  │                                                 │    │
│  │  Default Deal Threshold: [15] %                 │    │
│  │                                                 │    │
│  │  Regions to Monitor:                            │    │
│  │  [x] US   [x] EU   [x] UK   [x] Other          │    │
│  │                                                 │    │
│  │  [Save Monitoring Settings]                     │    │
│  │                                                 │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  Notification Settings                                  │
│  ┌─────────────────────────────────────────────────┐    │
│  │                                                 │    │
│  │  Email Notifications:                           │    │
│  │  [x] Enable email notifications                 │    │
│  │                                                 │    │
│  │  Email Address: [user@example.com]              │    │
│  │                                                 │    │
│  │  Quiet Hours:                                   │    │
│  │  From [22:00] To [08:00]                        │    │
│  │                                                 │    │
│  │  [Save Notification Settings]                   │    │
│  │                                                 │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Notifications Panel

```
┌─────────────────────────────────────────────────────────┐
│  Notifications                                [X]       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Mark All as Read]                                     │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │ • New deal found: Make Noise Maths - $220       │    │
│  │   25% below average price                       │    │
│  │   April 6, 2025 - 10:15 AM                      │    │
│  ├─────────────────────────────────────────────────┤    │
│  │ • Watchlist alert: Expert Sleepers Disting      │    │
│  │   $165 (22% below average)                      │    │
│  │   April 6, 2025 - 9:30 AM                       │    │
│  ├─────────────────────────────────────────────────┤    │
│  │ • Monitoring session started                    │    │
│  │   April 6, 2025 - 9:00 AM                       │    │
│  ├─────────────────────────────────────────────────┤    │
│  │ • New deal found: Mutable Instruments Plaits    │    │
│  │   $180 (15% below average)                      │    │
│  │   April 5, 2025 - 4:45 PM                       │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  [Load More]                                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Mobile Responsive Design

The application will be responsive and adapt to different screen sizes. Key considerations for mobile design:

1. **Navigation**: Convert top navigation to hamburger menu on small screens
2. **Tables**: Responsive tables that stack columns vertically on small screens
3. **Modals**: Full-screen modals on mobile devices
4. **Touch Targets**: Larger touch targets for mobile users

## Color Scheme

The application will use a modern, clean color scheme:

- Primary: #3F51B5 (Indigo)
- Secondary: #FF4081 (Pink)
- Backgr
(Content truncated due to size limit. Use line ranges to read in chunks)