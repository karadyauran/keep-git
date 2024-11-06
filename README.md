# KeepGit 𝌊

KeepGit is a Python script that generates code daily, saving it in a specified folder to maintain active contributions and GitHub statistics. Initially, this project was inspired by a personal desire to keep a steady GitHub contribution streak, but it quickly evolved into a full-fledged project with automation potential.

> This project also inspired the development of a new solution – **AI Developer**, a Go-based tool for rapid MVP development, designed to help startups automate their project building processes. More on this below.

---

## Project Inspiration and Background 𝌊

**KeepGit** began as a personal project for maintaining GitHub activity. During its development, new possibilities for process automation were discovered, leading to the inception of a more advanced project, **AI Developer**.

### About the AI Developer Project 𝌊

**AI Developer** is a system that assists startup founders and developers in quickly launching their ideas by creating MVPs in the shortest time possible. Built on Go, it offers enhanced functionalities for automated application design. **AI Developer** is currently in active development.

> [Visit AI Developer repository on GitHub](https://github.com/karadyauran/ai-developer-light)

---

## Installation and Setup 𝌊

1. **Download the repository** and create an `.env` file based on `example.env`.  
   - In this file, insert your **GitHub token** (grant it permissions for commits, pushes, and repository management) and **OpenAI token** to enable API functionality.

2. **Edit Repository Configurations:**  
   - Open `app/config/config.yaml` and in the `repo:` section, add the name of your repository in the format `your_username/repo_name`.  
   - This should be a **public, empty, and newly created repository**.

3. **Environment Setup:**  
   - From the root directory, run the following commands:
     - Create a virtual environment: `python -m venv .venv`
     - Activate the environment: `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
     - Install dependencies: `pip install -r requirements.txt`

4. **Launch the Application:**  
   - Run the command `python -m app.main` from the root directory to start the application.

---

## Contact 𝌊

Author: Alex Karadiaur  
LinkedIn: [click here](https://www.linkedin.com/in/karadyauran/)
