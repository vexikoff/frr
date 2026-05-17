# Free Reward Routine (FRR)

## Legal and Compliance Notice

This software is distributed strictly for educational, research, and local system testing purposes. 

Automating, simulating, or manipulating application activity to influence third-party platform status indicators may conflict with the Terms of Service of those platforms. The developers of this utility do not endorse, facilitate, or guarantee compliance with any external platform policies. Users are solely responsible for reviewing and adhering to all applicable Terms of Service, developer policies, and local regulations. Use of this tool is at your own risk. The authors assume no liability for account restrictions, service limitations, or other consequences resulting from its use.

## Overview

Free Reward Routine is a Windows-based command-line utility designed to simulate local application runtime for testing and observing how desktop platforms detect active processes. The application is compiled and distributed as a standalone executable file. It does not require external dependencies at runtime, communicates only with a read-only configuration endpoint during initialization, and performs all operations locally within the user's temporary directory.

## Technical Operation

1. Initialization: The executable verifies administrative privileges. If unavailable, it automatically requests elevation via the Windows UAC prompt.
2. Configuration Retrieval: The utility fetches a JSON manifest from a public GitHub-hosted endpoint containing a list of supported identifiers and executable names.
3. User Selection: A searchable table is presented in the terminal. Users select a target identifier by ID or search query.
4. Local Execution: The program copies a standard Windows system executable to a temporary directory under the selected identifier's naming convention.
5. Runtime Simulation: The executable is launched in a hidden window state. A configurable duration timer (1 to 60 minutes) begins, accompanied by a terminal progress indicator.
6. Cleanup: Upon completion or manual termination, the process tree is forcefully closed. All generated files remain in the system temporary directory and can be removed manually or via standard disk cleanup utilities.

No network packets are sent to external services during runtime. No memory modification, code injection, or API hooking is performed. The utility relies exclusively on standard Windows process management APIs.

## System Requirements

- Operating System: Windows 10 or Windows 11 (64-bit recommended)
- Privileges: Administrator rights required for initial execution and process management
- Network: Active internet connection required only during startup to download the configuration manifest
- Disk Space: Minimal temporary storage in %TEMP%

## Distribution and Installation

The application is provided as a precompiled Windows executable. No Python environment or package manager is required for end-user operation.

To run:
1. Download the latest executable release from the official repository
2. Right-click the file and select Run as Administrator
3. Follow the terminal prompts

No installation routine is included. The executable is fully portable and leaves no persistent system modifications.

## Usage Instructions

1. Launch the executable with administrative privileges
2. Enter a search term or press Enter to view the full list
3. Input the corresponding ID number to select a target
4. Specify the runtime duration in minutes (default: 15)
5. Observe the progress indicator in the terminal
6. The process terminates automatically when the timer expires
7. Press Enter to close the utility

To exit early at any point, press Ctrl+C. The utility will safely terminate the active process before closing.

## Security and Transparency

- Open Process Management: Uses standard subprocess and Windows API calls for creation and termination
- No Persistent Files: All operations occur in the user-defined temporary directory
- Auditability: The source code is publicly available for independent review
- No Telemetry: The application does not collect, log, or transmit user data, system information, or runtime metrics
- Deterministic Behavior: Runtime duration and process lifecycle are strictly bounded by user input

## Contributing

Pull requests and issue reports are welcome. Contributions that improve stability, clarify documentation, or enhance security auditing will be reviewed. Requests or patches designed to evade detection mechanisms, bypass authentication, or violate platform policies will not be accepted.

## License

MIT License. See the LICENSE file included with the source distribution for full terms.
