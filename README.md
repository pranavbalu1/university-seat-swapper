# Class Seat Exchange Platform

A web application enabling students to manage their class schedules and exchange seats with peers, built with Svelte (frontend) and Django (backend).

## Features

- **Student Authentication**
  - Secure login with Student ID and password.
  - Registration system for new users.

- **Class Management**
  - Add/update classes with details (Course Number, Section, Instructor, Time).
  - View and manage enrolled courses.

- **Seat Exchange**
  - Request seats in other classes.
  - Offer seats for exchange.
  - Browse and manage seat exchange requests.

## Tech Stack

- **Frontend**: Svelte + TailwindCSS
- **Backend**: Django (with Django REST Framework)
- **Database**: SQL (SQLite by default; configurable to PostgreSQL/MySQL)
- **Authentication**: Django's built-in system
