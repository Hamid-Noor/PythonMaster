# Python Reverse Learning Platform

## Overview

This is a Persian-language Python learning platform built with Streamlit that implements a reverse learning approach. The platform provides code analysis, interactive exercises, and progress tracking to help users learn Python programming through analyzing existing code rather than starting from scratch.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit - chosen for rapid prototyping and easy deployment of data science applications
- **Language Support**: Persian/Farsi with RTL (Right-to-Left) text support
- **Layout**: Wide layout with expandable sidebar for better user experience
- **Multi-page Application**: Utilizes Streamlit's pages feature for organized navigation

### Backend Architecture
- **Application Structure**: Modular Python application with utility classes
- **Session Management**: Streamlit's session state for user data persistence
- **Code Analysis**: AST (Abstract Syntax Tree) parsing for Python code analysis
- **File I/O**: JSON-based data persistence for user progress

### Data Storage Solutions
- **PostgreSQL Database**: Primary storage for user data, exercises, progress, and analytics
- **Session State**: In-memory storage for temporary data during user sessions
- **Data Structure**: Relational database schema with proper indexing and constraints
- **Backward Compatibility**: JSON file support maintained for migration scenarios

### Authentication and Authorization
- **Current Implementation**: No authentication system (single-user application)
- **Session Management**: Basic session state management through Streamlit

## Key Components

### 1. Main Application (app.py)
- **Purpose**: Entry point and session management
- **Key Features**: 
  - Session state initialization
  - User progress loading/saving
  - Persian UI setup

### 2. Code Analysis Page (pages/1_تحلیل_کد.py)
- **Purpose**: Interactive code analysis and flowchart generation
- **Features**:
  - Pre-defined code samples
  - Real-time code execution
  - Flowchart visualization
  - Code explanation generation

### 3. Exercise Management (pages/2_تمرین_ها.py)
- **Purpose**: Interactive programming exercises
- **Features**:
  - Difficulty-based exercise filtering
  - Exercise selection and management
  - Progress tracking integration

### 4. Progress Tracking (pages/3_پیشرفت.py)
- **Purpose**: User progress visualization and statistics
- **Features**:
  - Comprehensive statistics dashboard
  - Progress visualization with charts
  - Achievement tracking

### 5. Utility Classes
- **CodeAnalyzer**: AST-based code analysis and explanation
- **FlowchartGenerator**: Graphviz-based flowchart generation from Python code
- **ExerciseManager**: Exercise loading and management
- **DatabaseManager**: PostgreSQL database operations and data management
- **Persian Text Utils**: RTL text and Persian UI support

## Data Flow

1. **User Interaction**: User interacts with Streamlit interface
2. **Session Management**: Data stored in Streamlit session state
3. **Code Analysis**: Python code parsed using AST module
4. **Visualization**: Flowcharts generated using Graphviz
5. **Progress Tracking**: User progress saved to JSON files
6. **Data Persistence**: Progress data loaded/saved between sessions

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework
- **AST**: Python's built-in Abstract Syntax Tree module
- **JSON**: Data serialization and storage
- **Graphviz**: Flowchart and diagram generation

### Database Libraries
- **PostgreSQL**: Primary database system
- **psycopg2-binary**: PostgreSQL adapter for Python
- **SQLAlchemy**: SQL toolkit and ORM

### Visualization Libraries
- **Matplotlib**: Chart and graph generation for progress tracking
- **Pandas**: Data manipulation for statistics

### System Dependencies
- **IO/StringIO**: Code execution and output capture
- **Contextlib**: Context management for code execution
- **OS**: File system operations

## Deployment Strategy

### Current Architecture
- **Single-user Application**: Designed for local or single-user deployment
- **File-based Storage**: No external database required
- **Streamlit Deployment**: Can be deployed on Streamlit Cloud, Heroku, or similar platforms

### Scalability Considerations
- **Data Storage**: Current JSON-based storage suitable for single users
- **Session Management**: Relies on Streamlit's session state (memory-based)
- **Code Execution**: Uses local Python interpreter for code analysis

### Security Considerations
- **Code Execution**: Limited to AST parsing (safer than exec/eval)
- **File Access**: Restricted to data directory for user progress
- **Input Validation**: Basic validation through Streamlit components

## Technical Notes

### Persian Language Support
- Custom CSS for RTL (Right-to-Left) text display
- Persian font support and text alignment
- Culturally appropriate UI elements and terminology

### Code Analysis Features
- **AST Parsing**: Safe code analysis without execution
- **Flowchart Generation**: Visual representation of code logic
- **Error Handling**: Graceful handling of invalid code inputs

### Exercise System
- **Difficulty Levels**: Beginner, Intermediate, Advanced
- **Progress Tracking**: Completion status and scoring
- **Dynamic Content**: Exercise loading from external sources

This architecture provides a solid foundation for a Persian-language Python learning platform with room for expansion to include database integration, user authentication, and more advanced features.