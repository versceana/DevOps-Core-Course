# Lab 1 Submission — DevOps Info Service

**Name:** Diana Yakupova  
**Group:** B23-CBS-02  
**Date:** 2026-01-28  
**Framework:** Flask 3.1.0

## 1. Framework Selection

I chose Flask for this project because it's the simplest Python web framework that meets all requirements. With only 2 endpoints needed and a tight deadline, Flask's minimal setup and straightforward documentation allowed me to deliver working code quickly.

## 2. Implementation Details

### Application Structure
- `app.py` - main application with all endpoints
- `requirements.txt` - single dependency: Flask==3.1.0
- `.gitignore` - standard Python/IDE ignore patterns
- `README.md` - complete user documentation
- `docs/LAB01.md` - this lab report
- `docs/screenshots/` - proof of functionality

### Key Features Implemented
1. **Main endpoint (`GET /`)** - returns service metadata, system info, runtime data, request details, and available endpoints
2. **Health endpoint (`GET /health`)** - returns service status with timestamp and uptime
3. **Environment-based configuration** - port, host, and debug mode configurable via env vars
4. **Error handling** - custom 404 and 500 error responses in JSON format
5. **Logging** - configurable logging with timestamps and levels

### Code Quality Measures
- Followed PEP 8 style guide
- Used meaningful function/variable names
- Added docstrings for all functions
- Modular code structure with separate helper functions
- Proper error handling for edge cases

## 3. Testing Results

Both endpoints work correctly:

### Main Endpoint (`GET /`)
Returns complete system information:
- Service: name, version, description, framework
- System: hostname, platform, architecture, CPU count, Python version  
- Runtime: uptime, current time, timezone
- Request: client IP, user agent, method, path
- Endpoints: list of available endpoints

### Health Endpoint (`GET /health`)
Returns health status:
- Status: "healthy"
- Timestamp: current UTC time in ISO format
- Uptime: seconds since application start

**Screenshots provided in `docs/screenshots/`:**
- `01-startup.png` - Application starting successfully
- `02-main-endpoint.png` - Main endpoint response in browser
- `03-health-check.png` - Health check response in browser

## 4. Configuration Management

The application supports three environment variables:
- `HOST` - binding address (default: 0.0.0.0)
- `PORT` - listening port (default: 5000)  
- `DEBUG` - enable debug mode (default: false)

Tested configurations:
- Default: `python app.py` (port 5000)
- Custom port: `PORT=8000 python app.py`
- Custom host/port: `HOST=127.0.0.1 PORT=3000 python app.py`

## 5. Challenges and Solutions

### Challenge: Port 5000 Already in Use
On macOS, port 5000 is often used by AirPlay Receiver. Solution: Use `PORT=8000 python app.py` to run on alternative port while keeping default configuration in documentation.

### Challenge: Boolean Environment Variable Parsing
Environment variables are strings, but debug mode needs boolean. Solution: Added `.lower() == 'true'` comparison for case-insensitive boolean parsing.

### Challenge: Uptime Human-Readable Format
Need both seconds and human-readable time. Solution: Implemented conversion from seconds to "X hours, Y minutes" format.

## 6. GitHub Actions Completed

- Starred course repository: https://github.com/inno-devops-labs/DevOps-Core-Course
- Starred simple-container-com/api: https://github.com/simple-container-com/api
- Followed professor (@Cre-eD) and TAs (@marat-biriushev, @pierrepicaud)
- Followed 3 classmates from course forks

## 7. Conclusion

All lab requirements completed successfully:
- ✅ Flask web service with two working endpoints
- ✅ Complete system information on main endpoint
- ✅ Health check endpoint for monitoring
- ✅ Environment-based configuration
- ✅ Error handling and logging
- ✅ Full documentation (README and lab report)
- ✅ Screenshots as proof of functionality
- ✅ GitHub community actions completed

The service is production-ready and prepared for further evolution in upcoming labs (containerization, CI/CD, monitoring).